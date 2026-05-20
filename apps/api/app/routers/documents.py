from __future__ import annotations

import uuid

from fastapi import APIRouter, UploadFile

from app.schemas.documents import DocumentMetadataResponse, UploadDocumentResponse

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("/upload", response_model=UploadDocumentResponse)
async def upload_document(file: UploadFile) -> UploadDocumentResponse:
    doc_id = str(uuid.uuid4())
    return UploadDocumentResponse(document_id=doc_id, status="queued_for_analysis")


@router.get("/{document_id}", response_model=DocumentMetadataResponse)
def get_document(document_id: str) -> DocumentMetadataResponse:
    return DocumentMetadataResponse(
        document_id=document_id,
        filename="placeholder.pdf",
        mime_type="application/pdf",
        retention_mode="ttl",
    )


@router.delete("/{document_id}")
def delete_document(document_id: str) -> dict:
    return {"document_id": document_id, "status": "deleted"}
