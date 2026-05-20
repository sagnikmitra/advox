from __future__ import annotations

DISCLAIMER = (
    "LEGAL DISCLAIMER:\n"
    "This AI agent provides legal information and procedural guidance based on the Indian legal framework, "
    "including BNS, BNSS, and BSA where applicable. It does not constitute formal legal advice, representation, "
    "or an attorney-client relationship. AI performance can vary; verify all critical citations, deadlines, "
    "and strategies with a certified legal practitioner before acting."
)


def inject_disclaimer(text: str) -> str:
    if DISCLAIMER in text:
        return text
    return f"{text}\n\n{DISCLAIMER}"
