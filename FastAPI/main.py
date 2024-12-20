from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from alchemy_models import SessionLocal, User
from entities import UserCreate, UserResponse

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
app = FastAPI()


@app.post(
    "/api/create_user",
    response_model=UserResponse
)
async def create_user(data: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = User(**data.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/api/get_users",
    response_model=list[UserResponse]
)
async def get_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))