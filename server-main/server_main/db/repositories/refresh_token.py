import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .sqlalchemy import AsyncSQLAlchemyRepository
from server_main.db.models.refresh_token import RefreshToken


class RefreshTokenRepository(AsyncSQLAlchemyRepository[RefreshToken]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, RefreshToken)

    async def get_by_token(self, token: str) -> RefreshToken | None:
        result = await self.db.execute(
            select(RefreshToken).filter(RefreshToken.token == token)
        )
        return result.scalars().first()

    async def get_by_token_fingerprint(
        self, token: str, fingerprint: str
    ) -> RefreshToken | None:
        result = await self.db.execute(
            select(RefreshToken).filter(
                RefreshToken.token == token, RefreshToken.fingerprint == fingerprint
            )
        )
        return result.scalars().first()

    async def revoke_token(self, refresh_token: RefreshToken) -> bool:
        refresh_token.is_revoked = True
        await self.db.commit()
        return True

    async def revoke_all_tokens_for_user(self, user_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(RefreshToken).filter(RefreshToken.user_id == user_id)
        )
        tokens = result.scalars().all()
        for token in tokens:
            token.is_revoked = True
        await self.db.commit()
        return len(tokens)
