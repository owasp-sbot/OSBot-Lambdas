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
