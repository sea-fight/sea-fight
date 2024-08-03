from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from server_main.web.integrations.redis import RedisManager
from server_main.web.integrations.rabbitmq import RabbitMQManager
from server_main.web.integrations.services import Mailer


class AppCtx(BaseModel):
    rabbitmq: RabbitMQManager
    redis: RedisManager
    mailer: Mailer
    db_session_factory: async_sessionmaker[AsyncSession]

    class Config:
        arbitrary_types_allowed = True


class EnhancedApp(FastAPI):
    _app_ctx: AppCtx | None

    @property
    def ctx(self) -> AppCtx:
        if self._app_ctx is None:
            raise ValueError("Attempt to get AppCtx before application initialization")
        return self._app_ctx
