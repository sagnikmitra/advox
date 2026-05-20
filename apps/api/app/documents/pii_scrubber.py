from __future__ import annotations

import re


PATTERNS = [
    (re.compile(r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b"), "[PERSON_1]"),
    (re.compile(r"\b\d{10}\b"), "[PHONE_1]"),
    (re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"), "[EMAIL_1]"),
    (re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b"), "[AADHAAR_REDACTED]"),
    (re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b"), "[PAN_REDACTED]"),
    (re.compile(r"\b[A-Z]{2}\d{2}[A-Z]{2}\d{4}\b"), "[VEHICLE_1]"),
    (re.compile(r"\b[\w._%+-]+@[\w.-]+\.[A-Za-z]{2,}\b"), "[EMAIL_1]"),
    (re.compile(r"\b\d{9,18}\b"), "[ACCOUNT_REDACTED]"),
]


def scrub_pii(text: str) -> str:
    redacted = text
    for pattern, replacement in PATTERNS:
        redacted = pattern.sub(replacement, redacted)

    redacted = re.sub(r"\bminor\b", "[MINOR_REDACTED]", redacted, flags=re.IGNORECASE)
    return redacted
