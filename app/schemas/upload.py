
from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    filename: str
    saved_path: str
    content_type: str
    size_bytes: int = Field(ge=0)
    chunks_indexed: int = Field(ge=0)
    message: str