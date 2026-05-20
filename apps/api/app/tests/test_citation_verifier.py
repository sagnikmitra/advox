from app.agents.citation_verifier import CitationVerificationAgent


def test_citation_verification_failure_blocks() -> None:
    agent = CitationVerificationAgent()
    result = agent.verify(["[Statute] Some Act - Section 1 -> bad-link"])
    assert result.passed is False
    assert "cannot be rendered as authoritative legal research" in (result.error or "")
