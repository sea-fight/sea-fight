from server_main.web.schemas.sign_up import SignUpRequestSchema
from server_main.db.repositories.user import UserRepository
from server_main.utils.security.password_hash import hash_password


async def sign_up_handler(
    user_repo: UserRepository, data: SignUpRequestSchema
) -> tuple[str, str, str]:
    """
    Returns:
        user id (UUID), refresh token, access token
    """
    # code: str = generate_email_verification_code()
    # redis: RedisClientFactory = app.state.redis

    access_token = "TODO:"
    refresh_token = "TODO:"

    user = await user_repo.create(
        username=data.username,
        nickname=data.nickname,
        access_token=access_token,
        refresh_token=refresh_token,
        email=data.email.__str__(),
        hashed_password=hash_password(data.password),
        verified=False,
    )
    return (user.id.__str__(), refresh_token, access_token)
    # email_sender: AsyncEmailSender = app.state.email_sender
    # redis_connection = await redis.get_connection(DB_EMAIL_CODE_VERIFY)
    # redis_connection.set(name=f"{user.id}", value={""}, ex=settings.email_code_expiretime)
    # render_email_verify_code(data.nickname, code: int)
