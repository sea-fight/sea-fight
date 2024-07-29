from pydantic import BaseModel, Field, EmailStr
from server_main.settings import settings
from server_main.web.schemas.base_response import BaseResponseSchema


class SendEmailCodeRequestSchema(BaseModel):
    email: EmailStr = Field(max_length=settings.email_max_length)


class SendEmailCodeResponseSchema(BaseResponseSchema): ...
