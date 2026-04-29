from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient


def _register_and_login(client: TestClient, email: str) -> str:
    password = "strong-password"
    client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password},
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    return response.json()["access_token"]


def test_measurements_endpoints_require_authentication(client: TestClient) -> None:
    list_response = client.get("/api/v1/measurements")
    create_response = client.post("/api/v1/measurements", json={"weight_kg": 80})
    latest_response = client.get("/api/v1/measurements/latest")

    assert list_response.status_code == 401
    assert create_response.status_code == 401
    assert latest_response.status_code == 401


def test_create_measurement_succeeds(client: TestClient) -> None:
    token = _register_and_login(client, "measurements-create@example.com")

    response = client.post(
        "/api/v1/measurements",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "weight_kg": 84.3,
            "body_fat_percent": 16.4,
            "waist_cm": 89.2,
            "notes": "Morning check-in",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] > 0
    assert body["user_id"] > 0
    assert body["weight_kg"] == 84.3
    assert body["body_fat_percent"] == 16.4
    assert body["waist_cm"] == 89.2
    assert body["notes"] == "Morning check-in"
    assert body["measured_at"] is not None


def test_create_measurement_invalid_payload_returns_422(client: TestClient) -> None:
    token = _register_and_login(client, "measurements-invalid@example.com")

    response = client.post(
        "/api/v1/measurements",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "weight_kg": 0,
            "body_fat_percent": 95,
            "waist_cm": -1,
        },
    )

    assert response.status_code == 422


def test_listing_measurements_is_scoped_to_current_user(client: TestClient) -> None:
    token_a = _register_and_login(client, "measurements-user-a@example.com")
    token_b = _register_and_login(client, "measurements-user-b@example.com")

    now = datetime.now(timezone.utc)  # noqa: UP017
    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}

    client.post(
        "/api/v1/measurements",
        headers=headers_a,
        json={"weight_kg": 80, "measured_at": (now - timedelta(days=1)).isoformat()},
    )
    client.post(
        "/api/v1/measurements",
        headers=headers_a,
        json={"weight_kg": 81, "measured_at": now.isoformat()},
    )
    client.post(
        "/api/v1/measurements",
        headers=headers_b,
        json={"weight_kg": 95, "measured_at": (now + timedelta(days=1)).isoformat()},
    )

    response = client.get(
        "/api/v1/measurements",
        headers=headers_a,
        params={"limit": 10, "offset": 0},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert body["limit"] == 10
    assert body["offset"] == 0
    measurements = body["items"]
    assert len(measurements) == 2
    assert [entry["weight_kg"] for entry in measurements] == [81.0, 80.0]


def test_latest_measurement_returns_most_recent(client: TestClient) -> None:
    token = _register_and_login(client, "measurements-latest@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    now = datetime.now(timezone.utc)  # noqa: UP017

    client.post(
        "/api/v1/measurements",
        headers=headers,
        json={"weight_kg": 83, "measured_at": (now - timedelta(hours=2)).isoformat()},
    )
    client.post(
        "/api/v1/measurements",
        headers=headers,
        json={"weight_kg": 82.5, "measured_at": now.isoformat()},
    )

    response = client.get("/api/v1/measurements/latest", headers=headers)

    assert response.status_code == 200
    assert response.json()["weight_kg"] == 82.5


def test_latest_measurement_returns_404_when_absent(client: TestClient) -> None:
    token = _register_and_login(client, "measurements-latest-none@example.com")

    response = client.get(
        "/api/v1/measurements/latest",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "No measurements found"}
