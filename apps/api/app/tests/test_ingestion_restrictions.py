from app.ingestion.jobs.ingestion_worker import run_ingestion_job
from app.ingestion.validators.captcha_detector import SOURCE_REQUIRES_MANUAL


def test_captcha_blocking() -> None:
    result = run_ingestion_job("https://services.ecourts.gov.in/demo", "captcha required")
    assert result["status"] == "blocked"
    assert SOURCE_REQUIRES_MANUAL in result["reason"]


def test_allowlist_blocking() -> None:
    result = run_ingestion_job("https://example.com/private", "ok")
    assert result["status"] == "blocked"
