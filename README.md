# 🏥 FlowCare Backend

> **Production-grade Queue & Appointment Booking System** built with FastAPI, PostgreSQL, and Clean Architecture principles.

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Tech Stack](#-tech-stack)
- [Architecture](#️-architecture)
- [Prerequisites](#-prerequisites)
- [Setup Instructions](#️-setup-instructions)
  - [Option 1: Docker (Recommended)](#option-1-docker-recommended)
  - [Option 2: Local Development](#option-2-local-development)
- [Environment Variables](#-environment-variables)
- [Database Migrations](#-database-migrations)
- [Seeding the Database](#-seeding-the-database)
- [Running Tests](#-running-tests)
- [API Usage Examples](#-api-usage-examples)
- [API Documentation](#-api-documentation)
- [Makefile Commands](#-makefile-commands)
- [Project Structure](#-project-structure)

---

## 📖 Overview

FlowCare is a backend system for managing appointment bookings and queues across multiple branches. It supports role-based access control (Admin, Branch Manager, Staff, Customer), file uploads via MinIO, background scheduling via APScheduler, and is fully containerized with Docker.

---

## 🚀 Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| ORM | SQLAlchemy 2.0 (Async) |
| Database | PostgreSQL 16 |
| Migrations | Alembic |
| File Storage | MinIO (S3-compatible) |
| Background Jobs | APScheduler |
| Containerization | Docker & Docker Compose |
| Linting / Formatting | Ruff |
| Type Checking | mypy |
| Testing | pytest |

---

## 🏗️ Architecture

FlowCare follows **Clean Architecture / DDD-lite** principles with a clear separation of concerns:

```
app/
├── domain/           # Pure business logic (Entities, Repository Interfaces,Domain Errors)
├── application/      # Use Cases and DTOs
├── infrastructure/   # DB Models, Repository Implementations, Security, Utilities
└── api/              # FastAPI Routes, Pydantic Schemas, Middleware
```

---

## ✅ Prerequisites

Before you begin, make sure you have the following installed:

- **Docker & Docker Compose** (for Docker setup)
- **Python 3.11+** (for local setup)
- **PostgreSQL 16** (for local setup)
- **Git**

---

## ⚙️ Setup Instructions

### Option 1: Docker (Recommended)

This method spins up the API, PostgreSQL, and MinIO all together.

**1. Clone the repository:**
```bash
git clone https://github.com/Source-C0de/FlowCare_Backend.git
cd FlowCare_Backend
```

**2. Configure your environment:**
```bash
cp .env.example .env
```

> ⚠️ **Important:** When using Docker, update these two values in your `.env`:
> ```
> DB_HOST=postgres-db
> MINIO_ENDPOINT=minio:9000
> ```

**3. Build and start all services:**
```bash
make up
# or
docker compose up --build
```

**4. Apply database migrations (first time only):**
```bash
docker exec -it flowcare_api alembic upgrade head
```

**5. Seed the database (Optional):**
Seeding happens **automatically** on application startup. If you need to manually re-seed:
```bash
docker exec -it flowcare_api sh -c "export PYTHONPATH=. && python scripts/seed_db.py"
```

The API will be available at **http://localhost:8000**
Interactive docs: **http://localhost:8000/flowcare/docs**

---

### Option 2: Local Development

**1. Clone the repository:**
```bash
git clone https://github.com/Source-C0de/FlowCare_Backend.git
cd FlowCare_Backend
```

**2. Create and activate a virtual environment:**
```bash
python3.11 -m venv venv
source venv/bin/activate       # Linux / macOS
# venv\Scripts\activate        # Windows
```

**3. Install dependencies:**
```bash
make install
# or
pip install -r requirements.txt
```

**4. Configure your environment:**
```bash
cp .env.example .env
# Edit .env with your local values (DB_HOST=localhost, MINIO_ENDPOINT=localhost:9000)
```

**5. Create the PostgreSQL database:**
```bash
psql -U postgres -c "CREATE DATABASE flowcare_db;"
```

**6. Apply database migrations:**
```bash
make upgrade
```

**7. Seed the database (Optional):**
Seeding happens **automatically** on startup. To manually seed:
```bash
export PYTHONPATH=.
./venv/bin/python3 scripts/seed_db.py
```

**8. Start the development server:**
```bash
make dev
# or
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at **http://localhost:8000**

---

## 🔑 Environment Variables

Create a `.env` file in the project root by copying `.env.example`:

```bash
cp .env.example .env
```

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DB_HOST` | PostgreSQL host (`localhost` or `postgres-db` for Docker) | `localhost` | ✅ |
| `DB_PORT` | PostgreSQL port | `5432` | ✅ |
| `DB_NAME` | Database name | `flowcare_db` | ✅ |
| `DB_USER` | Database user | `postgres` | ✅ |
| `DB_PASSWORD` | Database password | `postgres` | ✅ |
| `JWT_SECRET_KEY` | Secret key for signing JWT tokens | — | ✅ |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token lifetime in minutes | `60` | ✅ |
| `ADMIN_EMAIL` | Default admin account email | `admin@system.com` | ✅ |
| `ADMIN_PASSWORD` | Default admin account password | `Admin@123` | ✅ |
| `ADMIN` | Role ID for Admin | `1` | ✅ |
| `BRANCH_MANAGER` | Role ID for Branch Manager | `2` | ✅ |
| `STAFF` | Role ID for Staff | `3` | ✅ |
| `CUSTOMER` | Role ID for Customer | `4` | ✅ |
| `MINIO_ENDPOINT` | MinIO endpoint (`localhost:9000` or `minio:9000` for Docker) | `localhost:9000` | ✅ |
| `MINIO_ACCESS_KEY` | MinIO access key | `minioadmin` | ✅ |
| `MINIO_SECRET_KEY` | MinIO secret key | `minioadmin` | ✅ |
| `MINIO_BUCKET_NAME` | MinIO bucket for file storage | `flowcare` | ✅ |
| `MINIO_REGION` | MinIO region | `us-east-1` | ✅ |
| `MINIO_SECURE` | Use HTTPS for MinIO | `False` | ✅ |
| `LOG_LEVEL` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) | `INFO` | ❌ |
| `DEBUG` | Enable debug mode | `True` | ❌ |

> 🔐 **Security Note:** Always generate a strong, random `JWT_SECRET_KEY` for production:
> ```bash
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

---

## 🗃️ Database Migrations

FlowCare uses **Alembic** for database schema versioning.

```bash
# Apply all pending migrations
make upgrade

# Create a new migration after model changes
make migration msg="add_user_profile_table"

# Roll back the last migration
make downgrade

# View migration history
make history

# Check current migration state
make current
```

---

### Unified Seed Script
We provide a unified seeding script that populates all core data AND appointment slots for the next 7 days:

```bash
export PYTHONPATH=.
./venv/bin/python3 scripts/seed_db.py
```

This seeds:
- **Roles:** Admin, Branch Manager, Staff, Customer
- **Branches:** Muscat Khuwair, Suhar Humbar (from JSON)
- **Service Types:** e.g., Consultation, Document Verification (from JSON)
- **Staff Assignments:** Links staff to service types
- **Appointment Slots:** Generates fresh slots for the next 7 days for every branch/service.

> 💡 **Automatic Seeding:** The application is configured to run this import automatically on startup via the lifespan event.

---

## 🧪 Running Tests

```bash
make test
# or
pytest -q
```

---

## 📡 API Usage Examples

> **Base URL:** `http://localhost:8000/api/v1`

All protected endpoints require a Bearer token obtained from the login endpoint.

---

### 🔐 Authentication

#### Register a Customer

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: multipart/form-data" \
  -F "email=customer@example.com" \
  -F "password=Password123" \
  -F "phone=+96812345678" \
  -F "id_image=@/path/to/your/id.jpg"
```

**Expected Response (`201 Created`):**
```json
{
  "id": "uuid-here",
  "email": "customer@example.com",
  "role": "CUSTOMER",
  "is_verified": false
}
```

---

#### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "password": "Password123"
  }'
```

**Expected Response (`200 OK`):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

> 💡 Copy the `access_token` and use it as `Authorization: Bearer <token>` in all subsequent requests.

---

### 📅 Appointments

#### Create an Appointment

```bash
curl -X POST http://localhost:8000/api/v1/appointment/create \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: multipart/form-data" \
  -F "branch_id=muscat-central" \
  -F "service_type_id=muscat-gen-cons" \
  -F "slot_id=slot_muscat-central_20240318_0900"
```

**Expected Response (`201 Created`):**
```json
{
  "status": "success",
  "message": "Appointment created successfully",
  "data": {
    "id": "uuid-here",
    "appointment_no": "APPT-ABCD1234",
    "branch_id": "br_muscat_001",
    "service_type_id": "svc_mus_001",
    "staff_id": "1",
    "status": "BOOKED",
    "slot_id": "slot_mus_001_...",
    "attachment_path": null
  }
}
```

---

#### Get My Appointments

```bash
curl -X GET http://localhost:8000/api/v1/appointment/my \
  -H "Authorization: Bearer <your_token>"
```

---

### 👥 Staff Management (Admin / Branch Manager)

#### Assign a Service to Staff

```bash
curl -X POST http://localhost:8000/api/v1/staff/{staff_id}/assign-service \
  -H "Authorization: Bearer <admin_or_manager_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "service_type_id": "service-uuid-here"
  }'
```

**Expected Response (`200 OK`):**
```json
{
  "staff_id": "uuid-here",
  "assigned_service": "General Consultation",
  "message": "Service assigned successfully"
}
```

---

#### Get All Branches

```bash
curl -X GET http://localhost:8000/api/v1/branches \
  -H "Authorization: Bearer <your_token>"
```

---

### 📮 Postman Collection

To explore the full API with Postman:

1. Import the base URL: `http://localhost:8000`
2. Set up an **environment variable** `base_url = http://localhost:8000/api/v1`
3. After login, save the `access_token` to an environment variable `token`
4. Add a header `Authorization: Bearer {{token}}` to all protected requests
5. Interactive API docs are also available at `http://localhost:8000/flowcare/docs` (Swagger UI)

---

## 📖 API Documentation

Once the server is running, interactive documentation is available at:

| Interface | URL |
|-----------|-----|
| Swagger UI | http://localhost:8000/flowcare/docs |
| ReDoc | http://localhost:8000/flowcare/redoc |
| OpenAPI JSON | http://localhost:8000/openapi.json |

---

## 🛠️ Makefile Commands

| Command | Description |
|---------|-------------|
| `make install` | Install Python dependencies |
| `make dev` | Start the development server with hot-reload |
| `make up` | Build and start all Docker services |
| `make down` | Stop and remove Docker containers and volumes |
| `make migration msg="..."` | Auto-generate a new Alembic migration |
| `make upgrade` | Apply all pending migrations |
| `make downgrade` | Roll back the last migration |
| `make history` | Show migration history |
| `make current` | Show the current migration revision |
| `make test` | Run the test suite |
| `make lint` | Run Ruff linter |
| `make format` | Auto-format code with Ruff |
| `make type` | Run mypy type checks |

---

## 📁 Project Structure

```
FlowCare_Backend/
├── app/                  # Application source code
├── alembic/              # Database migration history
├── scripts/              # Unified seeding and utility scripts
├── tests/                # Unit and integration tests
├── .env.example          # Environment variable template
├── docker-compose.yml    # Docker orchestration
├── Dockerfile            # Application image definition
├── alembic.ini           # Alembic configuration
├── Makefile              # Developer shortcuts
├── example.json          # Seed data source
├── pyproject.toml        # Tooling configuration
└── requirements.txt      # Dependency list
```

---

## 🐳 Docker Services

| Service | Container Name | Port |
|---------|---------------|------|
| FastAPI App | `flowcare_api` | `8000` |
| PostgreSQL | `flowcare_db_container` | `5432` |
| MinIO Storage | `flowcare_minio` | `9000` (API), `9001` (Console) |

> 💡 Access the MinIO web console at **http://localhost:9001** with credentials from your `.env` (`MINIO_ACCESS_KEY` / `MINIO_SECRET_KEY`).

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push and open a Pull Request

