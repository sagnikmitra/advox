from urllib.parse import urlparse

ALLOWED_DOMAINS = {
    "indiacode.nic.in",
    "sci.gov.in",
    "services.ecourts.gov.in",
    "judgments.ecourts.gov.in",
    "calcuttahighcourt.gov.in",
    "delhihighcourt.nic.in",
    "bombayhighcourt.nic.in",
    "mhc.tn.gov.in",
    "karnatakajudiciary.kar.nic.in",
    "districts.ecourts.gov.in",
    "njdg.ecourts.gov.in",
    "doj.gov.in",
    "egazette.gov.in",
    "legislative.gov.in",
    "wb.gov.in",
    "wblc.gov.in",
}


def is_allowlisted(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return any(host == domain or host.endswith(f".{domain}") for domain in ALLOWED_DOMAINS)
