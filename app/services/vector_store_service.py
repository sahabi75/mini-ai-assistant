"""Stores and searches document embeddings using a persistent ChromaDB collection."""

import chromadb

from app.core.config import get_settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)

_collection = None


def _get_collection():
    """Create (or reuse) the persistent ChromaDB collection."""
    global _collection
    if _collection is None:
        settings = get_settings()
        logger.info("Initializing ChromaDB at '%s'", settings.chroma_persist_dir)
        client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        _collection = client.get_or_create_collection(name=settings.chroma_collection_name)
    return _collection


def add_documents(
    ids: list[str],
    texts: list[str],
    embeddings: list[list[float]],
    metadatas: list[dict],
) -> None:
    """Add documents (with their embeddings and metadata) to the vector store."""
    if not ids:
        logger.warning("No documents to add.")
        return

    collection = _get_collection()
    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    logger.info("Added %d documents to the vector store", len(ids))


def similarity_search(query_embedding: list[float], top_k: int = 5) -> list[dict]:
    """Find the top_k most similar documents to the given query embedding.

    Returns a list of dicts with id, text, metadata, and distance.
    """
    collection = _get_collection()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    matches = []
    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i in range(len(ids)):
        matches.append({
            "id": ids[i],
            "text": documents[i],
            "metadata": metadatas[i],
            "distance": distances[i],
        })

    logger.info("Similarity search returned %d results", len(matches))
    return matches