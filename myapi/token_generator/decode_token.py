import datetime

from jose import jwt

from exception import TokenExpired


def decode_jwt(token : str) -> dict[str, str]:
    today = datetime.datetime.utcnow().timestamp()
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    if payload['exp'] < today:
        raise TokenExpired
    return payload