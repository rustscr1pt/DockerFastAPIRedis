import redis
from redis import Redis


def check_redis_connection(redis_client: Redis):
    try:
        redis_client.ping()
        print("Connected to Redis!")
    except redis.ConnectionError as e:
        print(f"Redis connection failed: {e}")
