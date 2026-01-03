import hashlib
from typing import List

VECTOR_DIM = 128


def _hash_to_vector(text: str, dim: int = VECTOR_DIM) -> List[float]:
    # deterministic pseudo-embedding using SHA256 bytes
    h = hashlib.sha256(text.encode("utf-8")).digest()
    vector = []
    # expand bytes deterministically to floats
    for i in range(dim):
        b = h[i % len(h)]
        # map byte to [-1, 1]
        vector.append((b / 255.0) * 2.0 - 1.0)
    return vector


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Return deterministic embeddings for a list of texts."""
    return [_hash_to_vector(t) for t in texts]
