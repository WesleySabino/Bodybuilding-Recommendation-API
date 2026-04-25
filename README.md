# Bodybuilding Recommendation API

Backend-only FastAPI scaffold for the Bodybuilding Recommendation API MVP.

## Requirements

- Python 3.12+
- Docker and Docker Compose

## Local Setup

Create a virtual environment and install the app with development dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Copy the example environment file if you want local overrides:

```bash
cp .env.example .env
```

Run the API locally:

```bash
uvicorn app.main:app --reload
```

Check the health endpoint:

```bash
curl http://localhost:8000/api/v1/health
```

Expected response:

```json
{"status":"ok"}
```

Interactive API docs are available at:

```text
http://localhost:8000/docs
```

## Docker Compose (Step-by-step)

1. Build and start PostgreSQL + API:

```bash
docker compose up --build -d
```

2. Confirm containers are running:

```bash
docker compose ps
```

3. Smoke test the API:

```bash
curl http://localhost:8000/api/v1/health
```

Expected response:

```json
{"status":"ok"}
```

4. Stop containers when done:

```bash
docker compose down
```

## Tests

Run tests/lint from your local Python environment:

```bash
pytest
ruff check .
```

## Alembic

Alembic is configured for SQLAlchemy and PostgreSQL. The scaffold is ready for the next step: database models and initial migrations.

After models are added, create a migration:

```bash
alembic revision --autogenerate -m "create initial tables"
```

Apply migrations:

```bash
alembic upgrade head
```
