from __future__ import annotations

from app.schemas.sources import SourceRecord


def list_sources() -> list[SourceRecord]:
    return [
        SourceRecord(
            id="placeholder-source",
            title="Placeholder verified source registry",
            source_type="statute",
            authority_level="central_statute",
            verification_status="verified",
            index_status="indexed",
        )
    ]
