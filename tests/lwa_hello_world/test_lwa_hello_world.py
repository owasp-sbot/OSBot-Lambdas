import socketserver
import threading
from unittest                           import TestCase

import requests
from dotenv                             import load_dotenv
from osbot_utils.utils.Misc import list_set, bytes_to_str, random_port, str_to_bytes, random_text

from osbot_utils.utils.Dev import pprint

from osbot_aws.deploy.Deploy_Lambda        import Deploy_Lambda
from osbot_lambdas.lwa_hello_world.handler import run, lwa_message, MyHandler


# see https://github.com/awslabs/aws-lambda-web-adapter/

class test_lwa_hello_world(TestCase):

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     assert Deploy_Lambda(run).delete() is True

    def setUp(self) -> None:
        load_dotenv()
        self.handler_run   = run
        self.deploy_lambda = Deploy_Lambda(run)
        self.aws_lambda    = self.deploy_lambda.lambda_function()

    def test_invoke_directly(self):
        assert self.handler_run({}) == '(from lwa) hello world!'

    def test_deploy_lambda_function(self):
        #self.deploy_lambda.delete()
        aws_region  = self.deploy_lambda.osbot_setup.region_name
        layer_arn   = f"arn:aws:lambda:{aws_region}:753240598075:layer:LambdaAdapterLayerX86:17"
        self.deploy_lambda.set_env_variable('AWS_LAMBDA_EXEC_WRAPPER', '/opt/bootstrap')
        self.deploy_lambda.set_handler('osbot_lambdas/lwa_hello_world/run.sh')
        self.deploy_lambda.add_layer(layer_arn)
        assert self.deploy_lambda.update() == 'Successful'
        #pprint(self.aws_lambda.info())
        self.test_invoke_lambda_function()

    def test_invoke_lambda_function(self):
        result = self.deploy_lambda.invoke()
        assert result.get('statusCode')  == 200
        assert list_set  (result)        == ['body', 'headers', 'isBase64Encoded', 'multiValueHeaders', 'statusCode']
        assert result.get('body')        == lwa_message.format(name='World')

class test_local__lwa_hello_world(TestCase):
    httpd        : socketserver.TCPServer
    port         : int
    server_thread: threading.Thread

    @classmethod
    def setUpClass(cls):
        cls.port = random_port()
        # Start the server in a separate thread
        server_address = ('', cls.port)  # Use a different port for testing
        cls.httpd         = socketserver.TCPServer(server_address, MyHandler)
        cls.server_thread = threading.Thread(target=cls.httpd.serve_forever)
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        # Stop the server and the thread
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.server_thread.join()

    def test_do_GET(self):
        name = random_text('name')
        # Use the requests library to send a GET request
        response = requests.get(f'http://localhost:{self.port}?name={name}')

        # Asserting the response
        assert response.status_code == 201
        assert response.text        == lwa_message.format(name=name)