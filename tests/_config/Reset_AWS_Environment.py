import sys

from osbot_aws.apis.shell.Lambda_Shell import Lambda_Shell

sys.path.append('.')

from osbot_aws.apis.Lambda import Lambda
from osbot_lambdas.hello_world .handler import run as handler__hello_world
from osbot_lambdas.requests_get.handler import run as handler__requests_get
from osbot_lambdas.osbot_utils .handler import run as handler__osbot_utils


class Reset_AWS_Environment:

    def delete_lambda_functions(self):
        print("\n###### deleting test lambda functions created by tests ######\n")
        self.delete_lambda_function(handler__hello_world )
        self.delete_lambda_function(handler__requests_get)                  # todo - add layer deletion too
        self.delete_lambda_function(handler__osbot_utils )                  # todo - add layer deletion too
        print()

    def delete_lambda_function(self, handler):
        function_name = handler.__module__
        result        = Lambda(function_name).delete()
        if result:
            print(f" - {function_name}:deleted OK")
        else:
            print(f" - {function_name}: Not deleted")

    def delete_secrets(self):
        lambda_shell_secret = Lambda_Shell().secret
        if lambda_shell_secret.exists():
            assert lambda_shell_secret.delete_no_recovery() is True
            print(f" - deleted {lambda_shell_secret}")


if __name__ == '__main__':
    reset_aws_environment = Reset_AWS_Environment()
    reset_aws_environment.delete_lambda_functions()
    reset_aws_environment.delete_secrets()