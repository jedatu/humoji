import json
import os

from humoji import auth, decimalencoder
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')


def list(event, context):
    user_id = auth.get_user(event)
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # result = table.scan()
    result = table.query(
        KeyConditionExpression=Key('user_id').eq(user_id)
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder)
    }
    moods = []
    for result in result['Items']:
        mood = result.get('mood')
        if mood:
            moods.append(mood)
    average_mood = reduce(lambda x, y: x + y, moods) / len(moods)
    print('avg mood: ', average_mood)

    return {"Average mood:": average_mood}
