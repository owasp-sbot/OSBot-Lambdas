import inspect
from unittest import TestCase

from dotenv import load_dotenv

import osbot_lambdas
from osbot_aws.helpers.Create_Image_ECR import Create_Image_ECR

from osbot_utils.utils.Files import path_combine

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Functions import function_folder, module_file, module_folder, function_name, function_module, \
    module_name

from osbot_utils.utils.Misc import obj_info

from osbot_utils.testing.Trace_Call import trace_calls

from osbot_aws.deploy.Deploy_Lambda import Deploy_Lambda

from osbot_lambdas.docker_hello_world.handler import run

class test_docker_hello_world(TestCase):

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     assert Deploy_Lambda(run).delete() is True


    def setUp(self) -> None:
        load_dotenv()
        self.handler_run   = run
        self.deploy_lambda = Deploy_Lambda(run)

    def test_invoke_directly(self):
        assert self.handler_run({}) == 'docker - hello world!'

    def test__create_local_docker_container(self):
        image_name  = module_name(osbot_lambdas.docker_hello_world)
        path_images = module_folder(osbot_lambdas)

        create_image_ecr =  Create_Image_ECR(image_name=image_name, path_images=path_images)
        build_result     = create_image_ecr.build_image()
        assert build_result is True

                # volume_mapping = {path_layer_folder: "/var/task"}
                # container_id = api_docker.container_create(repository=repository, command= "/bin/bash", tag=image_tag, volumes=volume_mapping)
                # pprint(container_id)
        api_docker =  create_image_ecr.api_docker

        # these methods below use docker APIClient(version='auto')
        #container_id = create_image_ecr.api_docker.container_create(repository=repository, command='')
        #container_id = '_a117e64cd9ea6927cc3f2294a36345000194a83e23a801ad1dcb4494080743ff'
        #api_docker.container_start(container_id)
        # result = create_image_ecr.run_locally()
        # pprint(api_docker.images_names())
        repository    = create_image_ecr.image_repository()

        container     = api_docker.container_create(image_name=repository, command='')
        container_id  = container.container_id
        assert container.exists() is True
        print()
        print(f"created container with id: {container_id}")
        assert container.start() is True
        assert container.status() == 'running'

        assert "(rapid) exec '/var/runtime/bootstrap' (cwd=/var/task, handler=)" in container.logs()


        for container in api_docker.containers_all():
            if container.labels() == {}:
                short_id = container.short_id()
                status   =  container.status()
                if container.status() == 'running':
                    assert container.stop  () is True
                print(f"deleting container with id: {short_id} (status: {status})")
                assert container.delete() is True

        # todo: finish the test automation of the process of creating the docker image
        # return
        # if api_docker.container_status(container_id) == 'not found':
        #     repository   = create_image_ecr.image_repository()
        #     container_id = create_image_ecr.api_docker.container_create(repository=repository, command='')
        # if api_docker.container_status(container_id)  == 'running':
        #     pprint('container is running')
        #     pprint(api_docker.container(container_id))
        # return
        # folder__handler_run = function_folder(self.handler_run)
        # file__dockerfile    = path_combine(folder__handler_run, 'Dockerfile')
        #
        # #obj_info(docker_file.__dir__)
        # print()
        # pprint(file__dockerfile)

    #todo: add tests for publishing the docker image to ECR and execute it

    # def test_deploy_lambda_function(self):
    #     assert self.deploy_lambda.update() == 'Successful'
    #     self.test_invoke_lambda_function()
    #
    # #@trace_calls(include=['osbot', 'boto'])
    # def test_invoke_lambda_function(self):
    #     assert self.deploy_lambda.invoke() == 'hello world!'                    # without params
    #
    #     event = {'name':'AAA'}
    #     assert self.deploy_lambda.invoke(event) == 'hello AAA!'               # with params