# MVP Smoke Test Checklist

Use this checklist for a quick post-deploy validation.

## Preconditions

- API is running.
- Database migrations are applied.
- You have `curl` and `python` available.

## 1) Health

```bash
curl -sS http://localhost:8000/api/v1/health
```

Expected: `200 OK`.

## 2) Register

```bash
curl -sS -X POST http://localhost:8000/api/v1/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"smoke@example.com","password":"StrongPass123!"}'
```

Expected: `201 Created` and user payload.

## 3) Login

```bash
TOKEN=$(curl -sS -X POST http://localhost:8000/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"smoke@example.com","password":"StrongPass123!"}' \
  | python -c 'import json,sys;print(json.load(sys.stdin)["access_token"])')
```

Expected: token emitted into `$TOKEN`.

## 4) Profile

```bash
curl -sS -X PATCH http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"sex":"male","training_experience":"intermediate","goal":"muscle_gain"}'
```

Expected: `200 OK` and updated profile.

## 5) Measurement

```bash
curl -sS -X POST http://localhost:8000/api/v1/measurements \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"weight_kg":82.5,"body_fat_percent":17.0,"waist_cm":86.0,"notes":"smoke test"}'
```

Expected: `201 Created` and measurement payload.

## 6) Recommendation

```bash
curl -sS -X POST http://localhost:8000/api/v1/recommendations \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{}'
```

Expected: `200 OK` and recommendation payload containing `phase`.
