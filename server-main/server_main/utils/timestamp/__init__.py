from datetime import datetime, timezone


def get_utc_datetime() -> datetime:
    """
    Returns the current date and time in the UTC+0 timezone.
    """
    return datetime.now(timezone.utc)


def get_utc_datetime_str() -> str:
    """
    Returns the current date and time in the UTC+0 timezone.
    """
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def convert_str_to_datetime(
    date_str: str, date_format: str = "%Y-%m-%d %H:%M:%S"
) -> datetime:
    """
    Converts a string representation of a date and time to a datetime object with UTC+0 timezone.
    """
    local_dt = datetime.strptime(date_str, date_format)
    utc_dt = local_dt.replace(tzinfo=timezone.utc)
    return utc_dt
