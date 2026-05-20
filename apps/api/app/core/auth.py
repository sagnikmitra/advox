from __future__ import annotations

import httpx
from fastapi import Depends, HTTPException, Request

from app.core.config import settings
from app.core.db import fetch_one, DatabaseError


def get_current_user_id(request: Request) -> str | None:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ", 1)[1].strip()
    if not token:
        return None

    supabase_url = settings.supabase_url
    if not supabase_url:
        return None

    try:
        resp = httpx.get(
            f"{supabase_url}/auth/v1/user",
            headers={"Authorization": f"Bearer {token}", "apikey": settings.supabase_anon_key},
            timeout=10.0,
        )
        if resp.status_code != 200:
            return None
        auth_user = resp.json()
        auth_id = auth_user.get("id")
        if not auth_id:
            return None

        row = fetch_one("SELECT id::text FROM users WHERE auth_id = %s", (auth_id,))
        return row["id"] if row else None
    except (DatabaseError, Exception):
        return None


def require_auth(request: Request) -> str:
    user_id = get_current_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user_id
