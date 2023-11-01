# import pytest
# from unittest                                       import TestCase
# from dotenv                                         import load_dotenv
# from osbot_utils.utils.Http import GET
#
# from osbot_aws.helpers.Lambda_Layers_OSBot          import Lambda_Layers_OSBot
# from osbot_utils.utils.Dev                          import pprint
# from osbot_aws.apis.shell.Shell_Client              import Shell_Client
# from osbot_aws.apis.shell.Lambda_Shell              import Lambda_Shell
# from osbot_aws.deploy.Deploy_Lambda                 import Deploy_Lambda
# from osbot_lambdas.mangum_flask_fastapi.handler     import run
#
#
#
# class test_mangum_flask_fastapi(TestCase):
#
#     # @classmethod
#     # def tearDownClass(cls) -> None:
#     #     assert Deploy_Lambda(run).delete() is True
#
#     def setUp(self) -> None:
#         load_dotenv()
#         self.handler_run    = run
#         self.deploy_lambda  = Deploy_Lambda(run)
#         self.lambda_shell   = Lambda_Shell()
#         self.aws_region     = self.deploy_lambda.osbot_setup.region_name
#         self.aws_lambda     = self.deploy_lambda.lambda_function()
#         self.shell_client   = Shell_Client(self.aws_lambda)                 # helper class to invoke the lambda_shell methods inside lambda function
#
#     def test_deploy_lambda_function(self):
#         self.deploy_lambda.delete()
#         arn_layer__osbot_aws = Lambda_Layers_OSBot().osbot_aws()
#         arn_layer__flask     = Lambda_Layers_OSBot().flask    ()
#         arn_layer__fastapi   = Lambda_Layers_OSBot().fastapi  ()
#         arn_layer__mangum    = Lambda_Layers_OSBot().mangum   ()
#
#         self.deploy_lambda.add_layers([arn_layer__osbot_aws, arn_layer__flask, arn_layer__fastapi, arn_layer__mangum])
#
#         assert self.deploy_lambda.update() == 'Successful'
#
#         self.deploy_lambda.lambda_function().function_url_create_with_public_access()
#         self.test_invoke_lambda_function()
#
#     def test_invoke_lambda_function(self):
#         event = {'path': '/'}
#         result = self.deploy_lambda.lambda_function().invoke_return_logs(event)
#         pprint(result)
#
#         return
#
#         # todo: not working, result above result in: "RuntimeError: The adapter was unable to infer a handler to use for the event'
#         #result = self.deploy_lambda.lambda_function().invoke_return_logs()    # use this to get the lambda full server logs
#         expected_message = "Hello from mangum_flask_fastapi lambda"
#         function_url     = self.deploy_lambda.lambda_function().function_url()
#         result_invoke    = self.deploy_lambda.invoke()
#
#         assert result_invoke.get('statusCode') == 200
#         assert result_invoke.get('body'      ) == expected_message
#         assert result_invoke.get('headers'   ).get('server') == 'Werkzeug/2.1.2 Python/3.11.6'
#
#         assert GET(function_url) == expected_message