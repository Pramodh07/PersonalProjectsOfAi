from src.worker.parser_worker import ParserWorker


def test_parser_worker_with_local_bytes(tmp_path, monkeypatch):
    # create a fake object file
    p = tmp_path / "test.pdf"
    p.write_bytes(b"Patient: John Doe\nTotal: $100")

    # push job to file queue
    import os
    from src.queue import ParseQueue
    qpath = tmp_path / "queue.log"
    os.environ.setdefault("QUEUE_LOG_PATH", str(qpath))
    q = ParseQueue(queue_path=str(qpath))
    q.clear()
    # ensure fallback (no redis)
    q.push({"ingest_id": "test-ingest", "object": str(p)})

    worker = ParserWorker()
    res = worker.process_once()
    assert res is not None
    assert res["ingest_id"] == "test-ingest"
    assert res["pages"] >= 1
