from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/api/readiness")
def readiness() -> dict:
    return {"status": "ready", "checks": {"api": True}}
