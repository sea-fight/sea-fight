import redis.asyncio as redis
from loguru import logger
from server_main.web.schemas.send_email_code import SendEmailCodeRequestSchema
from server_main.web.integrations.services import Mailer
from server_main.utils.timestamp import get_utc_datetime_str
from server_main.utils.security.email_code import generate_email_verification_code
from server_main.settings import settings


# TODO: add create_timestamp and rename timestamp -> update_timestamp
async def send_email_code_handler(
    redis_connection: redis.Redis,
    mailer: Mailer,
    data: SendEmailCodeRequestSchema,
) -> bool:
    """
    Return: False if limit reached
    """
    logger.info("Process send_message_handler...")
    code = generate_email_verification_code()
    await mailer.immediatemail(data.email, "verify-email", {"code": code})
    return True
    # email_str = str(data.email)
    # raw_attempts: str | None = await redis_connection.hget(email_str, "attempts")  # type: ignore
    # attempts: int = 0
    # if raw_attempts is not None:
    #     attempts = int(raw_attempts)
    #
    # if attempts < settings.email_code_request_attempts_limit:
    #     logger.info(f"set attempts to {attempts + 1} for {email_str}")
    #     await redis_connection.hset(
    #         email_str,
    #         mapping={
    #             "timestamp": get_utc_datetime_str(),
    #             "code": code,
    #             "attempts": attempts + 1,
    #         },
    #     )  # type: ignore
    #
    #     logger.info(
    #         f"set redis write expiretime to {settings.email_code_expiretime} for {email_str}"
    #     )
    #     await redis_connection.expire(email_str, settings.email_code_expiretime)
    #     await send_mail(
    #         rabbitmq_connection,
    #         email_str,
    #         "verify-email.txt",
    #         {"code": str(code)},
    #     )
    #     return True
    #
    # await redis_connection.hset(
    #     email_str,
    #     mapping={
    #         "timestamp": get_utc_datetime_str(),
    #         "code": code,
    #         "attempts": attempts + 1,
    #     },
    # )  # type: ignore
    # await redis_connection.expire(email_str, settings.email_code_expiretime)
    # return False
