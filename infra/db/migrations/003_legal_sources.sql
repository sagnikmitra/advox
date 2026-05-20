CREATE TABLE legal_sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_type TEXT NOT NULL CHECK (
        source_type IN (
            'statute',
            'constitution',
            'judgment',
            'order',
            'cause_list',
            'court_rule',
            'notification',
            'manual_upload',
            'licensed_api'
        )
    ),
    authority_level TEXT NOT NULL CHECK (
        authority_level IN (
            'constitution',
            'supreme_court',
            'high_court',
            'district_court',
            'central_statute',
            'state_statute',
            'tribunal',
            'secondary'
        )
    ),
    title TEXT NOT NULL,
    court_name TEXT,
    bench TEXT,
    jurisdiction_state TEXT,
    jurisdiction_country TEXT DEFAULT 'India',
    case_number TEXT,
    cnr_number TEXT,
    neutral_citation TEXT,
    party_names TEXT[],
    judge_names TEXT[],
    act_name TEXT,
    section_number TEXT,
    article_number TEXT,
    paragraph_number TEXT,
    decision_date DATE,
    publication_date DATE,
    source_url TEXT,
    source_domain TEXT,
    language TEXT DEFAULT 'en',
    raw_content_hash TEXT,
    parsed_content_hash TEXT,
    parser_version TEXT,
    verification_status TEXT NOT NULL DEFAULT 'unverified'
        CHECK (verification_status IN ('unverified', 'pending_review', 'verified', 'rejected')),
    index_status TEXT NOT NULL DEFAULT 'not_indexed'
        CHECK (index_status IN ('not_indexed', 'queued', 'indexed', 'failed')),
    privacy_level TEXT NOT NULL DEFAULT 'public'
        CHECK (privacy_level IN ('public', 'sensitive_public', 'private_user_upload', 'confidential')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    retrieved_at TIMESTAMPTZ
);

CREATE INDEX idx_legal_sources_type ON legal_sources(source_type);
CREATE INDEX idx_legal_sources_authority ON legal_sources(authority_level);
CREATE INDEX idx_legal_sources_court ON legal_sources(court_name);
CREATE INDEX idx_legal_sources_act_section ON legal_sources(act_name, section_number);
CREATE INDEX idx_legal_sources_verification ON legal_sources(verification_status, index_status);
