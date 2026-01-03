import os
import asyncio
from src.ingestor import api

class DummyUploadFile:
    def __init__(self, filename, content, content_type='text/plain'):
        self.filename = filename
        self.content_type = content_type
        self._content = content

    async def read(self):
        return self._content


def test_ingest_endpoint():
    resp = asyncio.run(api.ingest(file=DummyUploadFile("test.txt", b"Patient: John Doe\nTotal: $100")))
    assert "ingest_id" in resp
    assert "object" in resp
