# Architecture Overview

This document describes the PoC architecture for the Insurance RAG pipeline.

Components:
- Ingestor: receives files, stores in MinIO, creates ingest record
- Parser: extracts page texts and metadata
- Extractor: extracts entities and chunks, prepares embeddings
- Vector DB: stores chunk embeddings and supports semantic search
- Validator & Adjudicator: rule-based & ML checks, decision engine
- Audit: immutable records of processing steps

Local dev: `docker-compose` brings up MinIO, Postgres, Redis, and Chroma. Services run with Uvicorn or similar ASGI server.
