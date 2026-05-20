CREATE TABLE legal_source_chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID NOT NULL REFERENCES legal_sources(id) ON DELETE CASCADE,
    chunk_index INT NOT NULL,
    chunk_text TEXT NOT NULL,
    normalized_text TEXT,
    token_count INT,
    embedding vector(1536),
    citation_label TEXT,
    page_number INT,
    paragraph_number TEXT,
    section_number TEXT,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_legal_source_chunks_source ON legal_source_chunks(source_id);
CREATE INDEX idx_legal_source_chunks_embedding
ON legal_source_chunks USING ivfflat (embedding vector_cosine_ops);

CREATE TABLE user_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    uploaded_by UUID REFERENCES users(id) ON DELETE SET NULL,
    original_filename TEXT NOT NULL,
    mime_type TEXT NOT NULL,
    storage_uri TEXT,
    file_hash TEXT NOT NULL,
    redacted_text TEXT,
    document_type TEXT CHECK (
        document_type IN (
            'fir',
            'legal_notice',
            'order_sheet',
            'judgment',
            'pleading',
            'petition',
            'affidavit',
            'contract',
            'unknown'
        )
    ),
    retention_mode TEXT NOT NULL DEFAULT 'ttl'
        CHECK (retention_mode IN ('ttl', 'workspace_saved', 'delete_immediately')),
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
