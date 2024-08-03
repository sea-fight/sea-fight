"""
This module provides an enhanced request class that extends FastAPI's Request class
to integrate with the EnhancedApp, allowing easy access to the application context.
"""

from fastapi import Request
from .app import EnhancedApp


class EnhancedRequest(Request):
    """
    An enhanced request class that extends FastAPI's Request class to integrate with the EnhancedApp.

    Properties:
        app (EnhancedApp): Property to access the EnhancedApp instance associated with the request.
    """

    @property
    def app(self) -> EnhancedApp:
        """
        Property to access the EnhancedApp instance associated with the request.

        Returns:
            EnhancedApp: The EnhancedApp instance.

        Overrides:
            The base class's app property to return an instance of EnhancedApp.
        """
        return super().app
