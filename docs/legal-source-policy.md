# Legal Source Policy

## Source hierarchy
1. Constitution of India and official constitutional publications.
2. Official central/state statutes (India Code, Legislative Department, Gazette/public notifications).
3. Official Supreme Court sources.
4. Official High Court and District public judgment/order portals.
5. Official public cause lists/rules/materials.
6. Licensed APIs (secondary unless reconciled with official sources).
7. Private manual uploads (tenant-private; not public corpus).

## Official source preference
Official sources override secondary sources in retrieval ranking and citation authority.

## Licensed API treatment
Licensed feeds are allowed only if usage rights permit product deployment. Mark as `licensed_api` and `secondary` unless officially matched.

## Public court source policy
Only public and lawfully accessible data. Never scrape login-protected or private court systems.

## Manual upload policy
Uploads are private workspace assets. No automatic promotion to public corpus.

## Verification status rules
Documents are citation eligible only when:
- `verification_status = verified`
- `index_status = indexed`

## Citation rules
Citations must follow deterministic format and pass citation verification checks.

## No hallucination rule
No legal assertion from model memory. Fail closed when verified sources unavailable.

## No CAPTCHA bypass rule
CAPTCHA-protected sources must return manual/API-required block message.

## No private court-data scraping rule
No e-filing/private account scraping, impersonation, or anti-abuse bypass.
