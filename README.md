# Employee Management REST API

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Auth](https://img.shields.io/badge/Auth-JWT%20Bearer-black)

REST API for departments and employees. Register, log in with JWT, then manage staff records. Delete employee is **ADMIN** only.

---

## Overview

Use this backend to:

- Register users and issue JWT access tokens
- Create and list departments
- Create, read, update, and delete employees
- Filter employees by name, department, and salary, with pagination

Stack: **FastAPI** + **PostgreSQL** + **SQLAlchemy**. Passwords are bcrypt hashes. Protected routes need `Authorization: Bearer <token>`.

---

## Tech Stack

| | |
| --- | --- |
| Language | Python |
| API | FastAPI + Uvicorn |
| Database | PostgreSQL (`psycopg`) |
| ORM / migrations | SQLAlchemy, Alembic |
| Schemas | Pydantic |
| Auth | JWT (`python-jose`), HTTP Bearer |
| Passwords | bcrypt |
| Config | `python-dotenv` |
| Middleware | Request logging |
| Tests | Pytest + `TestClient` (SQLite) |

No `requirements.txt` in this repo. Install packages listed under Setup.

---

## Project Structure

```text
employee-management-fastapi/
├── alembic.ini / alembic/     # Migrations (env.py uses DATABASE_URL)
├── app/
│   ├── main.py                # App, create_all(), routers, middleware
│   ├── core/config.py         # Settings, hash helpers, JWT
│   ├── database/session.py    # Engine, Session, get_db()
│   ├── models/                # User, Department, Employee tables
│   ├── schemas/               # Pydantic request/response models
│   ├── routes/                # /auth, /departments, /employees
│   ├── controllers/           # Thin layer over services
│   ├── services/              # Business logic
│   ├── dependencies/          # get_current_user, require_admin
│   └── middleware/            # Request logging
├── tests/                     # Auth + employee tests
├── .env.example
├── README.md
└── FUNDAMENTALS.md
```

Flow: **route → controller → service → model**.

---

## Installation / Setup

**Need:** Python 3.10+, PostgreSQL, Git.

```bash
git clone <repository-url>
cd employee-management-fastapi
```

```bash
python -m venv venv
# Windows: .\venv\Scripts\Activate.ps1
# macOS/Linux: source venv/bin/activate
```

```bash
pip install fastapi uvicorn sqlalchemy psycopg python-dotenv "python-jose[cryptography]" bcrypt pydantic[email] alembic pytest httpx
```

Copy env values into `.env` (see below). Do not commit `.env`.

---

## Environment Variables

Read by `app/core/config.py`:

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `DATABASE_URL` | Yes | — | e.g. `postgresql+psycopg://username:password@localhost:5432/employee_db` |
| `SECRET_KEY` | Yes | — | JWT signing secret |
| `ALGORITHM` | No | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `30` | Token lifetime |

`.env.example` uses `JWT_SECRET_KEY` / `JWT_ALGORITHM`. The **app reads `SECRET_KEY` and `ALGORITHM`**. Use these names in `.env`:

```env
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/employee_db
SECRET_KEY=replace_with_a_long_random_string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Database Setup & Migrations

```sql
CREATE DATABASE employee_db;
```

On startup, `main.py` runs `Base.metadata.create_all()` and creates `users`, `departments`, and `employees` if they are missing.

Alembic is configured in `alembic/env.py`. Optional:

```bash
alembic upgrade head
alembic revision --autogenerate -m "describe_change"
```

The initial revision is empty (`pass`). Fresh installs rely on `create_all()`. There is **no seed script** — register the first user via `POST /auth/register`. Use `role: "ADMIN"` if you need delete access.

---

## How to Run

From the project root, venv active:

```bash
# Development
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Production-style (no reload; set env vars on the host)
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

`GET /` → `{ "message": "Employee Management API is running! Go to /docs for Swagger UI." }`

No Docker or extra production build in this repo.

---

## API Documentation

| | |
| --- | --- |
| Swagger | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |
| OpenAPI | http://127.0.0.1:8000/openapi.json |

### Endpoints

| Method | Path | Auth | Notes |
| --- | --- | --- | --- |
| `GET` | `/` | Public | Health check |
| `POST` | `/auth/register` | Public | `201` — `name`, `email`, `password`, optional `role` (default `USER`). Duplicate email → `409` |
| `POST` | `/auth/login` | Public | `200` — returns JWT. Bad credentials → `401` |
| `GET` | `/auth/me` | Bearer | Current user |
| `POST` | `/departments/` | Bearer | `201` — `{ "name" }`. Duplicate → `409` |
| `GET` | `/departments/` | Bearer | List departments |
| `GET` | `/departments/{id}/employees` | Bearer | `404` if department missing |
| `POST` | `/employees/` | Bearer | `201` — `name`, `email`, `salary` (> 0), `department_id`. Bad dept → `400`, duplicate email → `409` |
| `GET` | `/employees/` | Bearer | Query: `search`, `department`, `min_salary`, `max_salary`, `page` (default 1), `limit` (default 10, max 100) |
| `GET` | `/employees/{id}` | Bearer | `404` if missing |
| `PUT` | `/employees/{id}` | Bearer | Full update (`EmployeeCreate`) |
| `PATCH` | `/employees/{id}` | Bearer | Partial update (`EmployeeUpdate`) |
| `DELETE` | `/employees/{id}` | **ADMIN** | Non-admin → `403` |

---

## Authentication

1. **Register** — `POST /auth/register`. Password hashed with bcrypt; never returned in JSON.
2. **Login** — `POST /auth/login`. Returns `{ "access_token", "token_type": "bearer" }`.
3. **Call APIs** — `Authorization: Bearer <token>`.
4. **Who am I** — `GET /auth/me`. Invalid token → `401`.
5. **Admin** — `DELETE /employees/{id}` uses `require_admin`. Role must be `ADMIN` or you get `403`.

JWT claims: `sub` (email), `role`, `id`, `exp`.

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"ada@example.com\",\"password\":\"changeme\"}"

curl http://127.0.0.1:8000/employees/ \
  -H "Authorization: Bearer <access_token>"
```

In Swagger, click **Authorize** and paste the token.

---

## How to Run Tests

Pytest uses SQLite (`tests/conftest.py`). PostgreSQL is not required.

```bash
pytest
pytest -v
pytest tests/test_auth.py
pytest tests/test_employees.py
```

| File | Coverage |
| --- | --- |
| `tests/test_auth.py` | Register, login, invalid password, duplicate email |
| `tests/test_employees.py` | 401 without token; department and employee flows with Bearer |
