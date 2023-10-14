from unittest import TestCase

from dotenv import load_dotenv
from osbot_aws.Dependencies import pip_install_dependency
from osbot_aws.deploy.Deploy_Lambda import Deploy_Lambda
from osbot_utils.utils.Dev import pprint

from osbot_lambdas.requests_get.handler import run


class test_requests_get(TestCase):


    def setUp(self) -> None:
        load_dotenv()
        self.handler_run   = run
        self.deploy_lambda = Deploy_Lambda(run)

    def test_create_layer_for_requests(self):
        # todo: use Lambda_Layer_Create to create layer for requests_get lambda function
        pass

    def test_invoke_directly(self):
        assert self.handler_run({}) == 'requests get'

    def test_deploy_lambda_function(self):
        assert self.deploy_lambda.update() == 'Successful'
        self.test_invoke_lambda_function()

    def test_invoke_lambda_function(self):
        assert self.deploy_lambda.invoke() == 'requests get'