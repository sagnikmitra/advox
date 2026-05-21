from __future__ import annotations

import logging
from collections.abc import Mapping, Sequence

import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from app.core.config import settings

logger = logging.getLogger(__name__)


class DatabaseError(RuntimeError):
    pass


# Module-level pool — lazy-initialized on first use.
_pool: ConnectionPool | None = None


def _get_pool() -> ConnectionPool:
    global _pool
    if _pool is not None:
        return _pool
    if not settings.database_url:
        raise DatabaseError("DATABASE_URL is not configured")
    _pool = ConnectionPool(
        conninfo=settings.database_url,
        min_size=2,
        max_size=10,
        kwargs={"row_factory": dict_row},
        open=True,
    )
    return _pool


def fetch_all(query: str, params: Sequence[object] | Mapping[str, object] | None = None) -> list[dict]:
    try:
        with _get_pool().connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                rows = cur.fetchall()
                return [dict(row) for row in rows]
    except DatabaseError:
        raise
    except Exception as exc:
        logger.exception("fetch_all failed")
        raise DatabaseError(str(exc)) from exc


def fetch_one(query: str, params: Sequence[object] | Mapping[str, object] | None = None) -> dict | None:
    try:
        with _get_pool().connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                row = cur.fetchone()
                return dict(row) if row else None
    except DatabaseError:
        raise
    except Exception as exc:
        logger.exception("fetch_one failed")
        raise DatabaseError(str(exc)) from exc


def execute(query: str, params: Sequence[object] | Mapping[str, object] | None = None) -> None:
    try:
        with _get_pool().connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
            conn.commit()
    except DatabaseError:
        raise
    except Exception as exc:
        logger.exception("execute failed")
        raise DatabaseError(str(exc)) from exc


def execute_returning(
    query: str, params: Sequence[object] | Mapping[str, object] | None = None
) -> dict | None:
    try:
        with _get_pool().connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                row = cur.fetchone()
            conn.commit()
            return dict(row) if row else None
    except DatabaseError:
        raise
    except Exception as exc:
        logger.exception("execute_returning failed")
        raise DatabaseError(str(exc)) from exc
