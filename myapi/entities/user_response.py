from datetime import datetime
from pydantic import BaseModel


class UserResponse(BaseModel):
    id : int
    name : str
    time : datetime
    class Config:
        orm_mode = True
        from_attributes = True