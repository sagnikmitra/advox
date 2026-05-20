#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import time
from collections import deque
from dataclasses import dataclass
from typing import Iterable
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

HREF_RE = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)

SEEDS: dict[str, list[str]] = {
    "bns_bnss_bsa": [
        "https://www.indiacode.nic.in/",
        "https://legislative.gov.in/",
    ],
    "supreme_court": [
        "https://www.sci.gov.in/judgements/",
        "https://www.sci.gov.in/cause-list/",
        "https://www.sci.gov.in/daily-orders/",
    ],
    "ecourts": [
        "https://services.ecourts.gov.in/",
        "https://judgments.ecourts.gov.in/",
        "https://njdg.ecourts.gov.in/",
    ],
    "high_courts": [
        "https://www.calcuttahighcourt.gov.in/",
        "https://delhihighcourt.nic.in/",
        "https://bombayhighcourt.nic.in/",
        "https://mhc.tn.gov.in/judis",
        "https://karnatakajudiciary.kar.nic.in/",
    ],
    "west_bengal": [
        "https://www.wb.gov.in/",
        "https://www.wblc.gov.in/",
        "https://www.calcuttahighcourt.gov.in/",
    ],
}


@dataclass
class CrawlResult:
    discovered: list[str]
    blocked_robots: list[str]
    fetch_failed: list[str]


def normalize(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return ""
    clean = parsed._replace(fragment="", query="")
    return clean.geturl().rstrip("/")


def should_keep(base_host: str, url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    if not host:
        return False
    if host == base_host or host.endswith(f".{base_host}"):
        return True
    # keep eCourts subdomains as a family
    if base_host.endswith("ecourts.gov.in") and host.endswith("ecourts.gov.in"):
        return True
    return False


def allowed_by_robots(url: str, ua: str, cache: dict[str, RobotFileParser]) -> bool:
    parsed = urlparse(url)
    host = parsed.netloc
    if host not in cache:
        robots = RobotFileParser()
        try:
            req = Request(f"{parsed.scheme}://{host}/robots.txt", headers={"User-Agent": ua})
            with urlopen(req, timeout=8.0) as resp:
                content = resp.read().decode("utf-8", errors="ignore").splitlines()
            robots.parse(content)
            cache[host] = robots
        except Exception:
            # fail open only when robots is unreachable
            cache[host] = robots
            return True
    rp = cache[host]
    try:
        return rp.can_fetch(ua, url)
    except Exception:
        return True


def extract_links(html: str, base_url: str) -> Iterable[str]:
    for match in HREF_RE.finditer(html):
        raw = match.group(1).strip()
        if raw.startswith(("mailto:", "javascript:", "#")):
            continue
        absolute = normalize(urljoin(base_url, raw))
        if absolute:
            yield absolute


def crawl(seed_urls: list[str], per_seed_limit: int, delay_s: float, timeout_s: float) -> CrawlResult:
    ua = "advox-legal-source-crawler/1.0 (+compliance; no-captcha-bypass)"
    discovered: list[str] = []
    blocked_robots: list[str] = []
    fetch_failed: list[str] = []
    robots_cache: dict[str, RobotFileParser] = {}

    for seed in seed_urls:
        seed = normalize(seed)
        if not seed:
            continue
        base_host = (urlparse(seed).hostname or "").lower()
        q = deque([seed])
        seen = {seed}
        count = 0
        while q and count < per_seed_limit:
            url = q.popleft()
            if not allowed_by_robots(url, ua, robots_cache):
                blocked_robots.append(url)
                continue
            req = Request(url, headers={"User-Agent": ua})
            try:
                with urlopen(req, timeout=timeout_s) as resp:
                    code = getattr(resp, "status", 200)
                    ctype = (resp.headers.get("Content-Type") or "").lower()
                    body = resp.read()
            except (HTTPError, URLError, TimeoutError):
                fetch_failed.append(url)
                continue
            time.sleep(delay_s)
            if code >= 400:
                fetch_failed.append(url)
                continue
            discovered.append(url)
            count += 1
            if "text/html" not in ctype:
                continue
            text = body.decode("utf-8", errors="ignore")
            for link in extract_links(text, url):
                if link in seen:
                    continue
                if not should_keep(base_host, link):
                    continue
                seen.add(link)
                q.append(link)

    return CrawlResult(discovered=sorted(set(discovered)), blocked_robots=blocked_robots, fetch_failed=fetch_failed)


def call_json(method: str, url: str, payload: dict, timeout_s: float) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = Request(
        url,
        data=data,
        method=method,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    with urlopen(req, timeout=timeout_s) as resp:
        return json.loads(resp.read().decode("utf-8", errors="ignore"))


def ingest_and_verify(api_base: str, urls: list[str], source_name: str, do_verify: bool, delay_s: float) -> dict:
    ingest_url = f"{api_base.rstrip('/')}/api/admin/sources/ingest"
    verify_url = f"{api_base.rstrip('/')}/api/admin/sources/verify"
    out: dict[str, list[dict]] = {"ingested": [], "blocked": [], "failed": [], "verified": []}
    for u in urls:
        payload = {"source_name": source_name, "target_url": u}
        try:
            res = call_json("POST", ingest_url, payload, 30.0)
        except Exception as exc:
            out["failed"].append({"url": u, "reason": f"ingest_http_error: {exc}"})
            continue
        status = res.get("status")
        if status == "success":
            out["ingested"].append({"url": u, "source_id": res.get("source_id")})
            if do_verify:
                try:
                    v = call_json("POST", verify_url, payload, 30.0)
                    out["verified"].append({"url": u, "status": v.get("status"), "chunks": v.get("chunks_indexed")})
                except Exception as exc:
                    out["failed"].append({"url": u, "reason": f"verify_http_error: {exc}"})
            time.sleep(delay_s)
        elif status == "blocked":
            out["blocked"].append({"url": u, "reason": res.get("reason", "blocked")})
        else:
            out["failed"].append({"url": u, "reason": res.get("reason", "failed")})
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Crawl official legal sources and ingest into Advox API.")
    parser.add_argument("--api-base", default="https://api.advox.sgnk.ai")
    parser.add_argument("--scope", default="all", choices=["all", *SEEDS.keys()])
    parser.add_argument("--per-seed-limit", type=int, default=10)
    parser.add_argument("--crawl-delay", type=float, default=1.0)
    parser.add_argument("--ingest-delay", type=float, default=0.5)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--output", default="infra/scripts/crawl_report.json")
    args = parser.parse_args()

    seed_urls = []
    if args.scope == "all":
        for group in SEEDS.values():
            seed_urls.extend(group)
    else:
        seed_urls = SEEDS[args.scope]

    crawl_result = crawl(
        seed_urls=seed_urls,
        per_seed_limit=args.per_seed_limit,
        delay_s=args.crawl_delay,
        timeout_s=args.timeout,
    )
    ingest_result = ingest_and_verify(
        api_base=args.api_base,
        urls=crawl_result.discovered,
        source_name=f"bulk_{args.scope}",
        do_verify=args.verify,
        delay_s=args.ingest_delay,
    )

    report = {
        "scope": args.scope,
        "seeds_count": len(seed_urls),
        "discovered_count": len(crawl_result.discovered),
        "blocked_robots_count": len(crawl_result.blocked_robots),
        "fetch_failed_count": len(crawl_result.fetch_failed),
        "ingested_count": len(ingest_result["ingested"]),
        "verified_count": len([x for x in ingest_result["verified"] if x.get("status") == "success"]),
        "blocked_count": len(ingest_result["blocked"]),
        "failed_count": len(ingest_result["failed"]),
        "details": {
            "blocked_robots": crawl_result.blocked_robots,
            "fetch_failed": crawl_result.fetch_failed,
            **ingest_result,
        },
    }
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(json.dumps({k: report[k] for k in report if k != "details"}, indent=2))
    print(f"Report written: {args.output}")


if __name__ == "__main__":
    main()
