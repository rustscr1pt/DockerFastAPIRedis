from fastapi import APIRouter, Depends, HTTPException

from entities import UserCreate
from sqlalchemy.orm import Session
from alchemy_models import get_db, User
from redis_manager import redis_client

auth_router = APIRouter()

@auth_router.get(
    "/login",

)
async def login(data : UserCreate, db: Session = Depends(get_db)):
    try:
        redis_key = f"user:{data.username}"
        cached_user = redis_client.hgetall(redis_key)
        if cached_user:
            cached_password = cached_user.get(b"password").decode('utf-8')
            if cached_password == data.password:
                return
            else:
                raise HTTPException(status_code=401, detail="Incorrect password")
        db_user = db.query(User).filter(User.username == data.username).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        if db_user.password != data.password:
            raise HTTPException(status_code=401, detail="Incorrect password")
