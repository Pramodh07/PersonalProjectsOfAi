import os
import sys
from pathlib import Path

# Ensure project root directory is on sys.path for tests so `import src.*` works
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
# add project root (not the inner src folder) so `src` is an importable package
sys.path.insert(0, str(ROOT))

# Use SQLite in-memory for tests to avoid requiring Postgres
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
# Ensure Redis is not required for tests
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/1")

# Create DB tables before tests run
import pytest

# Try to create tables if the DB backend is available; otherwise skip.
try:
    from src import db_init
    DB_AVAILABLE = True
except Exception:
    DB_AVAILABLE = False


@pytest.fixture(scope="session", autouse=True)
def init_db():
    if DB_AVAILABLE:
        try:
            db_init.create_tables()
        except Exception:
            pass
    yield
