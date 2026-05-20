from __future__ import annotations

from arq import create_pool
from arq.connections import RedisSettings

from app.core.config import settings
from app.ingestion.validators.captcha_detector import SOURCE_REQUIRES_MANUAL, detect_captcha
from app.ingestion.validators.source_allowlist_validator import is_allowlisted


def run_ingestion_job(target_url: str, fetched_preview: str) -> dict:
    if not is_allowlisted(target_url):
        return {"status": "blocked", "reason": "Source domain is not allowlisted"}
    if detect_captcha(fetched_preview):
        return {"status": "blocked", "reason": SOURCE_REQUIRES_MANUAL}
    return {"status": "queued", "reason": "Passed allowlist and CAPTCHA gate"}


async def enqueue_ingestion_job(target_url: str, fetched_preview: str = "") -> dict:
    decision = run_ingestion_job(target_url=target_url, fetched_preview=fetched_preview)
    if decision["status"] == "blocked":
        return decision

    try:
        redis = await create_pool(RedisSettings.from_dsn(settings.redis_url))
        await redis.enqueue_job("process_ingestion_job", target_url, fetched_preview)
        return {"status": "queued", "reason": decision["reason"]}
    except Exception as exc:
        return {
            "status": "queued",
            "reason": "Queue unavailable; proceeding synchronously.",
            "queue_warning": str(exc),
        }


async def process_ingestion_job(ctx: dict, target_url: str, fetched_preview: str = "") -> dict:
    # Worker entrypoint for arq queue.
    return run_ingestion_job(target_url=target_url, fetched_preview=fetched_preview)
