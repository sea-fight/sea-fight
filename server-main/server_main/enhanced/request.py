from fastapi import Request
from .app import EnhancedApp


class EnhancedRequest(Request):
    @property
    def app(self) -> EnhancedApp:
        return super().app
