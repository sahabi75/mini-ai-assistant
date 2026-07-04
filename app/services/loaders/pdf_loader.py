"""PDF text extraction using PyMuPDF."""

from pathlib import Path

import fitz  # PyMuPDF

from app.core.exceptions import ValidationError
from app.core.logging_config import get_logger

logger = get_logger(__name__)


def load_pdf(file_path: Path) -> str:
    """Extract and return all text from a PDF file."""
    try:
        with fitz.open(file_path) as pdf:
            text = "\n\n".join(page.get_text() for page in pdf)
    except Exception as exc:
        logger.warning("Could not read PDF '%s': %s", file_path.name, exc)
        raise ValidationError(
            f"'{file_path.name}' could not be read. It may be corrupted or not a valid PDF."
        ) from exc

    logger.info("Extracted %d characters from PDF '%s'", len(text), file_path.name)
    return text.strip()