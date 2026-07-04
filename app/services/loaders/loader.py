from pathlib import Path

from app.core.exceptions import ValidationError
from app.services.loaders.markdown_loader import load_markdown
from app.services.loaders.pdf_loader import load_pdf
from app.services.loaders.txt_loader import load_txt


def load_document(file_path: Path) -> str:
    """Load a document and return its extracted text.

    Supports .pdf, .txt, and .md files.
    """
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return load_pdf(file_path)
    elif extension == ".txt":
        return load_txt(file_path)
    elif extension == ".md":
        return load_markdown(file_path)
    else:
        raise ValidationError(f"Unsupported file type: '{extension}'")