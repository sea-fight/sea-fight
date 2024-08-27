from server_main.web.schemas.base_response import BaseResponseSchema
from server_main.web.schemas.auth.base import BaseAuthRequestSchema


class SignUpAnonRequestSchema(BaseAuthRequestSchema):
    pass


class SignUpAnonResponseSchema(BaseResponseSchema):
    token: str
