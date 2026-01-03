# Insurance RAG PoC

This PoC demonstrates a multi-agent RAG pipeline for insurance claim ingestion, extraction, validation, and adjudication.

Quick start (local dev):
- Install dependencies: `pip install -r requirements.txt` or use Poetry
- Start infra: `docker-compose -f infra/docker-compose.yml up` (MinIO, Postgres, Chroma, Redis)
- Run services with Uvicorn, e.g., `uvicorn src.ingestor.api:app --reload --port 8000`

See `docs/architecture.md` for design details and `tests/` for sample tests.
