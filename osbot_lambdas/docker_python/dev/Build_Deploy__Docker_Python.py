import requests
from osbot_aws.helpers.Create_Image_ECR import Create_Image_ECR
from osbot_lambdas import docker_python
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import parent_folder
from osbot_utils.utils.Misc import random_port


class Build_Deploy__Docker_Python:

    def __init__(self):
        self.image_name       = 'docker_python'
        self.path_images      = parent_folder(docker_python.path)
        self.create_image_ecr = Create_Image_ECR(image_name=self.image_name, path_images=self.path_images)
        self.api_docker       = self.create_image_ecr.api_docker

    def build_docker_image(self):
        self.create_image_ecr.ecr_login()               # needed to get the image from public.ecr.aws
        return self.create_image_ecr.build_image()

    def create_lambda(self):
        return 42

    def start_docker_container(self, local_port=9000):
        port_bindings = {8080: local_port}
        container     =  self.api_docker.container_create(image_name=self.repository(), port_bindings=port_bindings)
        container.start()
        return container

    def execute_docker_container(self):
        local_port = random_port()
        container = self.start_docker_container(local_port=local_port)
        url       = f"http://localhost:{local_port}/2015-03-31/functions/function/invocations"
        response  = requests.post(url, json={})
        container.stop()
        container.delete()
        return response.json()

    def push_to_ecr(self):
        if self.create_image_ecr.repository_exists() is False:      # make sure the repository exists in ecr
            self.create_image_ecr.create_repository()
        return self.create_image_ecr.push_image()

    def repository(self):
        return self.create_image_ecr.image_repository()