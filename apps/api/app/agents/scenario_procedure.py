from __future__ import annotations

from datetime import date

TRANSITION_WARNING = (
    "The applicable criminal statute may depend on the date of the incident. "
    "Please verify whether the incident occurred before or after 1 July 2024."
)


class ScenarioProcedureAgent:
    transition_date = date(2024, 7, 1)

    def transition_note(self, incident_date: date | None, legal_domain: str) -> str | None:
        if legal_domain != "criminal":
            return None
        if incident_date is None:
            return TRANSITION_WARNING
        if incident_date < self.transition_date:
            return "Use legacy criminal framework context (IPC/CrPC/Indian Evidence Act) with date validation."
        return "Use post-1 July 2024 criminal framework context (BNS/BNSS/BSA)."

    def fail_closed_for_missing_sources(self) -> str:
        return "[System Error: Verified source document not found. Cannot generate citation to prevent hallucination.]"
