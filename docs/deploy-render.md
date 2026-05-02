# Deploy on Render (Docker + Managed PostgreSQL)

This guide shows the easiest low-risk production path for this API on **Render** using the existing Docker setup. A `render.yaml` blueprint is included at the repo root as a starting point.

## What this app expects at startup

The container entrypoint uses `scripts/start.sh`, which does:

1. `alembic upgrade head` (applies DB migrations)
2. starts the API with Uvicorn (`app.main:app` on port `8000`)

If migrations fail, the app will not start. This is expected and protects schema consistency.

## Prerequisites

- A Render account
- Your code pushed to GitHub
- (Recommended) a strong randomly-generated JWT secret

## Required environment variables

Set these in Render for the web service:

- `DATABASE_URL` (from Render Postgres connection string)
- `JWT_SECRET_KEY` (**must be strong in production**)
- `ENVIRONMENT` (`production` on Render)

Other optional supported variables already in this app:

- `APP_NAME`
- `JWT_ALGORITHM` (default: `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES` (default: `60`)
- `PASSWORD_HASH_ALGORITHM` (default: `argon2id`)

## SQLAlchemy + psycopg URL compatibility note

This app is configured for SQLAlchemy using the **psycopg v3 driver**, so `DATABASE_URL` should use:

- `postgresql+psycopg://...`

If Render provides a URL like `postgres://...` or `postgresql://...`, convert it to `postgresql+psycopg://...` before saving it.

## Deploy from GitHub to Render (step-by-step)

1. In Render, click **New +** → **Blueprint** (recommended) or **Web Service**.
2. Connect your GitHub repo and select this repository.
3. If using Blueprint, Render reads `render.yaml` and proposes:
   - one PostgreSQL database
   - one Docker web service
4. Create/apply the resources.
5. In the web service Environment settings, confirm/set:
   - `ENVIRONMENT=production`
   - `JWT_SECRET_KEY=<strong-random-secret>`
   - `DATABASE_URL` is linked to your Render Postgres database (and uses `postgresql+psycopg://...`).
6. Trigger deploy.
7. Watch logs. You should see migration step first, then Uvicorn startup.

## Provisioning managed PostgreSQL in Render

If not using Blueprint:

1. Render → **New +** → **PostgreSQL**
2. Choose region/plan, create database.
3. Copy the internal/external connection string.
4. Update scheme to `postgresql+psycopg://...` if needed.
5. Add as `DATABASE_URL` in your web service env vars.

## Validate successful deployment

After deploy is live:

- Health check:

```bash
curl -fsS https://<your-service>.onrender.com/api/v1/health
```

- Open Swagger docs in browser:

`https://<your-service>.onrender.com/docs`

## Troubleshooting

### 1) Migration failure at startup

Symptoms: deploy logs stop after migration step or show Alembic/SQL errors.

Checks:
- Confirm DB is reachable from the service.
- Confirm `DATABASE_URL` scheme is `postgresql+psycopg://`.
- Confirm DB user has migration permissions.
- Re-run deploy after fixing env vars.

### 2) Bad `DATABASE_URL`

Symptoms: connection refused, DNS errors, authentication errors.

Checks:
- Host/port/user/password/database are correct.
- URL is complete and properly encoded.
- Scheme is compatible (`postgresql+psycopg://`).

### 3) Weak or missing `JWT_SECRET_KEY`

Symptoms: startup warnings in logs, insecure auth secret.

Fix:
- Set a long random secret (at least 32 chars recommended).
- Redeploy.

### 4) App crash loop

Symptoms: repeated restart/deploy failures.

Checks:
- Review latest deploy logs.
- Verify required env vars are present.
- Confirm migrations succeed.
- Temporarily scale down and redeploy after config correction.

## Rollback / redeploy checklist

1. Keep previous successful deploy ID/version noted.
2. If latest deploy fails, roll back to previous successful deploy in Render.
3. Re-check env vars (`DATABASE_URL`, `JWT_SECRET_KEY`, `ENVIRONMENT`).
4. Confirm DB connectivity.
5. Redeploy once logs and config are clean.
6. Re-run smoke checks:
   - `GET /api/v1/health`
   - open `/docs`
