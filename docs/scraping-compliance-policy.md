# Scraping Compliance Policy

- Scrape only allowlisted public legal sources.
- Respect robots.txt before crawl.
- Respect rate limits and bounded retries.
- Use clear product user-agent.
- No CAPTCHA bypass.
- No login bypass.
- No scraping of private e-filing systems.
- No unauthorized personal court-party data harvesting.
- Prefer official APIs/feeds when available.
- If CAPTCHA blocks source, use manual upload or official API route.
- Log every fetch event with timestamp and source metadata.
- Checksum every fetched document.
- Version every parser.
- Review each source before enabling citation use.
