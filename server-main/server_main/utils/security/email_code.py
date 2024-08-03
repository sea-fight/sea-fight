import secrets
import string
from server_main.settings import settings


def generate_email_verification_code() -> str:
    length = settings.email_code_length
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length)).upper()
