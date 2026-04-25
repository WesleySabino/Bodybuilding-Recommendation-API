# Codex Implementation Plan

Use this document to drive implementation step by step. Complete each step before moving to the next.

## Step 1 — Create Project Skeleton

Prompt:

```text
Create a FastAPI backend project for a bodybuilding recommendation API.

Use:
- Python 3.12+
- FastAPI
- SQLAlchemy 2.x
- Alembic
- PostgreSQL
- Pydantic v2
- pytest
- Docker Compose

Create the folder structure described in specs/05-architecture.md.
Add a health endpoint at GET /api/v1/health.
Add .env.example, Dockerfile, docker-compose.yml, pyproject.toml, and README.md.
Do not implement business logic yet.
```

Acceptance criteria:

```text
docker compose up starts the app
GET /api/v1/health returns 200
/docs loads successfully
```

## Step 2 — Database and Migrations

Prompt:

```text
Implement database setup using SQLAlchemy and Alembic.

Create SQLAlchemy models for:
- users
- weight_entries
- waist_entries
- recommendation_snapshots

Follow specs/04-data-model.md exactly.
Create the initial Alembic migration.
Add database session dependency.
```

Acceptance criteria:

```text
alembic upgrade head succeeds
all tables and indexes are created
```

## Step 3 — Auth

Prompt:

```text
Implement registration and login.

Follow specs/01-functional-requirements.md and specs/03-api-contract.md.
Use JWT bearer auth.
Hash passwords with Argon2id or bcrypt.
Never expose password_hash.
Add tests for auth behavior.
```

Acceptance criteria:

```text
user can register
user can login
JWT protects private endpoints
auth tests pass
```

## Step 4 — User Profile

Prompt:

```text
Implement authenticated user profile endpoints:
- GET /api/v1/users/me
- PATCH /api/v1/users/me/profile

Allow updating sex and height_cm.
Validate height_cm and sex.
Add tests.
```

Acceptance criteria:

```text
authenticated user can view and update profile
invalid values are rejected
unauthenticated requests fail
```

## Step 5 — Measurements

Prompt:

```text
Implement measurement endpoints:
- POST /api/v1/measurements/weight
- GET /api/v1/measurements/weight
- POST /api/v1/measurements/waist
- GET /api/v1/measurements/waist

Follow specs/01-functional-requirements.md and specs/03-api-contract.md.
Ensure entries are scoped to the authenticated user.
Prevent duplicate entries for the same user and date.
Add tests.
```

Acceptance criteria:

```text
users can create and list their own measurements
duplicate same-day entries are rejected
cross-user data leakage is impossible
measurement tests pass
```

## Step 6 — Recommendation Engine

Prompt:

```text
Implement the recommendation engine according to specs/02-domain-formulas.md.

Create pure calculation functions where possible.
Implement:
- BMI
- waist-to-height ratio
- 7-day average weight windows
- weekly weight change percentage
- waist change
- recommendation decision logic
- confidence logic
- feedback generation

Expose GET /api/v1/recommendations/current.
Persist recommendation snapshots if the snapshot model exists.
Add full unit and API tests.
```

Acceptance criteria:

```text
all formula unit tests pass
all recommendation branch tests pass
GET /recommendations/current returns expected response
missing required data returns useful errors
```

## Step 7 — Recommendation History

Prompt:

```text
Implement GET /api/v1/recommendations/history.

Return paginated recommendation snapshots for the authenticated user only.
Order by created_at descending.
Add tests.
```

Acceptance criteria:

```text
history returns only the current user's snapshots
pagination works
history tests pass
```

## Step 8 — Final Quality Pass

Prompt:

```text
Review the entire project for consistency and MVP readiness.

Add or improve:
- README setup instructions
- README API examples with curl
- OpenAPI tags
- consistent error handling
- test coverage
- type hints
- linting configuration

Do not add frontend code.
Do not expand scope beyond the MVP specs.
```

Acceptance criteria:

```text
pytest passes
linting passes
docker compose up works
README is sufficient for a new developer
```
