from app.schemas.recommendation import (
    CalorieGuidance,
    RecommendationRead,
    RecommendationRequest,
)

HIGH_BODY_FAT_PERCENT = 25.0


def generate_recommendation(request: RecommendationRequest) -> RecommendationRead:
    """Generate a deterministic, conservative recommendation.

    The engine is intentionally rules-based (no ML) so every output can be
    explained with explicit rationale and warnings.
    """

    profile = request.profile
    measurement = request.latest_measurement

    goal = profile.goal
    weight = measurement.weight_kg if measurement else None
    body_fat = measurement.body_fat_percent if measurement else None

    warnings: list[str] = []
    rationale: list[str] = []

    if goal is None:
        warnings.append("Goal is missing; defaulting to maintenance recommendation.")

    if measurement is None:
        warnings.append(
            "Latest measurement is missing; recommendation is less precise.",
        )
    else:
        if weight is None:
            warnings.append("Weight is missing; calorie guidance is conservative.")
        if body_fat is None:
            warnings.append(
                "Body-fat percentage is missing; "
                "body-composition adjustments are limited.",
            )

    is_high_body_fat = body_fat is not None and body_fat >= HIGH_BODY_FAT_PERCENT
    if is_high_body_fat:
        warnings.append(
            "Body-fat percentage is elevated; avoid aggressive bulking phases.",
        )

    has_enough_fat_loss_data = weight is not None and body_fat is not None

    phase = "maintenance"
    if goal == "fat_loss":
        if has_enough_fat_loss_data:
            phase = "cut"
            rationale.append(
                "Fat-loss goal with sufficient body data favors a cut phase.",
            )
        else:
            phase = "maintenance"
            warnings.append(
                "Insufficient weight/body-fat data for a confident cut; "
                "using maintenance.",
            )
    elif goal == "muscle_gain":
        if is_high_body_fat:
            # Conservative override: high body-fat users should not bulk aggressively.
            phase = "recomp"
            rationale.append(
                "Muscle-gain goal is moderated to recomp due to high body-fat level.",
            )
        else:
            phase = "lean_bulk"
            rationale.append(
                "Muscle-gain goal with acceptable body-fat favors lean bulk.",
            )
    elif goal == "recomp":
        phase = "recomp"
        rationale.append("Recomp goal selected directly.")
    elif goal == "maintenance" or goal is None:
        phase = "maintenance"
        rationale.append("Maintenance pathway selected.")

    if request.recent_measurements:
        first = request.recent_measurements[0].weight_kg
        last = request.recent_measurements[-1].weight_kg
        if first is not None and last is not None and first > 0:
            trend_percent = ((last - first) / first) * 100
            rationale.append(
                "Recent weight trend is "
                f"{trend_percent:+.1f}% across provided check-ins.",
            )

    if phase == "cut":
        calorie_guidance = CalorieGuidance(
            direction="deficit",
            suggested_percent_adjustment=-15.0,
            suggested_daily_calorie_delta=-350,
        )
        protein_g_per_kg = 2.2
        fat_g_per_kg = 0.8
        carbs_guidance = (
            "Fill remaining calories with carbs after protein and fat targets."
        )
    elif phase == "lean_bulk":
        calorie_guidance = CalorieGuidance(
            direction="surplus",
            suggested_percent_adjustment=8.0,
            suggested_daily_calorie_delta=250,
        )
        protein_g_per_kg = 1.8
        fat_g_per_kg = 0.8
        carbs_guidance = (
            "Prioritize carbs around training while keeping weight gain gradual."
        )
    elif phase == "recomp":
        calorie_guidance = CalorieGuidance(
            direction="maintenance",
            suggested_percent_adjustment=0.0,
            suggested_daily_calorie_delta=0,
        )
        protein_g_per_kg = 2.2
        fat_g_per_kg = 0.8
        carbs_guidance = (
            "Keep carbs performance-focused and adjust around training demand."
        )
    else:
        calorie_guidance = CalorieGuidance(
            direction="maintenance",
            suggested_percent_adjustment=0.0,
            suggested_daily_calorie_delta=0,
        )
        protein_g_per_kg = 1.6
        fat_g_per_kg = 0.8
        carbs_guidance = "Balance carbs with activity level to keep bodyweight stable."

    return RecommendationRead(
        phase=phase,
        calorie_guidance=calorie_guidance,
        protein_g_per_kg=protein_g_per_kg,
        fat_g_per_kg=fat_g_per_kg,
        carbs_guidance=carbs_guidance,
        rationale=rationale,
        warnings=warnings,
    )


__all__ = ["generate_recommendation", "HIGH_BODY_FAT_PERCENT"]
