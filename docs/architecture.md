# Architecture

Frontend:
- Next.js App Router with persona pages and persistent disclaimer bar.

Backend:
- FastAPI orchestrator with routing, scenario, research, citation verification, ingestion admin APIs.
- Agentized modules for routing, retrieval, procedures, document analysis, citation checks, safety.

Data:
- PostgreSQL + pgvector for source corpus/chunks/embeddings.
- Redis for queue/cache hooks.
- S3-compatible object storage for transient document files.

Safety gates:
1. Non-legal refusal check.
2. Verified-source retrieval requirement.
3. Citation verification gate.
4. Incident-date transition warnings for criminal law.
5. Mandatory disclaimer injection.
