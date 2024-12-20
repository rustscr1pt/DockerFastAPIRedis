from pydantic import BaseModel


class User(BaseModel):
    id : int
    name : str
    time : str
    class Config:
        orm_mode = True