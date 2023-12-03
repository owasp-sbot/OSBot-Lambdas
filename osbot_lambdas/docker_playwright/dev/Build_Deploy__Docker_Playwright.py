from osbot_aws.deploy.Deploy_Lambda import Deploy_Lambda
from osbot_aws.helpers.Create_Image_ECR import Create_Image_ECR
from osbot_lambdas import docker_playwright
from osbot_lambdas.docker_playwright.handler import run
from osbot_utils.testing.Duration import Duration
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_contents, parent_folder
from osbot_utils.utils.Misc import wait_for


class Build_Deploy__Docker_Playwright:

    def __init__(self):
        self.image_name       = 'docker_playwright'
        self.path_images      = parent_folder(docker_playwright.path)
        self.create_image_ecr =  Create_Image_ECR(image_name=self.image_name, path_images=self.path_images)
        self.deploy_lambda    =  Deploy_Lambda(run)

    def api_docker(self):
        return self.create_image_ecr.api_docker

    def build_docker_image(self):
        return self.create_image_ecr.build_image()

    def create_container(self):
        port_bindings = {8000: 8888}
        labels        = {"source": "build_deploy__docker_playwright"}
        return  self.api_docker().container_create(image_name=self.repository(), command='', port_bindings=port_bindings)

    def created_containers(self):
        created_containers = {}
        repository = self.repository()

        containers = self.api_docker().containers_all__with_image(repository)
        for container in containers:
            created_containers[container.container_id] = container
        return created_containers

    def create_lambda(self, delete_existing=False, wait_for_active=False):
        with Duration(prefix='create lambda > delete and create:'):
            lambda_function              = self.lambda_function()
            lambda_function.image_uri    = self.image_uri()
            lambda_function.architecture = 'arm64'
            if delete_existing:
                lambda_function.delete()
            result = lambda_function.create()
        if wait_for_active:
            with Duration(prefix='create lambda > wait for active:'):
                lambda_function.wait_for_state_active(max_wait_count=80)
        return result

    def create_lambda_function_url(self):
        lambda_ = self.lambda_function()
        if lambda_.function_url_exists() is False:
            lambda_.function_url_create_with_public_access()
        else:
            pprint("[create_lambda_function_url] skipping since function_url already existed")
        return lambda_.function_url_info()

    def execute_lambda(self):
        lambda_function = self.lambda_function()
        result = lambda_function.invoke()
        return result

    def lambda_function(self):
        return self.deploy_lambda.lambda_function()

    def dockerfile(self):
        return file_contents(self.path_dockerfile())

    def image_uri(self):
        return f"{self.repository()}:latest"

    def path_docker_playwright(self):
        return docker_playwright.path

    def path_dockerfile(self):
        return f'{self.path_docker_playwright()}/dockerfile'

    def repository(self):
        return self.create_image_ecr.image_repository()

    def start_container(self):
        container = self.create_container()
        container.start()
        return container

    def update_lambda_function(self):
        lambda_ = self.lambda_function()
        return lambda_.update_lambda_image_uri(self.image_uri())
