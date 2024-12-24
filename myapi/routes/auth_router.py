from fastapi import APIRouter, Depends, HTTPException
from entities import UserCreate
from sqlalchemy.orm import Session
from alchemy_models import get_db, User
from redis_manager import redis_client
from entities import Reply
from token_generator import encode_jwt

auth_router = APIRouter()

@auth_router.post("/login", response_model=Reply)
async def login(data: UserCreate, db: Session = Depends(get_db)) -> Reply:
    """
    Authenticates a user using their credentials (username and password). It checks the credentials
    against cached data in Redis or falls back to querying the database if not cached. On successful
    authentication, it generates and returns a JWT token.

    Args:
        data (UserCreate): The user credentials (username and password) for authentication.
        db (Session): The database session dependency, used to interact with the database.

    Returns:
        Reply: A response model containing a JWT token if authentication is successful.

    Raises:
        HTTPException:
            - 401: If the password is incorrect.
            - 404: If the user is not found or any other exception occurs during processing.

    Example:
        POST /login
        {
            "name": "john_doe",
            "password": "securepassword123"
        }

    This route will:
        1. Check Redis for cached user data.
        2. If the user exists in Redis, validate the password from the cached data.
        3. If the user is not cached, query the database for the user.
        4. Validate the password against the database entry.
        5. Return a JWT token if authentication is successful.
    """
    try:
        redis_key = f"user:{data.name}"
        cached_user = redis_client.hgetall(redis_key)
        if cached_user:
            cached_password = cached_user.get(b"password").decode('utf-8')
            cached_id = cached_user.get(b"id").decode('utf-8')
            if cached_password == data.password:
                return Reply(message=encode_jwt(cached_id))
            else:
                raise HTTPException(status_code=401, detail="Incorrect password")
        db_user = db.query(User).filter(User.name == data.name).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        if db_user.password != data.password:
            raise HTTPException(status_code=401, detail="Incorrect password")
        return Reply(message=encode_jwt(db_user.id))
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))