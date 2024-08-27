from fastapi import Depends
import redis.asyncio as redis
from result import Err, Ok, Result
from server_main.web.integrations.redis import (
    RedisDB,
)
from server_main.web.integrations.services import Mailer
from server_main.web.schemas.verify.email.send_code import (
    EmailSendCodeRequestSchema,
    EmailSendCodeResponseSchema,
)
from server_main.enhanced import EnhancedHTTPException
from server_main.handlers.verify.email.send_code import send_email_code_handler
from server_main.dependencies import (
    get_mailer,
    get_redis_connection,
)
from .router import router


@router.post("/send-code")
async def email_send_code(
    request_data: EmailSendCodeRequestSchema,
    redis_mailer: redis.Redis = Depends(
        get_redis_connection(RedisDB.EMAIL_CODE_VERIFY)
    ),
    mailer: Mailer = Depends(get_mailer),
) -> EmailSendCodeResponseSchema:
    result: Result[None, None] = await send_email_code_handler(
        redis_mailer, mailer, request_data
    )
    match result:
        case Ok(_):
            return EmailSendCodeResponseSchema(ok=1)
        case Err(_):
            raise EnhancedHTTPException(
                403,
                code="ATTEMPTS_LIMIT_REACHED",
                info={"cooldown": "30"},
            )
