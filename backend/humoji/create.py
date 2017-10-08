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
from jose import jwt

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
READER = geoip2.database.Reader('geolite/GeoLite2-City.mmdb')
AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']
AUTH0_CLIENT_SECRET = os.environ['AUTH0_CLIENT_SECRET']
AUTH0_DOMAIN = 'jedatu.auth0.com'
API_AUDIENCE = AUTH0_CLIENT_ID
ALGORITHMS = ["RS256"]


def get_token(event):
    """Obtains the access token from the Authorization Header
    """
    auth = event.get('authorizationToken')
    token = 1
    try:
        parts = auth.split()
        token = parts[1]
    except:
        pass
    return token


def get_user(event):
    token = get_token(event)
    jsonurl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            user_id = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://" + AUTH0_DOMAIN + "/"
            )
        except:
            pass
        else:
            return user_id


def create(event, context):
    user_id = get_user(event)
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
