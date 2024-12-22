from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserResponse(BaseModel):
    id : int
    name : str
    password : str
    access_token : Optional[str] = None
    time : datetime
    class Config:
        orm_mode = True
        from_attributes = True