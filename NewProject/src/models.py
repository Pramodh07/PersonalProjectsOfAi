from sqlalchemy import Table, Column, String, Integer, Float, DateTime, MetaData
from sqlalchemy.sql import func

metadata = MetaData()

claims = Table(
    "claims",
    metadata,
    Column("claim_id", String, primary_key=True),
    Column("ingest_id", String, nullable=False),
    Column("status", String, default="ingested"),
    Column("created_at", DateTime(timezone=True), server_default=func.now())
)

claim_files = Table(
    "claim_files",
    metadata,
    Column("file_id", String, primary_key=True),
    Column("claim_id", String),
    Column("s3_uri", String),
    Column("checksum", String),
)
