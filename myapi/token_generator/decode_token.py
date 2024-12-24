import datetime
import jwt
from exception import TokenExpired


def decode_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(
            jwt=token,
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