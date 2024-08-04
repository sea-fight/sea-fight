import uuid
from sqlalchemy import Boolean, Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from server_main.db.base import Base
from server_main.settings import settings


class User(Base):
    """
    database User class.

    :id: UUIDv4.
    :username: A name that is visible on the screen for example during a conversation.
    :nickname: A unique name that can be mentioned like in "Discord" FE: @boolmano.
    :access_token: The value that is used to identify the session.
    :refresh_token: The value that is used for making access_token
    :email: User email.
    :hashed_password: User password hashed in sha256.
    :created_at: User registration date UTC+0.
    :verified: User email verification.
    """

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String(settings.username_max_length))
    nickname = Column(String(settings.nickname_max_length), unique=True)
    access_token = Column(String)
    refresh_token = Column(String)
    email = Column(String(settings.email_max_length))
    hashed_password = Column(String(256))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    verified = Column(Boolean)
