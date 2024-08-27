from fastapi.routing import APIRouter
from . import sign_up

router = APIRouter()
router.include_router(sign_up.router, prefix="/sign-up")
