from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from alchemy_models import SessionLocal
from entities import User, UserCreate

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
app = FastAPI()


@app.post(
    "/api/create_user",
    response_model=User
)
async def create_user(data: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = User(**data.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"data" : db_user}
    except Exception as e:
        return {"error" : str(e)}


@app.get(
    "/api/get_users",
    response_model=list[User]
)
async def get_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        return {"data" : users}
    except Exception as e:
        return {"error" : str(e)}