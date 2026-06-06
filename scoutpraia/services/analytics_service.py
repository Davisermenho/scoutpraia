from __future__ import annotations

import pandas as pd


OFFENSIVE_ATTEMPT_EVENTS = {
    "shot_attempt",
    "two_point_attempt",
    "inflight_attempt",
    "shootout_attempt",
    "spin_shot",
}
GOAL_EVENTS = {
    "goal_scored",
    "two_point_goal",
    "inflight_goal",
    "shootout_goal",
}
TWO_POINT_ATTEMPT_EVENTS = {"two_point_attempt"}
TWO_POINT_GOAL_EVENTS = {"two_point_goal"}
SHOOTOUT_ATTEMPT_EVENTS = {"shootout_attempt"}
SHOOTOUT_GOAL_EVENTS = {"shootout_goal"}
SAVE_EVENTS = {"save", "save_shootout"}
CRITICAL_EVENT_TYPES = {
    "technical_error",
    "forced_error",
    "defensive_breakdown",
    "fast_break_against",
    "transition_recovery_bad",
    "goal_conceded",
}


def collective_kpis(
    events: pd.DataFrame,
    possessions: pd.DataFrame | None = None,
    set_segments: pd.DataFrame | None = None,
    taxonomy_status: str = "draft",
    event_definitions: pd.DataFrame | None = None,
) -> dict[str, object]:
    events_df = _events_frame(events)
    possessions_df = _possessions_frame(possessions)
    team_events = events_df[events_df["team_side"] == "team"]
    offensive_possessions = possessions_df[possessions_df["team_side"] == "team"]
    defensive_possessions = possessions_df[possessions_df["team_side"] == "opponent"]

    points_total = int(team_events["points_value"].sum()) if not team_events.empty else 0
    goals_total = _count_events(team_events, GOAL_EVENTS)
    shot_attempts = _count_events(team_events, OFFENSIVE_ATTEMPT_EVENTS)
    offensive_possession_total = int(len(offensive_possessions))
    defensive_possession_total = int(len(defensive_possessions))
    technical_errors = _count_events(team_events, {"technical_error"})
    defensive_stops = _count_events(team_events, {"defensive_stop"})
    transition_goals_conceded = _count_transition_goals_conceded(events_df)
    two_point_attempts = _count_events(team_events, TWO_POINT_ATTEMPT_EVENTS)
    two_point_goals = _count_events(team_events, TWO_POINT_GOAL_EVENTS)
    shootout_attempts = _count_events(team_events, SHOOTOUT_ATTEMPT_EVENTS)
    shootout_goals = _count_events(team_events, SHOOTOUT_GOAL_EVENTS)

    return {
        "points_total": points_total,
        "goals_total": goals_total,
        "offensive_possessions": offensive_possession_total,
        "defensive_possessions": defensive_possession_total,
        "points_per_possession": _safe_ratio(points_total, offensive_possession_total),
        "goals_per_possession": _safe_ratio(goals_total, offensive_possession_total),
        "offensive_conversion_rate": _safe_ratio(goals_total, shot_attempts),
        "conversion_rate": _safe_ratio(goals_total, shot_attempts),
        "technical_error_rate": _safe_ratio(technical_errors, offensive_possession_total),
        "defensive_stops_per_possession": _safe_ratio(
            defensive_stops, defensive_possession_total
        ),
        "transition_goals_conceded": transition_goals_conceded,
        "two_point_efficiency": _safe_ratio(two_point_goals, two_point_attempts),
        "shootout_efficiency": _safe_ratio(shootout_goals, shootout_attempts),
        "set_performance": _set_performance(team_events, set_segments),
        "critical_warnings": _critical_warnings(
            events_df, taxonomy_status, event_definitions
        ),
    }


def individual_kpis(
    events: pd.DataFrame,
    taxonomy_status: str = "draft",
    event_definitions: pd.DataFrame | None = None,
) -> dict[int, dict[str, object]]:
    events_df = _events_frame(events)
    team_events = events_df[
        (events_df["team_side"] == "team") & (events_df["player_id"].notna())
    ]
    if team_events.empty:
        return {}

    result: dict[int, dict[str, object]] = {}
    warnings = _critical_warnings(events_df, taxonomy_status, event_definitions)

    for player_id, player_events in team_events.groupby("player_id", sort=True):
        player_id_int = int(player_id)
        total_attempts = _count_events(player_events, OFFENSIVE_ATTEMPT_EVENTS)
        total_goals = _count_events(player_events, GOAL_EVENTS)
        goals_by_zone = player_events[player_events["event_type"].isin(GOAL_EVENTS)]

        result[player_id_int] = {
            "shot_attempts": total_attempts,
            "total_goals": total_goals,
            "total_conversion": _safe_ratio(total_goals, total_attempts),
            "conversion_by_type": {
                "regular": _safe_ratio(
                    _count_events(player_events, {"goal_scored"}),
                    _count_events(player_events, {"shot_attempt"}),
                ),
                "two_point": _safe_ratio(
                    _count_events(player_events, TWO_POINT_GOAL_EVENTS),
                    _count_events(player_events, TWO_POINT_ATTEMPT_EVENTS),
                ),
                "inflight": _safe_ratio(
                    _count_events(player_events, {"inflight_goal"}),
                    _count_events(player_events, {"inflight_attempt"}),
                ),
                "shootout": _safe_ratio(
                    _count_events(player_events, SHOOTOUT_GOAL_EVENTS),
                    _count_events(player_events, SHOOTOUT_ATTEMPT_EVENTS),
                ),
            },
            "conversion_by_zone": _zone_conversion(player_events, goals_by_zone),
            "turnovers": _count_events(player_events, {"turnover"}),
            "technical_errors": _count_events(player_events, {"technical_error"}),
            "steals": _count_events(player_events, {"steal"}),
            "blocks": _count_events(player_events, {"block"}),
            "saves": _count_events(player_events, SAVE_EVENTS),
            "direct_goal_participation": total_goals
            + _count_events(player_events, {"assist"}),
            "critical_warnings": warnings,
        }

    return result


def opponent_kpis(
    events: pd.DataFrame,
    possessions: pd.DataFrame | None = None,
    taxonomy_status: str = "draft",
    event_definitions: pd.DataFrame | None = None,
) -> dict[str, object]:
    events_df = _events_frame(events)
    possessions_df = _possessions_frame(possessions)
    opponent_events = events_df[events_df["team_side"] == "opponent"]
    opponent_possessions = possessions_df[possessions_df["team_side"] == "opponent"]

    if opponent_events.empty:
        return {
            "preferred_attack_side": None,
            "most_frequent_shooter_player_id": None,
            "top_two_point_scorer_player_id": None,
            "pressure_error_rate": None,
            "transition_vulnerability": None,
            "shootout_efficiency": None,
            "critical_warnings": _critical_warnings(
                events_df, taxonomy_status, event_definitions
            ),
        }

    shooting_events = opponent_events[
        opponent_events["event_type"].isin(OFFENSIVE_ATTEMPT_EVENTS | GOAL_EVENTS)
    ]
    side_counts = (
        shooting_events["zone"].fillna("").map(_attack_side).value_counts().to_dict()
    )
    preferred_attack_side = None
    if side_counts:
        preferred_attack_side = max(side_counts, key=side_counts.get)

    most_frequent_shooter = _top_player_id(
        shooting_events[shooting_events["player_id"].notna()]
    )
    top_two_point_scorer = _top_player_id(
        opponent_events[
            opponent_events["event_type"].isin(TWO_POINT_GOAL_EVENTS)
            & opponent_events["player_id"].notna()
        ]
    )
    pressure_error_rate = _safe_ratio(
        _count_events(opponent_events, {"forced_error"}),
        int(len(opponent_possessions)),
    )
    transition_vulnerability = _safe_ratio(
        _count_transition_events(opponent_events),
        int(len(opponent_possessions)),
    )
    shootout_efficiency = _safe_ratio(
        _count_events(opponent_events, SHOOTOUT_GOAL_EVENTS),
        _count_events(opponent_events, SHOOTOUT_ATTEMPT_EVENTS),
    )

    return {
        "preferred_attack_side": preferred_attack_side,
        "most_frequent_shooter_player_id": most_frequent_shooter,
        "top_two_point_scorer_player_id": top_two_point_scorer,
        "pressure_error_rate": pressure_error_rate,
        "transition_vulnerability": transition_vulnerability,
        "shootout_efficiency": shootout_efficiency,
        "critical_warnings": _critical_warnings(
            events_df, taxonomy_status, event_definitions
        ),
    }


def _events_frame(events: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "event_type",
        "event_subtype",
        "player_id",
        "secondary_player_id",
        "team_side",
        "timestamp_second",
        "outcome",
        "zone",
        "points_value",
        "set_id",
        "possession_id",
    ]
    return _frame_with_columns(events, columns)


def _possessions_frame(possessions: pd.DataFrame | None) -> pd.DataFrame:
    columns = [
        "id",
        "team_side",
        "set_id",
        "points_scored",
        "points_conceded",
    ]
    return _frame_with_columns(possessions, columns)


def _frame_with_columns(
    data: pd.DataFrame | None,
    columns: list[str],
) -> pd.DataFrame:
    if data is None:
        return pd.DataFrame(columns=columns)
    frame = data.copy()
    for column in columns:
        if column not in frame.columns:
            frame[column] = None
    return frame


def _count_events(events: pd.DataFrame, event_types: set[str]) -> int:
    if events.empty:
        return 0
    return int(events["event_type"].isin(event_types).sum())


def _safe_ratio(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return round(numerator / denominator, 3)


def _set_performance(
    team_events: pd.DataFrame,
    set_segments: pd.DataFrame | None,
) -> dict[int, dict[str, int]]:
    if team_events.empty:
        return {}

    set_mapping: dict[int, int] = {}
    if set_segments is not None and not set_segments.empty:
        set_frame = set_segments.copy()
        if "id" in set_frame.columns and "set_number" in set_frame.columns:
            set_mapping = {
                int(row["id"]): int(row["set_number"])
                for _, row in set_frame[["id", "set_number"]].dropna().iterrows()
            }

    performance: dict[int, dict[str, int]] = {}
    grouped = team_events.groupby("set_id", dropna=False)
    for set_id, set_events in grouped:
        set_key = 0 if pd.isna(set_id) else int(set_id)
        set_number = set_mapping.get(set_key, set_key)
        performance[set_number] = {
            "points_total": int(set_events["points_value"].sum()),
            "goals_total": _count_events(set_events, GOAL_EVENTS),
            "technical_errors": _count_events(set_events, {"technical_error"}),
        }
    return performance


def _zone_conversion(
    attempts: pd.DataFrame,
    goals: pd.DataFrame,
) -> dict[str, float | None]:
    result: dict[str, float | None] = {}
    attempt_counts = (
        attempts[attempts["event_type"].isin(OFFENSIVE_ATTEMPT_EVENTS)]
        .groupby("zone")
        .size()
        .to_dict()
    )
    goal_counts = goals.groupby("zone").size().to_dict()
    zones = sorted(set(attempt_counts) | set(goal_counts))
    for zone in zones:
        denominator = int(attempt_counts.get(zone, 0))
        numerator = int(goal_counts.get(zone, 0))
        result[str(zone)] = _safe_ratio(numerator, denominator)
    return result


def _attack_side(zone: str) -> str:
    if zone.startswith("left") or zone.startswith("6m_left"):
        return "left"
    if zone.startswith("right") or zone.startswith("6m_right"):
        return "right"
    return "center"


def _top_player_id(events: pd.DataFrame) -> int | None:
    if events.empty:
        return None
    counts = events.groupby("player_id").size()
    if counts.empty:
        return None
    return int(counts.sort_values(ascending=False).index[0])


def _count_transition_goals_conceded(events: pd.DataFrame) -> int:
    if events.empty:
        return 0
    goals_conceded = events[events["event_type"] == "goal_conceded"]
    return int(
        (
            goals_conceded["event_subtype"].fillna("").eq("transition")
            | goals_conceded["outcome"].fillna("").eq("transition")
        ).sum()
    )


def _count_transition_events(events: pd.DataFrame) -> int:
    if events.empty:
        return 0
    return int(
        events["event_type"].isin({"fast_break_against", "transition_recovery_bad"}).sum()
    ) + _count_transition_goals_conceded(events)


def _critical_warnings(
    events: pd.DataFrame,
    taxonomy_status: str,
    event_definitions: pd.DataFrame | None,
) -> list[str]:
    warnings: list[str] = []
    if taxonomy_status != "approved":
        warnings.append(
            "Taxonomia nao aprovada; KPIs criticos devem ser interpretados com cautela."
        )

    if event_definitions is None or event_definitions.empty or events.empty:
        return warnings

    definitions = event_definitions.copy()
    for column in ("event_type", "evidence_type"):
        if column not in definitions.columns:
            return warnings

    practical_event_types = set(
        definitions[
            definitions["evidence_type"].fillna("").eq("practical_hypothesis")
        ]["event_type"].tolist()
    )
    used_critical_types = sorted(
        (
            set(events["event_type"].dropna().tolist()) & practical_event_types
        )
        & CRITICAL_EVENT_TYPES
    )
    if used_critical_types:
        warnings.append(
            "KPIs usam eventos ainda praticos/hipoteticos: "
            + ", ".join(used_critical_types)
        )

    return warnings
