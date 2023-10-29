import pytest
from unittest                                       import TestCase

import requests
from dotenv                                         import load_dotenv
from osbot_utils.utils.Http import GET, GET_json

from osbot_aws.helpers.Lambda_Layers_OSBot          import Lambda_Layers_OSBot
from osbot_utils.utils.Dev                          import pprint
from osbot_aws.apis.shell.Shell_Client              import Shell_Client
from osbot_aws.apis.shell.Lambda_Shell              import Lambda_Shell
from osbot_aws.deploy.Deploy_Lambda                 import Deploy_Lambda
from osbot_lambdas.lwa_fastapi_streaming.handler    import run



class test_lwa_fastapi_streaming(TestCase):

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     assert Deploy_Lambda(run).delete() is True

    def setUp(self) -> None:
        load_dotenv()
        self.handler_run    = run
        self.deploy_lambda  = Deploy_Lambda(run)
        self.lambda_shell   = Lambda_Shell()
        self.aws_region     = self.deploy_lambda.osbot_setup.region_name
        self.aws_lambda     = self.deploy_lambda.lambda_function()
        self.shell_client   = Shell_Client(self.aws_lambda)                 # helper class to invoke the lambda_shell methods inside lambda function

    def test_deploy_lambda_function(self):
        #self.deploy_lambda.delete()
        arn_layer__lwa       = f"arn:aws:lambda:{self.aws_region}:753240598075:layer:LambdaAdapterLayerX86:17"
        arn_layer__osbot_aws = Lambda_Layers_OSBot().osbot_aws()
        arn_layer__fastapi   = Lambda_Layers_OSBot().fastapi()

        self.deploy_lambda.set_env_variable('AWS_LAMBDA_EXEC_WRAPPER', '/opt/bootstrap')        # todo add helper for adding lwa setup
        self.deploy_lambda.set_env_variable('AWS_LWA_INVOKE_MODE'    , 'response_stream')
        self.deploy_lambda.set_handler     ('osbot_lambdas/lwa_fastapi_streaming/run.sh')
        self.deploy_lambda.add_layers      ([arn_layer__lwa, arn_layer__osbot_aws, arn_layer__fastapi])

        assert self.deploy_lambda.update() == 'Successful'

        self.deploy_lambda.lambda_function().function_url_create_with_public_access(invoke_mode='RESPONSE_STREAM')

        self.test_function_url_stream()


    def test_function_url_stream(self):
        function_url = self.deploy_lambda.function_url()
        #pprint(f'using function url: {function_url}')
        response     = requests.get(function_url, stream=True)

        streamed_responses = []

        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                streamed_responses.append(decoded_line)

        assert response.status_code                           == 200
        assert response.headers.get('Connection'            ) == 'keep-alive'
        assert response.headers.get('x-amzn-Remapped-server') == 'uvicorn'
        assert response.headers.get('Content-Type'          ) == 'text/plain; charset=utf-8; charset=utf-8'
        assert response.headers.get('Transfer-Encoding'     ) ==  'chunked'

        assert streamed_responses == [ '[#0] This is streaming from Lambda ',
                                       '[#1] This is streaming from Lambda ',
                                       '[#2] This is streaming from Lambda ',
                                       '[#3] This is streaming from Lambda ',
                                       '[#4] This is streaming from Lambda ',
                                       '[#5] This is streaming from Lambda ',
                                       '[#6] This is streaming from Lambda ',
                                       '[#7] This is streaming from Lambda ',
                                       '[#8] This is streaming from Lambda ',
                                       '[#9] This is streaming from Lambda ']



    def test_invoke_lambda_function__check_fastapi_docs(self):
        function_url = self.deploy_lambda.lambda_function().function_url()
        docs_page    = GET     (f'{function_url}docs'        )
        open_api     = GET_json(f'{function_url}openapi.json')
        assert '<title>FastAPI - Swagger UI</title>' in docs_page
        assert open_api == {  'info'   : {'title': 'FastAPI', 'version': '0.1.0'}                                                            ,
                              'openapi': '3.1.0'                                                                                             ,
                              'paths'  : { '/': { 'get': { 'operationId': 'index__get'                                                       ,
                                                           'responses'  : { '200': { 'content'    : { 'application/json': { 'schema': { }}} ,
                                                                                     'description': 'Successful Response'}}                 ,
                                                           'summary'    : 'Index'}}}                                                          }