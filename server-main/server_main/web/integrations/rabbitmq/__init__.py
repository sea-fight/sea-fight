import json
import asyncio
import aio_pika
import aio_pika.abc
from server_main.settings import settings


async def _get_robust_connection() -> aio_pika.abc.AbstractRobustConnection:
    connection: aio_pika.abc.AbstractRobustConnection = await aio_pika.connect_robust(
        settings.rabbitmq_url, loop=asyncio.get_event_loop()
    )
    return connection


async def get_rabbitmq_connection():
    connection = await _get_robust_connection()
    try:
        yield connection
    finally:
        await connection.close()


async def send_mail(
    rabbitmq_connection: aio_pika.abc.AbstractRobustConnection,
    receiver: str,
    template: str,
    args: dict[str, str],
):
    """
    Use `server-mailer` for sending mails.

    From origin Golang code:
        Receiver string            `json:"receiver"`
        Template string            `json:"template"`
        Args     map[string]string `json:"args"`

    """
    channel = rabbitmq_connection.channel()
    data = {"receiver": receiver, "template": template, "args": args}
    await channel.default_exchange.publish(
        aio_pika.Message(body=json.dumps(data).encode()),
        routing_key=settings.rabbitmq_mailer_queue,
    )
