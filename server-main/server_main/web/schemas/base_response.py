from typing import TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class BaseResponseSchema(BaseModel):
    ok: int  # 0 or 1
