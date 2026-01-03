import os

try:
    from sqlalchemy import create_engine, MetaData
    from sqlalchemy.orm import sessionmaker

    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/claimsdb")
    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(bind=engine)
    metadata = MetaData()
except Exception:
    # Fall back to no-op session/engine for environments where SQLAlchemy
    # is unavailable or incompatible with Python version (useful for CI/test)
    engine = None
    metadata = None

    class NullSession:
        def execute(self, *args, **kwargs):
            return None

        def commit(self):
            return None

        def close(self):
            return None

    def SessionLocal():
        return NullSession()
