import pytest
from unittest                                       import TestCase
from dotenv                                         import load_dotenv
from osbot_utils.utils.Http import GET, GET_json

from osbot_aws.helpers.Lambda_Layers_OSBot          import Lambda_Layers_OSBot
from osbot_utils.utils.Dev                          import pprint
from osbot_aws.apis.shell.Shell_Client              import Shell_Client
from osbot_aws.apis.shell.Lambda_Shell              import Lambda_Shell
from osbot_aws.deploy.Deploy_Lambda                 import Deploy_Lambda
from osbot_lambdas.lwa_fastapi_hello_world.handler    import run



class test_lwa_fastapi_hello_world(TestCase):

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
        arn_layer__fastapi   = Lambda_Layers_OSBot().fastapi()

        self.deploy_lambda.set_env_variable('AWS_LAMBDA_EXEC_WRAPPER', '/opt/bootstrap')        # todo add helper for adding lwa setup
        self.deploy_lambda.set_handler     ('osbot_lambdas/lwa_fastapi_hello_world/run.sh')

        self.deploy_lambda.add_layers([arn_layer__lwa, arn_layer__osbot_aws, arn_layer__fastapi])

        assert self.deploy_lambda.update() == 'Successful'

        self.deploy_lambda.lambda_function().function_url_create_with_public_access()

        self.test_invoke_lambda_function()

    def test_invoke_lambda_function(self):
        # invoke_with_logs = self.deploy_lambda.lambda_function().invoke_return_logs()    # use this to get the lambda full server logs
        # pprint(invoke_with_logs)
        expected_message = '{"message":"Hello from lwa_fastapi_hello_world lambda"}'
        function_url     = self.deploy_lambda.lambda_function().function_url()
        result_invoke    = self.deploy_lambda.invoke()

        assert result_invoke.get('statusCode') == 200
        assert result_invoke.get('body'      ) == expected_message
        assert result_invoke.get('headers'   ).get('server') == 'uvicorn'

        assert GET(function_url) == expected_message

    def test_invoke_lambda_function__check_fastapi_docs(self):
        function_url = self.deploy_lambda.lambda_function().function_url()
        docs_page    = GET     (f'{function_url}docs'        )
        open_api     = GET_json(f'{function_url}openapi.json')
        assert '<title>FastAPI - Swagger UI</title>' in docs_page
        assert open_api == {  'info'   : {'title': 'FastAPI', 'version': '0.1.0'}                                                            ,
                              'openapi': '3.1.0'                                                                                             ,
                              'paths'  : { '/': { 'get': { 'operationId': 'root__get'                                                       ,
                                                           'responses'  : { '200': { 'content'    : { 'application/json': { 'schema': { }}} ,
                                                                                     'description': 'Successful Response'}}                 ,
                                                           'summary'    : 'Root'}}}                                                          }