from __future__ import annotations
from typing import Any
import json
import asyncio
import aio_pika
from loguru import logger


class RabbitMQManager:
    connection: aio_pika.abc.AbstractRobustConnection
    channel: aio_pika.abc.AbstractRobustChannel
    queues: dict[str, aio_pika.abc.AbstractRobustQueue]
    exchanges: dict[str, aio_pika.abc.AbstractRobustExchange]

    def __init__(
        self,
        connection: aio_pika.abc.AbstractRobustConnection,
        channel: aio_pika.abc.AbstractRobustChannel,
    ):
        self.connection = connection
        self.channel = channel
        self.queues = {}
        self.exchanges = {}

    @staticmethod
    async def initialize(rabbitmq_url: str) -> RabbitMQManager:
        logger.info("Connecting to RabbitMQ...")
        connection: aio_pika.abc.AbstractRobustConnection = (
            await aio_pika.connect_robust(rabbitmq_url, loop=asyncio.get_event_loop())
        )
        channel: aio_pika.abc.AbstractRobustChannel = await connection.channel()  # type: ignore
        logger.info("Connected to RabbitMQ")
        return RabbitMQManager(connection, channel)

    async def declare_queue(self, queue_name: str) -> aio_pika.abc.AbstractRobustQueue:
        logger.info(f"Declaring RabbitMQ queue: {queue_name}")
        queue: aio_pika.abc.AbstractRobustQueue = await self.channel.declare_queue(
            queue_name
        )
        self.queues[queue_name] = queue
        return queue

    async def declare_exchange(
        self,
        exchange_name: str,
    ) -> aio_pika.abc.AbstractRobustExchange:
        logger.info(f"Declaring RabbitMQ exchange: {exchange_name}")
        exchange = await self.channel.declare_exchange(
            exchange_name, aio_pika.ExchangeType.DIRECT
        )
        self.exchanges[exchange_name] = exchange
        return exchange

    async def bind_queue(
        self,
        queue: aio_pika.abc.AbstractQueue,
        exchange: aio_pika.abc.AbstractRobustExchange,
        routing_key: str,
    ):
        await queue.bind(exchange, routing_key=routing_key)
        logger.info(
            f"Bound queue {queue.name} to exchange {exchange.name} with routing key {routing_key}"
        )

    async def publish_message(
        self,
        exchange: aio_pika.abc.AbstractRobustExchange,
        routing_key: str,
        data: dict[str, Any],
    ):
        message = aio_pika.Message(body=json.dumps(data).encode())
        await exchange.publish(message, routing_key=routing_key)
        logger.info(
            f"Published message to exchange {exchange.name} with routing key {routing_key}"
        )


# async def send_mail(
#     # rabbitmq_connection: aio_pika.abc.AbstractRobustConnection,
#     rabbitmq_channel: aio_pika.abc.AbstractRobustChannel,
#     receiver: str,
#     template: str,
#     args: dict[str, str],
# ):
#     """
#     Use `server-mailer` for sending mails.
#
#     From origin Golang code:
#         Receiver string            `json:"receiver"`
#         Template string            `json:"template"`
#         Args     map[string]string `json:"args"`
#
#     """
#
#     queue = await declare_queue(rabbitmq_channel, settings.rabbitmq_mailer_queue)
#     exchange = await declare_exchange_and_bind_queue(
#         rabbitmq_channel, "mailer_exchange", queue
#     )
#
#     data = {"receiver": receiver, "template": template, "args": args}
#     await exchange.publish(
#         aio_pika.Message(body=json.dumps(data).encode()),
#         routing_key=settings.rabbitmq_mailer_queue,
#     )
#
# logger.info("Getting rabbitmq channel...")
# channel = rabbitmq_connection.channel()
#
# logger.info("Declare rabbitmq queue...")
# queue = await channel.declare_queue(settings.rabbitmq_mailer_queue)
# logger.info("Declare rabbitmq exchange for channel...")
# exchange = await channel.declare_exchange("")
#
# logger.info(f"Publishing message to rabbitmq {settings.rabbitmq_mailer_queue}")
# await exchange.publish(
#     aio_pika.Message(body=json.dumps(data).encode()),
#     routing_key=settings.rabbitmq_mailer_queue,
# )
