from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

from server_main.settings import settings
from .meta import metadata


class Base(AsyncAttrs, DeclarativeBase):
    """Base for all models."""

    metadata = metadata


engine = create_async_engine(
    str(settings.db_url),
    echo=settings.db_echo,
)


db_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
