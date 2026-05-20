from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AccessContext:
    tenant_id: str | None = None
    user_id: str | None = None
    role: str = "layman"


def ensure_admin(ctx: AccessContext) -> bool:
    return ctx.role == "admin"
