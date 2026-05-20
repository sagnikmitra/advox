CREATE TABLE ai_interactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE SET NULL,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    persona TEXT NOT NULL CHECK (persona IN ('layman', 'advocate')),
    route TEXT NOT NULL,
    language TEXT DEFAULT 'en',
    jurisdiction_state TEXT,
    incident_date DATE,
    prompt_hash TEXT NOT NULL,
    redacted_prompt TEXT,
    response_hash TEXT,
    model_name TEXT,
    retrieval_required BOOLEAN NOT NULL DEFAULT true,
    citation_verification_status TEXT CHECK (
        citation_verification_status IN ('not_required', 'passed', 'failed', 'partial')
    ),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE ai_response_citations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    interaction_id UUID NOT NULL REFERENCES ai_interactions(id) ON DELETE CASCADE,
    source_id UUID REFERENCES legal_sources(id) ON DELETE SET NULL,
    chunk_id UUID REFERENCES legal_source_chunks(id) ON DELETE SET NULL,
    citation_text TEXT NOT NULL,
    verification_status TEXT NOT NULL CHECK (
        verification_status IN ('verified', 'partially_verified', 'unverified', 'conflicting', 'missing')
    ),
    verification_notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
