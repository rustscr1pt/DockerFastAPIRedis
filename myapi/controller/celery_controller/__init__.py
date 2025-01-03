from .celery_base import app
from .tasks import cache_user_in_redis, fetch_users_from_db
