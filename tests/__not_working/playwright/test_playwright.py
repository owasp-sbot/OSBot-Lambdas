# todo: find a way to run playwright from a lambda (the code below is not working)
#       based on google search it looks like everybody who got it working used a docker image
#       which is what I'm trying to avoid (i.e. I want to see if we can run the browser using the normal lambda image, with the dependencies loaded from disk
# from unittest                           import TestCase
# from dotenv                             import load_dotenv
# from osbot_utils.utils.Misc import obj_info
#
# from osbot_aws.helpers.Lambda_Layer_Create import Lambda_Layer_Create
# from osbot_utils.utils.Dev import pprint
#
# from osbot_aws.deploy.Deploy_Lambda     import Deploy_Lambda
# from osbot_docker.API_Docker import API_Docker
# from osbot_lambdas.playwright.handler   import run
#
# class test_playwright(TestCase):
#
#
#     def setUp(self) -> None:
#         load_dotenv()
#         self.handler_run   = run
#         self.deploy_lambda = Deploy_Lambda(run)
#
#     def test_invoke_directly(self):
#         assert self.handler_run({}) == 'playwright execution will happen here'
#
#     def test_lambda_creation_using_docker(self):
#         layer_name = 'layer_files_for_playwright'
#         lambda_layer_create = Lambda_Layer_Create(layer_name=layer_name)
#         path_layer_folder   = lambda_layer_create.path_layer_folder()
#         lambda_layer_create.layer_folder_create()
#
#         api_docker      = API_Docker()
#         #repository     = "amazon/aws-lambda-python"
#         repository    = "public.ecr.aws/lambda/python"
#         image_tag       = "3.11"
#
#         if api_docker.image_exists(repository, image_tag) is False:
#             image = api_docker.image_pull(repository, image_tag)
#             pprint(image)
#
#         volume_mapping = {path_layer_folder: "/var/task"}
#         container_id = api_docker.container_create(repository=repository, command= "/bin/bash", tag=image_tag, volumes=volume_mapping)
#         pprint(container_id)
#         container_id = '5dc69fb89c1d08b733b8c8a925d616a623ae36685c71da7aeac59fdb1689c11e'
#         api_docker.container_start(container_id)
#         #api_docker.container_exec(container_id, "pip install playwright -t /var/task/python")
#
#         result = api_docker.container_exec(container_id, command="python -m playwright install chromium", workdir='/var/task/python')
#         pprint(result)
#
#         #pprint(api_docker.containers())
#         #docker_api.container_start(container)
#         #print(result)
#
#
#
#
#     def test_deploy_lambda_function(self):
#         assert self.deploy_lambda.update() == 'Successful'
#         self.test_invoke_lambda_function()
#
#     def test_invoke_lambda_function(self):
#         assert self.deploy_lambda.invoke() == 'hello world!'                    # without params
#
#         event = {'name':'AAA'}
#         assert self.deploy_lambda.invoke(event) == 'hello AAA!'               # with params