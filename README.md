# FlowCare (Queue & Appointment Booking System)

Backend solution for FlowCare — a production-grade **FastAPI + Postgres** system using **Clean Architecture / DDD-lite**.

---

## 🚀 Tech Stack

- **Framework:** FastAPI
- **ORM:** SQLAlchemy 2.0 (Async)
- **Database:** PostgreSQL 16
- **Migrations:** Alembic
- **Storage:** MinIO (compatible with S3)
- **Background Jobs:** APScheduler
- **Containerization:** Docker & Docker Compose

---

## 🏗️ Architecture (Clean Architecture)

- `app/domain/`: Pure business logic (Entities, Repository Interfaces, Domain Errors).
- `app/application/`: Application logic (Use Cases, DTOs).
- `app/infrastructure/`: Outside world (DB Models, Repository Implementations, Security, Utilities).
- `app/api/`: Interface Adapters (FastAPI Routes, Pydantic Schemas, Middleware).

---

## 🛠️ Setup Instructions

### Option 1: Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Source-C0de/FlowCare_Backend.git
   cd FlowCare_Backend
   ```

2. **Configure Environment:**
   ```bash
   cp .env.example .env
   # IMPORTANT: When using Docker, set:
   # DB_HOST=postgres-db
   # MINIO_ENDPOINT=minio:9000
   ```

3. **Start Services:**
   ```bash
   make up
   # or
   docker compose up --build
   ```

### Option 2: Local Development

1. **Create Virtual Environment:**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies:**
   ```bash
   make install
   ```

3. **Database Setup:**
   Ensure PostgreSQL is running and create the database:
   ```bash
   psql -U postgres -c "CREATE DATABASE flowcare_db;"
   ```

4. **Run Migrations:**
   ```bash
   make upgrade
   ```

5. **Start Dev Server:**
   ```bash
   make dev
   ```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=flowcare_db

# Security
JWT_SECRET_KEY=your_super_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Role IDs (Matching database seed)
ADMIN=1
BRANCH_MANAGER=2
STAFF=3
CUSTOMER=4

# MinIO Storage
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=flowcare
MINIO_REGION=us-east-1
MINIO_SECURE=False
```

---

## 🧬 Database & Seeding

### Migrations
- **Create Migration:** `make migration msg="feat_add_new_table"`
- **Apply Migration:** `make upgrade`
- **Rollback:** `make downgrade`

### Seeding Data
We provide scripts to populate the database with roles, branches, service types, and initial staff:

1. **Seed Core Data (Roles, Branches, Services, Staff):**
   ```bash
   export PYTHONPATH=.
   ./venv/bin/python3 scripts/seed_db.py
   ```

2. **Seed Appointment Slots:**
   ```bash
   ./venv/bin/python3 seed/seed_slots.py
   ```

---

## 📡 API Examples

### 1. Register a Customer
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: multipart/form-data" \
  -F "email=customer@example.com" \
  -F "password=Password123" \
  -F "phone=+96812345678" \
  -F "id_image=@/path/to/your/id.jpg"
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "password": "Password123"
  }'
```

### 3. Assign Service to Staff (Admin/Manager)
```bash
curl -X POST http://localhost:8000/api/v1/staff/{staff_id}/assign-service \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "service_type_id": "service_uuid_here"
  }'
```

### 4. Create Appointment
```bash
curl -X POST http://localhost:8000/api/v1/appointment/create \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: multipart/form-data" \
  -F "branch_id=muscat-central" \
  -F "service_type_id=muscat-gen-cons" \
  -F "slot_id=slot_muscat-central_20240318_0900"
```

---

## 📖 Documentation
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
