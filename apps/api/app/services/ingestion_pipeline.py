from __future__ import annotations

from datetime import datetime, timezone

import httpx

from app.core.db import DatabaseError, execute, execute_returning, fetch_all
from app.ingestion.normalizers.citation_normalizer import normalize_citation
from app.ingestion.parsers.html_parser import parse_html_to_text
from app.ingestion.parsers.pdf_parser import parse_pdf_to_text
from app.ingestion.validators.captcha_detector import SOURCE_REQUIRES_MANUAL, detect_captcha
from app.ingestion.validators.checksum_validator import sha256_bytes
from app.ingestion.validators.source_allowlist_validator import is_allowlisted
from app.rag.chunker import chunk_text
from app.rag.embeddings import EmbeddingProvider

EMBEDDER = EmbeddingProvider()


def _fetch_sync(url: str) -> bytes:
    with httpx.Client(timeout=20.0, follow_redirects=True) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.content


def _infer_source_type(url: str) -> str:
    lower = url.lower()
    if lower.endswith(".pdf"):
        return "judgment"
    if "judgment" in lower or "order" in lower:
        return "judgment"
    return "statute"


def _infer_authority(url: str) -> str:
    lower = url.lower()
    if "sci.gov.in" in lower:
        return "supreme_court"
    if "ecourts.gov.in" in lower:
        return "high_court"
    if "indiacode.nic.in" in lower:
        return "central_statute"
    return "secondary"


def ingest_source_document(source_name: str, target_url: str) -> dict:
    if not is_allowlisted(target_url):
        return {"status": "blocked", "reason": "Source domain is not allowlisted"}

    content = _fetch_sync(target_url)
    preview = content[:2000].decode("utf-8", errors="ignore")
    if detect_captcha(preview):
        return {"status": "blocked", "reason": SOURCE_REQUIRES_MANUAL}

    parsed_text = (
        parse_pdf_to_text(content)
        if target_url.lower().endswith(".pdf")
        else parse_html_to_text(content.decode("utf-8", errors="ignore"))
    )

    if not parsed_text.strip():
        return {"status": "failed", "reason": "Parsed text is empty"}

    now = datetime.now(timezone.utc).isoformat()
    source_row = execute_returning(
        """
        INSERT INTO legal_sources (
          source_type, authority_level, title, source_url, source_domain,
          raw_content_hash, parsed_content_hash, parser_version,
          verification_status, index_status, retrieved_at
        ) VALUES (
          %(source_type)s, %(authority_level)s, %(title)s, %(source_url)s, %(source_domain)s,
          %(raw_hash)s, %(parsed_hash)s, %(parser_version)s,
          'pending_review', 'not_indexed', %(retrieved_at)s
        )
        RETURNING id::text, title
        """,
        {
            "source_type": _infer_source_type(target_url),
            "authority_level": _infer_authority(target_url),
            "title": f"{source_name} :: {target_url}",
            "source_url": target_url,
            "source_domain": target_url.split("/")[2] if "/" in target_url else target_url,
            "raw_hash": sha256_bytes(content),
            "parsed_hash": sha256_bytes(parsed_text.encode("utf-8")),
            "parser_version": "ingestion_pipeline_v1",
            "retrieved_at": now,
        },
    )

    if not source_row:
        return {"status": "failed", "reason": "Could not create source row"}

    return {
        "status": "success",
        "source_id": source_row["id"],
        "title": source_row["title"],
        "reason": "Source discovered/fetched/parsed and pending verification",
    }


def verify_and_index_source(source_url: str) -> dict:
    source = fetch_all(
        """
        SELECT id::text, title, source_url
        FROM legal_sources
        WHERE source_url = %(source_url)s
        ORDER BY created_at DESC
        LIMIT 1
        """,
        {"source_url": source_url},
    )
    if not source:
        return {"status": "failed", "reason": "Source URL not found"}

    source_id = source[0]["id"]

    parsed_text_row = fetch_all(
        """
        SELECT parsed_content_hash, title
        FROM legal_sources
        WHERE id = %(id)s::uuid
        """,
        {"id": source_id},
    )

    # For this scaffold, we re-fetch source content and re-parse for deterministic indexing.
    content = _fetch_sync(source_url)
    parsed_text = (
        parse_pdf_to_text(content)
        if source_url.lower().endswith(".pdf")
        else parse_html_to_text(content.decode("utf-8", errors="ignore"))
    )

    chunks = chunk_text(parsed_text, max_chars=1200)
    if not chunks:
        return {"status": "failed", "reason": "No chunks generated"}

    execute("DELETE FROM legal_source_chunks WHERE source_id = %(source_id)s::uuid", {"source_id": source_id})

    for i, chunk in enumerate(chunks):
        embedding = EMBEDDER.embed(chunk)
        citation_label = normalize_citation(
            f"[Statute] {source[0]['title']} - Section {i + 1} -> {source_url}"
        )
        execute(
            """
            INSERT INTO legal_source_chunks (
              source_id, chunk_index, chunk_text, normalized_text, token_count, embedding, citation_label, metadata
            ) VALUES (
              %(source_id)s::uuid, %(chunk_index)s, %(chunk_text)s, %(normalized_text)s, %(token_count)s,
              %(embedding)s::vector, %(citation_label)s, %(metadata)s::jsonb
            )
            """,
            {
                "source_id": source_id,
                "chunk_index": i,
                "chunk_text": chunk,
                "normalized_text": normalize_citation(chunk),
                "token_count": max(1, len(chunk.split())),
                "embedding": str(embedding),
                "citation_label": citation_label,
                "metadata": "{}",
            },
        )

    execute(
        """
        UPDATE legal_sources
        SET verification_status = 'verified', index_status = 'indexed'
        WHERE id = %(source_id)s::uuid
        """,
        {"source_id": source_id},
    )

    return {"status": "success", "source_id": source_id, "chunks_indexed": len(chunks)}
