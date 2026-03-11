# FlowCare (Queue & Appointment Booking System)

Backend solution for Rihal Codestacker 2026.

Production-grade starter for **FastAPI + Postgres** using **Clean Architecture / DDD-lite**.




## Architecture (DDD-lite)

- `app/domain/`: Pure business logic (entities, repository interfaces, domain errors)
- `app/application/`: Use-cases (orchestrates domain + ports)
- `app/infrastructure/`: Adapters (DB models, repository implementations, external services)
- `app/api/`: FastAPI routers + schemas (delivery layer)
- `app/core/`: Cross-cutting concerns (settings, logging, DB session)


## Current Problems
1. **Broken imports** - `appointment.py` controller imports `AppointmentRepository` from use_cases (wrong)
2. **Typos everywhere** - `appoinment` vs `appointment`, `excute` vs `execute`
3. **SOLID violations**:
   - Use cases instantiate their own repos (violates DIP)
   - Use cases import FastAPI HTTPException (violates SRP - domain leaking into framework)
   - Schemas mixed with DTOs
   - No proper dependency injection
4. **Layer bleeding** - Application layer imports API schemas, Infra layer raises HTTP exceptions
5. **Duplicate Base class** in `db/base.py` and `db/session.py`
6. **Dead code** - `dependencies.py` references undefined symbols, commented out exception handlers
7. **No `__init__.py`** files in many packages



```
app/
├── __init__.py
├── main.py                          # FastAPI app creation
├── config.py                        # Settings (unchanged)
│
├── domain/                          # LAYER 1: Enterprise Business Rules
│   ├── __init__.py
│   ├── entities/                    # Pure domain objects
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── appointment.py
│   ├── exceptions.py                # Domain-level exceptions
│   └── interfaces/                  # Abstract repository contracts (ISP)
│       ├── __init__.py
│       ├── user_repository.py
│       └── appointment_repository.py
│
├── application/                     # LAYER 2: Application Business Rules
│   ├── __init__.py
│   ├── dtos/                        # Data Transfer Objects
│   │   ├── __init__.py
│   │   ├── auth_dto.py
│   │   └── appointment_dto.py
│   └── use_cases/                   # Use cases (SRP - one class per use case)
│       ├── __init__.py
│       ├── register_user.py
│       ├── login_user.py
│       ├── logout_user.py
│       └── book_appointment.py
│
├── infrastructure/                  # LAYER 3: Frameworks & Drivers
│   ├── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── base.py                  # Single Base class
│   │   ├── session.py               # Engine + session factory
│   │   └── connection.py            # Health check
│   ├── models/                      # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── user_model.py
│   │   ├── role_model.py
│   │   ├── appointment_model.py
│   │   ├── branch_model.py
│   │   ├── slot_model.py
│   │   ├── service_type_model.py
│   │   ├── staff_profile_model.py
│   │   ├── staff_service_type_model.py
│   │   ├── customer_profile_model.py
│   │   └── audit_log_model.py
│   ├── repositories/                # Concrete implementations (DIP)
│   │   ├── __init__.py
│   │   ├── user_repository_impl.py
│   │   └── appointment_repository_impl.py
│   └── security/
│       ├── __init__.py
│       ├── hashing.py               # Password hashing (SRP)
│       ├── jwt_handler.py           # JWT create/decode (SRP)
│       └── token_utils.py           # Token hashing
│
└── api/                             # LAYER 4: Interface Adapters
    ├── __init__.py
    ├── dependencies.py              # DI container - repo factories
    ├── middleware/
    │   ├── __init__.py
    │   ├── exception_handlers.py
    │   └── rbac.py
    └── v1/
        ├── __init__.py
        ├── router.py                # All route aggregation
        ├── schemas/                  # Request/Response schemas
        │   ├── __init__.py
        │   ├── user_schemas.py
        │   ├── auth_schemas.py
        │   └── appointment_schemas.py
        └── endpoints/               # Route handlers (thin controllers)
            ├── __init__.py
            ├── health.py
            ├── auth.py
            └── appointment.py
```

## SOLID Principles Applied
- **S** - Each use case is a single class with a single `execute()` method
- **O** - Repository interfaces allow extension without modification
- **L** - All repository implementations are substitutable for their interfaces
- **I** - Separate repository interfaces per domain concept
- **D** - Use cases depend on abstractions (interfaces), not implementations


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
