from __future__ import annotations


class SafetyEthicsAgent:
    crisis_terms = {
        "arrest",
        "custody",
        "domestic violence",
        "sexual offence",
        "threat",
        "minor",
        "self-harm",
    }

    def detect_crisis(self, message: str) -> bool:
        lower = message.lower()
        return any(term in lower for term in self.crisis_terms)
