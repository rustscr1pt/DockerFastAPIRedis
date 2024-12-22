import logging
from fastapi import APIRouter, HTTPException
from redis_manager import redis_client

logging.basicConfig(level=logging.INFO)

redis_router = APIRouter()

@redis_router.get("/check_cache")
async def check_cache():
    try:
        keys = redis_client.keys("*")  # Get all keys in Redis
        logging.info(f"Redis Keys: {keys}")
        return {"keys": keys}
    except Exception as e:
        logging.error(f"Error checking Redis: {e}")
        raise HTTPException(status_code=500, detail="Error checking Redis")