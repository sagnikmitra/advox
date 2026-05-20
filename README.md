# Advox (MVP Foundation)

Advox is a safety-first, citation-gated legal information system for India with two product flows:
- Layman procedural guidance (`/ask`)
- Advocate research and case workspace (`/advocate`)

## What it does
- Routes legal queries into scenario mapping, document analysis, statute lookup, and research workflows.
- Enforces verified-source-first behavior for legal assertions.
- Blocks unsafe authoritative rendering when citations cannot be verified.
- Implements ingestion connectors and compliance-safe scraping boundaries (no CAPTCHA bypass, no login scraping).
- Supports incident-date-aware criminal law transition logic (IPC/CrPC/Evidence Act vs BNS/BNSS/BSA).
- Provides multilingual-ready interfaces and glossary schema.

## What it does not do
- Does not provide final legal advice.
- Does not create attorney-client relationship.
- Does not invent statutes, citations, case names, or deadlines.
- Does not bypass CAPTCHA, scrape login portals, or scrape private e-filing systems.

## Monorepo structure
- `apps/web`: Next.js App Router frontend.
- `apps/api`: FastAPI orchestration backend, RAG and ingestion stubs.
- `infra/db/migrations`: PostgreSQL + pgvector migrations.
- `infra/scripts`: seed SQL.
- `docs`: safety, policy, architecture, contracts.

## Local setup
### 1. Prerequisites
- Node.js 20+
- Python 3.11+
- Docker + Docker Compose
- pnpm 9+

### 2. Configure environment
```bash
cp .env.example .env
```
Set `BASIC_AUTH_USER` and `BASIC_AUTH_PASSWORD` before exposing the app.

### 3. Start infrastructure
```bash
docker compose up -d postgres redis minio
```

### 4. Install dependencies
```bash
pnpm install
```

### 5. Run frontend
```bash
pnpm --filter web dev
```

### 6. Run backend
```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload --port 8000
```

### 6.1 Basic auth behavior
- Web app uses Next.js middleware basic auth.
- API uses FastAPI middleware basic auth.
- Health endpoints (`/api/health`, `/api/readiness`) remain unauthenticated for probes.

### 7. Run migrations
Use your migration runner of choice (Alembic/Flyway/psql). Example:
```bash
psql "$DATABASE_URL" -f infra/db/migrations/001_init_extensions.sql
psql "$DATABASE_URL" -f infra/db/migrations/002_users_and_tenants.sql
psql "$DATABASE_URL" -f infra/db/migrations/003_legal_sources.sql
psql "$DATABASE_URL" -f infra/db/migrations/004_documents_and_chunks.sql
psql "$DATABASE_URL" -f infra/db/migrations/005_ai_audit_and_citations.sql
psql "$DATABASE_URL" -f infra/db/migrations/006_ingestion_jobs.sql
psql "$DATABASE_URL" -f infra/db/migrations/007_advocate_workspace.sql
psql "$DATABASE_URL" -f infra/db/migrations/008_glossary_and_translations.sql
```

### 8. Run tests
```bash
cd apps/api
pytest
```

## Environment variables
See `.env.example` for all values. Key vars:
- `DATABASE_URL`
- `REDIS_URL`
- `S3_ENDPOINT`, `S3_BUCKET`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`
- `LLM_PROVIDER`, `LLM_MODEL`
- `EMBEDDING_PROVIDER`, `EMBEDDING_MODEL`
- `LEGAL_TRANSITION_DATE` (default `2024-07-01`)
- `BASIC_AUTH_ENABLED`
- `BASIC_AUTH_USER`
- `BASIC_AUTH_PASSWORD`

## Ingestion policy
- Allowlisted official/public legal sources only.
- Robots and rate-limit checks before fetch.
- CAPTCHA/login detection causes job block.
- Every fetched document must be checksummed and source tagged.
- Only `verification_status='verified'` and `index_status='indexed'` data is available for citation-backed RAG.

## Source verification policy
- Citation verification agent validates section/paragraph and source link references.
- Any `unverified`, `conflicting`, or `missing` citation blocks authoritative advocate output.
- Layman flow fails closed for unsupported legal assertions.

## Security notes
- Privacy-first by design with PII redaction before model calls.
- TTL-based document retention default.
- Tenant/user boundary model built into schema.
- Avoid raw prompt persistence by default (`prompt_hash` + redacted prompt).
- Basic auth enforced across frontend and backend for hosted baseline protection.

## Legal disclaimer
LEGAL DISCLAIMER:
This AI agent provides legal information and procedural guidance based on the Indian legal framework, including BNS, BNSS, and BSA where applicable. It does not constitute formal legal advice, representation, or an attorney-client relationship. AI performance can vary; verify all critical citations, deadlines, and strategies with a certified legal practitioner before acting.

## Roadmap
### Phase 1: MVP Foundation
- Persona UI
- Basic legal chat
- Upload parser
- RAG schema
- Source ingestion stubs
- Citation verifier
- Disclaimer
- PII scrubber

### Phase 2: Verified Legal Corpus
- India Code ingestion
- Constitution ingestion
- BNS/BNSS/BSA ingestion
- Supreme Court judgments
- High Court judgments
- Legal glossary
- Manual source review dashboard

### Phase 3: Advocate Workspace
- Case folders
- Document timelines
- Strategy notes
- Draft generation
- Precedent comparison
- Procedural deadline tracker

### Phase 4: Layman Vernacular Product
- Hindi/Bengali support
- Legalese simplifier
- Step-by-step procedural workflows
- Legal aid/handoff directory
- State-specific workflows

### Phase 5: Production Compliance
- Tenant isolation
- Audit trails
- Encryption
- ZDR contracts
- Admin review
- Monitoring
- Security testing
- Rate limiting
- Abuse prevention
