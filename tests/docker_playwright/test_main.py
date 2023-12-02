# import pytest
# import os
#
# import requests
# from unittest import TestCase
# from dotenv     import load_dotenv
# from fastapi.testclient import TestClient
#
# from osbot_aws.apis.shell.Lambda_Shell import Lambda_Shell
# from osbot_lambdas.docker_playwright.main import app
# from osbot_utils.utils.Dev import pprint, jprint
# from osbot_utils.utils.Files import file_create_from_bytes
# from osbot_utils.utils.Functions import function_source_code
# from osbot_utils.utils.Json import json_dumps, json_loads
# from osbot_utils.utils.Misc import base64_to_bytes
#
#
# @pytest.mark.skip('Fix tests')
# class test_main(TestCase):
#
#     def test_root(self):
#         client = TestClient(app)
#         response = client.get("/")
#         assert response.status_code == 200
#         assert response.json() == {"message": "Hello World...123"}
#
#
#     def test_get_html(self):
#         client = TestClient(app)
#         response = client.get("/get-html")
#         assert response.status_code == 200
#         assert '<title>Example Domain</title>'  in response.text
#
#     def test_get_screenshot(self):
#         client = TestClient(app)
#         target = "https://www.google.com"
#         response = client.get(f"/get-screenshot?url={target}")
#         assert response.status_code == 200
#         screnshot_bytes = base64_to_bytes(response.text)
#         file_create_from_bytes('test_img.png', screnshot_bytes)
#
#
#     def test_lambda_shell__directly__ping(self):
#         lambda_shell = Lambda_Shell()
#         payload = {'method_name': 'ping', 'auth_key': lambda_shell.get_lambda_shell_auth()}
#
#         client = TestClient(app)
#
#         response = client.post("/lambda-shell",
#             json= payload,
#             headers={"Content-Type": "application/json"}
#         )
#
#         assert response.status_code == 200
#         assert response.text == '"pong"'
#
#
#     def test_lambda_shell__directly__python_exec(self):
#
#         def code():
#             result = 40 + 2123
#             return result
#
#         def exec_function(function):
#             function_name = function.__name__
#             function_code = function_source_code(function)
#             exec_code = f"{function_code}\nresult= {function_name}()"
#             lambda_shell = Lambda_Shell()
#
#             payload = {'method_name': 'python_exec', 'method_kwargs': {'code': exec_code},
#                        'auth_key': lambda_shell.get_lambda_shell_auth()}
#             client = TestClient(app)
#
#             response = client.post(url    = "/lambda-shell",
#                                    json   = payload,
#                                    headers= {"Content-Type": "application/json"})
#
#             return response.text
#
#         result = exec_function(code)
#         pprint(result)
#
#
#     def test_lambda_shell__lambda__ping(self):
#         load_dotenv()
#         lambda_shell = Lambda_Shell()
#         payload      = {'method_name': 'ping', 'auth_key': lambda_shell.get_lambda_shell_auth()}
#         server       = os.getenv('DOCKER_PLAYWRIGHT_SERVER')
#         url          = f'{server}/lambda-shell'
#         data         = json_dumps(payload)
#         kwargs       = dict(url=url  ,
#                             data=data,
#                             headers={"Content-Type": "application/json"})
#
#         response = requests.post(**kwargs)
#         assert response.status_code == 200
#         assert response.text        == '"pong"'
#
#     def test_lambda_shell__lambda__exec_code(self):
#         load_dotenv()
#         server       = os.getenv('DOCKER_PLAYWRIGHT_SERVER')
#         url          = f'{server}/lambda-shell'
#
#         def code():
#             result = 40 + 2
#             return result
#
#         def exec_function(function):
#             function_name = function.__name__
#             function_code = function_source_code(function)
#             exec_code = f"{function_code}\nresult= {function_name}()"
#             lambda_shell = Lambda_Shell()
#
#             payload = {'method_name': 'python_exec', 'method_kwargs': {'code': exec_code},
#                        'auth_key': lambda_shell.get_lambda_shell_auth()}
#             data = json_dumps(payload)
#             kwargs = dict(url=url, data=data, headers={"Content-Type": "application/json"})
#             response = requests.post(**kwargs)
#             return response.text
#
#         result = exec_function(code)
#
#         assert result == '42'
#
# class test_debug_playwright_startup_issue_in_lambda(TestCase):
#
#     def exec_function(self,function):
#         load_dotenv()
#         server        = os.getenv('DOCKER_PLAYWRIGHT_SERVER')
#         url           = f'{server}/lambda-shell'
#         function_name = function.__name__
#         function_code = function_source_code(function)
#         exec_code     = f"{function_code}\nresult= {function_name}()"
#         lambda_shell  = Lambda_Shell()
#         payload       = {'method_name'  : 'python_exec'                        ,
#                          'method_kwargs': {'code': exec_code}                  ,
#                          'auth_key'     : lambda_shell.get_lambda_shell_auth() }
#         data          = json_dumps(payload)
#         kwargs        = dict(url=url, data=data, headers={"Content-Type": "application/json"})
#         response      = requests.post(**kwargs)
#         return response.text
#
#     def test__confirm_exec_function_is_working(self):
#         def code():
#             return 40 + 2
#
#         assert self.exec_function(code) == '42'
#
#     def test__check_playwright_set(self):
#         def code():
#             from osbot_utils.utils.Files import files_list
#             from playwright.sync_api import sync_playwright
#             # import os
#             # path = '/ms-playwright'
#             # return files_list(path)
#             # #return dict(os.environ)
#             url = 'https://example.com'
#             url = 'https://www.google.com/404'
#             try:
#                 with sync_playwright() as p:
#                     browser = p.chromium.launch(args=["--disable-gpu", "--single-process"])
#                     page = browser.new_page()
#                     page.goto(url)
#                     return f'{page.content()}'
#                 # with sync_playwright() as playwright:
#                 #     browser = playwright.chromium.launch(headless=False)
#                 #sync_playwright()
#                 # with sync_playwright() as p:
#                 #     pass
#                     #browser = p.chromium.launch(headless=True)
#                 # aaa = sync_playwright().start()
#                 # return f'{aaa}'
#                 return 'ok'
#             except Exception as error:
#                 return str(error)
#
#             #return f'{sync_playwright}'
#
#
#         result =  self.exec_function(code)
#         pprint(result)
#         #data   = json_loads(result)
#         #pprint(data)