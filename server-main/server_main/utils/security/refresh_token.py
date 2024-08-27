from datetime import datetime, timezone, timedelta
from server_main.settings import settings


def std_exp(dt_now: datetime) -> datetime:
    return dt_now + timedelta(seconds=settings.refresh_token_expire)
