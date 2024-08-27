# TODO:
async def sign_up_user_handler(): ...


# from result import Ok, Err, Result
# import redis.asyncio as redis
# from loguru import logger
# from server_main.enhanced import EnhancedHTTPException
# from server_main.web.schemas.sign_up import SignUpRequestSchema
# from server_main.db.repositories.user import UserRepository
# from server_main.db.models.user import User
#
#
# # TODO: add check_email endpoint with redis caching...
# async def sign_up_handler(
#     redis_mailer: redis.Redis, user_repo: UserRepository, data: SignUpRequestSchema
# ) -> Result[tuple[str, str, str], EnhancedHTTPException]:
#     """
#     Returns:
#         Result:
#             Ok(tuple(user id (UUID in str), refresh token, access token))
#             Err(EnhancedHTTPException)
#     """
#     access_token = "TODO:"
#     refresh_token = "TODO:"
#
#     code: bytes | None = await redis_mailer.hget(str(data.email), "code")  # type: ignore
#     # TODO: refactoring
#     # returning an HTTP exception looks not right tbh
#     # but now it's good enough
#
#     user_with_same_email: User | None = await user_repo.get_by_email(data.email)
#     if user_with_same_email is not None:
#         return Err(EnhancedHTTPException(409, "EMAIL_NOT_UNIQUE", {}))
#
#     if code is None:
#         return Err(EnhancedHTTPException(410, "CODE_GONE", {}))
#     if code.decode() != data.code:
#         return Err(EnhancedHTTPException(400, "CODE_INCORRECT", {}))
#
#     user = await user_repo.create(
#         username=data.username,
#         refresh_token=refresh_token,
#         email=str(data.email),
#     )
#     # TODO: add redis for cache
#     return Ok((str(user.id), refresh_token, access_token))
