# Define the User model
from sqlalchemy import Column, String, Integer, DateTime, func
from .models import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))  # Specify a length for VARCHAR
    time = Column(DateTime, default=func.now())  # Correctly define the column