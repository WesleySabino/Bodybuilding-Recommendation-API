from fastapi import Depends
from fastapi.testclient import TestClient

from app.api.deps import get_current_user


def test_register_succeeds(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "new-user@example.com", "password": "strong-password"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] > 0
    assert body["email"] == "new-user@example.com"


def test_duplicate_register_fails(client: TestClient) -> None:
    payload = {"email": "duplicate@example.com", "password": "strong-password"}
    client.post("/api/v1/auth/register", json=payload)

    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 409
    assert response.json() == {"detail": "Email already registered"}


def test_login_succeeds(client: TestClient) -> None:
    register_payload = {"email": "login@example.com", "password": "strong-password"}
    client.post("/api/v1/auth/register", json=register_payload)

    response = client.post("/api/v1/auth/login", json=register_payload)

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert isinstance(body["access_token"], str)
    assert body["access_token"]


def test_login_fails_with_wrong_password(client: TestClient) -> None:
    client.post(
        "/api/v1/auth/register",
        json={"email": "wrong-pass@example.com", "password": "correct-password"},
    )

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "wrong-pass@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid email or password"}


def test_protected_dependency_rejects_invalid_token(client: TestClient) -> None:
    @client.app.get("/api/v1/test-protected")
    def test_protected(_: object = Depends(get_current_user)) -> dict[str, str]:
        return {"status": "ok"}

    response = client.get(
        "/api/v1/test-protected",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}
