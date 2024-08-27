import uuid
from datetime import datetime
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from server_main.db.base import Base
from server_main.settings import settings

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from server_main.db.models.refresh_token import RefreshToken


class User(Base):
    """
    Database model for storing users.

    :id: UUID.
    :username: A name that is visible on the screen, for example, during a conversation.
    :email: User email.
    :created_at: User registration date UTC+0.
    :last_active_at: User last action date UTC+0.

    :refresh_tokens: List of refresh tokens associated with the user.
    """

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String(settings.username_max_length))
    email: Mapped[str] = mapped_column(
        String(settings.email_max_length), unique=True, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    last_active_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken", back_populates="user", cascade="all, delete-orphan"
    )
