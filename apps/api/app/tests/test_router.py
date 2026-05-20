from app.agents.gateway_router import GatewayRouterAgent
from app.schemas.ai import RouteRequest


def test_non_legal_refusal_route() -> None:
    agent = GatewayRouterAgent()
    res = agent.route(RouteRequest(message="What is the weather today?", persona="layman"))
    assert res.route == "refusal"


def test_bns_ipc_transition_warning_missing_date() -> None:
    agent = GatewayRouterAgent()
    res = agent.route(RouteRequest(message="Police refused FIR after theft", persona="layman"))
    assert "incident_date" in res.missing_critical_fields
