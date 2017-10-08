import json
import logging
import os
import time
import uuid

import boto3
import geoip2.database

from humoji import auth

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
READER = geoip2.database.Reader('geolite/GeoLite2-City.mmdb')


def create(event, context):
    mood_map = {5: 'angry', 4: 'sad', 3: 'indifferent', 2: 'content', 1: 'happy'}
    user_id = auth.get_user(event)
    if not user_id:
        return {'message': 'Unauthorized'}

    data = json.loads(event['body'])
    if 'mood' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the mood item.")
        return
    # print(event['requestContext']['identity']['sourceIp'])

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    ip = None
    try:
        ip = event['requestContext']['identity']['sourceIp']
    except:
        pass

    item = {
        'id': str(uuid.uuid1()),
        'timestamp': timestamp,
        'mood': int(data['mood']),
        'user_id': user_id
    }
    enrich_payload(item, ip)

    # write the todo to the database
    table.put_item(Item=item)
    print(
        'RECEIVED interaction from our website. The mood is: {}. Location: {}'.format(
            mood_map[int(data['mood'])],
            item['location'].get('country')
        )
    )
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


def enrich_payload(payload, ip=None):
    """All enrichment of the given payload should happen in this function.
    It accepts the initial payload and returns the payload with additional
    information.
    """
    if ip:
        payload['ip'] = ip
        location = get_location_for_ip(ip)
        if location:
            payload['location'] = location
    return payload


def get_location_for_ip(ip, reader=READER):
    """For a given IP Address, returns a dictionary with city, region,
    country, latitude, and longitude
    On failure it will return an empty dictionary, rather than raise an exception.
    """

    location = {}

    try:
        resp = READER.city(ip)
        location = {
            'city': resp.city.name,
            'region': resp.subdivisions.most_specific.name,
            'country': resp.country.name,
            'latitude': str(resp.location.latitude),
            'longitude': str(resp.location.longitude)
        }
    except Exception as e:
        logger.exception('get_location failed.')

    return location
