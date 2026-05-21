"""eCourts India case search client.

Supports CNR-based case status lookup across:
- District courts (services.ecourts.gov.in)
- High courts (hcservices.ecourts.gov.in)
- Supreme Court (main.sci.gov.in)

Note: eCourts uses CAPTCHA protection. This client handles the flow
but captcha solving requires either manual input or an external service.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import UTC, datetime

import httpx
from bs4 import BeautifulSoup

DISTRICT_ECOURT_BASE = "https://services.ecourts.gov.in/ecourtindia_v6"
HC_ECOURT_BASE = "https://hcservices.ecourts.gov.in/hcservices"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


@dataclass
class CaseStatus:
    cnr_number: str
    case_type: str = ""
    case_number: str = ""
    filing_date: str = ""
    registration_date: str = ""
    court_name: str = ""
    judge_name: str = ""
    status: str = ""
    next_hearing: str = ""
    decision_date: str = ""
    disposition: str = ""
    petitioner: str = ""
    respondent: str = ""
    petitioner_advocate: str = ""
    respondent_advocate: str = ""
    acts_sections: list[str] = field(default_factory=list)
    case_history: list[dict] = field(default_factory=list)
    orders: list[dict] = field(default_factory=list)
    raw_html: str = ""
    source: str = ""
    fetched_at: str = ""
    error: str = ""


def parse_cnr(cnr: str) -> dict:
    """Parse a CNR number into components.

    CNR format: SSDDCCYYNNNNNNN
    SS = state code, DD = district code, CC = court complex code,
    YY = year, NNNNNNN = serial number
    """
    cnr = cnr.strip().upper().replace(" ", "").replace("-", "")
    if len(cnr) < 16:
        return {"valid": False, "error": "CNR must be 16 characters"}
    return {
        "valid": True,
        "cnr": cnr,
        "state_code": cnr[:2],
        "district_code": cnr[2:4],
        "court_code": cnr[4:6],
        "year": cnr[6:8],
        "serial": cnr[8:],
    }


def _extract_table_data(soup: BeautifulSoup, table_id: str) -> list[list[str]]:
    table = soup.find("table", {"id": table_id}) or soup.find("table", class_=table_id)
    if not table:
        return []
    rows = []
    for tr in table.find_all("tr"):
        cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
        if cells:
            rows.append(cells)
    return rows


def _extract_party_info(soup: BeautifulSoup) -> tuple[str, str, str, str]:
    petitioner = ""
    respondent = ""
    pet_adv = ""
    res_adv = ""

    party_table = soup.find("table", {"id": "party_info"})
    if not party_table:
        party_divs = soup.find_all("div", class_="party_info")
        for div in party_divs:
            text = div.get_text(strip=True)
            if "petitioner" in text.lower():
                petitioner = text
            elif "respondent" in text.lower():
                respondent = text
        return petitioner, respondent, pet_adv, res_adv

    rows = party_table.find_all("tr")
    section = ""
    for row in rows:
        text = row.get_text(strip=True)
        if "petitioner" in text.lower() and "advocate" not in text.lower():
            section = "petitioner"
        elif "respondent" in text.lower() and "advocate" not in text.lower():
            section = "respondent"
        elif "advocate" in text.lower() and "petitioner" in text.lower():
            section = "pet_adv"
        elif "advocate" in text.lower() and "respondent" in text.lower():
            section = "res_adv"
        else:
            cells = [td.get_text(strip=True) for td in row.find_all("td")]
            name = " ".join(cells).strip()
            if name:
                if section == "petitioner":
                    petitioner = (petitioner + ", " + name) if petitioner else name
                elif section == "respondent":
                    respondent = (respondent + ", " + name) if respondent else name
                elif section == "pet_adv":
                    pet_adv = (pet_adv + ", " + name) if pet_adv else name
                elif section == "res_adv":
                    res_adv = (res_adv + ", " + name) if res_adv else name

    return petitioner, respondent, pet_adv, res_adv


def parse_case_html(html: str, cnr: str) -> CaseStatus:
    """Parse eCourts HTML response into structured case data."""
    result = CaseStatus(
        cnr_number=cnr,
        raw_html=html,
        fetched_at=datetime.now(UTC).isoformat(),
        source="ecourts",
    )

    if not html or "no record" in html.lower() or "invalid" in html.lower():
        result.error = "No record found for this CNR"
        return result

    soup = BeautifulSoup(html, "html.parser")

    # Case details table
    case_rows = _extract_table_data(soup, "case_detail")
    for row in case_rows:
        if len(row) >= 2:
            label = row[0].lower().strip()
            val = row[1].strip()
            if "case type" in label:
                result.case_type = val
            elif "filing" in label and "number" in label:
                result.case_number = val
            elif "filing" in label and "date" in label:
                result.filing_date = val
            elif "registration" in label and "date" in label:
                result.registration_date = val

    # Status
    status_rows = _extract_table_data(soup, "case_status")
    for row in status_rows:
        if len(row) >= 2:
            label = row[0].lower().strip()
            val = row[1].strip()
            if "status" in label and "case" in label:
                result.status = val
            elif "next" in label and "hearing" in label:
                result.next_hearing = val
            elif "decision" in label and "date" in label:
                result.decision_date = val
            elif "court" in label and "number" not in label:
                result.court_name = val
            elif "judge" in label:
                result.judge_name = val
            elif "disposition" in label:
                result.disposition = val

    # Party info
    pet, res, pet_adv, res_adv = _extract_party_info(soup)
    result.petitioner = pet
    result.respondent = res
    result.petitioner_advocate = pet_adv
    result.respondent_advocate = res_adv

    # Acts/sections
    act_rows = _extract_table_data(soup, "act_table")
    for row in act_rows[1:]:
        if row:
            result.acts_sections.append(" - ".join(row))

    # Case history
    history_rows = _extract_table_data(soup, "history_table")
    for row in history_rows[1:]:
        if len(row) >= 3:
            result.case_history.append({
                "judge": row[0] if len(row) > 0 else "",
                "hearing_date": row[1] if len(row) > 1 else "",
                "purpose": row[2] if len(row) > 2 else "",
            })

    # Orders
    order_rows = _extract_table_data(soup, "order_table")
    for row in order_rows[1:]:
        if len(row) >= 2:
            result.orders.append({
                "date": row[0] if len(row) > 0 else "",
                "order": row[1] if len(row) > 1 else "",
            })

    return result


async def fetch_case_by_cnr(cnr: str) -> CaseStatus:
    """Attempt to fetch case status from eCourts by CNR number.

    This initiates the flow but captcha solving is the bottleneck.
    Returns partial data or a captcha_required error.
    """
    parsed = parse_cnr(cnr)
    if not parsed["valid"]:
        return CaseStatus(cnr_number=cnr, error=parsed["error"])

    result = CaseStatus(
        cnr_number=parsed["cnr"],
        fetched_at=datetime.now(UTC).isoformat(),
        source="ecourts",
    )

    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            home = await client.get(f"{DISTRICT_ECOURT_BASE}/", headers=HEADERS)
            if home.status_code != 200:
                result.error = "eCourts service unreachable"
                return result

            soup = BeautifulSoup(home.text, "html.parser")
            captcha_img = soup.find("img", {"id": "captcha_image"})
            app_token_input = soup.find("input", {"id": "app_token"})
            app_token = app_token_input["value"] if app_token_input and app_token_input.get("value") else ""

            if captcha_img:
                result.error = "captcha_required"
                result.status = "captcha_required"
                return result

            data = {
                "cino": parsed["cnr"],
                "fcaptcha_code": "",
                "ajax_req": "true",
                "App_token": app_token,
            }
            resp = await client.post(
                f"{DISTRICT_ECOURT_BASE}/?p=cnr_status/searchByCNR/",
                headers={**HEADERS, "Content-Type": "application/x-www-form-urlencoded"},
                data=data,
            )

            if resp.status_code == 200 and resp.text.strip():
                return parse_case_html(resp.text, parsed["cnr"])

            result.error = f"eCourts returned status {resp.status_code}"
            return result

    except Exception as exc:
        result.error = str(exc)
        return result


def get_court_hierarchy() -> dict:
    """Return the Indian court hierarchy structure."""
    return {
        "supreme_court": {
            "name": "Supreme Court of India",
            "jurisdiction": "All India",
            "benches": ["Principal Bench, New Delhi"],
        },
        "high_courts": {
            "count": 25,
            "note": "Each state/group of states has a High Court with original and appellate jurisdiction",
        },
        "district_courts": {
            "note": "District & Sessions Courts in every district, subordinate to the High Court of that state",
            "types": [
                "District & Sessions Court",
                "Chief Judicial Magistrate Court",
                "Judicial Magistrate First Class",
                "Civil Judge (Senior Division)",
                "Civil Judge (Junior Division)",
            ],
        },
        "specialized": [
            "Family Courts",
            "Consumer Courts (District/State/National)",
            "Labour Courts / Industrial Tribunals",
            "NCLT (National Company Law Tribunal)",
            "NCLAT (National Company Law Appellate Tribunal)",
            "DRT (Debt Recovery Tribunal)",
            "ITAT (Income Tax Appellate Tribunal)",
            "NGT (National Green Tribunal)",
            "SAT (Securities Appellate Tribunal)",
            "Armed Forces Tribunal",
            "CAT (Central Administrative Tribunal)",
        ],
    }
