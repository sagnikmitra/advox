COURT_MAP = {
    "supreme court": "Supreme Court of India",
    "delhi hc": "High Court of Delhi",
}


def normalize_court_name(name: str) -> str:
    key = name.strip().lower()
    return COURT_MAP.get(key, name.strip())
