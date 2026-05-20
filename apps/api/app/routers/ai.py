from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.agents.citation_verifier import CitationVerificationAgent
from app.agents.gateway_router import GatewayRouterAgent
from app.agents.scenario_procedure import ScenarioProcedureAgent
from app.agents.translator import TranslationAgent
from app.rag.retriever import VerifiedRetriever
from app.schemas.ai import (
    CitationVerificationRequest,
    CitationVerificationResponse,
    ResearchRequest,
    RouteRequest,
    RouteResponse,
    ScenarioRequest,
    ScenarioResponse,
)
from app.services.disclaimer_service import inject_disclaimer
from app.services.llm_client import LLMClient, LLMClientError

router = APIRouter(prefix="/api/ai", tags=["ai"])
gateway = GatewayRouterAgent()
scenario_agent = ScenarioProcedureAgent()
citation_agent = CitationVerificationAgent()
translator = TranslationAgent()
retriever = VerifiedRetriever()
llm_client = LLMClient()

NON_LEGAL_REFUSAL = (
    "I can only help with Indian legal information, legal procedure, court-document analysis, "
    "and legal research workflows. Please ask a question related to Indian law or legal process."
)


@router.post("/route", response_model=RouteResponse)
def route_message(payload: RouteRequest) -> RouteResponse:
    return gateway.route(payload)


@router.post("/scenario", response_model=ScenarioResponse)
def scenario(payload: ScenarioRequest) -> ScenarioResponse:
    routed = gateway.route(payload)
    if routed.route == "refusal":
        return ScenarioResponse(content=inject_disclaimer(NON_LEGAL_REFUSAL), blocked=True)

    chunks = retriever.retrieve(payload.message, payload.state)
    if not chunks:
        return ScenarioResponse(
            content=inject_disclaimer(scenario_agent.fail_closed_for_missing_sources()),
            blocked=True,
        )

    transition = scenario_agent.transition_note(payload.incident_date, routed.legal_domain)
    context = "\n\n".join(f"{chunk.citation_label}\n{chunk.text[:900]}" for chunk in chunks[:6])
    prompt = (
        f"Persona: {payload.persona}\n"
        f"Language: {payload.language}\n"
        f"State: {payload.state or 'unknown'}\n"
        f"Incident Date: {payload.incident_date or 'unknown'}\n\n"
        "Task: Provide legal information and procedural guidance only from the verified context. "
        "Do not invent statutes or judgments. If context is insufficient, explicitly say so.\n\n"
        f"User Query:\n{payload.message}\n\nVerified Context:\n{context}\n"
    )
    try:
        generated = llm_client.generate(prompt)
    except LLMClientError:
        generated = "Based on verified sources available in the system..."
    citations = "\n".join(f"- {chunk.citation_label}" for chunk in chunks[:6])
    content = generated
    if transition:
        content += f"\n\n{transition}"
    content += f"\n\nSources used:\n{citations}"
    return ScenarioResponse(content=inject_disclaimer(content))


@router.post("/document/analyze", response_model=ScenarioResponse)
def analyze_document(payload: ScenarioRequest) -> ScenarioResponse:
    return ScenarioResponse(
        content=inject_disclaimer(
            "Document analyzer scaffold active. Upload pipeline and verified-citation extraction required before legal assertions."
        )
    )


@router.post("/research", response_model=ScenarioResponse)
def research(payload: ResearchRequest) -> ScenarioResponse:
    chunks = retriever.retrieve(payload.query, payload.state)
    if not chunks:
        return ScenarioResponse(
            content=inject_disclaimer(scenario_agent.fail_closed_for_missing_sources()),
            blocked=True,
        )
    citations = [chunk.citation_label for chunk in chunks[:10]]
    verification = citation_agent.verify(citations)
    if not verification.passed:
        return ScenarioResponse(content=inject_disclaimer(verification.error or "Citation verification failed."), blocked=True)

    context = "\n\n".join(f"{chunk.citation_label}\n{chunk.text[:900]}" for chunk in chunks[:8])
    prompt = (
        f"Persona: {payload.persona}\n"
        f"Language: {payload.language}\n"
        f"State: {payload.state or 'unknown'}\n\n"
        "Task: Produce concise legal research notes using only verified context below. "
        "Do not add claims not present in context.\n\n"
        f"Research Query:\n{payload.query}\n\nVerified Context:\n{context}\n"
    )
    try:
        points = llm_client.generate(prompt)
    except LLMClientError:
        points = "\n".join(f"- {chunk.text[:280]}" for chunk in chunks[:5])
    cites = "\n".join(f"- {item.citation_text}" for item in verification.items)
    content = f"Based on verified sources available in the system...\n\nExtracted points:\n{points}\n\nVerified citations:\n{cites}"
    return ScenarioResponse(content=inject_disclaimer(content))


@router.post("/citation/verify", response_model=CitationVerificationResponse)
def verify_citations(payload: CitationVerificationRequest) -> CitationVerificationResponse:
    return citation_agent.verify(payload.citations)


@router.post("/translate", response_model=ScenarioResponse)
def translate(payload: ScenarioRequest) -> ScenarioResponse:
    prompt = (
        f"Translate the following legal text into '{payload.language}'. "
        "Preserve legal meaning and keep citations unchanged.\n\n"
        f"{payload.message}"
    )
    try:
        translated = llm_client.generate(prompt)
    except LLMClientError:
        translated = translator.translate(payload.message, payload.language)
    return ScenarioResponse(content=inject_disclaimer(translated))


@router.post("/refusal-check", response_model=ScenarioResponse)
def refusal_check(payload: ScenarioRequest) -> ScenarioResponse:
    if gateway.is_legal_query(payload.message):
        raise HTTPException(status_code=400, detail="Query is legal; refusal not applicable")
    return ScenarioResponse(content=inject_disclaimer(NON_LEGAL_REFUSAL), blocked=True)
