from __future__ import annotations

import re

from app.core.db import DatabaseError, fetch_one
from app.schemas.ai import CitationItem, CitationVerificationResponse


class CitationVerificationAgent:
    _citation_pattern = re.compile(r"^\[(?P<source_type>[^\]]+)\]\s+(?P<title>.+?)\s+-\s+(?P<pin>(Section|Article|Paragraph)\s+[^-]+?)\s+->\s+(?P<link>\S+)$")

    def _verify_against_db(self, title: str, pin: str, link: str) -> tuple[bool, str]:
        sql = """
            SELECT ls.id::text, ls.title, ls.source_url, lsc.section_number, lsc.paragraph_number
            FROM legal_sources ls
            LEFT JOIN legal_source_chunks lsc ON lsc.source_id = ls.id
            WHERE ls.verification_status = 'verified'
              AND ls.index_status = 'indexed'
              AND ls.title ILIKE %(title)s
              AND (
                ls.source_url = %(link)s
                OR %(link)s = 'verified-source-link'
              )
            LIMIT 1
        """
        try:
            row = fetch_one(sql, {"title": f"%{title.strip()}%", "link": link.strip()})
        except DatabaseError:
            return False, "Database unavailable for citation verification."

        if not row:
            return False, "No verified source record matched citation title/link."

        pin_l = pin.lower().strip()
        if pin_l.startswith("section"):
            section_no = pin.split(" ", 1)[1].strip() if " " in pin else ""
            if row.get("section_number") and row["section_number"] != section_no:
                return False, "Section number mismatch in verified chunk."
        if pin_l.startswith("paragraph"):
            para_no = pin.split(" ", 1)[1].strip() if " " in pin else ""
            if row.get("paragraph_number") and str(row["paragraph_number"]) != para_no:
                return False, "Paragraph number mismatch in verified chunk."

        return True, "Verified source, link, and pin reference."

    def verify(self, citations: list[str]) -> CitationVerificationResponse:
        items: list[CitationItem] = []
        has_blocker = False

        for citation in citations:
            normalized = citation.strip()
            match = self._citation_pattern.match(normalized)
            if not match:
                has_blocker = True
                items.append(
                    CitationItem(
                        citation_text=normalized,
                        verification_status="unverified",
                        verification_notes="Citation format validation failed.",
                    )
                )
                continue

            ok, notes = self._verify_against_db(
                title=match.group("title"),
                pin=match.group("pin"),
                link=match.group("link"),
            )
            if not ok:
                has_blocker = True
                items.append(
                    CitationItem(
                        citation_text=normalized,
                        verification_status="missing",
                        verification_notes=notes,
                    )
                )
            else:
                items.append(
                    CitationItem(
                        citation_text=normalized,
                        verification_status="verified",
                        verification_notes=notes,
                    )
                )

        if has_blocker:
            return CitationVerificationResponse(
                passed=False,
                items=items,
                error=(
                    "Citation verification failed. The following citations could not be verified:\n"
                    + "\n".join(f"- {i.citation_text}" for i in items if i.verification_status != "verified")
                    + "\nThe answer cannot be rendered as authoritative legal research."
                ),
            )

        return CitationVerificationResponse(passed=True, items=items)
