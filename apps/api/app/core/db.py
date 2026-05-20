from __future__ import annotations

from collections.abc import Mapping, Sequence

import psycopg
from psycopg.rows import dict_row

from app.core.config import settings


class DatabaseError(RuntimeError):
    pass


def _connect() -> psycopg.Connection:
    if not settings.database_url:
        raise DatabaseError("DATABASE_URL is not configured")
    return psycopg.connect(settings.database_url, row_factory=dict_row)


def fetch_all(query: str, params: Sequence[object] | Mapping[str, object] | None = None) -> list[dict]:
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                rows = cur.fetchall()
                return [dict(row) for row in rows]
    except Exception as exc:  # pragma: no cover - dependent on external DB
        raise DatabaseError(str(exc)) from exc


def fetch_one(query: str, params: Sequence[object] | Mapping[str, object] | None = None) -> dict | None:
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                row = cur.fetchone()
                return dict(row) if row else None
    except Exception as exc:  # pragma: no cover - dependent on external DB
        raise DatabaseError(str(exc)) from exc


def execute(query: str, params: Sequence[object] | Mapping[str, object] | None = None) -> None:
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
            conn.commit()
    except Exception as exc:  # pragma: no cover - dependent on external DB
        raise DatabaseError(str(exc)) from exc


def execute_returning(
    query: str, params: Sequence[object] | Mapping[str, object] | None = None
) -> dict | None:
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                row = cur.fetchone()
            conn.commit()
            return dict(row) if row else None
    except Exception as exc:  # pragma: no cover - dependent on external DB
        raise DatabaseError(str(exc)) from exc
