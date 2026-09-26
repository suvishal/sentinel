# Sentinel

Cloud-native monitoring and incident investigation platform. The goal is to cut the time engineers spend finding the right log during a production incident.

**Owner's intent:** Vishal is building this to learn backend engineering and to show in interviews. He must be able to explain every line, so:
- Prefer explaining and reviewing over writing large chunks of code. When asked to implement, keep changes small, one concept at a time, and explain the *why*.
- Don't introduce a new library, pattern, or abstraction without saying what it is and why it's needed.
- Don't jump ahead of the roadmap below.

## Current scope (v0.1): receive → store → search → view logs

`Client → FastAPI → PostgreSQL`. See `docs/architecture.md` and `the_idea.md`. Everything else comes later.

## Layout

- `backend/app/main.py`: FastAPI routes (`/`, `/health`, `/version`, `POST/GET /logs`, `PUT/DELETE /logs/{id}`)
- `backend/app/models.py`: SQLAlchemy models (`Log` table: level, service, message, timestamp, request_id)
- `backend/app/schemas.py`: Pydantic v2 schemas (`LogLevel` enum, `LogCreate`, `LogUpdate`, `Log`)
- `backend/app/crud.py`: DB operations; routes call these, never query the DB directly
- `backend/app/database.py`: engine, `SessionLocal`, `Base`, `get_db` dependency; reads `DATABASE_URL` from env
- `alembic/`: migrations (`alembic/env.py` adds `backend/` to `sys.path`)
- `backend/tests/`: pytest + `TestClient`; `conftest.py` overrides `get_db` with a separate test database

## Commands

```bash
# Run everything in Docker (needs .env copied from .env.example)
docker compose up --build

# Tests (from repo root; pytest.ini sets pythonpath=backend)
# Needs a running Postgres and a sentinel_test database
TEST_DATABASE_URL=postgresql://<user>@localhost:5432/sentinel_test pytest

# Migrations (from repo root)
alembic revision --autogenerate -m "<message>"
alembic upgrade head
```

## Conventions

- Adding a field or endpoint touches, in order: `models.py` → Alembic migration → `schemas.py` → `crud.py` → `main.py` → a test in `backend/tests/`. Use the `add-endpoint` skill.
- Every schema change needs an Alembic migration. Never rely on `Base.metadata.create_all` outside tests.
- Every new endpoint or filter gets at least one happy-path test and one validation or 404 test.
- Return proper status codes: 201 on create, 204 on delete, 404 when missing, 422 comes from Pydantic.
- Never commit secrets. `.env` is gitignored; update `.env.example` when you add a variable.
- Commit messages: short imperative prefix, e.g. `feat:`, `fix:`, `test:`, `build:`, `docs:`.

## Known gaps (fix when relevant, ask before large refactors)

- `the_idea.md` still has unresolved merge-conflict markers.
- `crud.create_log` uses `datetime.now()` (naive local time); timestamps should be UTC-aware.
- `alembic.ini` hardcodes a local `sqlalchemy.url`; it should read `DATABASE_URL` from the environment.
- Alembic has no initial migration that creates `logs`: `f12a16fc1aeb` only alters it (`down_revision = None`), so `alembic upgrade head` fails on an empty database.
- `backend/README.md` is empty.
- No CI yet to run tests on PRs.

## Roadmap (don't build ahead of this without asking)

1. Harden v0.1: fix the gaps above, add CI, add more tests.
2. Rule-based anomaly detection over stored logs.
3. AI-driven log analysis (summaries, incident grouping).
4. Frontend (deferred).
