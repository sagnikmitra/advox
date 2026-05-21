"""Tests for eCourts client — CNR parsing and HTML parsing."""
from app.services.ecourts_client import parse_cnr, parse_case_html


def test_valid_cnr_parsing():
    result = parse_cnr("WBBA020001232024")
    assert result["valid"] is True
    assert result["state_code"] == "WB"
    assert result["district_code"] == "BA"
    assert result["court_code"] == "02"
    assert result["year"] == "00"
    assert result["serial"] == "01232024"


def test_short_cnr_invalid():
    result = parse_cnr("WB123")
    assert result["valid"] is False
    assert "16 characters" in result["error"]


def test_cnr_strips_spaces_and_dashes():
    result = parse_cnr("WB-BA-02-00-01232024")
    assert result["valid"] is True
    assert result["cnr"] == "WBBA020001232024"


def test_cnr_uppercases():
    result = parse_cnr("wbba020001232024")
    assert result["cnr"] == "WBBA020001232024"


def test_parse_empty_html():
    result = parse_case_html("", "TEST1234567890AB")
    assert result.error == "No record found for this CNR"


def test_parse_no_record_html():
    result = parse_case_html("No record found for this case", "TEST1234567890AB")
    assert result.error == "No record found for this CNR"


def test_parse_invalid_html():
    result = parse_case_html("This page contains invalid results", "TEST1234567890AB")
    assert result.error == "No record found for this CNR"
