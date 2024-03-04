'''

JWT Token Generation: signJWT(userID: str) -> dict generates a JSON Web Token with a 10-minute expiration, returning it as an "access_token" in a dictionary.

JWT Token Decoding: decodeJWT(token: str) -> dict decodes the provided JWT token, returning its contents as a dictionary if valid and not expired.

'''

import time
import jwt
from decouple import config


JWT_SECRET = config('secret')
JWT_ALGORITHM = config('algorithm')


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(userID: str):
    payload = {
        "userID": userID,
        "expiry": time.time() + 600000
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decoded_token if decoded_token['expiry'] >= time.time() else None
    except:
        return {}
