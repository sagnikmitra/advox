from __future__ import annotations

import io

import pdfplumber
from docx import Document


def parse_document_text(raw_bytes: bytes, filename: str) -> str:
    lower = filename.lower()
    if lower.endswith(".docx"):
        doc = Document(io.BytesIO(raw_bytes))
        return "\n".join(p.text for p in doc.paragraphs if p.text).strip()

    if lower.endswith(".pdf"):
        text_parts: list[str] = []
        with pdfplumber.open(io.BytesIO(raw_bytes)) as pdf:
            for page in pdf.pages:
                text_parts.append(page.extract_text() or "")
        return "\n".join(text_parts).strip()

    try:
        return raw_bytes.decode("utf-8", errors="ignore")
    except Exception:
        return f"Could not parse document: {filename}"
