"""Custom application exceptions.

Each of these maps to a specific HTTP status code via the exception
handlers registered in app/main.py, so service code can raise a
meaningful exception without needing to know about HTTP at all.
"""


class AppError(Exception):
    """Base class for all custom application exceptions."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class ValidationError(AppError):
    """Raised when user input is invalid. Maps to HTTP 400."""


class NotFoundError(AppError):
    """Raised when a requested resource does not exist. Maps to HTTP 404."""


class ExternalServiceError(AppError):
    """Raised when an external service (e.g. Gemini) fails. Maps to HTTP 502."""