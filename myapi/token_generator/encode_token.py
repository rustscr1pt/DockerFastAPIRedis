import datetime
from jose import jwt

def encode_jwt(user_id : int) -> str:
    expire_date_unix = (datetime.datetime.utcnow() + datetime.timedelta(hours=24)).timestamp()
    token = jwt.encode(
        {'user_id': user_id, 'exp': expire_date_unix},
        'secret',
        algorithm='HS256',
    )
    return token