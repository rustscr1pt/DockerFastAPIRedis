import datetime
import jwt
from fastapi.security import HTTPAuthorizationCredentials

from model.entities.exception import TokenExpired


def decode_jwt(token: HTTPAuthorizationCredentials) -> dict:
    try:
        payload = jwt.decode(
            jwt=token.credentials,
            key='secret',
            algorithms=['HS256']
        )
        if payload['exp'] < datetime.datetime.utcnow().timestamp():
            raise TokenExpired("Token has expired")
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpired("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")