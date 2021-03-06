import json
import os

import boto3

from humoji import auth, decimalencoder

dynamodb = boto3.resource('dynamodb')


def get(event, context):
    user_id = auth.get_user(event)
    if not user_id:
        return {'message': 'Unauthorized'}

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'user_id': user_id
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
