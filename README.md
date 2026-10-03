# Sentinel

**A monitoring and incident-investigation backend, built to cut the time engineers spend finding the right log during a production incident.**

Production incidents generate a lot of logs, and finding the one that matters is slow. The longer an investigation takes, the longer production stays impacted. I've seen this firsthand supporting enterprise storage platforms at Hitachi Vantara. Sentinel is my attempt to understand how monitoring systems work by building one from scratch.

> **Status: v0.1 (in progress).** Receive → store → search → view logs. See the [roadmap](#roadmap) and [known limitations](#known-limitations).

---

## Features

- **Ingest logs** over a REST API with validated input (level, service, message)
- **Search and filter** by level, service, free-text message search, time range and request ID
- **Paginate** results with `limit` / `offset`
- **Update and delete** individual log entries
- **Health and version endpoints** for basic observability
- **Containerized**: API + PostgreSQL run together with Docker Compose
- **Schema migrations** with Alembic
- **Tests** with pytest against a separate test database

## Architecture

```
Client  ──HTTP──▶  FastAPI (routes)  ──▶  CRUD layer  ──▶  SQLAlchemy  ──▶  PostgreSQL
                        │
                  Pydantic schemas
                  (request/response validation)
```

The code is layered so each part has one job:

| Layer | File | Responsibility |
|---|---|---|
| Routes | `backend/app/main.py` | HTTP endpoints and status codes |
| Schemas | `backend/app/schemas.py` | Pydantic v2 models that validate input and shape output |
| CRUD | `backend/app/crud.py` | All database reads and writes. Routes never query the DB directly |
| Models | `backend/app/models.py` | SQLAlchemy `Log` table (indexed on `id` and `request_id`) |
| Database | `backend/app/database.py` | Engine, sessions, and the `get_db` dependency (injected per request) |

## Tech stack

Python 3.12 · FastAPI · Pydantic v2 · SQLAlchemy 2.0 · PostgreSQL · Alembic · pytest · Docker / Docker Compose

## API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/version` | API version |
| `POST` | `/logs` | Create a log entry (returns `201`) |
| `GET` | `/logs` | List logs with filters and pagination |
| `PUT` | `/logs/{id}` | Update a log entry (`404` if missing) |
| `DELETE` | `/logs/{id}` | Delete a log entry (`204`, or `404` if missing) |

**`GET /logs` query parameters:** `level` (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`), `service`, `search`, `start_time`, `end_time`, `request_id`, `limit` (1–100, default 25), `offset` (default 0).

Interactive docs are available at `http://localhost:8000/docs` once the API is running.

### Example

```bash
# Create a log
curl -X POST http://localhost:8000/logs \
  -H "Content-Type: application/json" \
  -d '{"level": "ERROR", "service": "payments", "message": "Timeout connecting to database"}'
```

```json
{
  "level": "ERROR",
  "service": "payments",
  "message": "Timeout connecting to database",
  "id": 1,
  "timestamp": "2026-10-03T09:30:00",
  "request_id": "3f2b8c1e-..."
}
```

```bash
# Find all ERROR logs from the payments service that mention "timeout"
curl "http://localhost:8000/logs?level=ERROR&service=payments&search=timeout"
```

Each log gets a server-generated `request_id` (UUID), so a single event can be traced directly.

## Running locally

**Prerequisites:** Docker and Docker Compose.

```bash
git clone https://github.com/suvishal/sentinel.git
cd sentinel
cp .env.example .env        # then set your own POSTGRES_PASSWORD and DATABASE_URL
docker compose up --build
```

The API starts on `http://localhost:8000` once PostgreSQL passes its health check.

> **Note:** The `logs` table isn't created automatically on a fresh database yet (see [known limitations](#known-limitations)).

## Running tests

Tests use FastAPI's `TestClient` and override the `get_db` dependency to point at a separate test database, which is reset before each test.

```bash
pip install -r backend/requirements.txt
createdb sentinel_test
TEST_DATABASE_URL=postgresql://<user>@localhost:5432/sentinel_test pytest
```

## Project structure

```
sentinel/
├── backend/
│   ├── app/
│   │   ├── main.py          # API routes
│   │   ├── schemas.py       # Pydantic request/response models
│   │   ├── crud.py          # Database operations
│   │   ├── models.py        # SQLAlchemy models
│   │   └── database.py      # Engine, sessions, get_db dependency
│   ├── tests/               # pytest suite
│   └── requirements.txt
├── alembic/                 # Database migrations
├── docs/architecture.md
├── Dockerfile
└── docker-compose.yml
```

## Roadmap

1. **Harden v0.1:** fix the known limitations below, add CI, and expand test coverage
2. **Rule-based anomaly detection** over stored logs
3. **AI-driven log analysis:** incident summaries and grouping related logs
4. **Frontend** (deferred)

## Known limitations

These are tracked and will be fixed as part of hardening v0.1:

- Alembic has no initial migration that creates the `logs` table, so `alembic upgrade head` fails on an empty database
- `alembic.ini` uses a hardcoded local database URL instead of reading `DATABASE_URL`
- Timestamps use naive local time and should be timezone-aware UTC
- No CI pipeline runs the tests on pull requests yet

## License

[MIT](LICENSE)
