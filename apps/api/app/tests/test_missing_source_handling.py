from app.agents.scenario_procedure import ScenarioProcedureAgent


def test_missing_source_fail_closed_message() -> None:
    agent = ScenarioProcedureAgent()
    msg = agent.fail_closed_for_missing_sources()
    assert msg == "[System Error: Verified source document not found. Cannot generate citation to prevent hallucination.]"
