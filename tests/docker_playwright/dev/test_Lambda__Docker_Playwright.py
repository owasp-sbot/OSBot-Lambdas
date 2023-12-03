import requests
from unittest import TestCase

from osbot_lambdas.docker_playwright.dev.Lambda__Docker_Playwright import Lambda__Docker_Playwright
from osbot_utils.utils.Dev import pprint


class test_Lambda__Docker_Playwright(TestCase):

    def setUp(self):
        self.lambda_docker = Lambda__Docker_Playwright()

    def test__init__(self):
        assert type(self.lambda_docker) is Lambda__Docker_Playwright

    def test_a__build_docker_image(self):
        result = self.lambda_docker.build_docker_image()
        assert result.get('status') == 'ok'

    def test_b__publish_docker_image(self):
        result          = self.lambda_docker.publish_docker_image()
        auth_result     = result.get('auth_result')
        push_json_lines = result.get('push_json_lines')
        assert auth_result.get('Status') == 'Login Succeeded'
        assert 'errorDetail' not in push_json_lines

    def test_c__create_lambda_function(self):
        lambda_function   = self.lambda_docker.build_deploy.lambda_function()
        create_result     = self.lambda_docker.create_lambda_function()
        function_info     = lambda_function.info()

        assert create_result.get('create_result').get('status') == 'ok'
        assert create_result.get('function_url' ).get('AuthType'        ) == 'NONE'
        assert function_info.get('Code'         ).get('RepositoryType'  ) == 'ECR'
        assert function_info.get('Configuration').get('Architectures'   ) == [self.lambda_docker.build_deploy.image_architecture()]
        assert function_info.get('Configuration').get('LastUpdateStatus') == 'Successful'
        assert function_info.get('Configuration').get('State'           ) == 'Active'


    def test_d__update_lambda_function(self):
        update_status = self.lambda_docker.update_lambda_function()
        assert update_status == 'Successful'

    def test_e__invoke_lambda_function(self):
        expected_body   = '{"message":"Hello from docked_playwright lambda!!"}'
        lambda_function = self.lambda_docker.build_deploy.lambda_function()
        function_url    = lambda_function.function_url()
        lambda_invoke   = lambda_function.invoke()
        rest_invoke     = requests.get(function_url).text
        assert lambda_invoke.get('statusCode') == 200
        assert lambda_invoke.get('body'      ) == expected_body
        assert rest_invoke                     == expected_body

    def test_f__rebuild_and_publish(self):
        result = self.lambda_docker.rebuild_and_publish()
        assert result.get('build_result'  ).get('status')                    == 'ok'
        assert result.get('publish_result').get('auth_result').get('Status') == 'Login Succeeded'
        assert result.get('update_result' )                                  == 'Successful'

