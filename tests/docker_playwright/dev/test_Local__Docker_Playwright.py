from unittest import TestCase

from osbot_lambdas.docker_playwright.dev.Local__Docker_Playwright import Local__Docker_Playwright
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_name


class test_Local__Docker_Playwright(TestCase):

    def setUp(self):
        self.local_docker = Local__Docker_Playwright()

    def test___init__(self):
        assert self.local_docker.image_name                      == 'docker_playwright'
        assert folder_name(self.local_docker.path_images)        == 'osbot_lambdas'
        assert type(self.local_docker.create_image_ecr).__name__ == 'Create_Image_ECR'


    def test_setup(self):
        assert len(self.local_docker.containers_with_label()) == 0
        self.local_docker.setup()
        assert len(self.local_docker.containers_with_label()) == 1

        container = self.local_docker.container

        assert 'push-docker.sh'           in self.local_docker.container.exec('ls -la .')
        assert 'import sys'               in container.exec('cat ./handler.py')
        assert self.local_docker.GET('/') == '{"message":"Hello from docked_playwright lambda!!"}'
        assert 'GET / HTTP/1.1" 200 OK\n' in container.logs()


        pprint(self.local_docker.POST('/lambda-shell'), {})


        self.local_docker.delete_container()
        assert len(self.local_docker.containers_with_label()) == 0

