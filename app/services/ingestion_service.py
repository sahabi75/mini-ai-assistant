"""Ingestion pipeline: loads a document, chunks it, embeds it, and stores it."""

from pathlib import Path

from app.core.logging_config import get_logger
from app.services.chunking_service import chunk_text
from app.services.embedding_service import embed_texts
from app.services.loaders.loader import load_document
from app.services.vector_store_service import add_documents

logger = get_logger(__name__)


def index_document(file_path: Path, source_name: str) -> int:
    """Load, chunk, embed, and store a document in the vector store.

    Returns the number of chunks that were indexed.
    """
    text = load_document(file_path)

    if not text.strip():
        logger.warning("No text extracted from '%s'; nothing to index.", source_name)
        return 0

    chunks = chunk_text(text)

    if not chunks:
        logger.warning("No chunks created for '%s'; nothing to index.", source_name)
        return 0

    embeddings = embed_texts(chunks)

    ids = [f"{source_name}_chunk{i}" for i in range(len(chunks))]
    metadatas = [{"source": source_name, "chunk_index": i} for i in range(len(chunks))]

    add_documents(ids=ids, texts=chunks, embeddings=embeddings, metadatas=metadatas)

    logger.info("Indexed %d chunks from '%s'", len(chunks), source_name)
    return len(chunks)