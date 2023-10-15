from unittest import TestCase

from dotenv import load_dotenv
from osbot_utils.testing.Trace_Call import trace_calls

from osbot_aws.deploy.Deploy_Lambda import Deploy_Lambda

from osbot_lambdas.hello_world.handler import run

class test_hello_world(TestCase):


    def setUp(self) -> None:
        load_dotenv()
        self.handler_run   = run
        self.deploy_lambda = Deploy_Lambda(run)

    def test_invoke_directly(self):
        assert self.handler_run({}) == 'hello world!'

    def test_deploy_lambda_function(self):
        assert self.deploy_lambda.update() == 'Successful'
        self.test_invoke_lambda_function()

    #@trace_calls(include=['osbot', 'boto'])
    def test_invoke_lambda_function(self):
        assert self.deploy_lambda.invoke() == 'hello world!'                    # without params

        event = {'name':'AAA'}
        assert self.deploy_lambda.invoke(event) == 'hello AAA!'               # with params