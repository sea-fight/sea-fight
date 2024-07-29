from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .web.api import router
from .web.schemas.error_response import EnhancedHTTPException, ErrorResponseSchema
from .db.base import db_session


app = FastAPI()
# app.state.redis = redis.RedisClientFactory(settings.redis_url)
app.state.db_session_factory = db_session
app.include_router(router)


@app.exception_handler(EnhancedHTTPException)
async def enhanced_exception_handler(request: Request, exc: EnhancedHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponseSchema(ok=0, code=exc.code, info=exc.info),
    )
