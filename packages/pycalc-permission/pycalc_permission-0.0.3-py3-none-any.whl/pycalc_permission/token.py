import datetime
import jwt
import uuid
from jwt import ExpiredSignatureError, InvalidSignatureError, ImmatureSignatureError
from rest_framework import exceptions
from django.conf import settings


def generate_access_token(user_id: str, roles: list[str]) -> str:
    payload = {"sub": user_id,
               "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=0, minutes=5),
               "roles": roles}
    return jwt.encode(payload=payload,
                      key=settings.PYCALC_AUTH['TOKEN_SECRET'],
                      algorithm=settings.PYCALC_AUTH['ALGORITHM'])


def generate_refresh_token(user_id: str):
    date = datetime.datetime.now(datetime.UTC)
    jwt_id = str(uuid.uuid4())
    payload = {"sub": user_id,
               "exp": date + datetime.timedelta(days=10),
               "nbf": date + datetime.timedelta(days=0, minutes=1),
               "jti": jwt_id,
               "iat": date}
    return jwt.encode(payload=payload,
                      key=settings.PYCALC_AUTH['REFRESH_SECRET'],
                      algorithm=settings.PYCALC_AUTH['ALGORITHM']), jwt_id


def _decode_token(token: str, secret: str, algorithm: str):
    try:
        return jwt.decode(jwt=token, key=secret, algorithms=algorithm)
    except ExpiredSignatureError:
        raise exceptions.AuthenticationFailed('Expired signature.')
    except InvalidSignatureError:
        raise exceptions.AuthenticationFailed('Invalid token.')
    except ImmatureSignatureError:
        raise exceptions.AuthenticationFailed('The token yet not valid.')
    except Exception as e:
        raise exceptions.AuthenticationFailed(e)


def decode_token(token: str):
    return _decode_token(token,
                         secret=settings.PYCALC_AUTH['TOKEN_SECRET'],
                         algorithm=settings.PYCALC_AUTH['ALGORITHM'])


def decode_refresh_token(token: str):
    return _decode_token(token,
                         secret=settings.PYCALC_AUTH['REFRESH_SECRET'],
                         algorithm=settings.PYCALC_AUTH['ALGORITHM'])
