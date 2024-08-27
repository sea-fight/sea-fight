from typing import Annotated
from result import Ok
from fastapi import Depends, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from server_main.db.repositories.user import UserRepository
from server_main.db.repositories.refresh_token import RefreshTokenRepository
from server_main.handlers.auth.reissue import auth_reissue_handler
from server_main.enhanced import EnhancedHTTPException
from server_main.web.schemas.auth.reissue import (
    ReissueRequestSchema,
    ReissueResponseSchema,
)
from server_main.dependencies import (
    get_db_session,
)
from server_main.settings import settings
from .router import router


@router.post("/reissue")
async def reissue(
    request_data: ReissueRequestSchema,
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
    db: AsyncSession = Depends(get_db_session),
) -> ReissueResponseSchema:
    if refresh_token is None:
        raise EnhancedHTTPException(401, "MISSING_REFRESH", {})
    result = await auth_reissue_handler(
        UserRepository(db),
        RefreshTokenRepository(db),
        refresh_token,
        request_data.fingerprint,
    )
    if isinstance(result, Ok):
        new_refresh_token, new_access_token = result.ok_value
        response.set_cookie(
            "refresh_token",
            new_refresh_token,
            max_age=settings.refresh_token_expire,
            httponly=True,
        )
        return ReissueResponseSchema(ok=1, token=new_access_token.encode())
    raise EnhancedHTTPException(400, result.err_value, {})
