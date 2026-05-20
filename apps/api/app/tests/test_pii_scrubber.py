from app.documents.pii_scrubber import scrub_pii


def test_pii_redaction() -> None:
    text = "Rahul Sharma called 9876543210 email rahul@example.com Aadhaar 1234 5678 9012"
    redacted = scrub_pii(text)
    assert "9876543210" not in redacted
    assert "rahul@example.com" not in redacted
    assert "1234 5678 9012" not in redacted
