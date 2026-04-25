# High-Level Architecture

## Architectural Style

Use a modular monolith API with feature-based folders. Keep the implementation simple but layered enough for maintainability.

## Suggested Folder Structure

```text
app/
  main.py
  api/
    v1/
      router.py
      auth.py
      users.py
      measurements.py
      recommendations.py
      health.py
  core/
    config.py
    security.py
    dependencies.py
    errors.py
  db/
    session.py
    base.py
    migrations/
  models/
    user.py
    measurement.py
    recommendation.py
  schemas/
    auth.py
    user.py
    measurement.py
    recommendation.py
  services/
    auth_service.py
    user_service.py
    measurement_service.py
    recommendation_service.py
  repositories/
    user_repository.py
    measurement_repository.py
    recommendation_repository.py
  tests/
    conftest.py
    test_auth.py
    test_users.py
    test_measurements.py
    test_recommendations.py
alembic/
Dockerfile
docker-compose.yml
pyproject.toml
README.md
.env.example
```

## Layer Responsibilities

### Routers

- Define API endpoints.
- Parse request schemas.
- Call service layer.
- Return response schemas.
- Should not contain business calculations.

### Schemas

- Define Pydantic request/response models.
- Validate input ranges.
- Shape API responses.

### Services

- Implement business logic.
- Handle recommendation formulas.
- Coordinate repositories.
- Raise domain-specific exceptions.

### Repositories

- Encapsulate database queries.
- Keep SQLAlchemy code out of services where possible.

### Models

- Define SQLAlchemy database tables.
- Keep model logic minimal.

### Core

- App configuration.
- JWT helpers.
- Password hashing.
- Dependency injection.
- Shared errors.

## Request Flow Example

```text
GET /api/v1/recommendations/current
  -> recommendations router
  -> current_user dependency
  -> recommendation service
  -> measurement repository
  -> user repository
  -> formula calculation
  -> optional snapshot persistence
  -> response schema
```

## Security Requirements

- Hash passwords with Argon2id or bcrypt.
- Never log passwords.
- Never return password hashes.
- JWT secret must come from environment variables.
- Protected endpoints must require bearer token.
- All user-scoped queries must filter by `user_id`.

## Configuration

Environment variables:

```text
APP_NAME=Bodybuilding Recommendation API
ENVIRONMENT=development
DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/bodybuilding_api
JWT_SECRET_KEY=change-me
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
PASSWORD_HASH_ALGORITHM=argon2id
```

## Docker Compose Services

```text
api
postgres
```

The API service should depend on PostgreSQL and expose port `8000`.

## Non-Goals

Do not implement:

- Frontend.
- Complex nutrition calculations.
- Workout programming.
- AI recommendations.
- Payments.
- Admin dashboard.
