from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from server_main.db.repositories.user import UserRepository
from server_main.db.dependencies import get_db_session
from server_main.web.schemas.sign_up import (
    SignUpRequestSchema,
    SignUpResponseSchema,
)
from server_main.handlers.sign_up import sign_up_handler
from .router import router


@router.post("/sign_up", response_model=SignUpResponseSchema)
async def sign_up(
    request_data: SignUpRequestSchema, db: AsyncSession = Depends(get_db_session)
) -> SignUpResponseSchema:
    id, refresh, access = await sign_up_handler(UserRepository(db), request_data)
    return SignUpResponseSchema(ok=1, id=id, refresh_token=refresh)
