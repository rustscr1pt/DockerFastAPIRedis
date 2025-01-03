from fastapi import FastAPI
from controller import engine, redis_client, Base
from controller.alchemy_controller import initialize_database, create_tables
from view.routes import auth_router
from view.routes import user_router, redis_router
from controller.redis_manager import check_redis_connection

initialize_database(engine=engine)
check_redis_connection(redis_client=redis_client)
create_tables(engine=engine, Base=Base)
app = FastAPI()

app.include_router(user_router, prefix="/api", tags=["Users"])
app.include_router(auth_router, prefix="/api", tags=["Auth"])
app.include_router(redis_router, prefix="/redis", tags=["Redis"])
