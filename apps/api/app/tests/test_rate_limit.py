"""Tests for the rate limit middleware."""
from app.core.rate_limit import _get_limit, _buckets


def test_ai_routes_have_lower_limit():
    prefix, max_req, window = _get_limit("/api/ai/scenario")
    assert prefix == "/api/ai/"
    assert max_req == 20
    assert window == 60


def test_admin_routes_have_lower_limit():
    prefix, max_req, window = _get_limit("/api/admin/sources/ingest")
    assert prefix == "/api/admin/"
    assert max_req == 10


def test_default_limit_for_unknown_routes():
    prefix, max_req, window = _get_limit("/api/sources")
    assert prefix == "default"
    assert max_req == 60


def test_case_search_has_its_own_limit():
    prefix, max_req, window = _get_limit("/api/courts/case/search")
    assert prefix == "/api/courts/case/"
    assert max_req == 30
