INSERT INTO ingestion_sources (name, source_category, base_domain, is_official, requires_captcha, requires_login, max_requests_per_minute, notes)
VALUES
('India Code', 'statutory', 'indiacode.nic.in', true, false, false, 10, 'Primary statutory source'),
('Supreme Court of India', 'judgment', 'sci.gov.in', true, false, false, 8, 'Official Supreme Court source'),
('eCourts Services', 'court_portal', 'services.ecourts.gov.in', true, true, false, 5, 'Some routes may include anti-automation protections'),
('eSCR Judgments and Orders', 'judgment_portal', 'judgments.ecourts.gov.in', true, false, false, 8, 'Public judgments/orders portal')
ON CONFLICT DO NOTHING;
