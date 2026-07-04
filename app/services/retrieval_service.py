from app.core.exceptions import ValidationError
from app.core.logging_config import get_logger
from app.services.embedding_service import embed_text
from app.services.vector_store_service import similarity_search

logger = get_logger(__name__)


def retrieve_relevant_chunks(question: str, top_k: int = 5) -> list[dict]:
    """Find the top_k chunks most relevant to a question.

    Each result includes the chunk text, its metadata, and its distance
    (lower distance = more relevant).
    """
    if not question.strip():
        raise ValidationError("Question cannot be empty.")

    query_embedding = embed_text(question)
    results = similarity_search(query_embedding, top_k=top_k)

    logger.info("Retrieved %d chunks for question: '%s'", len(results), question)
    return results