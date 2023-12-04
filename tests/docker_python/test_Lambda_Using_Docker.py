import types

import requests
from unittest import TestCase

from osbot_lambdas                                         import docker_python
from osbot_lambdas.docker_python.dev.Lambda_Using_Docker   import Lambda_Using_Docker
from osbot_utils.utils.Dev                                 import pprint
from osbot_utils.utils.Files import folder_name, folder_exists, parent_folder
from osbot_utils.utils.Misc import random_port, obj_info


class test_Lambda_Using_Docker(TestCase):

    def setUp(self):
        self.target = docker_python
        self.docker_lambda = Lambda_Using_Docker(self.target)

    def test__init__(self):
        assert isinstance(self.target, types.ModuleType)
        assert self.target.__name__                           == 'osbot_lambdas.docker_python'
        assert folder_exists(self.target.path)                is True
        assert folder_name  (self.target.path)                == 'docker_python'
        assert folder_name  (parent_folder(self.target.path)) == 'osbot_lambdas'

        assert self.docker_lambda.image_name                  == 'docker_python'
        assert folder_name(self.docker_lambda.path_images)    == 'osbot_lambdas'
        assert self.docker_lambda.create_image_ecr.image_name == 'docker_python'


    def test_a__build_docker_image(self):
        result = self.docker_lambda.build_docker_image()
        assert result.get('status') == 'ok'

    def test_b__start_docker_container(self):
        local_port = random_port()
        container  = self.docker_lambda.start_docker_container(local_port=local_port)
        url        = f"http://localhost:{local_port}/2015-03-31/functions/function/invocations"
        response   = requests.post(url, json={})
        status     = container.info().get('status')
        container.stop()
        container.delete()

        assert status == 'running'
        assert response.json() == {"statusCode": 200, "body": "Hello from Lambda!"}

    def test_c__execute_docker_container(self):
        response = self.docker_lambda.execute_docker_container()
        assert response == {"statusCode": 200, "body": "Hello from Lambda!"}

    def test_d__push_to_ecr(self):
        result          = self.docker_lambda.push_to_ecr()
        auth_result     = result.get('auth_result')
        push_json_lines = result.get('push_json_lines')
        assert auth_result.get('Status') == 'Login Succeeded'
        assert 'errorDetail' not in push_json_lines

    def test_e__create_lambda(self):
        result = self.docker_lambda.create_lambda()
        assert result.get('Code'         ).get('RepositoryType') == 'ECR'
        assert result.get('Configuration').get('State'         ) == 'Active'

    def test_f__invoke_lambda(self):
        result = self.docker_lambda.invoke_lambda()
        assert result == {'body': 'Hello from Lambda!', 'statusCode': 200}

    def test_g__delete_lambda(self):
        assert self.docker_lambda.delete_lambda() is True
        assert self.docker_lambda.deploy_lambda.lambda_function().exists() is False

    # todo add feature to delete repository (since we also need to delete the images)
    # def test_h__delete_ecr_repository(self):
    #     result = self.docker_python.delete_ecr_repository()
    #     pprint(result)




