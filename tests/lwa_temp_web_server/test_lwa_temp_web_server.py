import pytest
from unittest                                       import TestCase
from dotenv                                         import load_dotenv
from osbot_aws.helpers.Lambda_Layers_OSBot          import Lambda_Layers_OSBot
from osbot_utils.utils.Dev                          import pprint
from osbot_aws.apis.shell.Shell_Client              import Shell_Client
from osbot_aws.apis.shell.Lambda_Shell              import Lambda_Shell
from osbot_aws.deploy.Deploy_Lambda                 import Deploy_Lambda
from osbot_lambdas.lwa_temp_web_server.handler      import run



class test_lwa_temp_web_server(TestCase):

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

    # @pytest.mark.skip("blocks test since it opens up the web server")
    # def test_invoke_directly(self):
    #     temp_web_server = self.handler_run()
    #     pprint(temp_web_server)

    def test_deploy_lambda_function(self):
        arn_layer__lwa       = f"arn:aws:lambda:{self.aws_region}:753240598075:layer:LambdaAdapterLayerX86:17"
        arn_layer__osbot_aws = Lambda_Layers_OSBot().osbot_aws()

        self.deploy_lambda.set_env_variable('AWS_LAMBDA_EXEC_WRAPPER', '/opt/bootstrap')
        self.deploy_lambda.set_handler     ('osbot_lambdas/lwa_temp_web_server/run.sh')

        self.deploy_lambda.add_layer(arn_layer__lwa)
        self.deploy_lambda.add_layer(arn_layer__osbot_aws)

        assert self.deploy_lambda.update() == 'Successful'

        self.test_invoke_lambda_function()

    def test_invoke_lambda_function(self):
        # result = self.deploy_lambda.lambda_function().invoke_return_logs()    # use this to get the lambda full server logs
        result = self.deploy_lambda.invoke()

        assert result.get('statusCode') == 200
        assert result.get('headers').get('server') == 'SimpleHTTP/0.6 Python/3.11.6'
        body = result.get('body')
        assert '<title>Directory listing for /</title>' in body
        assert '<li><a href="opt/">opt/</a></li>'       in body
