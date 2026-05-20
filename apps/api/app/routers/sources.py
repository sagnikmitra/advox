from __future__ import annotations

from fastapi import APIRouter

from app.schemas.sources import SourceRecord
from app.services.source_service import list_sources

router = APIRouter(prefix="/api/sources", tags=["sources"])


@router.get("", response_model=list[SourceRecord])
def get_sources() -> list[SourceRecord]:
    return list_sources()


@router.get("/{source_id}", response_model=SourceRecord)
def get_source(source_id: str) -> SourceRecord:
    for source in list_sources():
        if source.id == source_id:
            return source
    return SourceRecord(
        id=source_id,
        title="Unknown source",
        source_type="statute",
        authority_level="secondary",
        verification_status="unverified",
        index_status="not_indexed",
    )
