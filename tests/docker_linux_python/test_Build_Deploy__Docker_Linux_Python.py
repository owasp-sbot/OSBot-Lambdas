from unittest import TestCase

from osbot_lambdas.docker_linux_python.dev.Build_Deploy__Docker_Linux_Python import Build_Deploy__Docker_Linux_Python
from osbot_utils.utils.Files import folder_name


class test_Build_Deploy__Docker_Linux_Python(TestCase):

    def setUp(self):
        self.docker_linux_python = Build_Deploy__Docker_Linux_Python()

    def test__init__(self):
        assert self.docker_linux_python.image_name                   == 'docker_linux_python'
        assert folder_name(self.docker_linux_python.path_images)     == 'osbot_lambdas'
        assert self.docker_linux_python.create_image_ecr.image_name  == 'docker_linux_python'
