from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class SourceType(str, Enum):
    statute = "statute"
    judgment = "judgment"
    order = "order"
    cause_list = "cause_list"


class AuthorityLevel(str, Enum):
    constitution = "constitution"
    supreme_court = "supreme_court"
    high_court = "high_court"
    district_court = "district_court"
    central_statute = "central_statute"
    state_statute = "state_statute"
    secondary = "secondary"


@dataclass(slots=True)
class SourceDiscoveryQuery:
    query: str
    jurisdiction: str | None = None


@dataclass(slots=True)
class SourceCandidate:
    url: str
    title: str


@dataclass(slots=True)
class FetchResult:
    url: str
    content: bytes
    content_type: str


@dataclass(slots=True)
class ParsedLegalDocument:
    title: str
    text: str
    metadata: dict


@dataclass(slots=True)
class NormalizedLegalDocument:
    title: str
    text: str
    metadata: dict


@dataclass(slots=True)
class VerificationResult:
    status: str
    notes: str


class LegalSourceConnector(Protocol):
    source_name: str
    source_type: SourceType
    authority_level: AuthorityLevel

    async def discover(self, query: SourceDiscoveryQuery) -> list[SourceCandidate]: ...

    async def fetch(self, candidate: SourceCandidate) -> FetchResult: ...

    async def parse(self, fetch_result: FetchResult) -> ParsedLegalDocument: ...

    async def normalize(self, parsed: ParsedLegalDocument) -> NormalizedLegalDocument: ...

    async def verify(self, normalized: NormalizedLegalDocument) -> VerificationResult: ...
