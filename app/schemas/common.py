
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard error response shape returned by the global exception handlers."""

    detail: str