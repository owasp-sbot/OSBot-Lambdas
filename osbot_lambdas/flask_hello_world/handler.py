from osbot_utils.utils.Json import json_dumps

from osbot_aws.apis.shell.Lambda_Shell import lambda_shell
from serverless_wsgi import handle_request
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@lambda_shell
def run(event, context=None):
    if event.get('headers'   ) is None: event['headers'   ] = []
    if event.get('httpMethod') is None: event['httpMethod'] = 'GET'
    if event.get('path'      ) is None: event['path'      ] = '/'
    return handle_request(app, event, context)
