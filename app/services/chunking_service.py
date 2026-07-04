"""Text chunking service using LangChain's RecursiveCharacterTextSplitter."""

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import get_settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)


def chunk_text(
    text: str,
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> list[str]:
    """Split text into overlapping chunks.

    chunk_size and chunk_overlap default to the values set in the
    environment (CHUNK_SIZE / CHUNK_OVERLAP) if not provided.
    """
    settings = get_settings()
    chunk_size = chunk_size or settings.chunk_size
    chunk_overlap = chunk_overlap if chunk_overlap is not None else settings.chunk_overlap

    if not text.strip():
        logger.warning("Received empty text; no chunks created.")
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = splitter.split_text(text)

    logger.info(
        "Split text into %d chunks (chunk_size=%d, chunk_overlap=%d)",
        len(chunks), chunk_size, chunk_overlap,
    )
    return chunks