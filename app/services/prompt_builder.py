
from app.core.logging_config import get_logger

logger = get_logger(__name__)

NO_ANSWER_MESSAGE = "I couldn't find that information in the uploaded documents."


def _format_context(chunks: list[dict]) -> str:
    """Format retrieved chunks into a numbered context block with sources."""
    if not chunks:
        return "No relevant context was found."

    parts = []
    for i, chunk in enumerate(chunks, start=1):
        source = chunk.get("metadata", {}).get("source", "unknown")
        parts.append(f"[{i}] (source: {source})\n{chunk['text']}")

    return "\n\n".join(parts)


def _format_history(history: list[dict[str, str]]) -> str:
    """Format conversation history into a simple role: content transcript."""
    if not history:
        return "No previous conversation."

    lines = [f"{turn['role']}: {turn['content']}" for turn in history]
    return "\n".join(lines)


def build_prompt(
    question: str,
    retrieved_chunks: list[dict],
    conversation_history: list[dict[str, str]] | None = None,
) -> str:
    """Build the full prompt for the LLM.

    retrieved_chunks: results from the retrieval service, e.g.
        [{"text": ..., "metadata": {...}, "distance": ...}, ...]
    conversation_history: previous turns, e.g.
        [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    """
    context = _format_context(retrieved_chunks)
    history = _format_history(conversation_history or [])

    prompt = f"""You are an AI assistant that answers questions using only the retrieved context below.

Retrieved Context:
{context}

Conversation History:
{history}

User Question:
{question}

Instructions:
- Answer using ONLY the information in the Retrieved Context and Conversation History above.
- Do not use outside knowledge. Do not make up or guess any information.
- If the answer is not available in the Retrieved Context or Conversation History, respond with exactly:
  "{NO_ANSWER_MESSAGE}"
- Never hallucinate facts, sources, or details that are not present above.
"""

    logger.info("Built prompt for question: '%s' (%d context chunks)", question, len(retrieved_chunks))
    return prompt