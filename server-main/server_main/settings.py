from pydantic_settings import BaseSettings
from yarl import URL
from dotenv import load_dotenv
from .utils.environment import required_env

load_dotenv()


class Settings(BaseSettings):
    isdocker: bool = bool(int(required_env("ISDOCKER")))
    secret_key: str = required_env("SECRET_KEY")
    alg: str = "HS256"
    access_token_expire: int = int(required_env("ACCESS_TOKEN_EXPIRE_MINUTES")) * 60
    refresh_token_expire: int = int(required_env("REFRESH_TOKEN_EXPIRE_MINUTES")) * 60
    db_host: str = required_env("DB_HOST")
    db_port: int = int(required_env("DB_PORT"))
    db_remote_ip: str = required_env("DB_REMOTE_IP")
    db_user: str = required_env("POSTGRES_USER")
    db_password: str = required_env("POSTGRES_PASSWORD")
    db_base: str = required_env("POSTGRES_DB")
    db_echo: bool = True

    redis_host: str = required_env("REDIS_HOST")
    redis_port: int = int(required_env("REDIS_PORT"))
    redis_password: str = required_env("REDIS_PASSWORD")

    rabbitmq_url: str = required_env("RABBITMQ_URL")
    rabbitmq_mailer_queue: str = required_env("RABBITMQ_MAILER_QUEUE")

    username_max_length: int = 32
    username_min_length: int = 4
    nickname_max_length: int = 32
    nickname_min_length: int = 4
    email_max_length: int = 256
    password_min_length: int = 4

    email_code_length: int = 8
    email_code_expiretime: int = 3600  # in seconds
    email_code_request_attempts_limit: int = 3

    @property
    def db_url(self) -> URL:
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_password,
            path=f"/{self.db_base}",
        )

    @property
    def redis_url(self) -> URL:
        return URL.build(
            scheme="redis",
            host=self.redis_host,
            port=self.redis_port,
            password=self.redis_password,
        )


settings = Settings()
