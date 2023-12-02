from osbot_aws.helpers.Create_Image_ECR import Create_Image_ECR
from osbot_lambdas import docker_playwright
from osbot_utils.utils.Files import file_contents, parent_folder


class Build_Deploy__Docker_Playwright:

    def __init__(self):
        self.image_name       = 'docker_playwright'
        self.path_images      = parent_folder(docker_playwright.path)
        self.create_image_ecr =  Create_Image_ECR(image_name=self.image_name, path_images=self.path_images)


    def api_docker(self):
        return self.create_image_ecr.api_docker

    def build_docker_image(self):
        return self.create_image_ecr.build_image()

    def create_container(self):
        return  self.api_docker().container_create(image_name=self.repository(), command='')

    def created_containers(self):
        created_containers = {}
        repository = self.repository()

        containers = self.api_docker().containers_all__with_image(repository)
        for container in containers:
            created_containers[container.container_id] = container
        return created_containers

    def dockerfile(self):
        return file_contents(self.path_dockerfile())

    def path_docker_playwright(self):
        return docker_playwright.path

    def path_dockerfile(self):
        return f'{self.path_docker_playwright()}/Dockerfile'

    def repository(self):
        return self.create_image_ecr.image_repository()
