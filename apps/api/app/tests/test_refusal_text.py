from app.routers.ai import NON_LEGAL_REFUSAL


def test_non_legal_refusal_text_domain_bound() -> None:
    assert "I can only help with Indian legal information" in NON_LEGAL_REFUSAL
