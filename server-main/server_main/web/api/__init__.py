from fastapi.routing import APIRouter
from . import sign_up
from . import send_email_code

router = APIRouter()
router.include_router(sign_up.router)
router.include_router(send_email_code.router)
