# FlowCare (Queue & Appointment Booking System)

Backend solution for Rihal Codestacker 2026.

Production-grade starter for **FastAPI + Postgres** using **Clean Architecture / DDD-lite**.

## Architecture (DDD-lite)

- `app/domain/`: Pure business logic (entities, repository interfaces, domain errors)
- `app/application/`: Use-cases (orchestrates domain + ports)
- `app/infrastructure/`: Adapters (DB models, repository implementations, external services)
- `app/api/`: FastAPI routers + schemas (delivery layer)
- `app/core/`: Cross-cutting concerns (settings, logging, DB session)

## Quick start (local)

1) Create env file:

```bash
cp .env.dev .env
```

2) Run Postgres + API:

```bash
docker compose up --build
```

API:
- `GET /api/v1/health`
- Docs at `/docs`

## Dev setup (without Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:create_app --factory --reload
```

## Migrations

```bash
alembic upgrade head
```
# FlowCare_Backend
