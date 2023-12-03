import requests
from unittest import TestCase

from osbot_aws.apis.Lambda import Lambda
from osbot_lambdas.docker_playwright.dev.Build_Deploy__Docker_Playwright import Build_Deploy__Docker_Playwright
from osbot_utils.testing.Duration import Duration
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_exists, folder_name, file_exists, file_name
from osbot_utils.utils.Http import wait_for_port
from osbot_utils.utils.Misc import wait_for


class test_Build_Deploy__Docker_Playwright(TestCase):

    def setUp(self) -> None:
        self.build_deploy  = Build_Deploy__Docker_Playwright()
        self.aws_config     = self.build_deploy.create_image_ecr.aws_config
        self.aws_account_id = self.aws_config.aws_session_account_id()

    def test__init__(self):
        create_image_ecr = self.build_deploy.create_image_ecr
        assert type(create_image_ecr).__name__ == 'Create_Image_ECR'
        assert create_image_ecr.image_name     == 'docker_playwright'

    def test_build_docker_image(self):
        result = self.build_deploy.build_docker_image()
        assert result.get('status' ) == 'ok'
        assert result.get('tags')[0] == f'{self.aws_account_id}.dkr.ecr.eu-west-2.amazonaws.com/{self.build_deploy.image_name}:latest'

    def test_create_container(self):
        container    = self.build_deploy.create_container()
        container_id = container.container_id
        assert container.status() == 'created'
        created_containers = self.build_deploy.created_containers()
        assert len(created_containers) == 1
        assert container_id in created_containers
        assert container.delete() is True
        assert len(self.build_deploy.created_containers().items()) == 0

    def test_create_lambda(self):
        delete_existing = False
        wait_for_active = True
        lambda_function = self.build_deploy.lambda_function()
        with Duration(prefix='create lambda:'):
            create_result   = self.build_deploy.create_lambda(delete_existing=delete_existing, wait_for_active=wait_for_active)
            lambda_info     = lambda_function.info()
            if delete_existing is True:
                assert create_result.get('status') == 'ok'
            assert lambda_info.get('Configuration').get('State') == 'Active'

        with Duration(prefix='invoke lambda 1st:'):
            invoke_result   = lambda_function.invoke()
            assert invoke_result.get('body') == '{"message":"Hello from docked_playwright lambda"}'

        with Duration(prefix='invoke lambda 2nd:'):
            invoke_result   = lambda_function.invoke()
            assert invoke_result.get('body') == '{"message":"Hello from docked_playwright lambda"}'

        with Duration(prefix='invoke lambda 3rd:'):
            invoke_result   = lambda_function.invoke()
            assert invoke_result.get('body') == '{"message":"Hello from docked_playwright lambda"}'


    def test_execute_lambda(self):
        result = self.build_deploy.execute_lambda()
        assert result.get('body') == '{"message":"Hello from docked_playwright lambda"}'

    def test_start_container(self):
        assert self.build_deploy.build_docker_image().get('status' ) == 'ok'
        container = self.build_deploy.start_container()
        ports     = container.info().get('ports')

        assert container.status() == 'running'
        assert len(ports) == 1
        assert ports.get('8000/tcp')[0].get('HostPort') == '8888'

        with Duration():
            for i in range(0,10):
                if 'Uvicorn running on ' in container.logs():
                    pprint(container.logs())
                    break
                print(f'[{i}] waiting for Uvicorn running on in container logs')
                wait_for(0.1)

        url = "http://localhost:8888"

        response = requests.get(url)
        assert response.status_code == 200
        assert response.text == '{"message":"Hello from docked_playwright lambda!!"}'

        assert container.stop() is True
        assert container.status() == 'exited'
        assert container.delete() is True


    def test_dockerfile(self):
        assert self.build_deploy.dockerfile().startswith('FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy')

    def test_path_docker_playwright(self):
        assert folder_exists(self.build_deploy.path_docker_playwright()) is True
        assert folder_name  (self.build_deploy.path_docker_playwright()) == 'docker_playwright'

    def test_path_dockerfile(self):
        assert file_exists(self.build_deploy.path_dockerfile())
        assert file_name  (self.build_deploy.path_dockerfile()) == 'dockerfile'