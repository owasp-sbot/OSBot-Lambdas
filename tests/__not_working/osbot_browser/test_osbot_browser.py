# from unittest import TestCase
#
# from dotenv import load_dotenv
# from osbot_utils.utils.Dev import pprint
#
# from osbot_aws.deploy.Deploy_Lambda import Deploy_Lambda
#
# from osbot_lambdas.osbot_browser.handler import run
#
# class test_osbot_browser(TestCase):
#
#
#     def setUp(self) -> None:
#         load_dotenv()
#         self.handler_run   = run
#         self.deploy_lambda = Deploy_Lambda(run)
#
#     def test_invoke_directly(self):
#         result = self.handler_run({})
#         pprint(result)
#
#
#     def test_deploy_lambda_function(self):
#         # packages = [ dict(name='syncer', target_aws_lambda=False)            ,
#         #             'git+https://github.com/owasp-sbot/OSBot-AWS.git@dev'    ,
#         #             'git+https://github.com/owasp-sbot/OSBot-Browser.git@dev',
#         #             'git+https://github.com/owasp-sbot/OSBot-Utils.git@dev'  ,
#         #             'pyyaml'        ,
#         #             'pyppeteer'     ,
#         #             'python-dotenv' ]
#         # self.deploy_lambda.set_packages_using_layer(packages)
#         assert self.deploy_lambda.update() == 'Successful'
#         result = self.deploy_lambda.invoke()
#         pprint(result)
#
#     def test_invoke_osbot_browser(self):
#         pass
#
#
#     #@trace_calls(include=['osbot', 'boto'])
#     def test_invoke_lambda_function(self):
#         assert self.deploy_lambda.invoke() == 'hello world!'                    # without params
#
#         event = {'name':'AAA'}
#         assert self.deploy_lambda.invoke(event) == 'hello AAA!'               # with params