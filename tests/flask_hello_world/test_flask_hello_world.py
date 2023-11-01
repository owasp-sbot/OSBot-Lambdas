from unittest                                   import TestCase
from urllib.error import HTTPError

import pytest
from dotenv                                     import load_dotenv
from osbot_utils.utils.Dev import pprint

from osbot_utils.utils.Http import GET
from osbot_aws.deploy.Deploy_Lambda             import Deploy_Lambda
from osbot_aws.helpers.Lambda_Layers_OSBot      import Lambda_Layers_OSBot
from osbot_lambdas.flask_hello_world.handler    import run


class test_flask_hello_world(TestCase):

    @classmethod
    def tearDownClass(cls) -> None:
        assert Deploy_Lambda(run).delete() is True

    def setUp(self) -> None:
        load_dotenv()
        self.handler_run   = run
        self.deploy_lambda = Deploy_Lambda(run)
        self.lambda_shell  = self.deploy_lambda.lambda_shell()

    def test_deploy_lambda_function(self):
        arn_layer__flask     = Lambda_Layers_OSBot().flask()
        arn_layer__osbot_aws = Lambda_Layers_OSBot().osbot_aws()
        self.deploy_lambda.add_layers([arn_layer__flask, arn_layer__osbot_aws])
        assert self.deploy_lambda.update() == 'Successful'
        self.test_invoke_lambda_function()

    @pytest.mark.skip("can't run on CI because Flask dependency is not installed")
    def test_invoke_directly(self):
        assert self.handler_run({}) == { 'body'           : 'Hello World!'                          ,
                                         'headers'        : {'Content-Length': '12'                 ,
                                                         'Content-Type': 'text/html; charset=utf-8'},
                                         'isBase64Encoded': False                                   ,
                                         'statusCode'     : 200                                     }

    def test_invoke_lambda_function(self):
        expected_response = {  'body'           : 'Hello World!'                                 ,
                               'headers'        : { 'Content-Length': '12'                       ,
                                                    'Content-Type'  : 'text/html; charset=utf-8'},
                               'isBase64Encoded': False                                          ,
                               'statusCode'     : 200                                            }
        event = {"path" : '/'}
        assert self.deploy_lambda.invoke(event) == expected_response
        assert self.deploy_lambda.invoke(     ) == expected_response

    # note: every now and then this test fails in CI (but passes on another runs))
    def test_lambda_shell_invoke(self):

        def run_in_lambda():
            return 42

        assert self.lambda_shell.exec_function(run_in_lambda) == 42     # confirm lambda_shell is working ok

        result = self.deploy_lambda.invoke()                            # this will activate the lambda and populate the app value
        assert result.get('body') == 'Hello World!'

        def get_app_variable():
            from osbot_lambdas.flask_hello_world.handler import app
            return f"{app}"
        assert self.lambda_shell.exec_function(get_app_variable) == "<Flask 'osbot_lambdas.flask_hello_world.handler'>"

    # note: every now and then this test fails in CI (but passes on another runs))
    def test_lambda_shell_invoke__add_new_flask_endpoint(self):
        def add_new_endpoint():
            from osbot_lambdas.flask_hello_world.handler import app
            current_urls = [rule.rule for rule in app.url_map.iter_rules()]
            endpoint_url = '/new_endpoint'
            if endpoint_url in current_urls:
                return current_urls

            def new_endpoint():
                return 'Hello from the new endpoint!'

            app.route('/new_endpoint')(new_endpoint)
            new_urls = [rule.rule for rule in app.url_map.iter_rules()]
            return new_urls


        new_endpoint          = '/new_endpoint'
        flask_url_map         = self.lambda_shell.exec_function(add_new_endpoint)
        new_endpoint_response = self.deploy_lambda.invoke({'path':new_endpoint})

        assert new_endpoint in flask_url_map
        assert new_endpoint_response ==  { 'body'           : 'Hello from the new endpoint!'                 ,
                                           'headers'        : { 'Content-Length': '28'                       ,
                                                                'Content-Type'  : 'text/html; charset=utf-8'},
                                           'isBase64Encoded': False                                          ,
                                           'statusCode'     : 200                                            }

    def test_setup_lambda_url(self):
        lambda_function = self.deploy_lambda.lambda_function()
        function_arn    = lambda_function.function_arn()
        function_url    = lambda_function.function_url_create_with_public_access()

        assert lambda_function.function_url_exists() is True
        assert function_url.startswith("https:")

        assert lambda_function.policy_statements() == [ { 'Action'   : 'lambda:InvokeFunctionUrl'                               ,
                                                          'Condition': {'StringEquals': {'lambda:FunctionUrlAuthType': 'NONE'}} ,
                                                          'Effect'   : 'Allow'                                                  ,
                                                          'Principal': '*'                                                      ,
                                                          'Resource' : function_arn                                             ,
                                                          'Sid'      : 'FunctionURLAllowPublicAccess'                           }]
        function_url = lambda_function.function_url()

        assert GET(function_url) == 'Hello World!'
        try:
            assert GET(function_url+'aaaa') == 'Hello World!'
        except HTTPError as http_error:
            from osbot_utils.utils.Misc import obj_info
            assert http_error.status == 404
            assert http_error.msg    == 'Not Found'
        assert GET(function_url+'new_endpoint') == 'Hello from the new endpoint!'