import time
import logging
from ..queue import ParseQueue
from ..parser.pdf_loader import extract_text_from_pdf_bytes
from ..extractor import extract_entities_and_chunks
from ..vector.upsert import upsert_chunks_to_vector_db
from ..validator import validate_entities
from ..adjudicator import adjudicate_claim
from ..audit.logger import audit_event
from minio import Minio
import os

logger = logging.getLogger("parser_worker")

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
BUCKET = os.getenv("BUCKET", "claims")


class ParserWorker:
    def __init__(self):
        self.queue = ParseQueue()
        try:
            self.minio = Minio(MINIO_ENDPOINT, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY, secure=False)
        except Exception:
            self.minio = None

    def process_once(self):
        job = self.queue.pop()
        if not job:
            return None
        ingest_id = job.get("ingest_id")
        object_name = job.get("object")
        audit_event(ingest_id, "parse:start", "parser_worker", {"object": object_name})
        # fetch object from minio (or read local fallback)
        pdf_bytes = None
        if self.minio:
            try:
                resp = self.minio.get_object(BUCKET, object_name)
                pdf_bytes = resp.read()
            except Exception as e:
                logger.exception("failed to read from minio: %s", e)
                # fallback: try local file path if MinIO fails
                try:
                    with open(object_name, "rb") as f:
                        pdf_bytes = f.read()
                except Exception as e2:
                    logger.exception("failed to read local fallback object: %s", e2)
        else:
            # fallback: try local file with object_name path
            try:
                with open(object_name, "rb") as f:
                    pdf_bytes = f.read()
            except Exception as e:
                logger.exception("failed to read local object: %s", e)

        if pdf_bytes is None:
            audit_event(ingest_id, "parse:fail", "parser_worker", {"reason": "missing_object"})
            return None

        pages = extract_text_from_pdf_bytes(pdf_bytes)
        audit_event(ingest_id, "parse:parsed", "parser_worker", {"pages": len(pages)})

        extraction = extract_entities_and_chunks(pages)
        chunks = extraction.get("chunks", [])
        entities = extraction.get("entities", [])

        upserted = upsert_chunks_to_vector_db(chunks)
        audit_event(ingest_id, "vector:upsert", "parser_worker", {"chunks": len(upserted)})

        validation = validate_entities(entities)
        audit_event(ingest_id, "validate:done", "validator", {"results": validation})

        decision = adjudicate_claim(entities, validation)
        audit_event(ingest_id, "adjudicate:done", "adjudicator", {"decision": decision})

        return {
            "ingest_id": ingest_id,
            "pages": len(pages),
            "chunks": len(chunks),
            "entities": len(entities),
            "decision": decision,
        }


if __name__ == "__main__":
    worker = ParserWorker()
    while True:
        res = worker.process_once()
        if res:
            logger.info("Processed job: %s", res)
        time.sleep(1)
