Alembic migrations directory (PoC).

This folder will contain Alembic environment and migration scripts.
For the PoC we use a simple create_all migration in `env.py` to create tables
using `src.models.metadata`. Replace with versioned migrations for production.
