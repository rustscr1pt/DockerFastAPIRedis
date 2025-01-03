from pydantic import BaseModel, constr, field_validator
import re


class UserCreate(BaseModel):
    name: constr(min_length=3, max_length=50)
    password: constr(min_length=3, max_length=50)

    @field_validator("password")
    def validate_password(cls, value):
        if not re.search(r"[a-z]", value):
            raise ValueError("password must contain at least one lowercase letter")
        if not re.search(r"[A-Z]", value):
            raise ValueError("password must contain at least one uppercase letter")
        if not re.search(r"\d", value):
            raise ValueError("password must contain at least one digit")
        return value
