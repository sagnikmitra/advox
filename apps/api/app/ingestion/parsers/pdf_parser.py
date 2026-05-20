from __future__ import annotations

import io

import pdfplumber


def parse_pdf_to_text(raw: bytes) -> str:
    text_parts: list[str] = []
    with pdfplumber.open(io.BytesIO(raw)) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts).strip()
