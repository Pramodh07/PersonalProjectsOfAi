from typing import List

# Minimal PDF loader abstraction for PoC

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> List[str]:
    """Return list of page texts. In PoC, a simple placeholder.
    Replace with PyPDFLoader or pdfminer or OCR pipeline for scanned PDFs.
    """
    # TODO: implement real PDF parsing
    return [pdf_bytes.decode(errors='ignore')]
