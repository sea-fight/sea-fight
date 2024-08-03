from typing import Any
from fastapi import HTTPException


class EnhancedHTTPException(HTTPException):
    """
    A custom exception class that extends FastAPI's HTTPException to include additional
    context-specific attributes for error handling.

    Attributes:
        code (str): A custom error code associated with the exception.
        info (Any): An additional information about the error. Must be JSON-serializable.

    Usage example:
         ```python
         raise EnhancedHTTPException(status_code=404, code="NOT_FOUND", info={"not_found": ["user_1", "user_2"]})
         ```
    """

    def __init__(self, status_code: int, code: str, info: Any):
        """
        Initialize the EnhancedHTTPException with a status code, custom code, and additional information.

        Args:
            status_code (int): The HTTP status code for the exception.
            code (str): A custom error code.
            info (Any): An additional information about the error. Must be JSON-serializable.
        """
        super().__init__(status_code=status_code, detail=str(info))
        self.code = code
        self.info = info
