from typing import List, Dict

# Simple extractor that returns mock entities and chunks for a document

def extract_entities_and_chunks(text_pages: List[str]) -> Dict:
    chunks = []
    entities = []
    for i, page in enumerate(text_pages):
        chunks.append({
            "page": i+1,
            "text": page[:1000],
            "tokens": len(page.split())
        })
        # mock entity extraction
        if "patient" in page.lower():
            entities.append({"type": "patient", "value": "John Doe", "page": i+1})
    return {"chunks": chunks, "entities": entities}
