from fastapi import FastAPI

from entities import User, UserCreate

app = FastAPI()


@app.post(
    "/api/create_user",
    response_model=User
)
async def create_user(user: UserCreate):
