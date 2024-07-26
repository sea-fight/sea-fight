from fastapi import FastAPI
from .web.api import router
from .web.integrations import smtp, redis
from .db.base import db_session
from .settings import settings

app = FastAPI()
# app.state.redis = redis.RedisClientFactory(settings.redis_url)
app.state.db_session_factory = db_session
app.include_router(router)
