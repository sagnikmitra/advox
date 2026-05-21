from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Request

from app.core.auth import require_auth
from app.core.db import DatabaseError, fetch_one
from app.ingestion.jobs.ingestion_worker import enqueue_ingestion_job
from app.schemas.sources import IngestionRequest
from app.services.ingestion_pipeline import ingest_source_document, verify_and_index_source

router = APIRouter(prefix="/api/admin", tags=["admin"])


def _require_admin(request: Request, user_id: str = Depends(require_auth)) -> str:
    """Verify caller is authenticated AND has admin role."""
    row = fetch_one("SELECT role FROM users WHERE id = %s", (user_id,))
    if not row or row["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user_id


@router.post("/sources/ingest")
async def ingest_source(payload: IngestionRequest, _admin: str = Depends(_require_admin)) -> dict:
    queue_warning: str | None = None
    queued = await enqueue_ingestion_job(payload.target_url, fetched_preview="")
    queue_warning = queued.get("queue_warning")
    if queued["status"] == "blocked":
        return {"job_id": str(uuid.uuid4()), **queued}

    try:
        ingested = ingest_source_document(payload.source_name, payload.target_url)
    except DatabaseError as exc:
        ingested = {"status": "failed", "reason": str(exc)}
    except Exception as exc:
        ingested = {"status": "failed", "reason": f"Ingestion pipeline error: {exc}"}
    if queue_warning:
        ingested["queue_warning"] = queue_warning
    return {"job_id": str(uuid.uuid4()), **ingested}


@router.post("/sources/verify")
def verify_source(payload: IngestionRequest, _admin: str = Depends(_require_admin)) -> dict:
    try:
        result = verify_and_index_source(payload.target_url)
    except DatabaseError as exc:
        result = {"status": "failed", "reason": str(exc)}
    return {"source_name": payload.source_name, **result}


@router.get("/ingestion/jobs")
def list_jobs(_admin: str = Depends(_require_admin)) -> dict:
    return {"jobs": []}


@router.get("/ingestion/jobs/{job_id}")
def get_job(job_id: str, _admin: str = Depends(_require_admin)) -> dict:
    return {"job_id": job_id, "status": "queued"}
