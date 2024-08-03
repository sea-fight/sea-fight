import json
from aio_pika import Message
from aio_pika.abc import AbstractRobustExchange, AbstractRobustQueue
from loguru import logger
from server_main.web.integrations.rabbitmq import RabbitMQManager


class Mailer:
    queue: AbstractRobustQueue
    exchange: AbstractRobustExchange

    def __init__(
        self,
        queue: AbstractRobustQueue,
        exchange: AbstractRobustExchange,
        mailer_queue_name: str,
    ):
        self.queue = queue
        self.exchange = exchange
        self.mailer_queue_name = mailer_queue_name

    @staticmethod
    async def initialize(rabbitmq: RabbitMQManager, mailer_queue_name: str):
        logger.info("Initializing Mailer...")
        queue = await rabbitmq.declare_queue(mailer_queue_name)
        logger.info("Mailer queue successfully declared")
        exchange = await rabbitmq.declare_exchange("mailer_exchange")
        logger.info("Mailer exchange successfully declared")
        await queue.bind(exchange, mailer_queue_name)
        logger.info("Mailer queue successfully binded to exchange")
        logger.info("Mailer initialization successfully finished")
        return Mailer(queue, exchange, mailer_queue_name)

    async def immediatemail(self, receiver: str, template: str, args: dict[str, str]):
        # from Golang code:
        # type Message struct {
        # 	Receiver string            `json:"receiver"`
        # 	Template string            `json:"template"`
        # 	Args     map[string]string `json:"args"`
        # }
        message = Message(
            body=json.dumps(
                {
                    "kind": "immediatemail",
                    "receiver": receiver,
                    "template": template,
                    "args": args,
                }
            ).encode()
        )
        await self.exchange.publish(message, self.mailer_queue_name)
        # logs on mailer service side
