

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed application settings sourced from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Application ---
    app_name: str = "mini-ai-assistant"
    app_env: str = "development"
    log_level: str = "INFO"

    # --- API ---
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # --- Google Gemini ---
    google_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    # --- Embeddings ---
    embedding_model: str = "BAAI/bge-small-en-v1.5"

    # --- ChromaDB ---
    chroma_persist_dir: str = "./data/chroma_db"
    chroma_collection_name: str = "knowledge_base"

    # --- Knowledge Ingestion ---
    raw_data_dir: str = "./data/raw"
    processed_data_dir: str = "./data/processed"
    chunk_size: int = 1000
    chunk_overlap: int = 150

    # --- Document Upload ---
    upload_dir: str = "./uploads"
    max_upload_size_mb: int = 20

    # --- Tools ---
    orders_data_path: str = "./data/orders.json"
    products_data_path: str = "./data/products.json"

    # --- Session Memory ---
    session_memory_backend: str = "in_memory"
    session_ttl_seconds: int = 3600


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance (loaded once per process)."""
    return Settings()