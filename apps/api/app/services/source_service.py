from __future__ import annotations

from app.core.db import fetch_all, fetch_one, DatabaseError
from app.schemas.sources import SourceRecord


def list_sources() -> list[SourceRecord]:
    try:
        rows = fetch_all(
            "SELECT id, title, source_type, authority_level, verification_status, index_status "
            "FROM legal_sources ORDER BY created_at DESC LIMIT 100"
        )
        return [SourceRecord(**row) for row in rows]
    except DatabaseError:
        return []


def get_source_by_id(source_id: str) -> SourceRecord | None:
    try:
        row = fetch_one(
            "SELECT id, title, source_type, authority_level, verification_status, index_status "
            "FROM legal_sources WHERE id = %s",
            (source_id,),
        )
        return SourceRecord(**row) if row else None
    except DatabaseError:
        return None
