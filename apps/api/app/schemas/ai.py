from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


Persona = Literal["layman", "advocate"]
RouteType = Literal[
    "scenario_mapping",
    "document_analysis",
    "precedent_research",
    "statute_lookup",
    "procedural_guidance",
    "translation",
    "advocate_handoff",
    "refusal",
]


class RouteRequest(BaseModel):
    message: str
    persona: Persona = "layman"
    language: str = "en"
    state: str | None = None
    incident_date: date | None = None
    documents: list[str] = Field(default_factory=list)


class RouteResponse(BaseModel):
    route: RouteType
    persona: Persona
    language: str
    jurisdiction_state: str | None
    legal_domain: str
    urgency: Literal["low", "medium", "high", "emergency"]
    requires_verified_sources: bool = True
    requires_citation_verification: bool = True
    requires_human_lawyer: bool = False
    missing_critical_fields: list[str] = Field(default_factory=list)


class ScenarioRequest(RouteRequest):
    pass


class ScenarioResponse(BaseModel):
    content: str
    blocked: bool = False


class ResearchRequest(RouteRequest):
    query: str


class CitationItem(BaseModel):
    citation_text: str
    verification_status: Literal[
        "verified",
        "partially_verified",
        "unverified",
        "conflicting",
        "missing",
    ]
    verification_notes: str | None = None


class CitationVerificationRequest(BaseModel):
    draft_answer: str
    citations: list[str]


class CitationVerificationResponse(BaseModel):
    passed: bool
    items: list[CitationItem]
    error: str | None = None
