import redis.asyncio as redis
from loguru import logger
from result import Ok, Err, Result
from server_main.web.schemas.verify.email.send_code import EmailSendCodeRequestSchema
from server_main.web.integrations.services import Mailer
from server_main.utils.timestamp import get_utc_datetime_str
from server_main.utils.security.email_code import generate_email_verification_code
from server_main.settings import settings


# TODO: add create_timestamp and rename timestamp -> update_timestamp
# Maybe remove timestamp record at all?
async def send_email_code_handler(
    redis_mailer: redis.Redis,
    mailer: Mailer,
    data: EmailSendCodeRequestSchema,
) -> Result[None, None]:
    """
    Return: False if limit reached
    """
    logger.info("Process send_message_handler...")
    code = generate_email_verification_code()
    email_str = str(data.email)

    raw_attempts: bytes | None = await redis_mailer.hget(email_str, "attempts")  # type: ignore
    attempts: int = 0
    if raw_attempts is not None:
        attempts = int(raw_attempts)

    if attempts < settings.email_code_request_attempts_limit:
        attempts += 1
        logger.info(f"Set attempts to {attempts} for {email_str}")
        await redis_mailer.hset(
            email_str,
            mapping={
                "timestamp": get_utc_datetime_str(),
                "code": code,
                "attempts": attempts,
            },
        )  # type: ignore

        logger.info(
            f"Set redis record expiretime to {settings.email_code_expiretime} for {email_str}"
        )
        await redis_mailer.expire(email_str, settings.email_code_expiretime)

        await mailer.immediatemail(data.email, "verify-email", {"code": code})
        return Ok(None)

    await redis_mailer.hset(
        email_str,
        mapping={
            "timestamp": get_utc_datetime_str(),
            "code": code,
            "attempts": attempts + 1,
        },
    )  # type: ignore
    await redis_mailer.expire(email_str, settings.email_code_expiretime)
    return Err(None)
