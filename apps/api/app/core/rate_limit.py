"""Simple in-memory rate limiter middleware.

Uses a sliding-window token bucket per IP. Good enough for single-instance
Vercel serverless — for multi-instance, swap to Redis-backed.
"""
from __future__ import annotations

import logging
import time
from collections import defaultdict
from collections.abc import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

logger = logging.getLogger(__name__)

# Rate limits: (max_requests, window_seconds)
_LIMITS: dict[str, tuple[int, int]] = {
    "/api/ai/": (20, 60),        # 20 AI calls per minute per IP
    "/api/admin/": (10, 60),     # 10 admin calls per minute
    "/api/courts/case/": (30, 60),  # 30 case searches per minute
}
_DEFAULT_LIMIT = (60, 60)  # 60 requests per minute for everything else

# {ip: {prefix: [(timestamp, ...)]}}
_buckets: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))


def _get_limit(path: str) -> tuple[str, int, int]:
    for prefix, (max_req, window) in _LIMITS.items():
        if path.startswith(prefix):
            return prefix, max_req, window
    return "default", _DEFAULT_LIMIT[0], _DEFAULT_LIMIT[1]


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip health checks
        if request.url.path in ("/api/health", "/api/readiness"):
            return await call_next(request)

        ip = request.client.host if request.client else "unknown"
        path = request.url.path
        prefix, max_req, window = _get_limit(path)

        now = time.monotonic()
        bucket = _buckets[ip][prefix]

        # Prune expired entries
        cutoff = now - window
        _buckets[ip][prefix] = bucket = [t for t in bucket if t > cutoff]

        if len(bucket) >= max_req:
            logger.warning("Rate limit hit: ip=%s path=%s count=%d", ip, path, len(bucket))
            return JSONResponse(
                status_code=429,
                content={"error": "Too many requests. Please slow down."},
                headers={"Retry-After": str(window)},
            )

        bucket.append(now)
        return await call_next(request)
