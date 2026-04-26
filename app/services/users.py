from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User, UserProfile


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email))


def create_user(db: Session, email: str, hashed_password: str) -> User:
    user = User(email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_profile(db: Session, user_id: int) -> UserProfile | None:
    return db.scalar(select(UserProfile).where(UserProfile.user_id == user_id).limit(1))


def get_or_upsert_profile(db: Session, user_id: int) -> UserProfile:
    profile = get_user_profile(db, user_id)
    if profile is not None:
        return profile

    profile = UserProfile(user_id=user_id)
    db.add(profile)
    return profile
