from jose import jwt

def decode_jwt(token : str) -> dict[str, str]:
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    return payload