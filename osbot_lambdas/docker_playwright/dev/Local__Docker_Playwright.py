from pprint import pformat
import requests
from osbot_aws.helpers.Create_Image_ECR import Create_Image_ECR
from osbot_lambdas import docker_playwright
from osbot_utils.testing.Duration import Duration
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import parent_folder, path_combine
from osbot_utils.utils.Misc import wait_for


class Local__Docker_Playwright:

    def __init__(self):
        self.image_name       = 'docker_playwright'
        self.path_images      = parent_folder(docker_playwright.path)
        self.create_image_ecr = Create_Image_ECR(image_name=self.image_name, path_images=self.path_images)
        self.docker_image     = self.create_image_ecr.docker_image
        self.api_docker       = self.create_image_ecr.api_docker
        self.label_source     = 'local__docker_playwright'
        self.labels           = {'source': self.label_source}
        self.volume_path      = path_combine(self.path_images, 'docker_playwright')
        self.local_port       = 8888
        self.port_bindings    = {8000: self.local_port }
        self.volumes       = { self.volume_path: { 'bind': '/var/task',
                                                   'mode': 'ro'       }}
        self.container        = None

    def create_or_reuse_container(self):
        containers = self.containers_with_label()
        if len(containers) > 0:                                         # if we have one, return it
            return next(iter(containers.values()))

        kwargs = { 'labels'        : self.labels        ,               # if not create one with the correct label
                   'volumes'       : self.volumes       ,
                   'port_bindings' : self.port_bindings }
        container = self.docker_image.create_container(**kwargs)
        container.start()                                               # start container
        return container

    def containers_with_label(self):
        by_labels  = self.api_docker.containers_all__by_labels()
        containers = by_labels.get('source', {}).get(self.label_source, {})
        return containers

    def delete_container(self):
        self.container.stop()
        self.container.delete()

    def GET(self, path=''):
        if path.startswith('/') is False:
            path = f'/{path}'
        local_url = f'http://localhost:{self.local_port}{path}'
        return requests.get(local_url).text

    def setup(self):
        self.container = self.create_or_reuse_container()                         # make sure we have at least one running
        self.wait_for_server_running()

    def server_running(self):
        return 'Uvicorn running on ' in self.container.logs()

    def wait_for_server_running(self, max_count=40, delay=0.5):
        for i in range(max_count):
            if self.server_running():
                return True
            print(f'waiting for server to start (attempt {i})')
            wait_for(delay)
        return False



