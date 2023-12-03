from unittest import TestCase

from osbot_lambdas.docker_playwright.dev.Lambda__Docker_Playwright import Lambda__Docker_Playwright
from osbot_utils.utils.Dev import pprint


class test_Lambda__Docker_Playwright(TestCase):

    def setUp(self):
        self.lambda_docker = Lambda__Docker_Playwright()

    def test__init__(self):
        assert type(self.lambda_docker) is Lambda__Docker_Playwright

    def test_build_docker_image(self):
        result = self.lambda_docker.build_docker_image()
        assert result.get('status') == 'ok'

    def test_publish_docker_image(self):
        result          = self.lambda_docker.publish_docker_image()
        auth_result     = result.get('auth_result')
        push_json_lines = result.get('push_json_lines')
        assert auth_result.get('Status') == 'Login Succeeded'
        assert 'errorDetail' not in push_json_lines

    def test_update_lambda_function(self):
        update_status = self.lambda_docker.update_lambda_function()
        assert update_status == 'Successful'

    def test_rebuild_and_publish(self):
        result = self.lambda_docker.rebuild_and_publish()
        pprint(result)
        assert result.get('build_result'  ).get('status')                    == 'ok'
        assert result.get('publish_result').get('auth_result').get('Status') == 'Login Succeeded'
        assert result.get('update_result' )                                  == 'Successful'