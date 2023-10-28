import sys
sys.path.append('/opt/python')          # this needs to be done since LWA loses the path to the layers


def run():
    from flask import Flask

    app = Flask(__name__)

    @app.route('/')
    def index():
        return "Hello from lwa_flask_hello_world lambda"

    app.run(port=8080)

if __name__ == '__main__':
    run()                                  # to be triggered from run.sh