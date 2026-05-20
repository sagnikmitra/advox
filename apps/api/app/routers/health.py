from __future__ import annotations

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["health"])


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
    return {
        "status": "ready",
        "checks": {
            "api": True,
            "database": db_ok,
            "database_configured": bool(settings.database_url),
            "gemini_configured": bool(settings.gemini_api_key),
        },
        "db_error": db_error,
    }
