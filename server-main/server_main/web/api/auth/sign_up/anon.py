from server_main.db.repositories.refresh_token import RefreshTokenRepository

from fastapi import Depends, Response
from result import Ok
from sqlalchemy.ext.asyncio import AsyncSession
from server_main.settings import settings
from server_main.db.repositories.user import UserRepository
from server_main.enhanced import EnhancedHTTPException

from server_main.web.schemas.auth.sign_up.anon import (
    SignUpAnonRequestSchema,
    SignUpAnonResponseSchema,
)
from server_main.dependencies import (
    get_db_session,
)

from server_main.handlers.auth.sign_up.anon import sign_up_anon_handler
from .router import router


@router.post("/anon", response_model=SignUpAnonResponseSchema)
async def anon(
    request_data: SignUpAnonRequestSchema,
    response: Response,
    db: AsyncSession = Depends(get_db_session),
) -> SignUpAnonResponseSchema:
    result = await sign_up_anon_handler(
        UserRepository(db), RefreshTokenRepository(db), request_data.fingerprint
    )
    if isinstance(result, Ok):
        refresh, access = result.ok_value
        response.set_cookie(
            "refresh_token",
            refresh,
            max_age=settings.refresh_token_expire,
            httponly=True,
        )
        return SignUpAnonResponseSchema(ok=1, token=access.encode())
    raise EnhancedHTTPException(500, "UNHANDLED_YET", {})
