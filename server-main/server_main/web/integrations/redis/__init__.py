from __future__ import annotations
from typing import AsyncGenerator
from enum import Enum
import redis.asyncio as redis
from loguru import logger
from server_main.settings import settings


class RedisDB(Enum):
    EMAIL_CODE_VERIFY = 0
    CACHED = 1


class RedisManager:
    def __init__(self, redis_url: str):
        self._redis_url = redis_url
        self._pools: dict[RedisDB, redis.ConnectionPool] = {}

    @staticmethod
    async def initialize(redis_url: str) -> RedisManager:
        manager = RedisManager(redis_url)
        logger.info("Connecting to Redis...")

        for db in RedisDB:
            logger.info(f"Connecting to Redis [/{db.value} {db.name}]...")
            manager._pools[db] = redis.ConnectionPool.from_url(
                f"{redis_url}/{db.value}"
            )

        logger.info("Connected to Redis")
        return manager

    async def get_connection(self, db: RedisDB) -> redis.Redis:
        pool = self._pools.get(db)
        if pool is None:
            raise ValueError(f"No connection pool found for database {db}")
        return redis.Redis(connection_pool=pool)

    async def close(self):
        logger.info("Closing all Redis connection pools...")
        for pool in self._pools.values():
            logger.info(f"Closing {pool}")
            await pool.disconnect()
        logger.info("All Redis connection pools are successfully closed")


#
# # TODO: split into files
# class RedisClientFactory:
#     def __init__(self, base_url: URL):
#         self.base_url = base_url
#
#     async def get_connection(self, db: int):
#         return redis.from_url(
#             (self.base_url / str(db)).__str__(), decode_responses=True
#         )
#
#     async def get_connection_by_url(self, url: URL):
#         return redis.from_url(url)
#
#
# redis_factory = RedisClientFactory(settings.redis_url)
#
#
# def get_redis_connection(
#     db: RedisDB,
# ) -> Callable[[], AsyncGenerator[redis.Redis, None]]:
#     async def get_redis_connection() -> AsyncGenerator[redis.Redis, None]:
#         connection = await redis_factory.get_connection(db.value)
#         try:
#             yield connection
#         finally:
#             await connection.close()
#
#     return get_redis_connection
