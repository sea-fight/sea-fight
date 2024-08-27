from pydantic import BaseModel


class BaseResponseSchema(BaseModel):
    ok: int  # 0 or 1
