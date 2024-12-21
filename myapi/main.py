from fastapi import FastAPI
from alchemy_models import initialize_database, create_tables
from user_routes import router

initialize_database()
create_tables()
app = FastAPI()
app.include_router(router, prefix="/api", tags=["Users"])