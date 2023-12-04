import json


def lambda_handler(event, context):
    # Your processing logic here
    message = 'Hello from Lambda!'

    return {
        'statusCode': 200,
        'body': message
    }