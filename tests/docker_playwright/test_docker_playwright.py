# import pytest
# from unittest import TestCase
#
# from dotenv import load_dotenv
#
# import osbot_lambdas
# from osbot_aws.helpers.Create_Image_ECR import Create_Image_ECR
# from osbot_utils.utils.Dev import pprint
#
# from osbot_utils.utils.Functions import module_folder, module_name
# from osbot_aws.deploy.Deploy_Lambda import Deploy_Lambda
# from osbot_lambdas.docker_playwright.handler import run
#
# @pytest.mark.skip('Fix tests')
# class docker_playwright(TestCase):
#
#     # @classmethod
#     # def tearDownClass(cls) -> None:
#     #     assert Deploy_Lambda(run).delete() is True
#
#
#     def setUp(self) -> None:
#         load_dotenv()
#         self.handler_run   = run
#         self.deploy_lambda = Deploy_Lambda(run)
#
#     def test_invoke_directly(self):
#         assert self.handler_run({}) == 'docker playwright!'
#
#     def test__create_local_docker_container(self):
#         image_name  = module_name(osbot_lambdas.docker_playwright)
#         path_images = module_folder(osbot_lambdas)
#
#         create_image_ecr =  Create_Image_ECR(image_name=image_name, path_images=path_images)
#         pprint(create_image_ecr)
#         build_result     = create_image_ecr.build_image()
#         print(build_result)
#         assert build_result.get('status') == 'ok'
#
#         api_docker =  create_image_ecr.api_docker
#
#         # these methods below use docker APIClient(version='auto')
#         #container_id = create_image_ecr.api_docker.container_create(repository=repository, command='')
#         #container_id = '_a117e64cd9ea6927cc3f2294a36345000194a83e23a801ad1dcb4494080743ff'
#         #api_docker.container_start(container_id)
#         # result = create_image_ecr.run_locally()
#         # pprint(api_docker.images_names())
#         repository    = create_image_ecr.image_repository()
#
#         container     = api_docker.container_create(image_name=repository, command='')
#         container_id  = container.container_id
#         assert container.exists() is True
#         print()
#         print(f"created container with id: {container_id}")
#         start_result = container.start()
#         pprint(start_result)
#
#         assert container.start() is True
#         assert container.status() == 'running'
#
#         return
#         assert "(rapid) exec '/var/runtime/bootstrap' (cwd=/var/task, handler=)" in container.logs()
#
#
#         for container in api_docker.containers_all():
#             if container.labels() == {}:
#                 short_id = container.short_id()
#                 status   =  container.status()
#                 if container.status() == 'running':
#                     assert container.stop  () is True
#                 print(f"deleting container with id: {short_id} (status: {status})")
#                 assert container.delete() is True
#
#         # todo: finish the test automation of the process of creating the docker image
#         # return
#         # if api_docker.container_status(container_id) == 'not found':
#         #     repository   = create_image_ecr.image_repository()
#         #     container_id = create_image_ecr.api_docker.container_create(repository=repository, command='')
#         # if api_docker.container_status(container_id)  == 'running':
#         #     pprint('container is running')
#         #     pprint(api_docker.container(container_id))
#         # return
#         # folder__handler_run = function_folder(self.handler_run)
#         # file__dockerfile    = path_combine(folder__handler_run, 'Dockerfile')
#         #
#         # #obj_info(docker_file.__dir__)
#         # print()
#         # pprint(file__dockerfile)
#
#     #todo: add tests for publishing the docker image to ECR and execute it
#
#     # def test_deploy_lambda_function(self):
#     #     assert self.deploy_lambda.update() == 'Successful'
#     #     self.test_invoke_lambda_function()
#     #
#     # #@trace_calls(include=['osbot', 'boto'])
#     # def test_invoke_lambda_function(self):
#     #     assert self.deploy_lambda.invoke() == 'hello world!'                    # without params
#     #
#     #     event = {'name':'AAA'}
#     #     assert self.deploy_lambda.invoke(event) == 'hello AAA!'               # with params
#
#
#
#     # def setUp(self) -> None:
#     #     load_dotenv()
#     #     self.handler_run    = run
#     #     self.deploy_lambda  = Deploy_Lambda(run)
#     #     self.lambda_shell   = Lambda_Shell()
#     #     self.aws_region     = self.deploy_lambda.osbot_setup.region_name
#     #     self.aws_lambda     = self.deploy_lambda.lambda_function()
#     #     self.shell_client   = Shell_Client(self.aws_lambda)                 # helper class to invoke the lambda_shell methods inside lambda function
#
#     def test_deploy_lambda_function(self):
#
#
#         self.deploy_lambda.set_env_variable('AWS_LAMBDA_EXEC_WRAPPER', '/opt/bootstrap')        # todo add helper for adding lwa setup
#         self.deploy_lambda.set_handler     ('osbot_lambdas/docker_playwright/run.sh')
#         self.deploy_lambda.set_container_image('470426667096.dkr.ecr.eu-west-2.amazonaws.com/docker_playwright:latest')
#
#
#         pprint(self.deploy_lambda.update())
#         return
#         assert self.deploy_lambda.update() == 'Successful'
#
#         self.deploy_lambda.lambda_function().function_url_create_with_public_access()
#
#         self.test_invoke_lambda_function()
#
#     def test_invoke_lambda_function(self):
#         # invoke_with_logs = self.deploy_lambda.lambda_function().invoke_return_logs()    # use this to get the lambda full server logs
#         # pprint(invoke_with_logs)
#         expected_message = '{"message":"Hello from lwa_fastapi_hello_world lambda"}'
#         function_url     = self.deploy_lambda.lambda_function().function_url()
#         result_invoke    = self.deploy_lambda.invoke()
#
#         assert result_invoke.get('statusCode') == 200
#         assert result_invoke.get('body'      ) == expected_message
#         assert result_invoke.get('headers'   ).get('server') == 'uvicorn'
#
#         assert GET(function_url) == expected_message