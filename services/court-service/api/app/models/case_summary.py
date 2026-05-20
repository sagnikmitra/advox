from pydantic import BaseModel
from typing import Optional


class Party(BaseModel):
    name: str
    advocate: Optional[str] = None


class CaseSummaryResponse(BaseModel):
    court: str
    case_type: str
    cnr_number: str
    filing_number: str
    filing_date: str
    registration_number: str
    registration_date: str
    current_status: str
    nature_of_disposal: str
    decision_date: str
    judge: str
    petitioner: Party
    respondent: Party
