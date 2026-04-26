from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.models.user import User
from app.services.users import get_user_by_email


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None

    return user
