from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class Measurement(Base):
    __tablename__ = "measurements"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    weight_kg: Mapped[float] = mapped_column(nullable=False)
    body_fat_percent: Mapped[float | None] = mapped_column(nullable=True)
    waist_cm: Mapped[float | None] = mapped_column(nullable=True)
    notes: Mapped[str | None] = mapped_column(String(500), nullable=True)
    measured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="measurements")

    __table_args__ = (
        CheckConstraint("weight_kg > 0", name="ck_measurements_weight_kg_positive"),
        CheckConstraint(
            "body_fat_percent IS NULL OR body_fat_percent BETWEEN 1 AND 80",
            name="ck_measurements_body_fat_percent_range",
        ),
        Index("ix_measurements_user_id_measured_at", "user_id", "measured_at"),
    )
