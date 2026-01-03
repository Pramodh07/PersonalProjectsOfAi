import os
from fastapi.testclient import TestClient
from src.ingestor import api

client = TestClient(api.app)

def test_ingest_endpoint():
    resp = client.post("/ingest", files={"file": ("test.txt", b"Patient: John Doe\nTotal: $100")})
    assert resp.status_code == 200
    body = resp.json()
    assert "ingest_id" in body
    assert "object" in body
