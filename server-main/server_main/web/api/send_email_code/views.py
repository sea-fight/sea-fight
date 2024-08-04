from fastapi import Depends
from redis.asyncio import Redis
from server_main.web.integrations.redis import (
    RedisDB,
)
from server_main.web.integrations.services import Mailer
from server_main.web.schemas.send_email_code import (
    SendEmailCodeRequestSchema,
    SendEmailCodeResponseSchema,
)
from server_main.enhanced import EnhancedHTTPException
from server_main.handlers.send_email_code import send_email_code_handler
from server_main.dependencies import (
    get_mailer,
    get_redis_connection,
)
from .router import router


@router.post("/send-email-code")
async def send_email_code(
    request_data: SendEmailCodeRequestSchema,
    redis_connection: Redis = Depends(get_redis_connection(RedisDB.EMAIL_CODE_VERIFY)),
    mailer: Mailer = Depends(get_mailer),
) -> SendEmailCodeResponseSchema:
    if await send_email_code_handler(redis_connection, mailer, request_data):
        return SendEmailCodeResponseSchema(ok=1)
    raise EnhancedHTTPException(
        403,
        code="ATTEMPTS_LIMIT_REACHED",
        info="Слишком много попыток! Попробуйте через 30 минут.",
    )
