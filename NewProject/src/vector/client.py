import json
from typing import List, Dict
from pathlib import Path

STORAGE = Path("vector_store.jsonl")


def upsert_vectors(entries: List[Dict]):
    """Upsert list of entries to a local JSONL file as PoC. Each entry should
    contain: chunk_id, text, embedding, metadata
    """
    existing = {}
    if STORAGE.exists():
        with STORAGE.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    existing[obj["chunk_id"]] = obj
                except Exception:
                    continue
    # apply upserts
    for e in entries:
        existing[e["chunk_id"]] = e
    # rewrite file
    with STORAGE.open("w", encoding="utf-8") as f:
        for obj in existing.values():
            f.write(json.dumps(obj) + "\n")
    return list(existing.values())


def get_all_vectors():
    items = []
    if STORAGE.exists():
        with STORAGE.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    items.append(json.loads(line))
                except Exception:
                    continue
    return items
