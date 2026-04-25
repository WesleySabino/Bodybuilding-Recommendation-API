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

### Run the same checks with Docker + uv (Python 3.12)

If you prefer not to install Python/uv locally, use the official `uv` Docker image:

1. Sync dependencies (including dev extras):

```bash
docker run --rm \
  -v "$PWD":/workspace \
  -w /workspace \
  ghcr.io/astral-sh/uv:python3.12-bookworm \
  uv sync --extra dev
```

2. Run tests:

```bash
docker run --rm \
  -v "$PWD":/workspace \
  -w /workspace \
  ghcr.io/astral-sh/uv:python3.12-bookworm \
  uv run --python 3.12 pytest
```

3. Run lint:

```bash
docker run --rm \
  -v "$PWD":/workspace \
  -w /workspace \
  ghcr.io/astral-sh/uv:python3.12-bookworm \
  uv run --python 3.12 ruff check .
```


## Step-by-step: Test Ruff with Docker

Use this flow when you want lint results without relying on your local Python install.

1. From the repo root, pull (or let Docker pull) the uv image:

```bash
docker pull ghcr.io/astral-sh/uv:python3.12-bookworm
```

2. Install project dependencies (including dev tools like Ruff) inside the container:

```bash
docker run --rm \
  -v "$PWD":/workspace \
  -w /workspace \
  ghcr.io/astral-sh/uv:python3.12-bookworm \
  uv sync --extra dev
```

3. Run Ruff checks:

```bash
docker run --rm \
  -v "$PWD":/workspace \
  -w /workspace \
  ghcr.io/astral-sh/uv:python3.12-bookworm \
  uv run --python 3.12 ruff check .
```

4. (Optional) Auto-fix what Ruff can fix safely, then re-run checks:

```bash
docker run --rm \
  -v "$PWD":/workspace \
  -w /workspace \
  ghcr.io/astral-sh/uv:python3.12-bookworm \
  uv run --python 3.12 ruff check . --fix
```

5. If the previous command changed files, verify clean lint output by running Step 3 again.

A successful run ends with output similar to:

```text
All checks passed!
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
