import redis

# Redis connection pool for better performance
redis_pool = redis.ConnectionPool(host="redis_manager", port=6379, decode_responses=True)
redis_client = redis.Redis(connection_pool=redis_pool)

# Function to test Redis connection
def check_redis_connection():
    try:
        redis_client.ping()
        print("Connected to Redis!")
    except redis.ConnectionError as e:
        print(f"Redis connection failed: {e}")
