from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .sqlalchemy import AsyncSQLAlchemyRepository
from server_main.db.models.user import User


class UserRepository(AsyncSQLAlchemyRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).filter(User.email == email))
        return result.scalars().first()
