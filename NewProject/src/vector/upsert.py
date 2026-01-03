# Vector upsert abstraction for PoC
from ..extractor.embedder import embed_texts
from .client import upsert_vectors
import uuid


def upsert_chunks_to_vector_db(chunks, embeddings_provider=None, vector_client=None):
    """Prepare embeddings for chunks and upsert to local vector store (PoC).

    Each chunk should include 'text' and 'chunk_index' and 'page'. We will
    generate deterministic embeddings and upsert with a chunk_id.
    """
    texts = [c["text"] for c in chunks]
    embeddings = embed_texts(texts)
    entries = []
    for c, emb in zip(chunks, embeddings):
        chunk_id = c.get("chunk_id") or str(uuid.uuid4())
        c["chunk_id"] = chunk_id
        entries.append({
            "chunk_id": chunk_id,
            "text": c["text"],
            "embedding": emb,
            "metadata": {"page": c.get("page"), "chunk_index": c.get("chunk_index")},
        })
    upserted = upsert_vectors(entries)
    return upserted
