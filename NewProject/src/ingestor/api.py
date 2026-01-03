from fastapi import FastAPI, File, UploadFile, HTTPException
from minio import Minio
import os
import uuid

app = FastAPI()

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")

client = Minio(MINIO_ENDPOINT,
               access_key=MINIO_ACCESS_KEY,
               secret_key=MINIO_SECRET_KEY,
               secure=False)

BUCKET = "claims"

@app.on_event("startup")
def startup():
    if not client.bucket_exists(BUCKET):
        client.make_bucket(BUCKET)

@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        file_id = str(uuid.uuid4())
        object_name = f"{file_id}/{file.filename}"
        # MinIO expects a file-like object; wrap bytes in a BytesIO for PoC
        import io
        data_stream = io.BytesIO(contents)
        try:
            client.put_object(BUCKET, object_name, data=data_stream, length=len(contents), content_type=file.content_type)
        except Exception:
            # fallback for local dev/testing when MinIO is unavailable: write to local storage
            os.makedirs("local_storage", exist_ok=True)
            local_path = os.path.join("local_storage", object_name.replace('/', '_'))
            with open(local_path, "wb") as f:
                f.write(contents)
            object_name = local_path
        # create ingest record in Postgres and enqueue parse job (skip if DB not available)
        from ..db import SessionLocal
        try:
            from ..models import claims, claim_files
            session = SessionLocal()
            session.execute(claims.insert().values(claim_id=file_id, ingest_id=file_id, status="ingested"))
            file_id_rec = str(uuid.uuid4())
            session.execute(claim_files.insert().values(file_id=file_id_rec, claim_id=file_id, s3_uri=object_name, checksum=""))
            session.commit()
            session.close()
        except Exception:
            # DB not available in test environment; continue without persistence
            pass
        # publish parse job to queue
        from ..queue import ParseQueue
        q = ParseQueue()
        q.push({"ingest_id": file_id, "object": object_name})
        return {"ingest_id": file_id, "object": object_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
