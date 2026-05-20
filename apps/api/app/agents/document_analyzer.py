from __future__ import annotations

from app.documents.parser import parse_document_text


class DocumentAnalyzerAgent:
    def analyze(self, raw_bytes: bytes, filename: str) -> dict:
        parsed = parse_document_text(raw_bytes, filename)
        return {
            "executive_summary": "Placeholder analysis. Verified citation pipeline required before legal assertions.",
            "raw_excerpt": parsed[:500],
            "risk_radar": [
                "Missing verification for extracted citations",
                "Timeline/deadline needs authoritative source validation",
            ],
        }
