from __future__ import annotations

from pydantic import BaseModel


class UploadDocumentResponse(BaseModel):
    document_id: str
    status: str


class DocumentMetadataResponse(BaseModel):
    document_id: str
    filename: str
    mime_type: str
    retention_mode: str
