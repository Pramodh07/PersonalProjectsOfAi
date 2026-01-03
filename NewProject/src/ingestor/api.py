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
        client.put_object(BUCKET, object_name, data=contents, length=len(contents), content_type=file.content_type)
        # TODO: create ingest record in Postgres and enqueue parse job
        return {"ingest_id": file_id, "object": object_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
