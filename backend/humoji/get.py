import json
import os

import boto3

from humoji import decimalencoder, get_user

dynamodb = boto3.resource('dynamodb')



def get(event, context):
    user_id = get_user(event)
    if not user_id:
        return {'message': 'Unauthorized'}

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
