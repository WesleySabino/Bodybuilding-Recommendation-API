from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.user import UserMeRead, UserProfileUpdate
from app.services.users import get_or_upsert_profile

router = APIRouter()
DbSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("/me", response_model=UserMeRead, summary="Get current user")
def read_current_user(current_user: CurrentUser) -> UserMeRead:
    return UserMeRead(
        id=current_user.id,
        email=current_user.email,
        profile=current_user.profile,
    )


@router.patch("/me", response_model=UserMeRead, summary="Update current user profile")
def update_current_user_profile(
    payload: UserProfileUpdate,
    db: DbSession,
    current_user: CurrentUser,
) -> UserMeRead:
    profile = get_or_upsert_profile(db, current_user.id)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(current_user)

    return UserMeRead(
        id=current_user.id,
        email=current_user.email,
        profile=current_user.profile,
    )
