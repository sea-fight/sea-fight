from __future__ import annotations

from email.mime.multipart import MIMEMultipart
import aiosmtplib
from loguru import logger

from server_main.settings import settings


class AsyncEmailSender:
    """Class for sending emails using an async API without blocking the main thread.

    Attributes:
        smtp_server: SMTP server address.
        smtp_port: SMTP server port.
        email_sender: Email address of the sender.
        email_password: Password for the sender's email.
        smtp_client: aiosmtplib.SMTP client instance.
    """

    # smtp_server, smtp_port, email_sender, email_password = required_env_many(
    #     "SMTP_SERVER",
    #     "SMTP_PORT",
    #     "EMAIL_SENDER",
    #     "EMAIL_SENDER_PASSWORD",
    # )

    def __init__(
        self, smtp_server: str, smtp_port: int, email_sender: str, email_password: str
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_sender = email_sender
        self.email_password = email_password
        self.smtp_client: aiosmtplib.SMTP = aiosmtplib.SMTP(
            hostname=self.smtp_server, port=self.smtp_port
        )

    async def _connect(self) -> aiosmtplib.SMTP:
        """Connect to the email server.

        Returns:
            aiosmtplib.SMTP: An instance of the SMTP client.
        """
        if not self.smtp_client.is_connected:
            await self.smtp_client.connect()
            await self.smtp_client.login(self.email_sender, self.email_password)
        return self.smtp_client

    async def _reconnect(self) -> aiosmtplib.SMTP:
        """Reconnect to the email server if the connection is lost.

        Returns:
            aiosmtplib.SMTP: An instance of the SMTP client.
        """
        logger.info("Reconnecting to SMTP server...")
        self.smtp_client.close()
        return await self._connect()

    async def send_email(self, msg: MIMEMultipart) -> bool:
        """Send an email to the receiver.

        Args:
            msg: The MIMEMultipart object to be sent.

        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """
        try:
            if not self.smtp_client.is_connected:
                await self._connect()
            await self.smtp_client.send_message(msg)
            logger.info(f"Email to {msg['To']} sent successfully.")
        except aiosmtplib.errors.SMTPServerDisconnected:
            logger.warning("SMTP server disconnected. Attempting to reconnect...")
            try:
                await self._reconnect()
                await self.smtp_client.send_message(msg)
                logger.info(
                    f"Email to {msg['To']} sent successfully after reconnection."
                )
            except Exception as reconnection_exception:
                logger.error(
                    f"Failed to send email to {msg['To']} after reconnection: {reconnection_exception}"
                )
                return False
        except Exception as exception:
            logger.error(f"Failed to send email to {msg['To']}: {exception}")
            return False
        return True


async def get_email_sender():
    email_sender = AsyncEmailSender(
        settings.smtp_server,
        settings.smtp_port,
        settings.email_sender,
        settings.email_sender_password,
    )
    await email_sender._connect()
    try:
        yield email_sender
    finally:
        await email_sender.smtp_client.quit()
