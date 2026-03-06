# FlowCare (Queue & Appointment Booking System)

Backend solution for Rihal Codestacker 2026.

Production-grade starter for **FastAPI + Postgres** using **Clean Architecture / DDD-lite**.




## Architecture (DDD-lite)

- `app/domain/`: Pure business logic (entities, repository interfaces, domain errors)
- `app/application/`: Use-cases (orchestrates domain + ports)
- `app/infrastructure/`: Adapters (DB models, repository implementations, external services)
- `app/api/`: FastAPI routers + schemas (delivery layer)
- `app/core/`: Cross-cutting concerns (settings, logging, DB session)



## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI 0.111 |
| ORM | SQLAlchemy 2.0 (async) |
| Database | PostgreSQL 16 |
| Migrations | Alembic |
| Auth | HTTP Basic Auth + Passlib/bcrypt |
| File Storage | Local filesystem (MinIO-ready) |
| Background Jobs | APScheduler (cron) |
| Containerisation | Docker + docker-compose |
| Testing | pytest + httpx |

---

## Setup Instructions
### Option A: Docker (Recommended)

**Prerequisites:** Docker Desktop or Docker Engine + docker-compose

## Quick start (local)

1) Create env file:

```bash
# 1. Clone the repository
git clone https://github.com/your-username/flowcare-backend.git
cd flowcare-backend

# 2. Copy and configure environment
cp .env.example .env
# Edit .env if needed (defaults work out-of-the-box with Docker)

# 3. Start all services
docker-compose up --build

# API is now running at:
#   http://localhost:8000
#   Swagger UI: http://localhost:8000/docs
#   ReDoc:      http://localhost:8000/redoc
#   MinIO UI:   http://localhost:9001
```


### Option B: Local Development

**Prerequisites:** Python 3.12+, PostgreSQL 16

```bash
# 1. Clone and enter project
git clone https://github.com/your-username/flowcare-backend.git
cd flowcare-backend

# 2. Create virtual environment
python3.11 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
make install 
    or
pip install -r requirements.txt

# 4. Start PostgreSQL and create database
psql -U postgres -c "CREATE USER flowcare WITH PASSWORD 'flowcare123';"
psql -U postgres -c "CREATE DATABASE flowcare_db OWNER flowcare;"

# 5. Configure environment
cp .env.example .env
# Update DATABASE_URL in .env if your credentials differ

# 6. Run migrations
alembic upgrade head

# 7. Start the server
uvicorn main:app --reload --port 8000
```



## Database Migrations

```bash
# Apply all migrations
alembic upgrade head

# Create a new migration (after model changes)
alembic revision --autogenerate -m "description"

# Rollback one step
alembic downgrade -1

# View current revision
alembic current
```

---


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
pip install -r requirements.txt
uvicorn app.main:app --factory --reload
```

## Migrations

```bash
alembic upgrade head
```
# FlowCare_Backend
