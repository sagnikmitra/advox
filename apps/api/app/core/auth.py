from __future__ import annotations

import logging

import jwt
from fastapi import Depends, HTTPException, Request

from app.core.config import settings
from app.core.db import fetch_one, DatabaseError

logger = logging.getLogger(__name__)


def _decode_supabase_jwt(token: str) -> dict | None:
    """Verify and decode a Supabase JWT locally using the JWT secret.

    Falls back to the anon key as HMAC secret if jwt_secret isn't set
    (Supabase signs JWTs with the project JWT secret).
    """
    secret = settings.supabase_jwt_secret
    if not secret:
        # Fallback: can't verify locally without the secret
        return None
    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms=["HS256"],
            audience="authenticated",
        )
        return payload
    except jwt.ExpiredSignatureError:
        logger.debug("JWT expired")
        return None
    except jwt.InvalidTokenError as exc:
        logger.debug("JWT invalid: %s", exc)
        return None


def _get_auth_id_from_token(token: str) -> str | None:
    """Extract the Supabase auth user id (sub claim) from a Bearer token."""
    # Try local verification first (fast, no network)
    payload = _decode_supabase_jwt(token)
    if payload:
        return payload.get("sub")

    # Fallback: remote verification via Supabase (slow, requires network)
    if not settings.supabase_url:
        return None
    try:
        import httpx

        resp = httpx.get(
            f"{settings.supabase_url}/auth/v1/user",
            headers={
                "Authorization": f"Bearer {token}",
                "apikey": settings.supabase_anon_key,
            },
            timeout=10.0,
        )
        if resp.status_code != 200:
            return None
        auth_user = resp.json()
        return auth_user.get("id")
    except Exception:
        logger.exception("Remote JWT verification failed")
        return None


def get_current_user_id(request: Request) -> str | None:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ", 1)[1].strip()
    if not token:
        return None

    auth_id = _get_auth_id_from_token(token)
    if not auth_id:
        return None

    try:
        row = fetch_one("SELECT id::text FROM users WHERE auth_id = %s", (auth_id,))
        return row["id"] if row else None
    except (DatabaseError, Exception):
        return None


def require_auth(request: Request) -> str:
    user_id = get_current_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user_id
