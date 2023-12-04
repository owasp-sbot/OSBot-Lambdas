from osbot_aws.helpers.Create_Image_ECR import Create_Image_ECR
from osbot_lambdas import docker_linux_python
from osbot_utils.utils.Files import parent_folder


class Build_Deploy__Docker_Linux_Python:

    def __init__(self):
        self.image_name       = 'docker_linux_python'
        self.path_images      = parent_folder(docker_linux_python.path)
        self.create_image_ecr = Create_Image_ECR(image_name=self.image_name, path_images=self.path_images)