# tasks_router

A minimal FastAPI service implementing an async SQLAlchemy + PostgreSQL scaffold for managing tasks and users.

This repository provides a compact, opinionated starting point for building REST APIs with async database access, Alembic migrations, and a layered project structure (routers, services, repositories, models, schemas).

**Key features**
- Async FastAPI application (`tasks_router.main`) using `uvicorn` for development.
- Async SQLAlchemy models and repositories (`tasks_router.models`, `tasks_router.repositories`).
- Alembic migrations configured at the project root (`alembic.ini`, `migrations/`).
- Clear separation: routers, services, repositories, models, schemas.
- Basic test suite (see `tests/`).

Getting started
---------------

Prerequisites
- Python 3.10+ recommended
- PostgreSQL database
- A virtual environment (recommended)

Quickstart (development)
1. Create and activate a virtual environment:

	python -m venv .venv
	source .venv/bin/activate

2. Install dependencies (use your preferred tool; this project uses `pyproject.toml`):

	pip install -r requirements.txt

3. Configure environment variables (example):

	export DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
	export ALEMBIC_INI=alembic.ini

	Note: The project loads configuration from `tasks_router.infrastructure.configurations` — check it for additional settings.

4. Apply database migrations:

	alembic upgrade head

5. Run the app (development):

	uvicorn tasks_router.main:app --reload --host 0.0.0.0 --port 8000

Project structure overview
--------------------------
- `tasks_router/main.py` — FastAPI app factory and entrypoint.
- `tasks_router/routers/` — API route definitions (`task_router.py`, `user_router.py`, `system_router.py`).
- `tasks_router/services/` — Business logic layer (`task_service.py`, `user_service.py`).
- `tasks_router/repositories/` — DB access layer (`task_repo.py`, `user_repo.py`).
- `tasks_router/models/` — SQLAlchemy ORM models (`task_model.py`, `user_model.py`, `base_model.py`).
- `tasks_router/schema/` — Pydantic request/response schemas.
- `tasks_router/infrastructure/` — DB initialization and configuration helpers (`initiate_db.py`, `configurations.py`).
- `migrations/` and `alembic.ini` — Alembic migration environment and versions.
- `tests/` — Test suite (unit + integration-style tests).

Configuration & conventions
-------------------------
- Database connections use SQLAlchemy's async engine with `asyncpg`.
- Migrations: use Alembic from project root; migration scripts are under `migrations/versions`.
- Logging configuration is in `tasks_router/logging_config.py`.

Testing
-------
Run the test suite with `pytest` from the project root. Ensure you have a test database configured (the tests may expect a local dev DB or use fixtures to create temporary DB resources).

Example:

	pytest -q

Notes & next steps
------------------
- Add a `requirements.txt` or ensure `pyproject.toml` contains the exact dependencies for reproducible installs.
- Consider `.env` support or a Docker compose file for local development DB orchestration.
- Add CI pipeline steps to run tests and migrations automatically.

License
-------
This project has no license file included. Add a `LICENSE` if you intend to open-source this repository.

Where to look in the code
-------------------------
- App entry: [tasks_router/main.py](tasks_router/main.py#L1)
- DB init: [tasks_router/infrastructure/initiate_db.py](tasks_router/infrastructure/initiate_db.py#L1)
- Example router: [tasks_router/routers/task_router.py](tasks_router/routers/task_router.py#L1)
- Models: [tasks_router/models/task_model.py](tasks_router/models/task_model.py#L1)

If you'd like, I can:
- Run the test suite and report results.
- Add a `requirements.txt` or update `pyproject.toml` with pinned versions.
- Create a Docker Compose developer environment (Postgres + service).

----
Generated on 2026-05-29.
