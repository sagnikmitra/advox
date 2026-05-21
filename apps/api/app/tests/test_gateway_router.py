"""Tests for gateway router — legal/non-legal classification and routing."""
from app.agents.gateway_router import GatewayRouterAgent
from app.schemas.ai import RouteRequest


def test_legal_query_detected():
    agent = GatewayRouterAgent()
    assert agent.is_legal_query("How to file an FIR for theft?") is True


def test_non_legal_query_rejected():
    agent = GatewayRouterAgent()
    assert agent.is_legal_query("What's the weather in Delhi?") is False


def test_criminal_route_without_date_warns():
    agent = GatewayRouterAgent()
    res = agent.route(RouteRequest(message="How to file FIR after arrest", persona="layman"))
    assert res.route != "refusal"
    assert "incident_date" in res.missing_critical_fields
    assert res.legal_domain == "criminal"


def test_advocate_persona_routes_to_research():
    agent = GatewayRouterAgent()
    res = agent.route(RouteRequest(message="bail provisions under BNS", persona="advocate"))
    assert res.route == "precedent_research"


def test_emergency_urgency():
    agent = GatewayRouterAgent()
    res = agent.route(RouteRequest(message="arrest custody domestic violence", persona="layman"))
    assert res.urgency == "emergency"
    assert res.requires_human_lawyer is True


def test_document_route():
    agent = GatewayRouterAgent()
    res = agent.route(RouteRequest(
        message="analyze this court order",
        persona="layman",
        documents=["order.pdf"],
    ))
    assert res.route == "document_analysis"


def test_non_legal_routes_to_refusal():
    agent = GatewayRouterAgent()
    res = agent.route(RouteRequest(message="make me a pizza recipe", persona="layman"))
    assert res.route == "refusal"
    assert res.legal_domain == "non_legal"
