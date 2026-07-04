"""Generates text embeddings using Sentence Transformers."""

from sentence_transformers import SentenceTransformer

from app.core.config import get_settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)

_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    """Load the embedding model once and reuse it on later calls."""
    global _model
    if _model is None:
        settings = get_settings()
        logger.info("Loading embedding model: %s", settings.embedding_model)
        _model = SentenceTransformer(settings.embedding_model)
    return _model


def embed_text(text: str) -> list[float]:
    """Generate an embedding vector for a single piece of text."""
    model = _get_model()
    vector = model.encode(text, normalize_embeddings=True)
    return vector.tolist()


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Generate embedding vectors for a list of texts."""
    if not texts:
        return []

    model = _get_model()
    vectors = model.encode(texts, normalize_embeddings=True)

    logger.info("Generated embeddings for %d texts", len(texts))
    return vectors.tolist()