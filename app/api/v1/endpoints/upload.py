
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.logging_config import get_logger
from app.schemas.common import ErrorResponse
from app.schemas.upload import UploadResponse
from app.services.ingestion_service import index_document
from app.services.upload_service import save_uploaded_file

router = APIRouter(tags=["upload"])
logger = get_logger(__name__)


@router.post(
    "/upload",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid file (unsupported type, empty, or too large)"},
        500: {"model": ErrorResponse, "description": "File saved but indexing failed"},
    },
)
async def upload_document(file: UploadFile = File(...)) -> UploadResponse:
    """Upload a PDF, TXT, or Markdown document and index it into the vector store.

    Validation errors (bad file type, empty file, too large) are handled by
    the global exception handler in main.py and return HTTP 400.
    """
    saved = await save_uploaded_file(file)

    saved_path = Path(saved["saved_path"])
    source_name = saved_path.name

    try:
        chunk_count = index_document(saved_path, source_name)
    except Exception as exc:
        # Special case: the file WAS saved, but indexing failed. This needs
        # its own message so the caller knows the upload itself succeeded.
        logger.exception("Failed to index document '%s'", source_name)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File was uploaded but indexing failed: {exc}",
        ) from exc

    return UploadResponse(
        **saved,
        chunks_indexed=chunk_count,
        message="Document Indexed Successfully",
    )