#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-}"
TOKEN="${2:-${TOKEN:-}}"

if [[ -z "${BASE_URL}" ]]; then
  echo "Usage: $0 <BASE_URL> [TOKEN]"
  echo "Example: $0 https://your-service.onrender.com"
  exit 1
fi

BASE_URL="${BASE_URL%/}"

echo "[INFO] Running deployment smoke checks against: ${BASE_URL}"

health_code=$(curl -sS -o /tmp/smoke_health_body.json -w "%{http_code}" "${BASE_URL}/api/v1/health")
if [[ "${health_code}" != "200" ]]; then
  echo "[FAIL] Health check failed (HTTP ${health_code}) at /api/v1/health"
  cat /tmp/smoke_health_body.json || true
  exit 1
fi

echo "[PASS] Health check passed: /api/v1/health"

if [[ -n "${TOKEN}" ]]; then
  me_code=$(curl -sS -o /tmp/smoke_me_body.json -w "%{http_code}" \
    -H "Authorization: Bearer ${TOKEN}" \
    "${BASE_URL}/api/v1/users/me")

  if [[ "${me_code}" != "200" ]]; then
    echo "[FAIL] Authenticated check failed (HTTP ${me_code}) at /api/v1/users/me"
    cat /tmp/smoke_me_body.json || true
    exit 1
  fi

  echo "[PASS] Authenticated check passed: /api/v1/users/me"
else
  echo "[INFO] TOKEN not provided; skipping authenticated endpoint check."
fi

echo "[PASS] Smoke deploy checks completed successfully."
