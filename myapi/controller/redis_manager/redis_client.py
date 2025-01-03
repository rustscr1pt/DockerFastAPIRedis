import redis

# Redis connection pool for better performance
redis_pool = redis.ConnectionPool(
    host="redis_manager", port=6379, decode_responses=True
)
redis_client = redis.Redis(connection_pool=redis_pool)
