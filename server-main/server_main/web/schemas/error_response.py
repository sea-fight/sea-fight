from fastapi import HTTPException
from .base_response import BaseResponseSchema


class ErrorResponseSchema(BaseResponseSchema):
    code: str
    info: str


class EnhancedHTTPException(HTTPException):
    def __init__(self, status_code: int, code: str, info: str):
        super().__init__(status_code=status_code, detail=info)
        self.code = code
        self.info = info
