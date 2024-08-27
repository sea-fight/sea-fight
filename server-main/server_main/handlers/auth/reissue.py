import uuid
from result import Err, Ok, Result

from server_main.db.repositories.user import UserRepository
from server_main.db.repositories.refresh_token import RefreshTokenRepository
from server_main.utils.timestamp import get_utc_datetime
from server_main.utils.security.refresh_token import std_exp
from server_main.utils.security.access_token import AccessToken
from server_main.web.schemas.auth.reissue import (
    ReissueRequestSchema,
)


async def auth_reissue_handler(
    user_repo: UserRepository,
    refresh_token_repo: RefreshTokenRepository,
    refresh_token: str,
    fingerprint: str,
) -> Result[tuple[str, AccessToken], str]:
    refresh_token_db = await refresh_token_repo.get_by_token_fingerprint(
        refresh_token, fingerprint
    )
    if refresh_token_db is None:
        return Err("INVALID_DATA")  # Refresh or fingerprint
    user_db = await refresh_token_db.awaitable_attrs.user
    new_refresh_token = await refresh_token_repo.create(
        token=str(uuid.uuid4()),
        user_id=user_db.id,
        fingerprint=fingerprint,
        expires_at=std_exp(get_utc_datetime()),
    )

    return Ok(
        (
            new_refresh_token.token,
            AccessToken.new(user_db.id, user_db.created_at),
        )
    )
