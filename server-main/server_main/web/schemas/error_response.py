from typing import Any
from .base_response import BaseResponseSchema


class ErrorResponseSchema(BaseResponseSchema):
    code: str
    info: Any
