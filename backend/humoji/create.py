import json
import logging
import os
import time
import uuid

import boto3
dynamodb = boto3.resource('dynamodb')


def create(event, context):
    data = json.loads(event['body'])
    if 'mood' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the mood item.")
        return
    print(event)

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    # user_id = context['user_id']

    item = {
        'id': str(uuid.uuid1()),
        # 'user_id': user_id,
        'mood': int(data['mood']),
        # 'user_id': str(uuid.uuid1()),
        'timestamp': timestamp,
    }

    try:
        ip = event['requestContext']['identity']['sourceIp']
        request_context = event['requestContext']
    except:
        pass
    else:
        item['ip'] = ip
        item['request_context'] = request_context
    print('\n\n\n', item)

    # write the todo to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item),
        "headers": {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Credentials': True
        }
    }

    return response
