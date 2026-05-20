from __future__ import annotations

from fastapi import FastAPI

from app.core.basic_auth import BasicAuthMiddleware
from app.core.config import settings
from app.routers import admin, ai, documents, health, sources

app = FastAPI(title=settings.app_name)
app.add_middleware(BasicAuthMiddleware)

app.include_router(ai.router)
app.include_router(documents.router)
app.include_router(sources.router)
app.include_router(admin.router)
app.include_router(health.router)
