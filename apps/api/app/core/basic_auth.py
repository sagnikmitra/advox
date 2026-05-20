from __future__ import annotations

import base64
import hmac
from collections.abc import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.config import settings


class BasicAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self._skip_paths = {"/api/health", "/api/readiness"}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not settings.basic_auth_enabled:
            return await call_next(request)

        if request.url.path in self._skip_paths:
            return await call_next(request)

        header = request.headers.get("Authorization", "")
        if not header.startswith("Basic "):
            return Response(status_code=401, headers={"WWW-Authenticate": "Basic"})

        encoded = header.split(" ", 1)[1].strip()
        try:
            decoded = base64.b64decode(encoded).decode("utf-8")
            user, password = decoded.split(":", 1)
        except Exception:
            return Response(status_code=401, headers={"WWW-Authenticate": "Basic"})

        user_ok = hmac.compare_digest(user, settings.basic_auth_user)
        pass_ok = hmac.compare_digest(password, settings.basic_auth_password)

        if not (user_ok and pass_ok):
            return Response(status_code=401, headers={"WWW-Authenticate": "Basic"})

        return await call_next(request)
