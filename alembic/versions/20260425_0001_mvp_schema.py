"""add mvp schema

Revision ID: 20260425_0001
Revises:
Create Date: 2026-04-25 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260425_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "user_profiles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("sex", sa.String(length=50), nullable=True),
        sa.Column("birth_date", sa.Date(), nullable=True),
        sa.Column("height_cm", sa.Float(), nullable=True),
        sa.Column("training_experience", sa.String(length=20), nullable=True),
        sa.Column("goal", sa.String(length=20), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "goal IS NULL OR goal IN ('fat_loss', 'muscle_gain', "
            "'recomp', 'maintenance')",
            name="ck_user_profiles_goal_valid",
        ),
        sa.CheckConstraint(
            "height_cm IS NULL OR height_cm > 0",
            name="ck_user_profiles_height_cm_positive",
        ),
        sa.CheckConstraint(
            "training_experience IS NULL OR training_experience IN "
            "('beginner', 'intermediate', 'advanced')",
            name="ck_user_profiles_training_experience_valid",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index(
        op.f("ix_user_profiles_user_id"),
        "user_profiles",
        ["user_id"],
        unique=True,
    )

    op.create_table(
        "measurements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("weight_kg", sa.Float(), nullable=False),
        sa.Column("body_fat_percent", sa.Float(), nullable=True),
        sa.Column("waist_cm", sa.Float(), nullable=True),
        sa.Column("notes", sa.String(length=500), nullable=True),
        sa.Column("measured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "body_fat_percent IS NULL OR body_fat_percent BETWEEN 1 AND 80",
            name="ck_measurements_body_fat_percent_range",
        ),
        sa.CheckConstraint("weight_kg > 0", name="ck_measurements_weight_kg_positive"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_measurements_user_id"),
        "measurements",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        "ix_measurements_user_id_measured_at",
        "measurements",
        ["user_id", "measured_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_measurements_user_id_measured_at", table_name="measurements")
    op.drop_index(op.f("ix_measurements_user_id"), table_name="measurements")
    op.drop_table("measurements")

    op.drop_index(op.f("ix_user_profiles_user_id"), table_name="user_profiles")
    op.drop_table("user_profiles")

    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
