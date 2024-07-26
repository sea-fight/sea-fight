from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints, EmailStr
from server_main.settings import settings
from server_main.web.schemas.base_response import BaseResponseSchema


class SignUpRequestSchema(BaseModel):
    username: Annotated[
        str,
        StringConstraints(
            min_length=settings.username_min_length,
            max_length=settings.username_max_length,
        ),
    ]
    nickname: Annotated[
        str,
        StringConstraints(
            min_length=settings.nickname_min_length,
            max_length=settings.nickname_max_length,
        ),
    ]
    email: EmailStr = Field(max_length=settings.email_max_length)
    password: Annotated[
        str,
        StringConstraints(
            min_length=settings.password_min_length,
        ),
    ]


class SignUpResponseSchema(BaseResponseSchema):
    id: str  # uuid
    refresh_token: str
