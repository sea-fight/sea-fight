"""
This package provides an enhanced FastAPI application with additional context for
    - RabbitMQ
    - Redis
    - Mailer Service
    - database session management
The context is accessible via a property of the app for easy integration throughout the application.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from server_main.web.integrations.redis import RedisManager
from server_main.web.integrations.rabbitmq import RabbitMQManager
from server_main.web.integrations.services import Mailer


class AppCtx(BaseModel):
    """
    Represents the application context holding various integrations.

    Attributes:
        rabbitmq (web.integrations.rabbitmq.RabbitMQManager): Manager for RabbitMQ connections and operations.
        redis (web.integrations.redis.RedisManager): Manager for Redis connections and operations.
        mailer (web.integrations.service.mailer.Mailer): Service for handling mail operations.
        db_session_factory (async_sessionmaker[AsyncSession]): Factory for creating asynchronous database sessions.
    """

    rabbitmq: RabbitMQManager
    redis: RedisManager
    mailer: Mailer
    db_session_factory: async_sessionmaker[AsyncSession]

    class Config:
        arbitrary_types_allowed = True


class EnhancedApp(FastAPI):
    """
    An enhanced FastAPI application with an application context for various integrations.

    Properties:
        ctx (AppCtx): Property to access the application context. Raises a `ValueError` if accessed before initialization.
    """

    _app_ctx: AppCtx | None

    @property
    def ctx(self) -> AppCtx:
        """
        Property to access the application context.

        Returns:
            AppCtx: The application context.

        Raises:
            ValueError: If the context is accessed before the application is initialized.
        """
        if self._app_ctx is None:
            raise ValueError("Attempt to get AppCtx before application initialization")
        return self._app_ctx
