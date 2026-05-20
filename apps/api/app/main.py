from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.basic_auth import BasicAuthMiddleware
from app.core.config import settings
from app.routers import admin, ai, documents, health, sources, users

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://advox.sgnk.ai", "http://localhost:3000"],
    allow_origin_regex=r"https://advox-.*-sagnik\.vercel\.app",
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(BasicAuthMiddleware)

app.include_router(ai.router)
app.include_router(documents.router)
app.include_router(sources.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(health.router)
