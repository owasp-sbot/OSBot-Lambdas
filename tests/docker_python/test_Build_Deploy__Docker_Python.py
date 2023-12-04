import requests
from unittest import TestCase

from osbot_lambdas.docker_python.dev.Build_Deploy__Docker_Python import Build_Deploy__Docker_Python
from osbot_utils.utils.Files import folder_name
from osbot_utils.utils.Misc  import random_port


class test_Build_Deploy__Docker_Python(TestCase):

    def setUp(self):
        self.docker_python = Build_Deploy__Docker_Python()

    def test__init__(self):
        assert self.docker_python.image_name == 'docker_python'
        assert folder_name(self.docker_python.path_images) == 'osbot_lambdas'
        assert self.docker_python.create_image_ecr.image_name == 'docker_python'

    def test_a__build_docker_image(self):
        result = self.docker_python.build_docker_image()
        assert result.get('status') == 'ok'

    def test_b__start_docker_container(self):
        local_port = random_port()
        container  = self.docker_python.start_docker_container(local_port=local_port)
        url        = f"http://localhost:{local_port}/2015-03-31/functions/function/invocations"
        response   = requests.post(url, json={})
        status     = container.info().get('status')
        container.stop()
        container.delete()

        assert status == 'running'
        assert response.json() == {"statusCode": 200, "body": "Hello from Lambda!"}

    def test_c__execute_docker_container(self):
        response = self.docker_python.execute_docker_container()
        assert response == {"statusCode": 200, "body": "Hello from Lambda!"}

    def test_d__push_to_ecr(self):
        result          = self.docker_python.push_to_ecr()
        auth_result     = result.get('auth_result')
        push_json_lines = result.get('push_json_lines')
        assert auth_result.get('Status') == 'Login Succeeded'
        assert 'errorDetail' not in push_json_lines

    def test_e__create_lambda(self):
        result = self.docker_python.create_lambda()
        assert result == 42         # todo: finish function



