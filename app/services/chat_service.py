
from app.core.logging_config import get_logger
from app.services.gemini_service import generate_answer
from app.services.prompt_builder import build_prompt
from app.services.query_rewriter import rewrite_query
from app.services.retrieval_service import retrieve_relevant_chunks
from app.services.session_memory_service import load_memory, save_message
from app.services.tool_router import route

logger = get_logger(__name__)


def handle_chat(session_id: str, message: str) -> str:
    """Process one chat turn and return the assistant's reply.

    Resolves pronouns/follow-ups against history, then tries a tool
    (order status, product search). If no tool matches, falls through to
    retrieval -> prompt -> Gemini.
    """
    history = load_memory(session_id)

    resolved_message = rewrite_query(message, history)

    tool_result = route(resolved_message)

    if tool_result is not None:
        reply = tool_result
    else:
        retrieved_chunks = retrieve_relevant_chunks(resolved_message)
        prompt = build_prompt(
            question=resolved_message,
            retrieved_chunks=retrieved_chunks,
            conversation_history=history,
        )
        reply = generate_answer(prompt)

    # Save the original message (not the rewritten one) so history stays natural.
    save_message(session_id, "user", message)
    save_message(session_id, "assistant", reply)

    logger.info("Handled chat turn for session '%s'", session_id)
    return reply