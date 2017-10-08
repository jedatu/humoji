import json
import logging
import os
import time
import uuid

import jwt
import boto3
import geoip2.database

from functools import wraps
import jwt
from urllib import urlopen
from decimal import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
READER = geoip2.database.Reader('geolite/GeoLite2-City.mmdb')
AUTH0_CLIENT_ID = 'eRoI93Zle2L4iBWmKmdFcrU2dfufX3qu6-'
AUTH0_CLIENT_SECRET = 'YUg9btEv9BhBfYBTIn76mkQlX4DQUg'

def iotclick(event, context):
    mood_map = {0: 'angry', 1: 'sad', 2: 'indifferent', 3: 'content', 4: 'happy'}
    mood = 0 # Long Press
    if event['clickType'] == 'DOUBLE':
      mood = 4
    elif event['clickType'] == 'SINGLE':
      mood = 2

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    user_id = 0
    if event['serialNumber'] == 'G030JF056266U9CF':
      user_id = 1

    ip = None
    try:
        ip = event['requestContext']['identity']['sourceIp']
    except:
        pass

    item = {
        'id': str(uuid.uuid1()),
        'timestamp': timestamp,
        'mood': int(mood),
        'user_id': user_id
    }
    enrich_payload(item, ip)

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
    print(
        'RECEIVED IOT AWS button click. The mood is: {}.'.format(
            mood_map[mood]
        )
    )
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
