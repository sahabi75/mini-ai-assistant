
from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.common import ErrorResponse
from app.services.chat_service import handle_chat

router = APIRouter(tags=["chat"])


@router.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        502: {"model": ErrorResponse, "description": "Gemini API failure"},
    },
)
def chat(request: ChatRequest) -> ChatResponse:
    """Send a message in a chat session and get a reply.

    session_id and message are validated by ChatRequest (must be non-blank).
    Other errors (Gemini failures, etc.) are handled by the global
    exception handlers in main.py.
    """
    reply = handle_chat(request.session_id, request.message)
    return ChatResponse(session_id=request.session_id, reply=reply)