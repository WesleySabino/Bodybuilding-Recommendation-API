# Bodybuilding Recommendation API

Backend-only FastAPI MVP for bodybuilding phase recommendations.

## API overview (MVP)

Base path: `/api/v1`

- `POST /auth/register` — create account.
- `POST /auth/login` — obtain bearer token.
- `GET /users/me` / `PATCH /users/me` — read/update current user profile.
- `POST /measurements`, `GET /measurements`, `GET /measurements/latest` — track progress snapshots.
- `POST /recommendations` — generate deterministic phase/macronutrient guidance.

Interactive OpenAPI docs (after starting the server):
- Swagger UI: `/docs`
- ReDoc: `/redoc`

Documentation:
- API contract: [`docs/api-contract.md`](docs/api-contract.md)
- Common errors: [`docs/errors.md`](docs/errors.md)
- MVP status: [`docs/mvp.md`](docs/mvp.md)

## Requirements

- Docker + Docker Compose
- (Optional) Python 3.12+ for non-Docker local development

## Environment setup

1. Copy the example env file:

```bash
cp .env.example .env
```

2. Update values as needed for your machine.

> `docker-compose.yml` overrides `DATABASE_URL` for the API container so it points to the `postgres` service.

## Local setup (without Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload
```

Health check:

```bash
curl http://localhost:8000/api/v1/health
```

## Docker Compose startup (recommended)

Build images:

```bash
docker compose build
```

Run tests in the API container:

```bash
docker compose run --rm api pytest
```

Start PostgreSQL + API:

```bash
docker compose up --build
```

The API container startup command runs migrations first (`alembic upgrade head`) and only starts Uvicorn if migrations succeed.

Health check after startup:

```bash
curl http://localhost:8000/api/v1/health
```

Stop services:

```bash
docker compose down
```


## Deploy on Render

For a beginner-friendly production path, use Render with Docker.

- Full guide: [`docs/deploy-render.md`](docs/deploy-render.md)
- Blueprint file: [`render.yaml`](render.yaml)

Required production env vars:

- `DATABASE_URL`
- `JWT_SECRET_KEY` (must be strong/random in production)
- `ENVIRONMENT=production`

You can also configure optional vars already supported by the app (for example `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, and `PASSWORD_HASH_ALGORITHM`).

## Deployment smoke test

After deployment, run:

```bash
./scripts/smoke_deploy.sh https://<your-service>.onrender.com
```

With an auth token (optional second arg):

```bash
./scripts/smoke_deploy.sh https://<your-service>.onrender.com "$TOKEN"
```

## Migration commands

Create a new migration:

```bash
alembic revision --autogenerate -m "describe_change"
```

Apply migrations:

```bash
alembic upgrade head
```

Rollback one migration:

```bash
alembic downgrade -1
```

Current migration for MVP schema:

```bash
alembic upgrade 20260425_0001
```

## Test setup

### Local

```bash
pytest
ruff check .
```

### Docker

```bash
docker compose run --rm api pytest
```

## Example curl flow (register → login → update profile → create measurement → recommendation)

Register:

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "demo@example.com",
    "password": "StrongPass123!"
  }'
```

Login and capture token:

```bash
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "demo@example.com",
    "password": "StrongPass123!"
  }' | python -c 'import json,sys; print(json.load(sys.stdin)["access_token"])')
```

Create a measurement:

```bash
curl -X POST http://localhost:8000/api/v1/measurements \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "weight_kg": 82.5,
    "body_fat_percent": 18.0,
    "waist_cm": 89.0,
    "notes": "weekly check-in"
  }'
```

Update profile (required before recommendations):

```bash
curl -X PATCH http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "sex": "male",
    "training_experience": "intermediate",
    "goal": "muscle_gain"
  }'
```

Get recommendation:

```bash
curl -X POST http://localhost:8000/api/v1/recommendations \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{}'
```
