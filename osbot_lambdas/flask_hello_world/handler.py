from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_aws.apis.shell.Lambda_Shell            import lambda_shell

class Flask_App:

    @cache_on_self
    def app(self):
        from flask import Flask
        return Flask(__name__)

    def setup(self):
        app = self.app()

        @app.route("/")
        def hello():
            return "Hello World!"
        return app

app = Flask_App().setup()

@lambda_shell
def run(event, context=None):
    from serverless_wsgi import handle_request
    if event.get('headers'   ) is None: event['headers'   ] = []
    if event.get('httpMethod') is None: event['httpMethod'] = 'GET'
    if event.get('path'      ) is None: event['path'      ] = '/'
    return handle_request(app, event, context)
