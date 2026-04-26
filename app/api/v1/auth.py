from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import create_access_token, hash_password
from app.schemas.auth import LoginRequest, Token, UserCreate, UserRead
from app.services.auth import authenticate_user
from app.services.users import create_user, get_user_by_email

router = APIRouter()
DbSession = Annotated[Session, Depends(get_db)]


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description=(
        "Creates a user account with a hashed password and returns the created user "
        "resource."
    ),
    responses={
        409: {"description": "Duplicate email (already registered)."},
        422: {
            "description": "Validation error in request payload.",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/HTTPValidationError"}
                }
            },
        },
    },
)
def register_user(payload: UserCreate, db: DbSession) -> UserRead:
    existing_user = get_user_by_email(db, payload.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    return create_user(
        db=db,
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )


@router.post(
    "/login",
    response_model=Token,
    summary="Log in and obtain an access token",
    description="Validates user credentials and returns a bearer JWT access token.",
    responses={
        401: {"description": "Authentication failure (invalid email or password)."},
        422: {
            "description": "Validation error in request payload.",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/HTTPValidationError"}
                }
            },
        },
    },
)
def login(payload: LoginRequest, db: DbSession) -> Token:
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": str(user.id)})
    return Token(access_token=access_token)
