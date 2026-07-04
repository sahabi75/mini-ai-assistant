"""Plain text (.txt) file loader."""

from pathlib import Path

from app.core.logging_config import get_logger

logger = get_logger(__name__)


def load_txt(file_path: Path) -> str:
    """Read and return the contents of a .txt file."""
    text = file_path.read_text(encoding="utf-8")
    logger.info("Extracted %d characters from TXT '%s'", len(text), file_path.name)
    return text.strip()