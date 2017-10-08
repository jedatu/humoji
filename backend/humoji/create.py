import json
import logging
import os
import time
import uuid
from decimal import *
from functools import wraps
from urllib import urlopen

import boto3
import geoip2.database
import jwt

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
READER = geoip2.database.Reader('geolite/GeoLite2-City.mmdb')
AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']
AUTH0_CLIENT_SECRET = os.environ['AUTH0_CLIENT_SECRET']


def get_user(event):
    auth_token = event.get('authorizationToken')
    if auth_token:
        auth_token = auth_token
        logger.info(auth_token)

    options = {
        'audience': AUTH0_CLIENT_ID
    }

    try:
        user_id = jwt.decode(auth_token, AUTH0_CLIENT_SECRET, options)
    except:
        return None
    else:
        return user_id


def create(event, context):
    user_id = 1#get_user(event)
    if not user_id:
        return {'message': 'Unauthorized'}

    data = json.loads(event['body'])
    if 'mood' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the mood item.")
        return
    print(event)
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
    print('payload', payload)
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
