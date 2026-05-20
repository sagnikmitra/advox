from pydantic import BaseModel


class CitationCheckResult(BaseModel):
    citation_text: str
    status: str
    notes: str | None = None
