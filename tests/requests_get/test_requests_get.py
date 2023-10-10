from unittest import TestCase

from dotenv import load_dotenv
from osbot_aws.deploy.Deploy_Lambda import Deploy_Lambda

from osbot_lambdas.requests_get.handler import run


class test_requests_get(TestCase):


    def setUp(self) -> None:
        load_dotenv()
        self.handler_run   = run
        self.deploy_lambda = Deploy_Lambda(run)

    def test_invoke_directly(self):
        assert self.handler_run({}) == 'requests get'

    def test_deploy_lambda_function(self):
        assert self.deploy_lambda.update() == 'Successful'
        self.test_invoke_lambda_function()

    def test_invoke_lambda_function(self):
        assert self.deploy_lambda.invoke() == 'requests get'