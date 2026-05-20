from __future__ import annotations

from fastapi import APIRouter

from app.schemas.sources import SourceRecord
from app.services.source_service import list_sources, get_source_by_id

router = APIRouter(prefix="/api/sources", tags=["sources"])


@router.get("", response_model=list[SourceRecord])
def get_sources() -> list[SourceRecord]:
    return list_sources()


@router.get("/{source_id}", response_model=SourceRecord | None)
def get_source(source_id: str) -> SourceRecord | None:
    return get_source_by_id(source_id)
