from fastapi import FastAPI
from alchemy_models import initialize_database, create_tables
from routes import user_router, redis_router
from redis_manager import check_redis_connection

initialize_database()
check_redis_connection()
create_tables()
app = FastAPI()

app.include_router(user_router, prefix="/api", tags=["Users"])
app.include_router(redis_router, prefix="/redis", tags=["Redis"])