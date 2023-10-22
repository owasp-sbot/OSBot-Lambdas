#
#
#
# def run(event, context=None):
#
#     import os
#     os.environ['PYPPETEER_HOME'] = '/tmp'
#     from pyppeteer.chromium_downloader import DOWNLOADS_FOLDER
#     from osbot_browser.browser.API_Browser import API_Browser
#     #return str(DOWNLOADS_FOLDER)
#
#     from osbot_browser.chrome.Chrome import Chrome
#     chrome_setup = Chrome().chrome_setup
#     return f"{chrome_setup}"
#     return
#
#     api = API_Browser(headless = True)
#
#     return api.sync__url()
#
#     #api.sync__open('https://www.google.com/404')
#     #return api.sync__html_raw()
# #
# # import os
# # from pyppeteer import launch
# #
# # os.environ['PYPPETEER_HOME'] = '/tmp'
# #
# # async def run(event, context):
# #     browser = await launch(args=['--no-sandbox'])
# #     page = await browser.newPage()
# #     await page.goto('https://example.com')
# #     await page.screenshot({'path': '/tmp/example.png'})
# #     await page.url()