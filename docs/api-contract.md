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

Request (MVP allows empty body if server derives from profile + latest measurement):
```json
{}
```

Success response `200`:
```json
{
  "id": "4f38d36a-733e-4f42-9cdc-bf3f51f6de99",
  "user_id": "2d87b6dc-61cf-4cab-982f-6f16a5d7a3af",
  "phase": "cut",
  "calories_guidance": {
    "target_kcal": 2400,
    "strategy": "~15% deficit from estimated maintenance"
  },
  "protein_guidance": {
    "grams": 170,
    "basis": "~2.0 g/kg body weight"
  },
  "fat_guidance": {
    "grams": 70,
    "basis": "~0.8 g/kg body weight"
  },
  "carbs_guidance": {
    "grams": 230,
    "basis": "remaining calories after protein/fat"
  },
  "rationale": [
    "Current profile goal is fat_loss.",
    "Recent trend indicates body weight above desired range for phase goals.",
    "A moderate deficit is selected to preserve training performance."
  ],
  "warnings": [
    "This is educational guidance and not medical advice."
  ],
  "generated_at": "2026-04-25T12:15:00Z"
}
```

Validation error `422` (e.g., missing profile prerequisites):
```json
{
  "detail": "Profile is incomplete: sex, height_cm, and goal are required"
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
