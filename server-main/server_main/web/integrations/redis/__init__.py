from collections.abc import Callable
from typing import AsyncGenerator
from enum import Enum
import redis.asyncio as redis
from yarl import URL
from server_main.settings import settings


class RedisDB(Enum):
    EMAIL_CODE_VERIFY = 0


# TODO: split into files
class RedisClientFactory:
    def __init__(self, base_url: URL):
        self.base_url = base_url

    async def get_connection(self, db: int):
        return redis.from_url(
            (self.base_url / str(db)).__str__(), decode_responses=True
        )

    async def get_connection_by_url(self, url: URL):
        return redis.from_url(url)


redis_factory = RedisClientFactory(settings.redis_url)


def get_redis_connection(
    db: RedisDB,
) -> Callable[[], AsyncGenerator[redis.Redis, None]]:
    async def get_redis_connection() -> AsyncGenerator[redis.Redis, None]:
        connection = await redis_factory.get_connection(db.value)
        try:
            yield connection
        finally:
            await connection.close()

    return get_redis_connection
