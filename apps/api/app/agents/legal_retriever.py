from __future__ import annotations

from dataclasses import dataclass

from app.core.db import DatabaseError, fetch_all


@dataclass(slots=True)
class RetrievedChunk:
    source_id: str
    chunk_id: str
    text: str
    citation_label: str
    verified: bool


class LegalRetrievalAgent:
    def retrieve_verified(self, query: str, jurisdiction: str | None = None) -> list[RetrievedChunk]:
        sql = """
            SELECT
              lsc.source_id::text AS source_id,
              lsc.id::text AS chunk_id,
              lsc.chunk_text AS text,
              COALESCE(
                lsc.citation_label,
                '[' || INITCAP(REPLACE(ls.source_type, '_', ' ')) || '] ' || ls.title ||
                COALESCE(' - Section ' || lsc.section_number, '') ||
                ' -> ' || COALESCE(ls.source_url, 'verified-source-link')
              ) AS citation_label
            FROM legal_source_chunks lsc
            JOIN legal_sources ls ON ls.id = lsc.source_id
            WHERE ls.verification_status = 'verified'
              AND ls.index_status = 'indexed'
              AND (
                lsc.normalized_text ILIKE %(q)s
                OR lsc.chunk_text ILIKE %(q)s
                OR ls.title ILIKE %(q)s
              )
              AND (%(jurisdiction)s IS NULL OR ls.jurisdiction_state = %(jurisdiction)s)
            ORDER BY
              CASE ls.authority_level
                WHEN 'constitution' THEN 1
                WHEN 'supreme_court' THEN 2
                WHEN 'central_statute' THEN 3
                WHEN 'high_court' THEN 4
                ELSE 9
              END,
              COALESCE(ls.decision_date, ls.publication_date) DESC NULLS LAST
            LIMIT 12
        """
        try:
            rows = fetch_all(
                sql,
                {
                    "q": f"%{query.strip()}%",
                    "jurisdiction": jurisdiction,
                },
            )
        except DatabaseError:
            return []

        return [
            RetrievedChunk(
                source_id=row["source_id"],
                chunk_id=row["chunk_id"],
                text=row["text"],
                citation_label=row["citation_label"],
                verified=True,
            )
            for row in rows
        ]
