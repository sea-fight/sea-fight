from server_main.web.schemas.base_response import BaseResponseSchema
from server_main.web.schemas.auth.base import BaseAuthRequestSchema


class ReissueRequestSchema(BaseAuthRequestSchema):
    pass


class ReissueResponseSchema(BaseResponseSchema):
    token: str
