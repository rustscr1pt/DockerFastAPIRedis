import logging
from fastapi import APIRouter, HTTPException
from redis_manager import redis_client

logging.basicConfig(level=logging.INFO)

redis_router = APIRouter()

@redis_router.get("/check_cache")
async def check_cache() -> dict:
    """
    Retrieves and logs all the keys currently stored in Redis. This route is useful for debugging
    and monitoring the contents of the Redis cache.

    Returns:
        dict: A dictionary containing the list of all keys in Redis under the "keys" key.

    Raises:
        HTTPException: If there is an error while accessing Redis.

    Example:
        GET /check_cache

    Response:
        {
            "keys": [
                "user:1",
                "user:2",
                "session:abcd1234"
            ]
        }

    This route will:
        1. Connect to the Redis instance.
        2. Retrieve all keys stored in Redis.
        3. Log the retrieved keys for debugging purposes.
        4. Return the list of keys as a JSON response.
    """
    try:
        keys = redis_client.keys("*")  # Get all keys in Redis
        logging.info(f"Redis Keys: {keys}")
        return {"keys": keys}
    except Exception as e:
        logging.error(f"Error checking Redis: {e}")
        raise HTTPException(status_code=500, detail="Error checking Redis")