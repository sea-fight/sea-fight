import uuid
from typing import Optional, Dict, Any, List
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from .sqlalchemy import AsyncSQLAlchemyRepository
from server_main.db.models.user import User


class UserRepository(AsyncSQLAlchemyRepository[User]):
    def __init__(self, db: AsyncSession):
        self.db = db
        self.model = User
