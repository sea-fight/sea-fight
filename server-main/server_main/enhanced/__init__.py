"""
This package provides an enhanced FastAPI application setup with additional context for integration with services like redis, rabbitmq, db, mailer and so on. It includes custom request handling
to access the application context easily throughout the application.

Classes:
    AppCtx (BaseModel): Represents the application context holding various integrations.
    EnhancedApp (FastAPI): An enhanced FastAPI application with an application context.
    EnhancedRequest (Request): An enhanced request class with a custom application property.
    EnhancedHTTPException (HTTPException): An enhanced exception class that include additional attributes for error handling.
"""

from .app import EnhancedApp, AppCtx
from .request import EnhancedRequest
from .exception import EnhancedHTTPException

__all__ = ["EnhancedApp", "AppCtx", "EnhancedRequest", "EnhancedHTTPException"]
