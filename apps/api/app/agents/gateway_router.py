from __future__ import annotations

from datetime import date
from typing import Iterable

from app.schemas.ai import RouteRequest, RouteResponse

LEGAL_KEYWORDS = {
    "fir",
    "bail",
    "arrest",
    "police",
    "court",
    "section",
    "petition",
    "notice",
    "judgment",
    "landlord",
    "tenant",
    "salary",
    "domestic violence",
    "cheque",
    "cnr",
    "ipc",
    "bns",
    "bnss",
    "bsa",
}

EMERGENCY_KEYWORDS = {
    "arrest",
    "custody",
    "domestic violence",
    "sexual",
    "threat",
    "minor",
    "assault",
}

CRIMINAL_KEYWORDS = {"fir", "arrest", "police", "bns", "ipc", "bnss", "crpc", "evidence", "bsa"}


class GatewayRouterAgent:
    transition_date = date(2024, 7, 1)

    def _contains(self, text: str, words: Iterable[str]) -> bool:
        text_l = text.lower()
        return any(w in text_l for w in words)

    def is_legal_query(self, message: str) -> bool:
        return self._contains(message, LEGAL_KEYWORDS)

    def route(self, req: RouteRequest) -> RouteResponse:
        message = req.message.strip()
        if not self.is_legal_query(message):
            return RouteResponse(
                route="refusal",
                persona=req.persona,
                language=req.language,
                jurisdiction_state=req.state,
                legal_domain="non_legal",
                urgency="low",
                requires_human_lawyer=False,
            )

        urgency = "emergency" if self._contains(message, EMERGENCY_KEYWORDS) else "medium"
        route = "document_analysis" if req.documents else "scenario_mapping"
        if "precedent" in message.lower() or req.persona == "advocate":
            route = "precedent_research"

        missing_fields: list[str] = []
        if self._contains(message, CRIMINAL_KEYWORDS) and req.incident_date is None:
            missing_fields.append("incident_date")

        return RouteResponse(
            route=route,
            persona=req.persona,
            language=req.language,
            jurisdiction_state=req.state,
            legal_domain="criminal" if self._contains(message, CRIMINAL_KEYWORDS) else "general",
            urgency=urgency,
            requires_human_lawyer=urgency == "emergency",
            missing_critical_fields=missing_fields,
        )
