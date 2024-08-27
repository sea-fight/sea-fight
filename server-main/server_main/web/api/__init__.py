from fastapi.routing import APIRouter
from . import auth
from . import verify

router = APIRouter()
router.include_router(auth.router, prefix="/auth")
router.include_router(verify.router, prefix="/verify")
