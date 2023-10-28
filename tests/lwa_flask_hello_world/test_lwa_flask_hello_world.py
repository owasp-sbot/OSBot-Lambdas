import pytest
from unittest                                       import TestCase
from dotenv                                         import load_dotenv
from osbot_utils.utils.Http import GET

from osbot_aws.helpers.Lambda_Layers_OSBot          import Lambda_Layers_OSBot
from osbot_utils.utils.Dev                          import pprint
from osbot_aws.apis.shell.Shell_Client              import Shell_Client
from osbot_aws.apis.shell.Lambda_Shell              import Lambda_Shell
from osbot_aws.deploy.Deploy_Lambda                 import Deploy_Lambda
from osbot_lambdas.lwa_flask_hello_world.handler    import run



class test_lwa_flask_hello_world(TestCase):

    @classmethod
    def tearDownClass(cls) -> None:
        assert Deploy_Lambda(run).delete() is True

    def setUp(self) -> None:
        load_dotenv()
        self.handler_run    = run
        self.deploy_lambda  = Deploy_Lambda(run)
        self.lambda_shell   = Lambda_Shell()
        self.aws_region     = self.deploy_lambda.osbot_setup.region_name
        self.aws_lambda     = self.deploy_lambda.lambda_function()
        self.shell_client   = Shell_Client(self.aws_lambda)                 # helper class to invoke the lambda_shell methods inside lambda function

    def test_deploy_lambda_function(self):
        arn_layer__lwa       = f"arn:aws:lambda:{self.aws_region}:753240598075:layer:LambdaAdapterLayerX86:17"
        arn_layer__osbot_aws = Lambda_Layers_OSBot().osbot_aws()
        arn_layer__flask     = Lambda_Layers_OSBot().flask()

        self.deploy_lambda.set_env_variable('AWS_LAMBDA_EXEC_WRAPPER', '/opt/bootstrap')        # todo add helper for adding lwa setup
        self.deploy_lambda.set_handler     ('osbot_lambdas/lwa_flask_hello_world/run.sh')

        self.deploy_lambda.add_layers([arn_layer__lwa, arn_layer__osbot_aws, arn_layer__flask])

        assert self.deploy_lambda.update() == 'Successful'

        self.deploy_lambda.lambda_function().function_url_create_with_public_access()

        self.test_invoke_lambda_function()

    def test_invoke_lambda_function(self):
        #result = self.deploy_lambda.lambda_function().invoke_return_logs()    # use this to get the lambda full server logs
        expected_message = "Hello from lwa_flask_hello_world lambda"
        result = self.deploy_lambda.invoke()
        assert result.get('statusCode') == 200
        assert result.get('body'      ) == expected_message
        assert result.get('headers'   ).get('server') == 'Werkzeug/2.1.2 Python/3.11.6'

        function_url = self.deploy_lambda.lambda_function().function_url()
        pprint(f'The function url is: {function_url}')
        assert GET(function_url) == expected_message



        # assert result.get('statusCode') == 200
        # assert result.get('headers').get('server') == 'SimpleHTTP/0.6 Python/3.11.6'
        # body = result.get('body')
        # assert '<title>Directory listing for /</title>' in body
        # assert '<li><a href="opt/">opt/</a></li>'       in body
