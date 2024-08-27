from fastapi.routing import APIRouter
from . import email

router = APIRouter()
router.include_router(email.router, prefix="/email")
