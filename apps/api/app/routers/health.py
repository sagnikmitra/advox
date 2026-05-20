from __future__ import annotations

from fastapi import APIRouter

from app.core.config import settings
from app.rag.retriever import VerifiedRetriever

router = APIRouter(tags=["health"])
_retriever = VerifiedRetriever()


@router.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/api/readiness")
def readiness() -> dict:
    db_ok = False
    db_error = None
    if settings.database_url:
        try:
            from app.core.db import fetch_one
            row = fetch_one("SELECT 1 AS ok")
            db_ok = row is not None
        except Exception as exc:
            db_error = str(exc)
    chunk_count = 0
    if db_ok:
        try:
            row = fetch_one(
                "SELECT count(*) AS c FROM legal_source_chunks lsc "
                "JOIN legal_sources ls ON ls.id = lsc.source_id "
                "WHERE ls.verification_status = 'verified' AND ls.index_status = 'indexed'"
            )
            chunk_count = row["c"] if row else 0
        except Exception:
            pass

    return {
        "status": "ready",
        "checks": {
            "api": True,
            "database": db_ok,
            "database_configured": bool(settings.database_url),
            "gemini_configured": bool(settings.gemini_api_key),
            "indexed_chunks": chunk_count,
        },
        "db_error": db_error,
    }


@router.get("/api/debug/retrieve")
def debug_retrieve(q: str = "FIR", jurisdiction: str | None = None) -> dict:
    try:
        chunks = _retriever.retrieve(q, jurisdiction)
        return {
            "query": q,
            "count": len(chunks),
            "chunks": [
                {"citation": c.citation_label, "text": c.text[:200]}
                for c in chunks[:5]
            ],
        }
    except Exception as exc:
        return {"error": str(exc)}
