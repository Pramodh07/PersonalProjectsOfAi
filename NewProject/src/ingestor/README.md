Ingestor service

- `POST /ingest` accepts multipart file upload and stores files in MinIO
- TODO: integrate with Postgres to create ingest record and enqueue parse job
- Start with: `uvicorn src.ingestor.api:app --reload --port 8000`
