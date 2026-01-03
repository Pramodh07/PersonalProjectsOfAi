from typing import List

def split_text_to_chunks(text: str, max_tokens: int = 200, overlap: int = 50) -> List[str]:
    """Simple whitespace token-based splitter with overlap.

    Args:
        text: input text
        max_tokens: max tokens per chunk
        overlap: number of tokens to overlap between chunks

    Returns:
        list of chunk strings
    """
    tokens = text.split()
    if not tokens:
        return []
    chunks = []
    start = 0
    while start < len(tokens):
        end = min(len(tokens), start + max_tokens)
        chunk_tokens = tokens[start:end]
        chunks.append(" ".join(chunk_tokens))
        if end == len(tokens):
            break
        start = max(0, end - overlap)
    return chunks
