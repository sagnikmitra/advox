from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.auth import require_auth
from app.core.db import fetch_one, fetch_all, execute, DatabaseError

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me")
def get_me(user_id: str = Depends(require_auth)) -> dict:
    try:
        row = fetch_one(
            "SELECT id::text, email, full_name, role, preferred_language, default_state, is_verified "
            "FROM users WHERE id = %s",
            (user_id,),
        )
        if not row:
            return {"error": "User not found"}

        advocate = None
        if row["role"] == "advocate":
            advocate = fetch_one(
                "SELECT bar_council_id, enrollment_number, practice_areas, verification_status "
                "FROM advocate_profiles WHERE user_id = %s",
                (user_id,),
            )

        return {**row, "advocate_profile": advocate}
    except DatabaseError as exc:
        return {"error": str(exc)}


@router.get("/me/conversations")
def list_conversations(user_id: str = Depends(require_auth)) -> dict:
    try:
        rows = fetch_all(
            "SELECT id::text, title, persona, language, jurisdiction_state, created_at, updated_at "
            "FROM conversations WHERE user_id = %s ORDER BY updated_at DESC LIMIT 50",
            (user_id,),
        )
        return {"conversations": rows}
    except DatabaseError:
        return {"conversations": []}


@router.get("/me/conversations/{conversation_id}/messages")
def get_conversation_messages(conversation_id: str, user_id: str = Depends(require_auth)) -> dict:
    try:
        conv = fetch_one(
            "SELECT id::text FROM conversations WHERE id = %s AND user_id = %s",
            (conversation_id, user_id),
        )
        if not conv:
            return {"messages": [], "error": "Not found"}

        rows = fetch_all(
            "SELECT id::text, role, content, route, blocked, created_at "
            "FROM conversation_messages WHERE conversation_id = %s ORDER BY created_at",
            (conversation_id,),
        )
        return {"messages": rows}
    except DatabaseError:
        return {"messages": []}


@router.get("/me/cases")
def list_cases(user_id: str = Depends(require_auth)) -> dict:
    try:
        rows = fetch_all(
            "SELECT id::text, title, court_name, case_number, cnr_number, matter_type, "
            "jurisdiction_state, status, created_at "
            "FROM legal_cases WHERE created_by = %s ORDER BY created_at DESC LIMIT 50",
            (user_id,),
        )
        return {"cases": rows}
    except DatabaseError:
        return {"cases": []}
