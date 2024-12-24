import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from alchemy_models import get_db, User
from entities import UserCreate, UserResponse
from redis_manager import redis_client
from token_generator import decode_jwt

logging.basicConfig(level=logging.INFO)

auth_scheme = HTTPBearer()
user_router = APIRouter()

@user_router.post("/create_user", response_model=UserResponse)
async def create_user(data: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    """
    Creates a new user and stores it in the database. The user is also cached in Redis for quick access.

    Args:
        data (UserCreate): The user data to create a new user.
        db (Session): The database session dependency, used to interact with the database.

    Returns:
        UserResponse: A Pydantic model of the created user, containing the user information.

    Raises:
        HTTPException: If there is an error during the user creation process (e.g., database error).

    Example:
        POST /create_user
        {
            "name": "john_doe",
            "email": "john@example.com",
            "password": "securepassword123"
        }

    This route will:
        1. Save the user to the database.
        2. Cache the user's data in Redis for fast retrieval.
        3. Return the created user response.
    """
    try:
        db_user = User(**data.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        user_response = UserResponse.from_orm(db_user)
        redis_client.set(f"user:{db_user.id}", user_response.json(), ex=300)
        return user_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_router.get("/get_users", response_model=list[UserResponse])
async def get_users(
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)
) -> list[UserResponse]:
    """
    Retrieves a list of users. First, it checks Redis for cached users, and if not found, it fetches them from the database.

    Args:
        db (Session): The database session dependency, used to interact with the database.
        credentials (HTTPAuthorizationCredentials): The authorization credentials containing the JWT token.

    Returns:
        list[UserResponse]: A list of Pydantic models representing the users.

    Raises:
        HTTPException: If there is an error during the process (e.g., database error or invalid token).

    Example:
        GET /get_users
        Authorization: Bearer <your_jwt_token>

    This route will:
        1. Decode and validate the JWT token.
        2. Attempt to retrieve user data from Redis.
        3. If no users are cached in Redis, it fetches the users from the database.
        4. Return a list of users, either from the cache or the database.
    """
    try:
        decode_jwt(credentials)
        user_ids = redis_client.keys("user:*")
        cached_users = [redis_client.get(user_id) for user_id in user_ids]
        if not cached_users:
            users = db.query(User).all()
            for user in users:
                user_response = UserResponse.from_orm(user)
                redis_client.set(f"user:{user.id}", user_response.json(), ex=300)
            return users
        else:
            return [UserResponse.parse_raw(user) for user in cached_users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
