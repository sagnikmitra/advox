"""Tests for the legal retriever — keyword extraction."""
from app.agents.legal_retriever import _extract_keywords, _escape_like


def test_extracts_meaningful_keywords():
    keywords = _extract_keywords("How to file an FIR for theft in West Bengal?")
    assert "fir" in keywords
    assert "theft" in keywords
    assert "west" in keywords
    # Stop words removed
    assert "how" not in keywords
    assert "to" not in keywords
    assert "an" not in keywords


def test_limits_to_8_keywords():
    long_query = "bail arrest fir police court section petition notice judgment landlord tenant salary"
    keywords = _extract_keywords(long_query)
    assert len(keywords) <= 8


def test_empty_query_returns_fallback():
    keywords = _extract_keywords("is the a an")
    # Falls back to raw words if all are stop words
    assert len(keywords) > 0


def test_escape_like_in_retriever():
    assert _escape_like("100%") == "100\\%"
    assert _escape_like("normal") == "normal"
