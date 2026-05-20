from __future__ import annotations

import httpx


async def fetch_url(url: str, timeout: float = 20.0) -> bytes:
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.content
