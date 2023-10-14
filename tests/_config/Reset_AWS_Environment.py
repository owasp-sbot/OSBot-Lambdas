import sys
sys.path.append('.')

from osbot_aws.apis.Lambda import Lambda
from osbot_lambdas.hello_world.handler  import run as hello_world_handler
from osbot_lambdas.requests_get.handler import run as requests_get_handler


class Reset_AWS_Environment:

    def delete_lambda_functions(self):
        print("\n###### deleting test lambda functions created by tests ######\n")
        self.delete_lambda_function(hello_world_handler )
        self.delete_lambda_function(requests_get_handler)                           # todo - add layer deletion too
        print()

    def delete_lambda_function(self, handler):
        function_name = handler.__module__
        result        = Lambda(function_name).delete()
        if result:
            print(f" - {function_name}:deleted OK")
        else:
            print(f" - {function_name}: Not deleted")


if __name__ == '__main__':
    Reset_AWS_Environment().delete_lambda_functions()