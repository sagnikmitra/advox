from __future__ import annotations

import hashlib


class EmbeddingProvider:
    def embed(self, text: str) -> list[float]:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        # Deterministic lightweight pseudo-embedding placeholder for indexing pipeline.
        base = [(b / 255.0) * 2 - 1 for b in digest]
        vector: list[float] = []
        while len(vector) < 1536:
            vector.extend(base)
        return vector[:1536]
