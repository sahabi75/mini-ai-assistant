
from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1, description="Unique ID for the conversation session.")
    message: str = Field(..., min_length=1, description="The user's message.")

    @field_validator("session_id", "message")
    @classmethod
    def not_blank(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("must not be blank")
        return stripped


class ChatResponse(BaseModel):
    session_id: str
    reply: str