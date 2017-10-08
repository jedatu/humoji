import json
import logging
import os
from urllib import urlopen

import boto3
from jose import jwt

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')

AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']
AUTH0_CLIENT_SECRET = os.environ['AUTH0_CLIENT_SECRET']
AUTH0_DOMAIN = 'jedatu.auth0.com'
API_AUDIENCE = AUTH0_CLIENT_ID
ALGORITHMS = ["RS256"]


def get_token(event):
    """Obtains the access token from the Authorization Header
    """
    auth = event.get('authorizationToken')
    try:
        parts = auth.split()
        token = parts[1]
    except:
        token = 1
    return token


def get_user(event):
    token = get_token(event)
    user_id = 1
    try:
        jsonurl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        rsa_key = {}

        for key in jwks["keys"]:
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
    except:
        pass
    return user_id
