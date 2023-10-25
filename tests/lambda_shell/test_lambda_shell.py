from unittest                               import TestCase
from dotenv                                 import load_dotenv
from osbot_utils.utils.Json                 import json_loads
from osbot_aws.apis.shell.Shell_Client      import Shell_Client
from osbot_aws.apis.shell.Lambda_Shell      import Lambda_Shell
from osbot_aws.deploy.Deploy_Lambda         import Deploy_Lambda
from osbot_lambdas.lambda_shell.handler     import run



class test_lambda_shell(TestCase):

    @classmethod
    def tearDownClass(cls) -> None:
        assert Deploy_Lambda(run).delete() is True

    def setUp(self) -> None:
        load_dotenv()
        self.handler_run   = run
        self.deploy_lambda = Deploy_Lambda(run)
        self.lambda_shell = Lambda_Shell()

    def test_lambda_shell(self):
        auth_key = self.lambda_shell.get_lambda_shell_auth()
        self.lambda_shell.shell_command = {'method_name': 'ping', 'auth_key': auth_key}
        assert self.lambda_shell.invoke() == 'pong'

    def test_invoke_directly(self):
        payload = {'lambda_shell': {'method_name': 'ping', 'auth_key': self.lambda_shell.get_lambda_shell_auth()}}
        assert self.handler_run(payload) == 'pong'

    def test_deploy_lambda_function(self):
        packages = ['git+https://github.com/owasp-sbot/OSBot-AWS.git@dev'    ,
                    'git+https://github.com/owasp-sbot/OSBot-Utils.git@dev'  ,
                    'boto3'        ,
                    'python-dotenv' ]
        self.deploy_lambda.set_packages_using_layer(packages)

        assert self.deploy_lambda.update() == 'Successful'
        self.test_invoke_lambda_function()

    def test_invoke_lambda_function(self):
        result = self.deploy_lambda.invoke()                    # this will trigger the lambda function
        assert result == 'lambda shell'                         # without the @lambda_shell being trigered

    def test_invoke_lambda_function__lambda_shell(self):
        payload = {'lambda_shell': {'method_name': 'ping'                                   ,       # simple lambda_shell command
                                    'auth_key'   : self.lambda_shell.get_lambda_shell_auth()}}      # auth value provided from 'lambda_shell_auth' AWS Secret
        assert self.deploy_lambda.invoke(payload) == 'pong'

    def test_execute_raw_python_code_in_lambda_function(self):
        aws_lambda    = self.deploy_lambda.lambda_function()                # reference to deployed lambda function
        lambda_client = Shell_Client(aws_lambda)                            # helper class to invoke the lambda_shell methods inside lambda function
        def get_lambda_env_variables():
            import json
            import os
            env_vars            = os.environ                                # Retrieve all environment variables
            env_vars_dict       = dict(env_vars)                            # Convert the environment variables from a dict-like object to a standard dictionary
            serialized_env_vars = json.dumps(env_vars_dict, indent=4)       # Serialize the dictionary to a JSON string,  'indent=4' is for pretty-printing, can be omitted
            return serialized_env_vars

        result = lambda_client.python_exec_function(get_lambda_env_variables)
        lambda_env_variables = json_loads(result)
        def assert_env_variables(key_values):
            for key,value in key_values.items():
                assert lambda_env_variables.get(key) == value

        expected_values = { 'AWS_DEFAULT_REGION'     : self.deploy_lambda.osbot_setup.region_name,
                            'PWD'                    : '/var/task'                               ,
                            'AWS_EXECUTION_ENV'      : 'AWS_Lambda_python3.11'                   ,
                            'AWS_LAMBDA_RUNTIME_API' : '127.0.0.1:9001' ,
                            'AWS_REGION'             : self.deploy_lambda.osbot_setup.region_name,
                            'AWS_XRAY_DAEMON_ADDRESS': '169.254.79.129:2000' ,
                            'PATH'                   : '/var/lang/bin:/usr/local/bin:/usr/bin/:/bin:/opt/bin' ,
                            'PYTHONPATH'             : '/var/runtime'                            ,
                           }
        assert_env_variables(expected_values)

    #@pytest.mark.skip("this test is not working")
    def test__setup_lambda_shell(self):
        lambda_shell_secret = self.lambda_shell.secret
        assert lambda_shell_secret.secret_id == 'lambda_shell_auth'
        if lambda_shell_secret.exists() is False:
            self.lambda_shell.reset_lambda_shell_auth()                     # use this to create the secret (which can take a couple seconds to start working)
        assert lambda_shell_secret.exists() is True