from datetime import date

TRANSITION_DATE = date(2024, 7, 1)


def map_criminal_framework(incident_date: date | None) -> str:
    if incident_date is None:
        return "transition_warning"
    if incident_date < TRANSITION_DATE:
        return "ipc_crpc_evidence_act"
    return "bns_bnss_bsa"
