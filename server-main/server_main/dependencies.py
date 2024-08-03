from typing import Callable, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis
import aio_pika
from server_main.enhanced.request import EnhancedRequest
from server_main.web.integrations.redis import RedisDB
from server_main.web.integrations.services.mailer import Mailer


def get_redis_connection(
    db: RedisDB,
) -> Callable[[EnhancedRequest], AsyncGenerator[redis.Redis, None]]:
    async def _get_redis_connection(
        request: EnhancedRequest,
    ) -> AsyncGenerator[redis.Redis, None]:
        connection = await request.app.ctx.redis.get_connection(db)
        try:
            yield connection
        finally:
            await connection.close()

    return _get_redis_connection


def get_rabbitmq_channel(
    request: EnhancedRequest,
) -> aio_pika.abc.AbstractRobustChannel:
    return request.app.ctx.rabbitmq.channel


def get_rabbitmq_connection(
    request: EnhancedRequest,
) -> aio_pika.abc.AbstractRobustConnection:
    return request.app.ctx.rabbitmq.connection


def get_rabbitmq_queue(
    queue: str,
) -> Callable[[EnhancedRequest], aio_pika.abc.AbstractRobustQueue]:
    def _get_rabbimq_queue(
        request: EnhancedRequest,
    ) -> aio_pika.abc.AbstractRobustQueue:
        return request.app.ctx.rabbitmq.queues[queue]

    return _get_rabbimq_queue


def get_rabbitmq_exchange(
    exchange: str,
) -> Callable[[EnhancedRequest], aio_pika.abc.AbstractRobustExchange]:
    def _get_rabbimq_exchange(
        request: EnhancedRequest,
    ) -> aio_pika.abc.AbstractRobustExchange:
        return request.app.ctx.rabbitmq.exchanges[exchange]

    return _get_rabbimq_exchange


def get_mailer(request: EnhancedRequest) -> Mailer:
    return request.app.ctx.mailer


async def get_db_session(
    request: EnhancedRequest,
) -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = request.app.ctx.db_session_factory()

    try:  # noqa: WPS501
        yield session
    finally:
        await session.commit()
        await session.close()
