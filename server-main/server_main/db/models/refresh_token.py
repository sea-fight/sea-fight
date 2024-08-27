from __future__ import annotations
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String, Boolean, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from server_main.db.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from server_main.db.models.user import User


class RefreshToken(Base):
    """
    Database model for storing refresh tokens.

    :id: Unique identifier for the refresh token.
    :token: The actual refresh token value.
    :user_id: Foreign key referencing the user who owns the token.
    :fingerprint: Additional identifier for the device.
    :expires_at: Time when the token expires.
    :created_at: Time when the token was created.
    :last_used_at: Last time the token was used.
    :is_revoked: Whether the token has been revoked.
    """

    __tablename__ = "refresh_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    token: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    fingerprint: Mapped[str] = mapped_column(String, nullable=True)
    expires_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    last_used_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    is_revoked: Mapped[bool] = mapped_column(default=False)

    user: Mapped[User] = relationship("User", back_populates="refresh_tokens")
