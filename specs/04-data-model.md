# Data Model

## Entity Relationship Summary

```text
User 1 --- many WeightEntry
User 1 --- many WaistEntry
User 1 --- many RecommendationSnapshot
```

## users

| Column | Type | Constraints |
|---|---|---|
| id | UUID | Primary key |
| name | String | Required, unique, indexed |
| password_hash | String | Required |
| sex | Enum | `male`, `female`, `other`, `unspecified`; default `unspecified` |
| height_cm | Numeric | Nullable |
| created_at | DateTime | Required |
| updated_at | DateTime | Required |

Indexes:

```text
unique index users_name_key on users(name)
```

## weight_entries

| Column | Type | Constraints |
|---|---|---|
| id | UUID | Primary key |
| user_id | UUID | Required, FK users.id |
| weight_kg | Numeric | Required |
| entry_date | Date | Required |
| created_at | DateTime | Required |

Indexes:

```text
unique index weight_entries_user_date_key on weight_entries(user_id, entry_date)
index weight_entries_user_date_idx on weight_entries(user_id, entry_date desc)
```

## waist_entries

| Column | Type | Constraints |
|---|---|---|
| id | UUID | Primary key |
| user_id | UUID | Required, FK users.id |
| waist_cm | Numeric | Required |
| entry_date | Date | Required |
| created_at | DateTime | Required |

Indexes:

```text
unique index waist_entries_user_date_key on waist_entries(user_id, entry_date)
index waist_entries_user_date_idx on waist_entries(user_id, entry_date desc)
```

## recommendation_snapshots

| Column | Type | Constraints |
|---|---|---|
| id | UUID | Primary key |
| user_id | UUID | Required, FK users.id |
| bmi | Numeric | Nullable |
| waist_to_height_ratio | Numeric | Nullable |
| weekly_weight_change_pct | Numeric | Nullable |
| waist_change_cm | Numeric | Nullable |
| recommendation | Enum | Required |
| confidence | Enum | Required |
| explanation | Text | Required |
| feedback | JSONB | Required, default `[]` |
| created_at | DateTime | Required |

Indexes:

```text
index recommendation_snapshots_user_created_idx on recommendation_snapshots(user_id, created_at desc)
```

## Enums

### Sex

```text
male
female
other
unspecified
```

### Recommendation

```text
bulk
lean_bulk
cut
maintain_or_recomposition
```

### Confidence

```text
low
medium
high
```

## SQLAlchemy Notes

- Use UUID primary keys.
- Use timezone-aware datetimes.
- Use server defaults where appropriate.
- Use `Numeric` for measurements or `Float` if speed/simplicity is preferred for MVP.
- Keep domain calculations in services, not model methods.
