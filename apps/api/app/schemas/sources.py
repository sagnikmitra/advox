from __future__ import annotations

from pydantic import BaseModel


class SourceRecord(BaseModel):
    id: str
    title: str
    source_type: str
    authority_level: str
    verification_status: str
    index_status: str


class IngestionRequest(BaseModel):
    source_name: str
    target_url: str
