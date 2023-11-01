# import sys
# sys.path.append('/opt/python')          # this needs to be done since LWA loses the path to the layers
#
# from osbot_utils.decorators.methods.cache_on_self import cache_on_self
# from osbot_aws.apis.shell.Lambda_Shell            import lambda_shell
# from fastapi                    import FastAPI, Depends
# from flask                      import Flask
# from starlette.routing          import Mount, Router
# from starlette.middleware.wsgi  import WSGIMiddleware
# from starlette.middleware import Middleware
# #from starlette.wsgi          import WSGIMiddleware
# from mangum                 import Mangum
#
# ## todo: this is not working (redirect loop)
# # # Flask app
# # flask_app = Flask(__name__)
# #
# # @flask_app.route("/flask")
# # def flask_endpoint():
# #     return "Hello from Flask!"
# #
# # # FastAPI app
# # fastapi_app = FastAPI()
# #
# # @fastapi_app.get("/fastapi")
# # def fastapi_endpoint():
# #     return {"message": "Hello from FastAPI!"}
# #
# # # Merging using Starlette
# # application = Router(
# #     routes=[
# #         Mount("/flask", app=WSGIMiddleware(flask_app)),
# #         Mount("/fastapi", app=fastapi_app)
# #     ]
# # )
#
# #handler = Mangum(application)
# # For AWS Lambda
#
# # todo: fix: this is working but not the unit tests: 'RuntimeError: The adapter was unable to infer a handler ...
# app = FastAPI()
#
#
# @app.get("/")
# def read_root():
#     return {"Hello": "World"}
#
#
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}
#
# handler = Mangum(app, lifespan="off")
#
# def run(event, context=None):
#     if event.get('headers'   ) is None: event['headers'     ] = []
#     if event.get('httpMethod') is None: event['httpMethod'  ] = 'GET'
#     if event.get('path'      ) is None: event['path'        ] = '/'
#
#     return handler(event,context)
#
# # todo: fix: also not working (final solution should be similar to this)
# # class Mangum_App:
# #
# #
# #     def router(self):
# #         flask_app = Flask(__name__)
# #
# #         @flask_app.route("/flask")
# #         def flask_endpoint():
# #             return "Hello from Flask!"
# #
# #         # FastAPI app
# #         fastapi_app = FastAPI()
# #
# #         @fastapi_app.get("/fastapi")
# #         def fastapi_endpoint():
# #             return {"message": "Hello from FastAPI!"}
# #
# #         # Merging using Starlette
# #
# #         router = Router( routes=[ Mount("/flask"  , app=WSGIMiddleware(flask_app)),
# #                                   Mount("/fastapi", app=fastapi_app             )])
# #         return router
# #
# #
# # run = Mangum(Mangum_App().router())
#
# # mangum_router = None
# #
# # @lambda_shell
# # def run(event, context=None):
# #     global mangum_router
# #     if mangum_router is None:
# #         mangum_router = Mangum_App().router()
# #
# #     if event.get('headers'   ) is None: event['headers'   ] = []
# #     if event.get('httpMethod') is None: event['httpMethod'] = 'GET'
# #     if event.get('path'      ) is None: event['path'      ] = '/'
# #     return Mangum(mangum_router)(event, context)