from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import redis.asyncio as redis
from server_main.web.schemas.email_verify import EmailVerifyRequestSchema
from server_main.web.integrations.smtp import AsyncEmailSender
from server_main.utils.timestamp import get_utc_datetime_str, convert_str_to_datetime
from server_main.utils.security.email_code import generate_email_verification_code
from server_main.settings import settings


async def send_email_code_handler(
    redis_conn: redis.Redis, smtp_conn: AsyncEmailSender, data: EmailVerifyRequestSchema
) -> bool:
    code = generate_email_verification_code()
    # TODO: check for attempts and return false when spamming
    await redis_conn.hset(
        data.email.__str__(),
        mapping={
            "timestamp": get_utc_datetime_str(),
            "code": code,
            "attempt": 1,
        },
    )  # type: ignore
    await redis_conn.expire(data.email.__str__(), settings.email_code_expiretime)
    text = f"<p>{code}</p>"
    msg = MIMEMultipart()
    msg["From"] = settings.email_sender
    msg["To"] = data.email
    msg["Subject"] = "Морской бой! Верификация электронной почты"
    msg.attach(MIMEText(text, "html"))
    await smtp_conn.send_email(msg)
    return True
