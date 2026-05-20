from __future__ import annotations

from app.agents.legal_retriever import LegalRetrievalAgent, RetrievedChunk


class VerifiedRetriever:
    def __init__(self) -> None:
        self.agent = LegalRetrievalAgent()

    def retrieve(self, query: str, jurisdiction: str | None = None) -> list[RetrievedChunk]:
        return self.agent.retrieve_verified(query=query, jurisdiction=jurisdiction)
