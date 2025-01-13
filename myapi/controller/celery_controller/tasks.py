from celery import shared_task
from controller import get_db
from controller.redis_manager import redis_client
from model import User, UserResponse


@shared_task
def cache_user_in_redis(user_id: int):
    """
    Cache a user in Redis after creation or update.
    """
    db = next(get_db())  # Get a new database session
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user_response = UserResponse.from_orm(user)
        redis_client.set(f"user:{user_id}", user_response.json(), ex=300)


@shared_task
def fetch_users_from_db():
    """
    Fetch all users from the database and cache them in Redis.
    """
    db = next(get_db())  # Get a new database session
    users = db.query(User).all()
    for user in users:
        user_response = UserResponse.from_orm(user)
        redis_client.set(f"user:{user.id}", user_response.json(), ex=300)
    return [user_response.dict() for user in users]
