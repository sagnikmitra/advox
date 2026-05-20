from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.services.source_service import list_sources, get_source_by_id

router = APIRouter(prefix="/api/sources", tags=["sources"])


@router.get("")
def get_sources():
    try:
        return list_sources()
    except Exception as exc:
        return JSONResponse(status_code=500, content={"error": str(exc)})


@router.get("/{source_id}")
def get_source(source_id: str):
    try:
        result = get_source_by_id(source_id)
        if result is None:
            return JSONResponse(status_code=404, content={"error": "not found"})
        return result
    except Exception as exc:
        return JSONResponse(status_code=500, content={"error": str(exc)})
