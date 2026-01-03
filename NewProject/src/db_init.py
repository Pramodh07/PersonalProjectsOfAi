from .db import engine, metadata


def create_tables():
    if engine is None or metadata is None:
        # Skip creating tables when SQLAlchemy is not available
        return
    metadata.create_all(bind=engine)
