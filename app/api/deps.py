from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db as _get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_db() -> Generator[Session, None, None]:
    yield from _get_db()


DbSession = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(
    db: DbSession,
    token: TokenDep,
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
    except ValueError as exc:
        raise credentials_exception from exc

    subject = payload.get("sub")
    if not subject:
        raise credentials_exception

    try:
        user_id = int(subject)
    except (TypeError, ValueError) as exc:
        raise credentials_exception from exc

    user = db.get(User, user_id)
    if not user:
        raise credentials_exception

    return user
