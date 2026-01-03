from src.vector.client import upsert_vectors, get_all_vectors


def test_vector_upsert(tmp_path):
    # remove existing store if present
    import os
    store = tmp_path / "vector_store.jsonl"
    if store.exists():
        store.unlink()
    # monkeypatch path
    from src.vector import client
    client.STORAGE = store

    entries = [
        {"chunk_id": "c1", "text": "hello", "embedding": [0.1, 0.2], "metadata": {"page": 1}},
        {"chunk_id": "c2", "text": "world", "embedding": [0.3, 0.4], "metadata": {"page": 1}},
    ]
    upsert_vectors(entries)
    all_items = get_all_vectors()
    assert len(all_items) == 2
    # upsert existing one
    entries2 = [{"chunk_id": "c1", "text": "hello2", "embedding": [0.5], "metadata": {"page": 1}}]
    upsert_vectors(entries2)
    all_items = get_all_vectors()
    assert any(i["text"] == "hello2" for i in all_items)
