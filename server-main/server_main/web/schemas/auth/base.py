from typing import Annotated
from pydantic import BaseModel, Field, StringConstraints, EmailStr
from server_main.settings import settings


class BaseAuthRequestSchema(BaseModel):
    fingerprint: Annotated[
        str,
        StringConstraints(
            max_length=settings.fingerprint_max_length,
        ),
    ]
