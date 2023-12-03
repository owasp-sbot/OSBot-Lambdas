import pytest
import requests
from unittest                                   import TestCase
from osbot_aws.AWS_Config                       import AWS_Config
from osbot_aws.apis.Lambda                      import Lambda
from osbot_aws.apis.test_helpers.Temp_Lambda    import Temp_Lambda
from osbot_utils.testing.Duration               import Duration
from osbot_utils.utils.Misc                     import wait_for, list_set



@pytest.mark.skip("No need to run this all the time ")
class test_BUG__AWS_Function_URL_Deletion(TestCase):

    def setUp(self) -> None:
        print()

    def test_bug__aws_race_condition_on_url_function(self):
        lambda_name = "temp_lambda_to_debug_function_url_race_condition"
        with Duration(prefix="[1st] Create and delete lambda function"):
            with Temp_Lambda(lambda_name=lambda_name) as temp_lambda:
                aws_config      : AWS_Config = temp_lambda.aws_config
                account_id      : str        = aws_config.account_id()
                region_name     : str        = aws_config.region_name()
                lambda_event    : dict       = {'name': 'user-ABC'}
                lambda_function : Lambda     = temp_lambda.aws_lambda

                lambda_function.function_url_delete()

                assert lambda_function.exists             () is True
                assert lambda_function.function_url_exists() is False

                create_result = lambda_function.function_url_create_with_public_access()
                function_url  = lambda_function.function_url()

                assert lambda_function.function_url_exists() is True

                del create_result['function_url_create']['CreationTime']            # confirm it exists and remove since it is always unique
                assert create_result == { 'function_set_policy': { 'Action'      : 'lambda:InvokeFunctionUrl',
                                                                   'Condition'   : { 'StringEquals': { 'lambda:FunctionUrlAuthType': 'NONE'}},
                                                                   'Effect'      : 'Allow',
                                                                   'Principal'   : '*',
                                                                   'Resource'    : f'arn:aws:lambda:{region_name}:{account_id}:function:{lambda_name}',
                                                                   'Sid'         : 'FunctionURLAllowPublicAccess'},
                                          'function_url_create': { 'AuthType'    : 'NONE',
                                                                   'FunctionArn' : f'arn:aws:lambda:{region_name}:{account_id}:function:{lambda_name}',
                                                                   'FunctionUrl' : function_url,
                                                                   'InvokeMode' : 'BUFFERED'}}

                assert lambda_function.invoke({}          )      == 'hello None'
                assert lambda_function.invoke(lambda_event)      == 'hello user-ABC'
                assert requests.get          (function_url).text == 'hello None'

                client         = lambda_function.client()                                           # using boto3 methods, not the OSBot_Lambda ones
                kwargs         = {"FunctionName": lambda_name,
                                  "Payload": '{"name":"boto3"}'}
                boto3_response = client.invoke(**kwargs)
                result_bytes   = boto3_response.get('Payload').read()
                result_string  = result_bytes.decode('utf-8')

                assert sorted(list(set(boto3_response))) == ['ExecutedVersion', 'Payload', 'ResponseMetadata', 'StatusCode']
                assert boto3_response.get('StatusCode')  == 200
                assert result_string == '"hello boto3"'


        assert lambda_function.exists()              is False                       # confirm lambda function has been deleted
        assert lambda_function.function_url_exists() is True                        # BUG: this should be False (but it is not)
        function_url = lambda_function.function_url()                               # BUG: we should be able to get this value
        assert function_url.endswith('.lambda-url.eu-west-2.on.aws/')               # BUG: confirmation that we got a good value after the lambda being deleted
        assert requests.get(function_url).text == '{"Message":"Forbidden"}'         # BUG: this should be '{"Message":null}'


        client = lambda_function.client()                                           # using boto3 methods, not the OSBot_Lambda ones
        try:
            client.invoke(FunctionName=lambda_name, Payload = "{}")
        except client.exceptions.ResourceNotFoundException as resource_not_found:
            expected_message = f'Function not found: arn:aws:lambda:{region_name}:{account_id}:function:{lambda_name}'
            assert resource_not_found.response.get('Message') ==  expected_message

        function_arn = f'arn:aws:lambda:{region_name}:{account_id}:function:{lambda_name}'

        function_url_config = client.get_function_url_config(FunctionName=function_arn)
        assert list_set(function_url_config) == ['AuthType', 'CreationTime', 'FunctionArn', 'FunctionUrl',
                                                 'InvokeMode', 'LastModifiedTime', 'ResponseMetadata']
        assert function_url_config.get('FunctionArn') == function_arn
        assert function_url_config.get('FunctionUrl') == function_url

        with Duration(prefix="[2nd] Create test and delete lambda function"):
            with Temp_Lambda(lambda_name=lambda_name) as temp_lambda:
                lambda_function = temp_lambda.aws_lambda
                assert lambda_function.exists()              is True                      # confirms lambda exists
                assert lambda_function.function_url_exists() is True                      # BUG: confirms lambda URL exists
                assert requests.get(function_url).text       == '{"Message":"Forbidden"}' # BUG: this should be '{"Message":null}'


        lambda_function.function_url_delete()                               # when we delete the function URL explicitly.

        with Duration(prefix="[3rd] Create and delete lambda function"):
            with Temp_Lambda(lambda_name=lambda_name) as temp_lambda:
                lambda_function = temp_lambda.aws_lambda
                assert lambda_function.exists()              is True                    # confirms lambda exists
                assert lambda_function.function_url_exists() is False                   # now we don't have the URL anymore
                assert requests.get(function_url).text == '{"Message":"Forbidden"}'     # BUG: this should be '{"Message":null}'

        old_function_url = function_url                                                 # pin the value of the previous function URL
        assert requests.get(old_function_url).text == '{"Message":"Forbidden"}'         # confirm that it has not been fully deleted

        with Duration(prefix="[4th] (after deletion) Create Lambda function and FunctionUrl"):
            with Temp_Lambda(lambda_name=lambda_name) as temp_lambda:
                lambda_function = temp_lambda.aws_lambda
                create_result = lambda_function.function_url_create_with_public_access()
                assert lambda_function.exists()              is True                    # confirms lambda exists
                assert lambda_function.function_url_exists() is True                    # now we don't have the URL anymore

                new_function_url = create_result.get('function_url_create').get('FunctionUrl')
                assert new_function_url != old_function_url
                assert requests.get(new_function_url).text == 'hello None'              # confirm that lambda function is working ok
                assert requests.get(old_function_url).text == 'hello None'              # BUG this url should not be valid anymore

        with Duration(prefix="[5th] Wait until the old function URL is deleted"):
            for i in range(1,60):
                response = requests.get(old_function_url).text
                if response == '{"Message":null}':
                    break
                wait_for(1)
            assert requests.get(old_function_url).text == '{"Message":null}'                # double check that the response
            assert requests.get(new_function_url).text == '{"Message":"Forbidden"}'         # BUG: this should also not be available
        return

    # execution results                                               (local run #1) | (local run #2)
    # [1st] Create and delete lambda function                           4s 502ms     |  4s 400ms
    # [2nd] Create test and delete lambda function                      2s 473ms     |  2s 413ms
    # [3rd] Create and delete lambda function                           2s 485ms     |  2s 593ms
    # [4th] (after deletion) Create Lambda function and FunctionUrl     3s 875ms     |  3s 427ms
    # [5th] Wait until the old function URL is deleted                  50s 371ms    |  50s 501ms

    def test_bug__aws_race_condition_on_url_function__wait_for_deletion(self):
        lambda_name = "temp_lambda_to_debug_function_url_race_condition_v2"
        with Duration(prefix="[1st] Create lambda and function URL (and delete function)"):
            with Temp_Lambda(lambda_name=lambda_name) as temp_lambda:
                lambda_function = temp_lambda.aws_lambda
                lambda_function.function_url_create_with_public_access()                    # create function_url
                function_url = lambda_function.function_url()                               # get function_url url
                assert requests.get(function_url).text == 'hello None'                      # confirm that lambda function is working ok

        assert lambda_function.function_url_exists() is True                                # BUG: function_url still exists
        assert requests.get(function_url).text == '{"Message":"Forbidden"}'                 # BUG: this should be '{"Message":null}'

        max_wait = 180                                                                      # wait max 3 minutes (180 secs) for the function_url to be deleted
        with Duration(prefix="[2nd] Wait for function URL deletion"):
            for i in range(max_wait):
                if lambda_function.function_url_exists() is False:                          # check if the function_url still exists
                    break
                wait_for(1)         # 1 second delay

        assert lambda_function.function_url_exists() is False                               # expected behaviour
        assert requests.get(function_url).text == '{"Message":null}'                        # expected behaviour

        with Duration(prefix="[3rd] Create lambda (and delete function)"):
            with Temp_Lambda(lambda_name=lambda_name) as temp_lambda:                       # after creating the same lambda function again
                lambda_function = temp_lambda.aws_lambda
                assert lambda_function.function_url_exists() is False                       # now the function URL doesn't exist

    # execution results                                                (local run #1)  | (local run #2)
    # [1st] Create lambda and function URL (and delete function)         3s 338ms      |   3s 623ms
    # [2nd] Wait for function URL deletion                              60s 468ms      |  60s 506ms
    # [3rd] Create lambda (and delete function)                          3s 192ms      |   2s 789ms
