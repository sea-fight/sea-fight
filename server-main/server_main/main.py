from contextlib import asynccontextmanager
from fastapi import Request
from fastapi.responses import JSONResponse
from .web.api import router
from .web.integrations.redis import RedisManager
from .web.integrations.rabbitmq import RabbitMQManager
from .web.integrations.services import Mailer
from .db.base import db_session
from .settings import settings
from .enhanced import AppCtx, EnhancedApp, EnhancedHTTPException

# TODO: delete user endpoint for dev purposes


@asynccontextmanager
async def lifespan(app: EnhancedApp):
    rabbitmq = await RabbitMQManager.initialize(settings.rabbitmq_url)
    redis = await RedisManager.initialize(str(settings.redis_url))
    mailer = await Mailer.initialize(rabbitmq, settings.rabbitmq_mailer_queue)
    db_session_factory = db_session
    app._app_ctx = AppCtx(
        rabbitmq=rabbitmq,
        db_session_factory=db_session_factory,
        redis=redis,
        mailer=mailer,
    )
    yield
    # TODO: add close


app = EnhancedApp(lifespan=lifespan)
app.include_router(router)


@app.exception_handler(EnhancedHTTPException)
async def enhanced_exception_handler(request: Request, exc: EnhancedHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"ok": 0, "code": exc.code, "info": exc.info},
    )
