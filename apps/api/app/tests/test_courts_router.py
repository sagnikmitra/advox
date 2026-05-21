"""Tests for courts router — ILIKE escaping and route ordering."""
from app.routers.courts import _escape_like


def test_escape_like_percent():
    assert _escape_like("100%") == "100\\%"


def test_escape_like_underscore():
    assert _escape_like("my_court") == "my\\_court"


def test_escape_like_backslash():
    assert _escape_like("test\\value") == "test\\\\value"


def test_escape_like_normal_text():
    assert _escape_like("Supreme Court") == "Supreme Court"


def test_escape_like_combined():
    assert _escape_like("50%_done\\") == "50\\%\\_done\\\\"
