from __future__ import annotations

import re
from dataclasses import dataclass

from app.core.db import DatabaseError, fetch_all


@dataclass(slots=True)
class RetrievedChunk:
    source_id: str
    chunk_id: str
    text: str
    citation_label: str
    verified: bool


STOP_WORDS = frozenset(
    "a an the is are was were be been being have has had do does did will would "
    "shall should may might can could of in to for on with at by from as into "
    "through during before after above below between under what how when where "
    "who which that this these those it its i me my we our you your he she they "
    "and or but not no nor so yet if then else than too also very much about "
    "please tell explain describe process procedure way".split()
)


def _extract_keywords(query: str) -> list[str]:
    words = re.findall(r"[a-zA-Z]{2,}", query.lower())
    keywords = [w for w in words if w not in STOP_WORDS]
    return keywords[:8] if keywords else words[:5]


class LegalRetrievalAgent:
    def retrieve_verified(self, query: str, jurisdiction: str | None = None) -> list[RetrievedChunk]:
        keywords = _extract_keywords(query)
        if not keywords:
            return []

        like_clauses = []
        params: dict[str, object] = {"jurisdiction": jurisdiction}
        for i, kw in enumerate(keywords):
            key = f"kw{i}"
            like_clauses.append(
                f"(lsc.normalized_text ILIKE %({key})s OR ls.title ILIKE %({key})s)"
            )
            params[key] = f"%{kw}%"

        where_keywords = " OR ".join(like_clauses)

        score_parts = []
        for i in range(len(keywords)):
            key = f"kw{i}"
            score_parts.append(
                f"(CASE WHEN lsc.normalized_text ILIKE %({key})s THEN 1 ELSE 0 END)"
            )
        score_expr = " + ".join(score_parts) if score_parts else "0"

        jurisdiction_clause = ""
        if jurisdiction:
            jurisdiction_clause = "AND (ls.jurisdiction_state = %(jurisdiction)s OR ls.jurisdiction_state IS NULL)"
            params["jurisdiction"] = jurisdiction

        sql = f"""
            SELECT
              ls.id::text AS source_id,
              lsc.id::text AS chunk_id,
              lsc.chunk_text AS text,
              COALESCE(
                lsc.citation_label,
                '[' || INITCAP(REPLACE(ls.source_type, '_', ' ')) || '] ' || ls.title ||
                COALESCE(' - Section ' || lsc.section_number, '') ||
                ' -> ' || COALESCE(ls.source_url, 'verified-source-link')
              ) AS citation_label,
              ({score_expr}) AS relevance_score
            FROM legal_source_chunks lsc
            JOIN legal_sources ls ON ls.id = lsc.source_id
            WHERE ls.verification_status = 'verified'
              AND ls.index_status = 'indexed'
              AND ({where_keywords})
              {jurisdiction_clause}
            ORDER BY
              ({score_expr}) DESC,
              CASE ls.authority_level
                WHEN 'constitution' THEN 1
                WHEN 'supreme_court' THEN 2
                WHEN 'central_statute' THEN 3
                WHEN 'high_court' THEN 4
                ELSE 9
              END,
              lsc.chunk_index
            LIMIT 12
        """
        try:
            rows = fetch_all(sql, params)
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
