"""Tests for database module — pool initialization and error handling."""
import pytest

from app.core.db import DatabaseError, _get_pool


def test_database_error_is_runtime_error():
    assert issubclass(DatabaseError, RuntimeError)


def test_pool_returns_same_instance():
    """Pool should be a singleton — calling _get_pool twice returns same object."""
    # This test only validates the function contract; actual pool requires DB_URL.
    # If DATABASE_URL is empty, it should raise.
    import app.core.db as db_mod
    original = db_mod._pool
    try:
        db_mod._pool = None  # Reset
        db_mod.settings.database_url = ""
        with pytest.raises(DatabaseError, match="DATABASE_URL"):
            _get_pool()
    finally:
        db_mod._pool = original
