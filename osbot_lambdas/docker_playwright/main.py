# from fastapi import FastAPI
# from pydantic import BaseModel
#
# from osbot_utils.utils.Dev import pprint
# from osbot_utils.utils.Misc import bytes_to_base64
#
# app = FastAPI()
#
# @app.get("/")
# async def root():
#
#     print("in root method")
#     return {"message": "Hello World. v0.12"}
#
# # @app.get("/osbot_playwright")
# # @lambda_shell
# # def lambda_shell():
#
#
#
#
# class Payload(BaseModel):
#     method_kwargs:dict
#     method_name: str
#     auth_key: str
#
# @app.post("/lambda-shell")
# def lambda_shell(payload:Payload    ):
#     from osbot_aws.apis.shell.Lambda_Shell import Lambda_Shell
#     shell_server = Lambda_Shell(dict(payload))
#
#     shell_server.valid_shell_request()
#     if shell_server.valid_shell_request():
#         return shell_server.invoke()
#
#     return f'lambda shell should be here: {payload}'
#
# @app.get("/html-sync")
# def html_sync(url='https://example.com'):
#     try:
#         from playwright.sync_api import sync_playwright
#         with sync_playwright() as p:
#             browser = p.chromium.launch(args=["--disable-gpu", "--single-process"])
#             page = browser.new_page()
#             page.goto(url)
#             return f'{page.content()}'
#     except Exception as error:
#         return str(error)
#
# @app.get("/get-html")
# async def get_html(url='https://example.com'):
#     try:
#         from playwright.async_api import async_playwright
#         playwright = await async_playwright().start()
#         browser    = await playwright.chromium.launch(headless=True)
#         page       = await browser.new_page()
#         await page.goto(url)
#         content    = await page.content()
#         #await page.close()
#         await browser.close()
#         return content
#     except Exception as e:
#         return "Error: " + str(e)
#
# @app.get("/get-playwright")
# async def get_playwright(url='https://example.com'):
#     try:
#         from playwright.async_api import async_playwright, Error
#         playwright = await async_playwright().start()
#         return f"playwright: {playwright}"
#     except Error as e:
#         return "Error: " + str(e)
#
# @app.get("/get-browser")
# async def get_browser(url='https://example.com'):
#     try:
#         from playwright.async_api import async_playwright, Error
#         playwright = await async_playwright().start()
#         browser    = await playwright.chromium.launch(headless=True)
#         return f"browser: {browser}"
#     except Error as e:
#         return "Error: " + str(e)
#
# @app.get("/get-page")
# async def get_page(url='https://example.com'):
#     try:
#         from playwright.async_api import async_playwright, Error
#         playwright = await async_playwright().start()
#         browser    = await playwright.chromium.launch(headless=True)
#         page       = await browser.new_page()
#         return f"page: {page}"
#     except Error as e:
#         return "Error: " + str(e)
#
# @app.get("/get-url")
# async def get_url(url='https://example.com'):
#     try:
#         from playwright.async_api import async_playwright, Error
#         playwright = await async_playwright().start()
#         browser    = await playwright.chromium.launch(headless=True)
#         page       = await browser.new_page()
#         await page.goto(url)
#         return f"page: {page.url}"
#
#     except Error as e:
#         return "Error: " + str(e)
#
# @app.get("/get-html")
# async def get_html(url='https://example.com'):
#     try:
#         from playwright.async_api import async_playwright, Error
#         playwright = await async_playwright().start()
#         browser    = await playwright.chromium.launch(headless=True)
#         page       = await browser.new_page()
#         await page.goto(url)
#         content    = await page.content()
#         #await page.close()
#         await browser.close()
#         return content
#     except Error as e:
#         return "Error: " + str(e)
#
#
# @app.get("/get-screenshot")
# async def get_html(url='https://example.com'):
#     try:
#         playwright = await async_playwright().start()
#         browser = await playwright.chromium.launch(headless=True)
#         page = browser.new_page()
#         page.goto(url)
#         screenshot = page.screenshot()            # Take a screenshot
#         return bytes_to_base64(screenshot)
#     except Error as e:
#         return "Error: " + str(e)
