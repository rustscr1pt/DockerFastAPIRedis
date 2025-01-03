import datetime
import jwt


def encode_jwt(user_id: int) -> str:
    expire_date = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    token = jwt.encode(
        payload={"user_id": user_id, "exp": expire_date},
        key="secret",
        algorithm="HS256",
    )
    return token
