---
name: add-endpoint
description: Add a new API endpoint, filter, or Log field to Sentinel end to end (model, migration, schema, CRUD, route, tests). Use when asked to add or change an endpoint or a column.
---

Add the requested endpoint or field to Sentinel. Work through these steps in order, and after each one explain in 1–2 sentences what changed and why, so Vishal can follow and explain it later.

1. **Clarify the contract first.** State the method, path, request body, query params, response model and status codes. If anything is ambiguous, ask before writing code.
2. **Model** (`backend/app/models.py`): only if the DB shape changes. Say whether the new column is nullable, and whether it needs an index (will it be filtered on?).
3. **Migration**: if the model changed, run `alembic revision --autogenerate -m "<what changed>"`, then read the generated file in `alembic/versions/` and check it matches the intent. Autogenerate misses some things (renames, server defaults).
4. **Schemas** (`backend/app/schemas.py`): Pydantic v2. Add validation with `Field(...)` where the input has limits.
5. **CRUD** (`backend/app/crud.py`): put all DB logic here. Return `None` for "not found" so the route can turn it into a 404.
6. **Route** (`backend/app/main.py`): thin. Validate with `Query(...)` bounds, call CRUD, map `None` to `HTTPException(404)`, and set the right `status_code`.
7. **Tests** (`backend/tests/test_logs.py`, or a new `test_<area>.py`): at least one happy-path test and one failure test (422 validation or 404). Use the existing `client` fixture.
8. **Verify**: run `pytest`. If Postgres isn't available, say so and list exactly what Vishal should run.
9. **Summarize** the change as a short commit message (`feat: ...`) plus a 3-bullet explanation he could give in an interview.
