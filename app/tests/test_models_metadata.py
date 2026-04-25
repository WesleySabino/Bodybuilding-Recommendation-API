from sqlalchemy import CheckConstraint

import app.models  # noqa: F401
from app.db.base import Base

EXPECTED_TABLES = {"users", "user_profiles", "measurements"}


def test_metadata_contains_mvp_tables() -> None:
    assert EXPECTED_TABLES.issubset(Base.metadata.tables.keys())


def test_measurements_table_constraints_and_indexes() -> None:
    measurements_table = Base.metadata.tables["measurements"]

    check_constraints = {
        constraint.name
        for constraint in measurements_table.constraints
        if isinstance(constraint, CheckConstraint)
    }

    assert "ck_measurements_weight_kg_positive" in check_constraints
    assert "ck_measurements_body_fat_percent_range" in check_constraints

    index_column_sets = {
        tuple(column.name for column in index.columns): index.name
        for index in measurements_table.indexes
    }
    assert ("user_id", "measured_at") in index_column_sets


def test_user_profiles_height_constraint_exists() -> None:
    profiles_table = Base.metadata.tables["user_profiles"]

    check_constraints = {
        constraint.name
        for constraint in profiles_table.constraints
        if isinstance(constraint, CheckConstraint)
    }

    assert "ck_user_profiles_height_cm_positive" in check_constraints
