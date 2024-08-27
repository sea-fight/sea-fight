from typing import Annotated

from pydantic import Field, StringConstraints, EmailStr
from server_main.settings import settings
from server_main.web.schemas.base_response import BaseResponseSchema
from server_main.web.schemas.auth.base import BaseAuthRequestSchema


class SignUpUserRequestSchema(BaseAuthRequestSchema):
    username: Annotated[
        str,
        StringConstraints(
            min_length=settings.username_min_length,
            max_length=settings.username_max_length,
        ),
    ]
    email: EmailStr = Field(max_length=settings.email_max_length)
    code: Annotated[
        str,
        StringConstraints(
            min_length=settings.email_code_length, max_length=settings.email_code_length
        ),
    ]


class SignUpUserResponseSchema(BaseResponseSchema):
    access_token: str
