SOURCE_REQUIRES_MANUAL = (
    "SOURCE_REQUIRES_MANUAL_ACCESS_OR_OFFICIAL_API: "
    "This source cannot be automatically scraped without violating anti-abuse protections. "
    "Use manual upload, official API access, or approved data-sharing route."
)


def detect_captcha(content: str) -> bool:
    marker_terms = ["captcha", "recaptcha", "hcaptcha", "cf-chl"]
    lower = content.lower()
    return any(term in lower for term in marker_terms)
