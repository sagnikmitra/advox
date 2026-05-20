import hashlib


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()
