from fastapi import APIRouter, Depends, HTTPException
from entities import UserCreate
from sqlalchemy.orm import Session
from alchemy_models import get_db, User
from redis_manager import redis_client
from entities import Reply
from token_generator import encode_jwt

auth_router = APIRouter()

@auth_router.post(
    "/login",
    response_model=Reply
)
async def login(data : UserCreate, db: Session = Depends(get_db)):
    try:
        redis_key = f"user:{data.username}"
        cached_user = redis_client.hgetall(redis_key)
        if cached_user:
            cached_password = cached_user.get(b"password").decode('utf-8')
            cached_id = cached_user.get(b"id").decode('utf-8')
            if cached_password == data.password:
                # Generate JWT token using the cached user's ID
                return Reply(message=encode_jwt(cached_id))
            else:
                raise HTTPException(status_code=401, detail="Incorrect password")
        db_user = db.query(User).filter(User.name == data.username).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        if db_user.password != data.password:
            raise HTTPException(status_code=401, detail="Incorrect password")
        redis_client.hset(redis_key, mapping={
            "name": db_user.name,
            "password": db_user.password,
        })
        return Reply(message=encode_jwt(db_user.id))
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
