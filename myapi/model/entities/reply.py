from typing import Any

from pydantic import BaseModel


class Reply(BaseModel):
    message: Any