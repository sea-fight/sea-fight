"""
This package provides utilities for retrieving environment variables safely. It includes
functions to fetch single or multiple environment variables, raising an error if any
requested variables are not found.

Functions:
    required_env: Retrieve a single environment variable safely.
    required_env_many: Retrieve multiple environment variables safely.
"""

from .required import required_env, required_env_many

__all__ = ["required_env", "required_env_many"]
