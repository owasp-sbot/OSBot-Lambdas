from unittest                           import TestCase
from dotenv                             import load_dotenv
from osbot_aws.deploy.Deploy_Lambda     import Deploy_Lambda
from osbot_lambdas.osbot_utils.handler  import run

class test_requests_get(TestCase):

    @classmethod
    def tearDownClass(cls) -> None:
        assert Deploy_Lambda(run).delete() is True

    def setUp(self) -> None:
        load_dotenv()
        self.handler_run   = run
        self.deploy_lambda = Deploy_Lambda(run)

    # def test_invoke_directly(self):
    #     assert self.handler_run({}) == 'hello osbot_utils!'

    def test_deploy_lambda_function(self):
        packages = ['git+https://github.com/owasp-sbot/OSBot-Utils.git@dev',
                    'python-dotenv']
        self.deploy_lambda.set_packages_using_layer(packages)
        assert self.deploy_lambda.update() == 'Successful'
        self.test_invoke_lambda_function()

    def test_invoke_lambda_function(self, file_in_temp=None):
        files_in_temp = self.deploy_lambda.invoke()
        assert type(files_in_temp) is list
        assert len (files_in_temp) > 0
        for file_in_tmp in files_in_temp:
            assert file_in_tmp.startswith('/tmp/tmp')