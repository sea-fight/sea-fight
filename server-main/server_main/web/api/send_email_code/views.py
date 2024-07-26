from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from server_main.db.repositories.user import UserRepository
from server_main.db.dependencies import get_db_session
from server_main.web.integrations.smtp import AsyncEmailSender, get_email_sender
from server_main.web.integrations.redis import (
    RedisClientFactory,
    RedisDB,
    get_redis_connection,
)
from server_main.web.schemas.email_verify import (
    EmailVerifyRequestSchema,
    EmailVerifyResponseSchema,
)
from server_main.handlers.send_email_code import send_email_code_handler
from .router import router


@router.post("/send-email-code")
async def send_email_code(
    request_data: EmailVerifyRequestSchema,
    db: AsyncSession = Depends(get_db_session),
    smtp_conn: AsyncEmailSender = Depends(get_email_sender),
    redis_conn: Redis = Depends(get_redis_connection(RedisDB.EMAIL_CODE_VERIFY)),
) -> EmailVerifyResponseSchema:
    await send_email_code_handler(redis_conn, smtp_conn, request_data)
    return EmailVerifyResponseSchema(ok=1)
