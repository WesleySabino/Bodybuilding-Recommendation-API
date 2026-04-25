# Domain Formulas and Recommendation Rules

## Units

All measurements must use metric units:

- Height: centimeters
- Weight: kilograms
- Waist circumference: centimeters

## BMI

```text
height_m = height_cm / 100
BMI = weight_kg / height_m^2
```

Use latest available weight.

Rounded output:

```text
bmi = round(BMI, 2)
```

## Waist-to-Height Ratio

```text
waist_to_height_ratio = waist_cm / height_cm
```

Use latest available waist circumference.

Rounded output:

```text
waist_to_height_ratio = round(waist_to_height_ratio, 3)
```

## Seven-Day Average Weight

Use averages instead of single daily weights to reduce noise.

```text
avg_weight_last_7d = average(weight entries from the most recent 7 calendar days with data)
avg_weight_previous_7d = average(weight entries from the 7 calendar days before that with data)
```

For MVP, if entries are missing, calculate over available entries in each window. The confidence score should reflect insufficient data.

## Weekly Weight Change

```text
weekly_weight_change_kg = avg_weight_last_7d - avg_weight_previous_7d
weekly_weight_change_pct = (weekly_weight_change_kg / avg_weight_previous_7d) * 100
```

Rounded output:

```text
weekly_weight_change_pct = round(weekly_weight_change_pct, 2)
```

If there is not enough data for the previous 7-day window, return `null`.

## Waist Change

```text
waist_change_cm = latest_waist_cm - previous_waist_cm
```

Rounded output:

```text
waist_change_cm = round(waist_change_cm, 1)
```

If fewer than two waist entries exist, return `null`.

## Recommendation Rules

Evaluate in this order:

```text
IF height_cm is missing:
    recommendation cannot be calculated

IF latest weight is missing:
    recommendation cannot be calculated

IF latest waist is missing:
    use BMI-only fallback with low confidence

IF BMI < 18.5:
    recommendation = "bulk"

ELSE IF waist_to_height_ratio >= 0.50:
    recommendation = "cut"

ELSE IF BMI >= 27:
    recommendation = "cut"

ELSE IF BMI >= 18.5 AND BMI <= 24.9 AND waist_to_height_ratio < 0.50:
    recommendation = "lean_bulk"

ELSE:
    recommendation = "maintain_or_recomposition"
```

## BMI-Only Fallback

If height and weight exist but waist does not:

```text
IF BMI < 18.5:
    recommendation = "bulk"
ELSE IF BMI >= 27:
    recommendation = "cut"
ELSE:
    recommendation = "maintain_or_recomposition"
```

Confidence must be `low`.

## Confidence Rules

```text
IF weight_entries_count < 7 OR waist_entries_count < 1:
    confidence = "low"

ELSE IF weight_entries_count >= 7 AND waist_entries_count < 2:
    confidence = "medium"

ELSE IF weight_entries_count >= 14 AND waist_entries_count >= 2:
    confidence = "high"

ELSE:
    confidence = "medium"
```

## Progress Feedback Rules

These are secondary explanations and should not override the main recommendation.

### Cutting

```text
IF recommendation == "cut" AND weekly_weight_change_pct is not null:
    IF weekly_weight_change_pct > -0.25:
        feedback = "Weight is not decreasing fast enough for a typical cut."
    IF weekly_weight_change_pct < -1.00:
        feedback = "Weight is decreasing aggressively. Consider a slower cut."
```

### Bulking or Lean Bulking

```text
IF recommendation in ["bulk", "lean_bulk"] AND weekly_weight_change_pct is not null:
    IF recommendation == "lean_bulk":
        target_min = 0.10
        target_max = 0.25
    ELSE:
        target_min = 0.25
        target_max = 0.50

    IF weekly_weight_change_pct < target_min:
        feedback = "Weight gain is slower than the target range."
    IF weekly_weight_change_pct > target_max:
        feedback = "Weight gain is faster than the target range."
```

### Waist During Bulk

```text
IF recommendation in ["bulk", "lean_bulk"] AND waist_change_cm is not null:
    IF waist_change_cm > 1.0:
        feedback = "Waist is increasing quickly; fat gain may be too fast."
```

## Target Weekly Weight Change Ranges

```text
cut: -1.00% to -0.25% bodyweight/week
lean_bulk: +0.10% to +0.25% bodyweight/week
bulk: +0.25% to +0.50% bodyweight/week
maintain_or_recomposition: -0.10% to +0.10% bodyweight/week
```
