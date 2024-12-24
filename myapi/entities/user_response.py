from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserResponse(BaseModel):
    id : int
    name : str
    password : str
    time : datetime
    class Config:
        from_attributes = True