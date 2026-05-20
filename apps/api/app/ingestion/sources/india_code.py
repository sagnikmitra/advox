from __future__ import annotations

import trafilatura

from app.ingestion.fetchers.http_fetcher import fetch_url
from app.ingestion.parsers.html_parser import parse_html_to_text
from app.ingestion.sources.base import (
    AuthorityLevel,
    FetchResult,
    LegalSourceConnector,
    NormalizedLegalDocument,
    ParsedLegalDocument,
    SourceCandidate,
    SourceDiscoveryQuery,
    SourceType,
    VerificationResult,
)


class IndiaCodeConnector(LegalSourceConnector):
    source_name = "india_code"
    source_type = SourceType.statute
    authority_level = AuthorityLevel.central_statute

    async def discover(self, query: SourceDiscoveryQuery) -> list[SourceCandidate]:
        q = query.query.strip().replace(" ", "+")
        return [
            SourceCandidate(
                url=f"https://www.indiacode.nic.in/simple-search?qs={q}",
                title=f"India Code search: {query.query.strip()}",
            )
        ]

    async def fetch(self, candidate: SourceCandidate) -> FetchResult:
        raw = await fetch_url(candidate.url)
        return FetchResult(url=candidate.url, content=raw, content_type="text/html")

    async def parse(self, fetch_result: FetchResult) -> ParsedLegalDocument:
        html = fetch_result.content.decode("utf-8", errors="ignore")
        extracted = trafilatura.extract(html) or parse_html_to_text(html)
        return ParsedLegalDocument(
            title="India Code Document",
            text=extracted,
            metadata={"source_url": fetch_result.url, "parser_version": "india_code_v1"},
        )

    async def normalize(self, parsed: ParsedLegalDocument) -> NormalizedLegalDocument:
        return NormalizedLegalDocument(title=parsed.title, text=parsed.text, metadata=parsed.metadata)

    async def verify(self, normalized: NormalizedLegalDocument) -> VerificationResult:
        if "indiacode.nic.in" not in str(normalized.metadata.get("source_url", "")):
            return VerificationResult(status="rejected", notes="Source URL not in India Code authority domain.")
        if len(normalized.text.strip()) < 100:
            return VerificationResult(status="pending_review", notes="Insufficient extracted text for automated verification.")
        return VerificationResult(status="pending_review", notes="Authority domain validated. Await legal reviewer sign-off.")
