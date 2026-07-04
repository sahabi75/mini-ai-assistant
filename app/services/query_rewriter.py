from app.core.logging_config import get_logger
from app.services.gemini_service import generate_answer

logger = get_logger(__name__)


def rewrite_query(message: str, history: list[dict[str, str]]) -> str:
    """Rewrite a message into a standalone query using conversation history.

    Returns the message unchanged if there's no history yet, or if the
    rewrite call fails for any reason (fail safe, not fail loud).
    """
    if not history:
        return message

    history_text = "\n".join(f"{turn['role']}: {turn['content']}" for turn in history)

    rewrite_prompt = f"""Rewrite the latest user message into a standalone message that makes sense without the conversation history. Resolve pronouns (he, she, it, my, I) and follow-up references (that, those, cheaper, similar) using the history below. If the message is already standalone, return it unchanged. Return ONLY the rewritten message, nothing else.

Conversation History:
{history_text}

Latest Message:
{message}

Rewritten Message:"""

    try:
        rewritten = generate_answer(rewrite_prompt).strip()
    except Exception:
        logger.warning("Query rewrite failed; using original message.")
        return message

    logger.info("Rewrote query: '%s' -> '%s'", message, rewritten)
    return rewritten