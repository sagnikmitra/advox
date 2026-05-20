from __future__ import annotations

import uuid

from fastapi import APIRouter

from app.core.db import DatabaseError
from app.ingestion.jobs.ingestion_worker import enqueue_ingestion_job
from app.schemas.sources import IngestionRequest
from app.services.ingestion_pipeline import ingest_source_document, verify_and_index_source

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/sources/ingest")
async def ingest_source(payload: IngestionRequest) -> dict:
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
def verify_source(payload: IngestionRequest) -> dict:
    try:
        result = verify_and_index_source(payload.target_url)
    except DatabaseError as exc:
        result = {"status": "failed", "reason": str(exc)}
    return {"source_name": payload.source_name, **result}


@router.get("/ingestion/jobs")
def list_jobs() -> dict:
    return {"jobs": []}


@router.get("/ingestion/jobs/{job_id}")
def get_job(job_id: str) -> dict:
    return {"job_id": job_id, "status": "queued"}
