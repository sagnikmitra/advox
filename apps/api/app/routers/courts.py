from __future__ import annotations

from fastapi import APIRouter, Query

from app.core.db import fetch_all, fetch_one, DatabaseError
from app.services.ecourts_client import (
    CaseStatus,
    fetch_case_by_cnr,
    get_court_hierarchy,
    parse_cnr,
)

router = APIRouter(prefix="/api/courts", tags=["courts"])


def _escape_like(value: str) -> str:
    """Escape ILIKE wildcard characters in user input."""
    return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


@router.get("")
def list_courts(
    court_type: str | None = None,
    state_code: str | None = None,
    q: str | None = None,
) -> dict:
    try:
        conditions = []
        params: list = []

        if court_type:
            conditions.append("court_type = %s")
            params.append(court_type)
        if state_code:
            conditions.append("state_code = %s")
            params.append(state_code.upper())
        if q:
            escaped = _escape_like(q)
            conditions.append("(name ILIKE %s OR district_name ILIKE %s OR state_name ILIKE %s)")
            params.extend([f"%{escaped}%", f"%{escaped}%", f"%{escaped}%"])

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        rows = fetch_all(
            f"SELECT id::text, name, short_name, court_type, state_code, state_name, "
            f"district_name, bench, website, ecourt_code, is_active "
            f"FROM courts {where} "
            f"ORDER BY "
            f"CASE court_type WHEN 'supreme_court' THEN 1 WHEN 'high_court' THEN 2 ELSE 3 END, "
            f"state_name, district_name "
            f"LIMIT 200",
            params,
        )
        return {"count": len(rows), "courts": rows}
    except DatabaseError as exc:
        return {"count": 0, "courts": [], "error": str(exc)}


@router.get("/states")
def list_states() -> dict:
    try:
        rows = fetch_all(
            "SELECT DISTINCT state_code, state_name FROM courts "
            "WHERE state_code IS NOT NULL ORDER BY state_name"
        )
        return {"states": rows}
    except DatabaseError:
        return {"states": []}


@router.get("/hierarchy")
def court_hierarchy() -> dict:
    return get_court_hierarchy()


@router.get("/stats")
def court_stats() -> dict:
    try:
        row = fetch_one(
            "SELECT "
            "count(*) FILTER (WHERE court_type = 'supreme_court') AS supreme_court, "
            "count(*) FILTER (WHERE court_type = 'high_court') AS high_courts, "
            "count(*) FILTER (WHERE court_type = 'district_court') AS district_courts, "
            "count(*) AS total "
            "FROM courts"
        )
        return {"stats": row or {}}
    except DatabaseError:
        return {"stats": {}}


# --- Case search routes MUST come before /{court_id} to avoid path conflict ---

@router.get("/case/parse-cnr")
def parse_cnr_number(cnr: str) -> dict:
    return parse_cnr(cnr)


@router.post("/case/search")
async def search_case(cnr: str = Query(..., min_length=16, max_length=20)) -> dict:
    result = await fetch_case_by_cnr(cnr)
    return {
        "cnr": result.cnr_number,
        "status": result.status or result.error,
        "case_type": result.case_type,
        "case_number": result.case_number,
        "court_name": result.court_name,
        "petitioner": result.petitioner,
        "respondent": result.respondent,
        "next_hearing": result.next_hearing,
        "filing_date": result.filing_date,
        "decision_date": result.decision_date,
        "disposition": result.disposition,
        "acts_sections": result.acts_sections,
        "case_history": result.case_history,
        "error": result.error if result.error else None,
    }


# --- Dynamic path param MUST come last ---

@router.get("/{court_id}")
def get_court(court_id: str) -> dict:
    try:
        row = fetch_one(
            "SELECT id::text, name, short_name, court_type, state_code, state_name, "
            "district_name, bench, address, website, ecourt_code, ecourt_state_code, "
            "ecourt_district_code, is_active "
            "FROM courts WHERE id = %s",
            (court_id,),
        )
        if not row:
            return {"error": "Court not found"}
        return row
    except DatabaseError as exc:
        return {"error": str(exc)}
