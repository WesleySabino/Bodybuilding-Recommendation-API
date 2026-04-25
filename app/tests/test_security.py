from datetime import timedelta

import pytest

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hashing_and_verification() -> None:
    password = "super-secret-password"

    hashed_password = hash_password(password)

    assert hashed_password != password
    assert verify_password(password, hashed_password)
    assert not verify_password("wrong-password", hashed_password)


def test_access_token_encode_decode_roundtrip() -> None:
    token = create_access_token(
        {"sub": "test-user-id"},
        expires_delta=timedelta(minutes=5),
    )

    payload = decode_access_token(token)

    assert payload["sub"] == "test-user-id"
    assert "exp" in payload


def test_decode_access_token_rejects_invalid_token() -> None:
    with pytest.raises(ValueError, match="Invalid or expired access token"):
        decode_access_token("not-a-valid-token")
