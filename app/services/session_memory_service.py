"""Stores and retrieves conversation history per session_id.

Uses a simple in-memory dictionary. Each session_id maps to a list of
messages, where each message is {"role": "user"/"assistant", "content": str}.
"""

from app.core.logging_config import get_logger

logger = get_logger(__name__)

# session_id -> list of messages
_sessions: dict[str, list[dict[str, str]]] = {}


def save_message(session_id: str, role: str, content: str) -> None:
    """Append a message to a session's conversation history."""
    if session_id not in _sessions:
        _sessions[session_id] = []

    _sessions[session_id].append({"role": role, "content": content})
    logger.info("Saved '%s' message to session '%s'", role, session_id)


def load_memory(session_id: str) -> list[dict[str, str]]:
    """Return the conversation history for a session (empty list if none)."""
    history = _sessions.get(session_id, [])
    logger.info("Loaded %d messages for session '%s'", len(history), session_id)
    return history


def clear_memory(session_id: str) -> None:
    """Remove all stored conversation history for a session."""
    if session_id in _sessions:
        del _sessions[session_id]
        logger.info("Cleared memory for session '%s'", session_id)
    else:
        logger.info("No memory to clear for session '%s'", session_id)