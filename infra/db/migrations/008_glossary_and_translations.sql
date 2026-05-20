CREATE TABLE legal_glossary (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    canonical_term TEXT NOT NULL,
    english_term TEXT NOT NULL,
    hindi_term TEXT,
    bengali_term TEXT,
    plain_language_explanation TEXT,
    technical_definition TEXT,
    related_statutes TEXT[],
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
