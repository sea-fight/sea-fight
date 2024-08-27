import uuid
from datetime import datetime, timedelta, timezone
from result import Ok, Err, Result
import redis.asyncio as redis
from loguru import logger
from server_main.db.repositories.refresh_token import RefreshTokenRepository
from server_main.db.repositories.user import UserRepository
from server_main.db.models.user import User
from server_main.web.schemas.auth.sign_up.anon import SignUpAnonRequestSchema
from server_main.utils.security.access_token import AccessToken
from server_main.enhanced import EnhancedHTTPException
from server_main.settings import settings


async def sign_up_anon_handler(
    user_repo: UserRepository,
    refresh_token_repo: RefreshTokenRepository,
    fingerprint: str,
) -> Result[tuple[str, AccessToken], str]:
    """
    Returns:
        Result:
            Ok(str, AccessToken))
            Err(EnhancedHTTPException)
    """
    refresh_expires_at = datetime.now(timezone.utc) + timedelta(
        seconds=settings.refresh_token_expire
    )  # TODO: server_main.utils.security.refresh_token.std_exp

    user = await user_repo.create(
        username="Аноним",
    )
    refresh_token = await refresh_token_repo.create(
        token=str(uuid.uuid4()),
        user_id=user.id,
        fingerprint=fingerprint,
        expires_at=refresh_expires_at,
    )

    access_token = AccessToken.new(user.id, user.created_at)

    return Ok((refresh_token.token, access_token))
