from __future__ import annotations

import pandas as pd


OFFENSIVE_ATTEMPT_EVENTS = {
    "shot_attempt",
    "two_point_attempt",
    "specialist_attempt",
    "inflight_attempt",
    "shootout_attempt",
    "spin_shot",
    "simple_shot",
    "inflight_shot",
    "goalkeeper_shot",
    "six_metre_throw",
}
GOAL_EVENTS = {
    "goal_scored",
    "two_point_goal",
    "specialist_goal",
    "inflight_goal",
    "shootout_goal",
}
FINALIZATION_V1_EVENTS = {
    "simple_shot",
    "spin_shot",
    "inflight_shot",
    "goalkeeper_shot",
    "six_metre_throw",
}
NO_SHOT_ATTACK_V1_EVENTS = {
    "ball_control_turnover",
    "offensive_foul_turnover",
    "passive_play_turnover",
    "substitution_error_turnover",
}
SIX_METRE_THROW_EVENTS = {"six_metre_throw"}
TWO_POINT_ATTEMPT_EVENTS = {"two_point_attempt", "specialist_attempt"}
TWO_POINT_GOAL_EVENTS = {"two_point_goal", "specialist_goal"}
SPECIALIST_ATTEMPT_EVENTS = {"specialist_attempt"}
SPECIALIST_GOAL_EVENTS = {"specialist_goal"}
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
    goals_total = _count_goals(team_events)
    shot_attempts = _count_attempts(team_events)
    offensive_possession_total = int(len(offensive_possessions))
    defensive_possession_total = int(len(defensive_possessions))
    technical_errors = _count_events(team_events, {"technical_error"})
    defensive_stops = _count_events(team_events, {"defensive_stop"})
    transition_goals_conceded = _count_transition_goals_conceded(events_df)
    two_point_attempts = _count_two_point_attempts(team_events)
    two_point_goals = _count_two_point_goals(team_events)
    specialist_attempts = _count_specialist_attempts(team_events)
    specialist_goals = _count_specialist_goals(team_events)
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
        "specialist_efficiency": _safe_ratio(specialist_goals, specialist_attempts),
        "shootout_efficiency": _safe_ratio(shootout_goals, shootout_attempts),
        "no_shot_attack_total": _count_events(team_events, NO_SHOT_ATTACK_V1_EVENTS),
        "no_shot_attack_causes": _no_shot_attack_causes(team_events),
        "finalization_attempts_total": _count_events(team_events, FINALIZATION_V1_EVENTS),
        "finalization_efficiency_by_type": _finalization_efficiency_by_type(team_events),
        "points_by_technical_type": _points_by_technical_type(team_events),
        "points_by_scorer_role": _points_by_scorer_role(team_events),
        "specialist_shots_total": _count_specialist_shots_total(team_events),
        "six_metre_throw_breakdown": _six_metre_throw_breakdown(team_events),
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
        total_attempts = _count_attempts(player_events)
        total_goals = _count_goals(player_events)
        goals_by_zone = player_events[_goal_mask(player_events)]

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
                    _count_two_point_goals(player_events),
                    _count_two_point_attempts(player_events),
                ),
                "specialist": _safe_ratio(
                    _count_specialist_goals(player_events),
                    _count_specialist_attempts(player_events),
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
            "finalization_attempts_total": _count_events(
                player_events, FINALIZATION_V1_EVENTS
            ),
            "finalization_efficiency_by_type": _finalization_efficiency_by_type(
                player_events
            ),
            "points_by_technical_type": _points_by_technical_type(player_events),
            "points_by_scorer_role": _points_by_scorer_role(player_events),
            "specialist_shots_total": _count_specialist_shots_total(player_events),
            "six_metre_throw_breakdown": _six_metre_throw_breakdown(player_events),
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
            "specialist_efficiency": None,
            "shootout_efficiency": None,
            "no_shot_attack_total": 0,
            "no_shot_attack_causes": {},
            "finalization_attempts_total": 0,
            "finalization_efficiency_by_type": {},
            "points_by_technical_type": {},
            "points_by_scorer_role": {},
            "specialist_shots_total": 0,
            "six_metre_throw_breakdown": {},
            "critical_warnings": _critical_warnings(
                events_df, taxonomy_status, event_definitions
            ),
        }

    shooting_events = opponent_events[
        _attempt_mask(opponent_events) | _goal_mask(opponent_events)
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
    top_two_point_scorer = _top_two_point_scorer_player_id(opponent_events)
    pressure_error_rate = _safe_ratio(
        _count_events(opponent_events, {"forced_error"}),
        int(len(opponent_possessions)),
    )
    transition_vulnerability = _safe_ratio(
        _count_transition_events(opponent_events),
        int(len(opponent_possessions)),
    )
    specialist_efficiency = _safe_ratio(
        _count_specialist_goals(opponent_events),
        _count_specialist_attempts(opponent_events),
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
        "specialist_efficiency": specialist_efficiency,
        "shootout_efficiency": shootout_efficiency,
        "no_shot_attack_total": _count_events(opponent_events, NO_SHOT_ATTACK_V1_EVENTS),
        "no_shot_attack_causes": _no_shot_attack_causes(opponent_events),
        "finalization_attempts_total": _count_events(
            opponent_events, FINALIZATION_V1_EVENTS
        ),
        "finalization_efficiency_by_type": _finalization_efficiency_by_type(
            opponent_events
        ),
        "points_by_technical_type": _points_by_technical_type(opponent_events),
        "points_by_scorer_role": _points_by_scorer_role(opponent_events),
        "specialist_shots_total": _count_specialist_shots_total(opponent_events),
        "six_metre_throw_breakdown": _six_metre_throw_breakdown(opponent_events),
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
        "result_possession",
        "scorer_role",
        "zone",
        "points_value",
        "derived_points",
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


def _attempt_mask(events: pd.DataFrame) -> pd.Series:
    if events.empty:
        return pd.Series(dtype=bool)
    return events["event_type"].isin(OFFENSIVE_ATTEMPT_EVENTS)


def _goal_mask(events: pd.DataFrame) -> pd.Series:
    if events.empty:
        return pd.Series(dtype=bool)
    legacy_goals = events["event_type"].isin(GOAL_EVENTS)
    v1_goals = events["event_type"].isin(FINALIZATION_V1_EVENTS) & events[
        "result_possession"
    ].fillna("").eq("goal")
    return legacy_goals | v1_goals


def _count_attempts(events: pd.DataFrame) -> int:
    if events.empty:
        return 0
    return int(_attempt_mask(events).sum())


def _count_goals(events: pd.DataFrame) -> int:
    if events.empty:
        return 0
    return int(_goal_mask(events).sum())


def _two_point_attempt_mask(events: pd.DataFrame) -> pd.Series:
    if events.empty:
        return pd.Series(dtype=bool)
    legacy = events["event_type"].isin(TWO_POINT_ATTEMPT_EVENTS)
    v1 = events["event_type"].isin(
        {"spin_shot", "inflight_shot", "goalkeeper_shot", "six_metre_throw"}
    ) | (
        events["event_type"].eq("simple_shot")
        & events["scorer_role"].fillna("").eq("specialist")
    )
    return legacy | v1


def _two_point_goal_mask(events: pd.DataFrame) -> pd.Series:
    if events.empty:
        return pd.Series(dtype=bool)
    legacy = events["event_type"].isin(TWO_POINT_GOAL_EVENTS)
    v1 = _two_point_attempt_mask(events) & events["result_possession"].fillna("").eq("goal")
    return legacy | v1


def _count_two_point_attempts(events: pd.DataFrame) -> int:
    if events.empty:
        return 0
    return int(_two_point_attempt_mask(events).sum())


def _count_two_point_goals(events: pd.DataFrame) -> int:
    if events.empty:
        return 0
    return int(_two_point_goal_mask(events).sum())


def _specialist_attempt_mask(events: pd.DataFrame) -> pd.Series:
    if events.empty:
        return pd.Series(dtype=bool)
    legacy = events["event_type"].isin(SPECIALIST_ATTEMPT_EVENTS)
    v1 = events["event_type"].isin(FINALIZATION_V1_EVENTS) & events["scorer_role"].fillna(
        ""
    ).eq("specialist")
    return legacy | v1


def _specialist_goal_mask(events: pd.DataFrame) -> pd.Series:
    if events.empty:
        return pd.Series(dtype=bool)
    legacy = events["event_type"].isin(SPECIALIST_GOAL_EVENTS)
    v1 = _specialist_attempt_mask(events) & events["result_possession"].fillna("").eq("goal")
    return legacy | v1


def _count_specialist_attempts(events: pd.DataFrame) -> int:
    if events.empty:
        return 0
    return int(_specialist_attempt_mask(events).sum())


def _count_specialist_goals(events: pd.DataFrame) -> int:
    if events.empty:
        return 0
    return int(_specialist_goal_mask(events).sum())


def _resolved_points(events: pd.DataFrame) -> pd.Series:
    if events.empty:
        return pd.Series(dtype=float)
    resolved = events["derived_points"].where(
        events["derived_points"].notna(), events["points_value"]
    )
    return pd.to_numeric(resolved, errors="coerce").fillna(0)


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


def _finalization_efficiency_by_type(events: pd.DataFrame) -> dict[str, float | None]:
    if events.empty:
        return {}
    result: dict[str, float | None] = {}
    for event_type in sorted(FINALIZATION_V1_EVENTS):
        attempt_count = _count_events(events, {event_type})
        goal_count = int(
            (
                events["event_type"].eq(event_type)
                & events["result_possession"].fillna("").eq("goal")
            ).sum()
        )
        result[event_type] = _safe_ratio(goal_count, attempt_count)
    return result


def _points_by_technical_type(events: pd.DataFrame) -> dict[str, int]:
    if events.empty:
        return {}
    technical_events = events[events["event_type"].isin(FINALIZATION_V1_EVENTS)]
    if technical_events.empty:
        return {}
    grouped = technical_events.groupby("event_type")["points_value"].sum().to_dict()
    return {str(key): int(value) for key, value in grouped.items()}


def _points_by_scorer_role(events: pd.DataFrame) -> dict[str, int]:
    if events.empty:
        return {}
    scoped = events[
        events["event_type"].isin(FINALIZATION_V1_EVENTS)
        & events["scorer_role"].notna()
    ]
    if scoped.empty:
        return {}
    grouped = scoped.groupby("scorer_role")["points_value"].sum().to_dict()
    return {str(key): int(value) for key, value in grouped.items()}


def _count_specialist_shots_total(events: pd.DataFrame) -> int:
    return _count_specialist_attempts(events)


def _six_metre_throw_breakdown(events: pd.DataFrame) -> dict[str, int]:
    if events.empty:
        return {}
    six_metre_events = events[events["event_type"].isin(SIX_METRE_THROW_EVENTS)]
    if six_metre_events.empty:
        return {}
    counts = (
        six_metre_events["result_possession"]
        .fillna("unknown")
        .value_counts()
        .sort_index()
        .to_dict()
    )
    return {str(key): int(value) for key, value in counts.items()}


def _no_shot_attack_causes(events: pd.DataFrame) -> dict[str, int]:
    if events.empty:
        return {}
    scoped = events[events["event_type"].isin(NO_SHOT_ATTACK_V1_EVENTS)]
    if scoped.empty:
        return {}
    causes = scoped["event_subtype"].fillna(scoped["event_type"]).value_counts().sort_index()
    return {str(key): int(value) for key, value in causes.to_dict().items()}


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


def _top_two_point_scorer_player_id(events: pd.DataFrame) -> int | None:
    if events.empty:
        return None
    scoped = events[
        _goal_mask(events) & events["player_id"].notna() & _resolved_points(events).eq(2)
    ]
    if scoped.empty:
        return None
    scored_two_point_events = scoped.assign(resolved_points=_resolved_points(scoped))
    points_by_player = scored_two_point_events.groupby("player_id")["resolved_points"].sum()
    if points_by_player.empty:
        return None
    return int(points_by_player.sort_values(ascending=False).index[0])


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
