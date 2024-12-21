from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from alchemy_models import get_db, User
from entities import UserCreate, UserResponse

router = APIRouter()

@router.post("/create_user", response_model=UserResponse)
async def create_user(data: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = User(**data.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_users", response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))