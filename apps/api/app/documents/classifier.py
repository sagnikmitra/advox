from __future__ import annotations


def classify_document(filename: str) -> str:
    name = filename.lower()
    if "fir" in name:
        return "fir"
    if "judgment" in name:
        return "judgment"
    if "notice" in name:
        return "legal_notice"
    return "unknown"
