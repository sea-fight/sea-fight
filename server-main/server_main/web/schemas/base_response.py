from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar("T")


class BaseResponseSchema(BaseModel):
    ok: int  # 0 or 1
