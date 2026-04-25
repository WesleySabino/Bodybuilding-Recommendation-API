from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.models import Measurement, User, UserProfile  # noqa: E402,F401
