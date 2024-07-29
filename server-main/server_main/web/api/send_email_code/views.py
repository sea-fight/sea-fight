from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from aio_pika.abc import AbstractRobustConnection
from server_main.db.dependencies import get_db_session
from server_main.web.integrations.redis import (
    RedisDB,
    get_redis_connection,
)
from server_main.web.integrations.rabbitmq import get_rabbitmq_connection
from server_main.web.schemas.send_email_code import (
    SendEmailCodeRequestSchema,
    SendEmailCodeResponseSchema,
)
from server_main.web.schemas.error_response import EnhancedHTTPException
from server_main.handlers.send_email_code import send_email_code_handler
from .router import router


@router.post("/send-email-code")
async def send_email_code(
    request_data: SendEmailCodeRequestSchema,
    db: AsyncSession = Depends(get_db_session),
    redis_connection: Redis = Depends(get_redis_connection(RedisDB.EMAIL_CODE_VERIFY)),
    rabbitmq_connection: AbstractRobustConnection = Depends(get_rabbitmq_connection),
) -> SendEmailCodeResponseSchema:
    if await send_email_code_handler(
        redis_connection, rabbitmq_connection, request_data
    ):
        return SendEmailCodeResponseSchema(ok=1)
    raise EnhancedHTTPException(
        403,
        code="ATTEMPTS_LIMIT_REACHED",
        info="Слишком много попыток! Попробуйте через 30 минут.",
    )
