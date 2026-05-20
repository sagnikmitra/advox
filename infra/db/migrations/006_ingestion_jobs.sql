CREATE TABLE ingestion_sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    source_category TEXT NOT NULL,
    base_domain TEXT NOT NULL,
    is_official BOOLEAN NOT NULL DEFAULT false,
    is_active BOOLEAN NOT NULL DEFAULT true,
    requires_captcha BOOLEAN NOT NULL DEFAULT false,
    requires_login BOOLEAN NOT NULL DEFAULT false,
    robots_policy_checked_at TIMESTAMPTZ,
    max_requests_per_minute INT DEFAULT 10,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE ingestion_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ingestion_source_id UUID REFERENCES ingestion_sources(id) ON DELETE SET NULL,
    job_type TEXT NOT NULL CHECK (
        job_type IN ('discover', 'fetch', 'parse', 'verify', 'embed', 'refresh')
    ),
    status TEXT NOT NULL DEFAULT 'queued'
        CHECK (status IN ('queued', 'running', 'success', 'failed', 'blocked')),
    target_url TEXT,
    error_message TEXT,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
