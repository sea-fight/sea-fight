"""
This module provides utility functions for working with date and time in the UTC+0 timezone.
It includes functions to get the current date and time in UTC, format it as a string, and
convert date strings to datetime objects in UTC.

Functions:
    get_utc_datetime: Get the current date and time in UTC+0.
    get_utc_datetime_str: Get the current date and time in UTC+0 as a formatted string.
    convert_str_to_datetime: Convert a date string to a datetime object in UTC+0.
"""

from datetime import datetime, timezone


def get_utc_datetime() -> datetime:
    """
    Get the current date and time in the UTC+0 timezone.

    Returns:
        datetime: The current date and time in UTC+0.
    """
    return datetime.now(timezone.utc)


def get_utc_datetime_str() -> str:
    """
    Get the current date and time in the UTC+0 timezone as a formatted string.

    Returns:
        str: The current date and time in UTC+0 formatted as "%Y-%m-%d %H:%M:%S".
    """
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def convert_str_to_datetime(
    date_str: str, date_format: str = "%Y-%m-%d %H:%M:%S"
) -> datetime:
    """
    Convert a string representation of a date and time to a datetime object with UTC+0 timezone.

    Args:
        date_str (str): The date and time string to convert.
        date_format (str, optional): The format of the date and time string. Defaults to "%Y-%m-%d %H:%M:%S".

    Returns:
        datetime: A datetime object representing the specified date and time in UTC+0.
    """
    local_dt = datetime.strptime(date_str, date_format)
    utc_dt = local_dt.replace(tzinfo=timezone.utc)
    return utc_dt
