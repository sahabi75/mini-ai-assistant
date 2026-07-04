"""Handles validating and saving uploaded documents."""

import uuid
from pathlib import Path

from fastapi import UploadFile

from app.core.config import get_settings
from app.core.exceptions import ValidationError
from app.core.logging_config import get_logger

logger = get_logger(__name__)

ALLOWED_EXTENSIONS = [".pdf", ".txt", ".md"]


class UploadError(ValidationError):
    """Raised when an uploaded file fails validation or cannot be saved."""


def _is_allowed_extension(filename: str) -> bool:
    extension = Path(filename).suffix.lower()
    return extension in ALLOWED_EXTENSIONS


async def save_uploaded_file(file: UploadFile) -> dict[str, str | int]:
    """Validate an uploaded file and save it to the uploads directory.

    Returns a dict with details about the saved file.
    Raises UploadError if validation fails.
    """
    settings = get_settings()

    if not file.filename:
        raise UploadError("Uploaded file is missing a filename.")

    if not _is_allowed_extension(file.filename):
        raise UploadError(
            f"Unsupported file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    contents = await file.read()

    if len(contents) == 0:
        raise UploadError(f"File '{file.filename}' is empty.")

    max_size_bytes = settings.max_upload_size_mb * 1024 * 1024
    if len(contents) > max_size_bytes:
        raise UploadError(
            f"File '{file.filename}' is larger than {settings.max_upload_size_mb} MB."
        )

    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Prefix with a short unique id to avoid overwriting files with the same name.
    safe_filename = Path(file.filename).name
    saved_filename = f"{uuid.uuid4().hex[:8]}_{safe_filename}"
    saved_path = upload_dir / saved_filename

    saved_path.write_bytes(contents)

    logger.info("Saved uploaded file '%s' to '%s'", file.filename, saved_path)

    return {
        "filename": file.filename,
        "saved_path": str(saved_path),
        "content_type": file.content_type or "application/octet-stream",
        "size_bytes": len(contents),
    }