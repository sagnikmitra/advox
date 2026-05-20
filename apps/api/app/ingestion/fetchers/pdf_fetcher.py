from app.ingestion.fetchers.http_fetcher import fetch_url


async def fetch_pdf(url: str) -> bytes:
    return await fetch_url(url)
