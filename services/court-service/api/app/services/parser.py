# # from bs4 import BeautifulSoup
# # from typing import Any, Dict, List, Optional
# # import html as html_module
# #
# # def parse_case_html(raw: str) -> Dict[str, Any]:
# #     # ─── Preprocess ───
# #     fixed = raw.replace(r'\/', '/')
# #     fixed = html_module.unescape(fixed)
# #     soup = BeautifulSoup(fixed, "html.parser")
# #
# #     # ─── 1. Court Name ───
# #     court_tag = soup.find("h2", id="chHeading")
# #     court_name: Optional[str] = court_tag.get_text(strip=True) if court_tag else None
# #
# #     # ─── 2. Case Details ───
# #     details: Dict[str, Optional[str]] = {}
# #     hdr1 = soup.find(lambda t: t.name == "h3" and "Case Details" in t.get_text())
# #     if hdr1:
# #         tbl = hdr1.find_next_sibling("table")
# #         for tr in tbl.find_all("tr"):
# #             tds = tr.find_all("td")
# #             if len(tds) >= 2:
# #                 key = tds[0].get_text(" ", strip=True)
# #                 val = " ".join(td.get_text(" ", strip=True) for td in tds[1:])
# #                 if key:
# #                     details[key] = val
# #
# #     # ─── 3. Case Status ───
# #     status: Dict[str, Optional[str]] = {}
# #     hdr2 = soup.find(lambda t: t.name == "h3" and "Case Status" in t.get_text())
# #     if hdr2:
# #         tbl = hdr2.find_next_sibling("table")
# #         for tr in tbl.find_all("tr"):
# #             tds = tr.find_all("td")
# #             if len(tds) >= 2:
# #                 key = tds[0].get_text(" ", strip=True)
# #                 val = tds[1].get_text(" ", strip=True)
# #                 if key:
# #                     status[key] = val
# #
# #     # ─── 4. Parties ───
# #     def extract_people(heading_text: str) -> List[Dict[str, Optional[str]]]:
# #         people: List[Dict[str, Optional[str]]] = []
# #         hdr = soup.find(lambda t: t.name == "h3" and heading_text in t.get_text())
# #         if not hdr:
# #             return people
# #         tbl = hdr.find_next_sibling("table")
# #         for td in tbl.find_all("td"):
# #             raw = td.get_text(" ", strip=True)
# #             # split on "Advocate-"
# #             if "Advocate-" in raw:
# #                 name, adv = raw.split("Advocate-", 1)
# #                 people.append({"name": name.strip(), "advocate": adv.strip()})
# #             else:
# #                 people.append({"name": raw.strip(), "advocate": None})
# #         return people
# #
# #     petitioners = extract_people("Petitioner")
# #     respondents = extract_people("Respondent")
# #
# #     return {
# #         "court_name": court_name,
# #         "case_details": details,
# #         "case_status": status,
# #         "parties": {
# #             "petitioners": petitioners,
# #             "respondents": respondents
# #         }
# #     }
# # app/services/parser.py
# from bs4 import BeautifulSoup
# from typing import Any, Dict, List, Optional
# import html as html_module
#
# def parse_case_html(raw: str) -> Dict[str, Any]:
#     # — Preprocess JSON‑style escapes & entities —
#     fixed = raw.replace(r'\/', '/')
#     fixed = html_module.unescape(fixed)
#     soup = BeautifulSoup(fixed, "html.parser")
#
#     # — 1. Court Name —
#     court_tag = soup.find("h2", id="chHeading")
#     court_name: Optional[str] = court_tag.get_text(strip=True) if court_tag else None
#
#     # — 2. Case Details —
#     details: Dict[str, Optional[str]] = {}
#     hdr1 = soup.find(lambda t: t.name == "h3" and "Case Details" in t.get_text())
#     if hdr1:
#         tbl = hdr1.find_next_sibling("table")
#         for tr in tbl.find_all("tr"):
#             tds = tr.find_all("td")
#             if len(tds) >= 2:
#                 key = tds[0].get_text(" ", strip=True)
#                 val = " ".join(td.get_text(" ", strip=True) for td in tds[1:])
#                 if key:
#                     details[key] = val
#
#     # — 3. Case Status —
#     status: Dict[str, Optional[str]] = {}
#     hdr2 = soup.find(lambda t: t.name == "h3" and "Case Status" in t.get_text())
#     if hdr2:
#         tbl = hdr2.find_next_sibling("table")
#         for tr in tbl.find_all("tr"):
#             tds = tr.find_all("td")
#             if len(tds) >= 2:
#                 key = tds[0].get_text(" ", strip=True)
#                 val = tds[1].get_text(" ", strip=True)
#                 if key:
#                     status[key] = val
#
#     # — 4. Parties —
#     def extract_people(heading_text: str) -> List[Dict[str, Optional[str]]]:
#         out: List[Dict[str, Optional[str]]] = []
#         hdr = soup.find(lambda t: t.name == "h3" and heading_text in t.get_text())
#         if not hdr:
#             return out
#         tbl = hdr.find_next_sibling("table")
#         for td in tbl.find_all("td"):
#             raw = td.get_text(" ", strip=True)
#             if "Advocate-" in raw:
#                 name, adv = raw.split("Advocate-", 1)
#                 out.append({"name": name.strip(), "advocate": adv.strip()})
#             else:
#                 out.append({"name": raw.strip(), "advocate": None})
#         return out
#
#     petitioners = extract_people("Petitioner")
#     respondents = extract_people("Respondent")
#
#     # 5. Case History — use a CSS selector so we match any table whose class list includes “history_table”
#     history: List[Dict[str, str]] = []
#     tbl = soup.select_one("table.history_table")
#     if tbl:
#         rows = tbl.find_all("tr")
#         # Skip the header row (assumed first)
#         for tr in rows[1:]:
#             tds = tr.find_all("td")
#             # We need at least 4 cells per your HTML
#             if len(tds) >= 4:
#                 judge = tds[0].get_text(strip=True)
#                 business_on = tds[1].get_text(strip=True)
#                 hearing_date = tds[2].get_text(strip=True)
#                 purpose = tds[3].get_text(strip=True)
#                 # Carry forward blank judges
#                 if not judge and history:
#                     judge = history[-1]["judge"]
#                 history.append({
#                     "judge": judge,
#                     "business_on": business_on,
#                     "hearing_date": hearing_date,
#                     "purpose": purpose
#                 })
#
#     return {
#         "court_name": court_name,
#         "case_details": details,
#         "case_status": status,
#         "parties": {
#             "petitioners": petitioners,
#             "respondents": respondents
#         },
#         "case_history": history
#     }
# app/services/parser.py
from bs4 import BeautifulSoup
from typing import Any, Dict, List, Optional
import html as html_module

def parse_case_html(raw: str) -> Dict[str, Any]:
    # Unescape JSON backslashes & entities
    fixed = raw.replace(r'\/', '/')
    fixed = html_module.unescape(fixed)
    soup = BeautifulSoup(fixed, "html.parser")

    # 1. Court Name
    court_tag = soup.find("h2", id="chHeading")
    court_name: Optional[str] = court_tag.get_text(strip=True) if court_tag else None

    # 2. Case Details
    details: Dict[str, Optional[str]] = {}
    hdr1 = soup.find(lambda t: t.name == "h3" and "Case Details" in t.get_text())
    if hdr1:
        tbl = hdr1.find_next_sibling("table")
        for tr in tbl.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) >= 2:
                key = tds[0].get_text(" ", strip=True)
                val = " ".join(td.get_text(" ", strip=True) for td in tds[1:])
                details[key] = val

    # 3. Case Status
    status: Dict[str, Optional[str]] = {}
    hdr2 = soup.find(lambda t: t.name == "h3" and "Case Status" in t.get_text())
    if hdr2:
        tbl = hdr2.find_next_sibling("table")
        for tr in tbl.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) >= 2:
                key = tds[0].get_text(" ", strip=True)
                val = tds[1].get_text(" ", strip=True)
                status[key] = val

    # 4. Parties
    def extract_people(label: str) -> List[Dict[str, Optional[str]]]:
        out: List[Dict[str, Optional[str]]] = []
        hdr = soup.find(lambda t: t.name == "h3" and label in t.get_text())
        if not hdr:
            return out
        tbl = hdr.find_next_sibling("table")
        for td in tbl.find_all("td"):
            raw = td.get_text(" ", strip=True)
            if "Advocate-" in raw:
                name, adv = raw.split("Advocate-", 1)
                out.append({"name": name.strip(), "advocate": adv.strip()})
            else:
                out.append({"name": raw.strip(), "advocate": None})
        return out

    petitioners = extract_people("Petitioner")
    respondents = extract_people("Respondent")

    # 5. Case History via the <table> after <table id="historyheading">
    history: List[Dict[str, str]] = []
    heading_tbl = soup.find("table", id="historyheading")
    if heading_tbl:
        hist_tbl = heading_tbl.find_next_sibling("table")
        if hist_tbl:
            rows = hist_tbl.find_all("tr")
            for tr in rows[1:]:  # skip header
                tds = tr.find_all("td")
                if len(tds) >= 4:
                    judge = tds[0].get_text(strip=True)
                    business_on = tds[1].get_text(strip=True)
                    hearing_date = tds[2].get_text(strip=True)
                    purpose = tds[3].get_text(strip=True)
                    if not judge and history:
                        judge = history[-1]["judge"]
                    history.append({
                        "judge": judge,
                        "business_on": business_on,
                        "hearing_date": hearing_date,
                        "purpose": purpose
                    })

    return {
        "court_name": court_name,
        "case_details": details,
        "case_status": status,
        "parties": {
            "petitioners": petitioners,
            "respondents": respondents
        },
        "case_history": history
    }
