# API Contract (MVP)

This document defines request/response examples for the MVP endpoints.

Base path: `/api/v1`

## Conventions
- Authentication uses `Authorization: Bearer <access_token>`.
- Timestamps are ISO-8601 UTC.
- IDs are UUIDs.
- Error format may evolve; examples are representative for MVP.

---

## 1) Register

### `POST /api/v1/auth/register`

Request:
```json
{
  "email": "athlete@example.com",
  "password": "Str0ngPass!",
  "full_name": "Alex Carter"
}
```

Success response `201`:
```json
{
  "id": "2d87b6dc-61cf-4cab-982f-6f16a5d7a3af",
  "email": "athlete@example.com",
  "created_at": "2026-04-25T12:00:00Z"
}
```

Error response `409` (email in use):
```json
{
  "detail": "Email already registered"
}
```

---

## 2) Login

### `POST /api/v1/auth/login`

Request:
```json
{
  "email": "athlete@example.com",
  "password": "Str0ngPass!"
}
```

Success response `200`:
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "expires_in": 3600
}
```

Error response `401`:
```json
{
  "detail": "Invalid credentials"
}
```

---

## 3) Get current user

### `GET /api/v1/users/me`

Headers:
- `Authorization: Bearer <access_token>`

Success response `200`:
```json
{
  "id": "2d87b6dc-61cf-4cab-982f-6f16a5d7a3af",
  "email": "athlete@example.com",
  "full_name": "Alex Carter",
  "profile": {
    "sex": "male",
    "birth_date": "1995-03-11",
    "height_cm": 178,
    "training_experience": "intermediate",
    "goal": "fat_loss"
  },
  "created_at": "2026-04-25T12:00:00Z",
  "updated_at": "2026-04-25T12:00:00Z"
}
```

Error response `401`:
```json
{
  "detail": "Not authenticated"
}
```

---

## 4) Update current user profile

### `PATCH /api/v1/users/me`

Headers:
- `Authorization: Bearer <access_token>`

Request (partial updates allowed):
```json
{
  "full_name": "Alex C.",
  "sex": "male",
  "birth_date": "1995-03-11",
  "height_cm": 178,
  "training_experience": "intermediate",
  "goal": "recomposition"
}
```

Success response `200`:
```json
{
  "id": "2d87b6dc-61cf-4cab-982f-6f16a5d7a3af",
  "email": "athlete@example.com",
  "full_name": "Alex C.",
  "profile": {
    "sex": "male",
    "birth_date": "1995-03-11",
    "height_cm": 178,
    "training_experience": "intermediate",
    "goal": "recomposition"
  },
  "updated_at": "2026-04-25T12:10:00Z"
}
```

Validation error `422`:
```json
{
  "detail": [
    {
      "loc": ["body", "height_cm"],
      "msg": "Input should be greater than 0",
      "type": "greater_than"
    }
  ]
}
```

---

## 5) Create measurement

### `POST /api/v1/measurements`

Headers:
- `Authorization: Bearer <access_token>`

Request:
```json
{
  "weight_kg": 84.2,
  "body_fat_pct": 17.5,
  "waist_cm": 87.0,
  "notes": "Morning fasted",
  "measured_at": "2026-04-25T07:00:00Z"
}
```

Success response `201`:
```json
{
  "id": "0f2d6cc4-42c6-4d0e-b969-dc6ea65ddf7d",
  "user_id": "2d87b6dc-61cf-4cab-982f-6f16a5d7a3af",
  "weight_kg": 84.2,
  "body_fat_pct": 17.5,
  "waist_cm": 87.0,
  "notes": "Morning fasted",
  "measured_at": "2026-04-25T07:00:00Z",
  "created_at": "2026-04-25T07:00:01Z"
}
```

---

## 6) List measurements

### `GET /api/v1/measurements`

Headers:
- `Authorization: Bearer <access_token>`

Query params (optional MVP suggestion):
- `limit` (default 30, max 100)
- `offset` (default 0)

Success response `200`:
```json
{
  "items": [
    {
      "id": "0f2d6cc4-42c6-4d0e-b969-dc6ea65ddf7d",
      "weight_kg": 84.2,
      "body_fat_pct": 17.5,
      "waist_cm": 87.0,
      "notes": "Morning fasted",
      "measured_at": "2026-04-25T07:00:00Z"
    },
    {
      "id": "911899b7-af95-44f7-b388-0a70fdca18e2",
      "weight_kg": 84.8,
      "body_fat_pct": 17.9,
      "waist_cm": 87.4,
      "notes": null,
      "measured_at": "2026-04-18T07:00:00Z"
    }
  ],
  "total": 2,
  "limit": 30,
  "offset": 0
}
```

---

## 7) Latest measurement

### `GET /api/v1/measurements/latest`

Headers:
- `Authorization: Bearer <access_token>`

Success response `200`:
```json
{
  "id": "0f2d6cc4-42c6-4d0e-b969-dc6ea65ddf7d",
  "weight_kg": 84.2,
  "body_fat_pct": 17.5,
  "waist_cm": 87.0,
  "notes": "Morning fasted",
  "measured_at": "2026-04-25T07:00:00Z"
}
```

Error response `404`:
```json
{
  "detail": "No measurements found"
}
```

---


## 8) Generate recommendation

### `POST /api/v1/recommendations`

Headers:
- `Authorization: Bearer <access_token>`

Behavior notes (MVP):
- The endpoint computes recommendations on demand and does **not** persist them.
- If the user profile does not exist, returns `400`.
- If no measurements exist, returns `400`.

Success response `200`:
```json
{
  "phase": "cut",
  "calorie_guidance": {
    "direction": "deficit",
    "suggested_percent_adjustment": -15.0,
    "suggested_daily_calorie_delta": -350
  },
  "protein_g_per_kg": 2.2,
  "fat_g_per_kg": 0.8,
  "carbs_guidance": "Fill remaining calories with carbs after protein and fat targets.",
  "rationale": [
    "Fat-loss goal with sufficient body data favors a cut phase.",
    "Recent weight trend is -1.1% across provided check-ins."
  ],
  "warnings": [
    "Body-fat percentage is elevated; avoid aggressive bulking phases."
  ]
}
```

Error response `400` (missing profile):
```json
{
  "detail": "User profile is required before requesting recommendations."
}
```

Error response `400` (missing measurements):
```json
{
  "detail": "At least one measurement is required before requesting recommendations."
}
```

---

## MVP Phase Enum

Allowed `phase` values:
- `cut`
- `lean_bulk`
- `recomp`
- `maintenance`

## Explicit Non-Goals

- No machine learning yet.
- No wearable integration.
- No meal planning.
- No payment/subscription.
- No frontend.

---
