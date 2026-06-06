import pandas as pd


def collective_kpis(events: pd.DataFrame) -> dict[str, float | int | None]:
    if events.empty:
        return {
            "points_total": 0,
            "shots": 0,
            "goals": 0,
            "conversion_rate": None,
            "technical_errors": 0,
        }

    shots = int(events["event_type"].isin(["shot_attempt", "goal_scored", "shot_missed"]).sum())
    goals = int(events["event_type"].isin(["goal_scored", "two_point_goal", "inflight_goal"]).sum())
    points_total = int(events.get("points_value", pd.Series(dtype=int)).sum())
    technical_errors = int((events["event_type"] == "technical_error").sum())

    return {
        "points_total": points_total,
        "shots": shots,
        "goals": goals,
        "conversion_rate": round(goals / shots, 3) if shots else None,
        "technical_errors": technical_errors,
    }
