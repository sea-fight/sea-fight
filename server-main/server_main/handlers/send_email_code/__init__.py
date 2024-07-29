from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import redis.asyncio as redis
from aio_pika.abc import AbstractRobustConnection
from server_main.web.schemas.send_email_code import SendEmailCodeRequestSchema
from server_main.web.integrations.rabbitmq import send_mail
from server_main.utils.timestamp import get_utc_datetime_str, convert_str_to_datetime
from server_main.utils.security.email_code import generate_email_verification_code
from server_main.settings import settings


# TODO: add create_timestamp and rename timestamp -> update_timestamp
async def send_email_code_handler(
    redis_connection: redis.Redis,
    rabbitmq_connection: AbstractRobustConnection,
    data: SendEmailCodeRequestSchema,
) -> bool:
    """
    Return: False if limit reached
    """
    code = generate_email_verification_code()
    email_str = str(data.email)
    attempts: int | None = await redis_connection.hget(email_str, "attempts")  # type: ignore
    if attempts is None:
        attempts = 0
    if attempts < settings.email_code_request_attempts_limit:
        await redis_connection.hset(
            email_str,
            mapping={
                "timestamp": get_utc_datetime_str(),
                "code": code,
                "attempts": attempts + 1,
            },
        )  # type: ignore

        await redis_connection.expire(email_str, settings.email_code_expiretime)
        await send_mail(
            rabbitmq_connection,
            email_str,
            "verify-email.txt",
            {"code": str(code)},
        )
        return True

    await redis_connection.hset(
        email_str,
        mapping={
            "timestamp": get_utc_datetime_str(),
            "code": code,
            "attempts": attempts + 1,
        },
    )  # type: ignore
    await redis_connection.expire(email_str, settings.email_code_expiretime)
    return False
