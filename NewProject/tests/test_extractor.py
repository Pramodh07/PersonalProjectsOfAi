from src.extractor.splitter import split_text_to_chunks
from src.extractor.embedder import embed_texts


def test_splitter_and_embedder():
    text = "word " * 500
    chunks = split_text_to_chunks(text, max_tokens=100, overlap=10)
    assert len(chunks) >= 5

    embs = embed_texts(chunks)
    assert len(embs) == len(chunks)
    assert all(len(e) == 128 for e in embs)

    # determinism check
    e1 = embed_texts([chunks[0]])[0]
    e2 = embed_texts([chunks[0]])[0]
    assert e1 == e2
