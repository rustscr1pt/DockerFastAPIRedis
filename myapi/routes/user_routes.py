import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from alchemy_models import get_db, User
from entities import UserCreate, UserResponse
from redis_manager import redis_client

logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.post("/create_user", response_model=UserResponse)
async def create_user(data: UserCreate, db: Session = Depends(get_db)):
    try:
        # Create and save the user in the database
        db_user = User(**data.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Convert the SQLAlchemy object to a Pydantic model
        user_response = UserResponse.from_orm(db_user)

        # Cache the user in Redis as a JSON string
        redis_client.set(f"user:{db_user.id}", user_response.json())

        return user_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_users", response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    try:
        # Attempt to get users from Redis
        user_ids = redis_client.keys("user:*")
        cached_users = [redis_client.get(user_id) for user_id in user_ids]

        if not cached_users:
            users = db.query(User).all()

            # Cache each user in Redis
            for user in users:
                # Serialize User object to JSON using UserResponse model
                user_response = UserResponse.from_orm(user)
                redis_client.set(f"user:{user.id}", user_response.json())
            return users
        else:
            # Deserialize cached JSON back to UserResponse objects
            return [UserResponse.parse_raw(user) for user in cached_users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/check_cache")
async def check_cache():
    try:
        keys = redis_client.keys("*")  # Get all keys in Redis
        logging.info(f"Redis Keys: {keys}")
        return {"keys": keys}
    except Exception as e:
        logging.error(f"Error checking Redis: {e}")
        raise HTTPException(status_code=500, detail="Error checking Redis")
