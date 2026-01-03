from typing import List, Dict
from .splitter import split_text_to_chunks

# Simple extractor that returns entities and semantic chunks for a document

def extract_entities_and_chunks(text_pages: List[str]) -> Dict:
    chunks = []
    entities = []
    for i, page in enumerate(text_pages):
        page_chunks = split_text_to_chunks(page, max_tokens=200, overlap=50)
        for idx, chunk in enumerate(page_chunks):
            chunks.append({
                "page": i + 1,
                "chunk_index": idx,
                "text": chunk,
                "tokens": len(chunk.split()),
            })
        # basic entity extraction (PoC)
        if "patient" in page.lower():
            entities.append({"type": "patient", "value": "John Doe", "page": i + 1})
    return {"chunks": chunks, "entities": entities}
