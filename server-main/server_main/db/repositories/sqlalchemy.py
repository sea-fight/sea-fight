from typing import Generic, Sequence, Type, TypeVar, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from server_main.db.base import Base
import uuid

T = TypeVar("T", bound=Base)


class AsyncSQLAlchemyRepository(Generic[T]):
    def __init__(self, db: AsyncSession, model: Type[T]):
        self.db = db
        self.model = model

    async def create(self, **kwargs) -> T:
        obj = self.model(**kwargs)
        try:
            self.db.add(obj)
            await self.db.commit()
            await self.db.refresh(obj)
        except IntegrityError:
            await self.db.rollback()
            raise
        return obj

    async def get_by_id(self, id: uuid.UUID) -> Optional[T]:
        if hasattr(self.model, "id"):
            result = await self.db.execute(
                select(self.model).filter(self.model.id == id)  # type: ignore
            )
            return result.scalars().first()
        else:
            raise

    async def update(self, id: uuid.UUID, **kwargs) -> Optional[T]:
        obj = await self.get_by_id(id)
        if not obj:
            return None
        for key, value in kwargs.items():
            setattr(obj, key, value)
        try:
            await self.db.commit()
            await self.db.refresh(obj)
        except IntegrityError:
            await self.db.rollback()
            raise
        return obj

    async def delete(self, id: uuid.UUID) -> bool:
        obj = await self.get_by_id(id)
        if not obj:
            return False
        await self.db.delete(obj)
        await self.db.commit()
        return True

    async def list_all(self) -> Sequence[T]:
        result = await self.db.execute(select(self.model))
        return result.scalars().fetchall()
