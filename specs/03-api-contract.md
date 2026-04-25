# API Contract

Base path:

```text
/api/v1
```

Authentication:

```text
Authorization: Bearer <access_token>
```

## Health

### GET /health

Response `200`:

```json
{
  "status": "ok"
}
```

## Auth

### POST /auth/register

Request:

```json
{
  "name": "john",
  "password": "strong-password"
}
```

Response `201`:

```json
{
  "id": "uuid",
  "name": "john",
  "sex": "unspecified",
  "height_cm": null,
  "created_at": "2026-04-24T12:00:00Z"
}
```

Errors:

- `409` if name already exists.
- `422` if request validation fails.

### POST /auth/login

Request:

```json
{
  "name": "john",
  "password": "strong-password"
}
```

Response `200`:

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer"
}
```

Errors:

- `401` if credentials are invalid.

## Users

### GET /users/me

Response `200`:

```json
{
  "id": "uuid",
  "name": "john",
  "sex": "male",
  "height_cm": 180.0,
  "created_at": "2026-04-24T12:00:00Z",
  "updated_at": "2026-04-24T12:00:00Z"
}
```

### PATCH /users/me/profile

Request:

```json
{
  "sex": "male",
  "height_cm": 180.0
}
```

Response `200`:

```json
{
  "id": "uuid",
  "name": "john",
  "sex": "male",
  "height_cm": 180.0,
  "created_at": "2026-04-24T12:00:00Z",
  "updated_at": "2026-04-24T12:10:00Z"
}
```

## Measurements

### POST /measurements/weight

Request:

```json
{
  "weight_kg": 82.4,
  "entry_date": "2026-04-24"
}
```

Response `201`:

```json
{
  "id": "uuid",
  "weight_kg": 82.4,
  "entry_date": "2026-04-24",
  "created_at": "2026-04-24T12:00:00Z"
}
```

Errors:

- `409` if user already has a weight entry for that date.

### GET /measurements/weight

Optional query parameters:

```text
from_date=2026-04-01
to_date=2026-04-24
limit=100
offset=0
```

Response `200`:

```json
{
  "items": [
    {
      "id": "uuid",
      "weight_kg": 82.4,
      "entry_date": "2026-04-24",
      "created_at": "2026-04-24T12:00:00Z"
    }
  ],
  "total": 1
}
```

### POST /measurements/waist

Request:

```json
{
  "waist_cm": 84.0,
  "entry_date": "2026-04-24"
}
```

Response `201`:

```json
{
  "id": "uuid",
  "waist_cm": 84.0,
  "entry_date": "2026-04-24",
  "created_at": "2026-04-24T12:00:00Z"
}
```

Errors:

- `409` if user already has a waist entry for that date.

### GET /measurements/waist

Optional query parameters:

```text
from_date=2026-04-01
to_date=2026-04-24
limit=100
offset=0
```

Response `200`:

```json
{
  "items": [
    {
      "id": "uuid",
      "waist_cm": 84.0,
      "entry_date": "2026-04-24",
      "created_at": "2026-04-24T12:00:00Z"
    }
  ],
  "total": 1
}
```

## Recommendations

### GET /recommendations/current

Response `200`:

```json
{
  "bmi": 25.43,
  "waist_to_height_ratio": 0.467,
  "weekly_weight_change_pct": 0.18,
  "waist_change_cm": 0.2,
  "recommendation": "maintain_or_recomposition",
  "confidence": "high",
  "explanation": "BMI is above the lean-bulk range, but waist-to-height ratio is below 0.50. A maintenance or recomposition phase is recommended until trend data supports a clearer direction.",
  "feedback": [
    "Current weekly weight change is close to maintenance."
  ],
  "calculated_at": "2026-04-24T12:00:00Z"
}
```

Errors:

- `400` if height is missing.
- `400` if no weight entry exists.
