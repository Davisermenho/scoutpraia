import pandas as pd

from scoutpraia.services.analytics_service import (
    collective_kpis,
    individual_kpis,
    opponent_kpis,
)
from scoutpraia.services.taxonomy_service import EVENT_DEFINITIONS


def build_fixture() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    events = pd.DataFrame(
        [
            {"event_type": "shot_attempt", "player_id": 1, "team_side": "team", "timestamp_second": 10, "zone": "left_wing", "points_value": 0, "set_id": 1, "possession_id": 1},
            {"event_type": "goal_scored", "player_id": 1, "team_side": "team", "timestamp_second": 11, "zone": "left_wing", "points_value": 1, "set_id": 1, "possession_id": 1},
            {"event_type": "technical_error", "player_id": 1, "team_side": "team", "timestamp_second": 20, "zone": "center", "points_value": 0, "set_id": 1, "possession_id": 2},
            {"event_type": "turnover", "player_id": 1, "team_side": "team", "timestamp_second": 21, "zone": "center", "points_value": 0, "set_id": 1, "possession_id": 2},
            {"event_type": "two_point_attempt", "player_id": 2, "team_side": "team", "timestamp_second": 30, "zone": "right_wing", "points_value": 0, "set_id": 1, "possession_id": 3},
            {"event_type": "two_point_goal", "player_id": 2, "team_side": "team", "timestamp_second": 31, "zone": "right_wing", "points_value": 2, "set_id": 1, "possession_id": 3},
            {"event_type": "assist", "player_id": 3, "team_side": "team", "timestamp_second": 31, "zone": "right_wing", "points_value": 0, "set_id": 1, "possession_id": 3},
            {"event_type": "shootout_attempt", "player_id": 2, "team_side": "team", "timestamp_second": 40, "zone": "shootout_lane", "points_value": 0, "set_id": 2, "possession_id": 4},
            {"event_type": "shootout_goal", "player_id": 2, "team_side": "team", "timestamp_second": 41, "zone": "shootout_lane", "points_value": 2, "set_id": 2, "possession_id": 4},
            {"event_type": "specialist_attempt", "player_id": 2, "team_side": "team", "timestamp_second": 42, "zone": "center", "points_value": 0, "set_id": 2, "possession_id": 9},
            {"event_type": "specialist_goal", "player_id": 2, "team_side": "team", "timestamp_second": 43, "zone": "center", "points_value": 2, "set_id": 2, "possession_id": 9},
            {"event_type": "defensive_stop", "player_id": 3, "team_side": "team", "timestamp_second": 50, "zone": "center", "points_value": 0, "set_id": 1, "possession_id": 5},
            {"event_type": "steal", "player_id": 3, "team_side": "team", "timestamp_second": 51, "zone": "center", "points_value": 0, "set_id": 1, "possession_id": 5},
            {"event_type": "block", "player_id": 3, "team_side": "team", "timestamp_second": 60, "zone": "center", "points_value": 0, "set_id": 1, "possession_id": 6},
            {"event_type": "save", "player_id": 4, "team_side": "team", "timestamp_second": 61, "zone": "center", "points_value": 0, "set_id": 2, "possession_id": 6},
            {"event_type": "forced_error", "player_id": 99, "team_side": "opponent", "timestamp_second": 52, "zone": "right_half", "points_value": 0, "set_id": 1, "possession_id": 5},
            {"event_type": "goal_conceded", "event_subtype": "transition", "player_id": 99, "team_side": "opponent", "timestamp_second": 70, "outcome": "transition", "zone": "left_half", "points_value": 1, "set_id": 2, "possession_id": 7},
            {"event_type": "fast_break_against", "player_id": 99, "team_side": "opponent", "timestamp_second": 71, "zone": "left_half", "points_value": 0, "set_id": 2, "possession_id": 7},
            {"event_type": "shootout_attempt", "player_id": 98, "team_side": "opponent", "timestamp_second": 80, "zone": "shootout_lane", "points_value": 0, "set_id": 2, "possession_id": 8},
            {"event_type": "shootout_goal", "player_id": 98, "team_side": "opponent", "timestamp_second": 81, "zone": "shootout_lane", "points_value": 2, "set_id": 2, "possession_id": 8},
            {"event_type": "shot_attempt", "player_id": 99, "team_side": "opponent", "timestamp_second": 53, "zone": "left_wing", "points_value": 0, "set_id": 1, "possession_id": 5},
            {"event_type": "goal_scored", "player_id": 99, "team_side": "opponent", "timestamp_second": 54, "zone": "left_wing", "points_value": 1, "set_id": 1, "possession_id": 5},
            {"event_type": "shot_attempt", "player_id": 99, "team_side": "opponent", "timestamp_second": 62, "zone": "left_half", "points_value": 0, "set_id": 1, "possession_id": 6},
            {"event_type": "shot_missed", "player_id": 99, "team_side": "opponent", "timestamp_second": 63, "zone": "left_half", "points_value": 0, "set_id": 1, "possession_id": 6},
            {"event_type": "two_point_goal", "player_id": 99, "team_side": "opponent", "timestamp_second": 72, "zone": "left_half", "points_value": 2, "set_id": 2, "possession_id": 7},
            {"event_type": "specialist_attempt", "player_id": 99, "team_side": "opponent", "timestamp_second": 90, "zone": "center", "points_value": 0, "set_id": 2, "possession_id": 10},
            {"event_type": "specialist_goal", "player_id": 99, "team_side": "opponent", "timestamp_second": 91, "zone": "center", "points_value": 2, "set_id": 2, "possession_id": 10},
        ]
    )

    possessions = pd.DataFrame(
        [
            {"id": 1, "team_side": "team", "set_id": 1, "points_scored": 1, "points_conceded": 0},
            {"id": 2, "team_side": "team", "set_id": 1, "points_scored": 0, "points_conceded": 0},
            {"id": 3, "team_side": "team", "set_id": 1, "points_scored": 2, "points_conceded": 0},
            {"id": 4, "team_side": "team", "set_id": 2, "points_scored": 2, "points_conceded": 0},
            {"id": 9, "team_side": "team", "set_id": 2, "points_scored": 2, "points_conceded": 0},
            {"id": 5, "team_side": "opponent", "set_id": 1, "points_scored": 0, "points_conceded": 1},
            {"id": 6, "team_side": "opponent", "set_id": 1, "points_scored": 0, "points_conceded": 0},
            {"id": 7, "team_side": "opponent", "set_id": 2, "points_scored": 0, "points_conceded": 3},
            {"id": 8, "team_side": "opponent", "set_id": 2, "points_scored": 0, "points_conceded": 2},
            {"id": 10, "team_side": "opponent", "set_id": 2, "points_scored": 0, "points_conceded": 2},
        ]
    )

    set_segments = pd.DataFrame(
        [
            {"id": 1, "set_number": 1},
            {"id": 2, "set_number": 2},
        ]
    )

    definitions = pd.DataFrame(EVENT_DEFINITIONS)
    return events, possessions, set_segments, definitions


def test_collective_individual_and_opponent_kpis_with_fixture() -> None:
    events, possessions, set_segments, definitions = build_fixture()

    collective = collective_kpis(
        events,
        possessions=possessions,
        set_segments=set_segments,
        taxonomy_status="draft",
        event_definitions=definitions,
    )
    individual = individual_kpis(
        events,
        taxonomy_status="draft",
        event_definitions=definitions,
    )
    opponent = opponent_kpis(
        events,
        possessions=possessions,
        taxonomy_status="draft",
        event_definitions=definitions,
    )

    assert collective["points_total"] == 7
    assert collective["goals_total"] == 4
    assert collective["points_per_possession"] == 1.4
    assert collective["goals_per_possession"] == 0.8
    assert collective["offensive_conversion_rate"] == 1.0
    assert collective["technical_error_rate"] == 0.2
    assert collective["defensive_stops_per_possession"] == 0.2
    assert collective["transition_goals_conceded"] == 1
    assert collective["two_point_efficiency"] == 1.0
    assert collective["specialist_efficiency"] == 1.0
    assert collective["shootout_efficiency"] == 1.0
    assert collective["set_performance"] == {
        1: {"points_total": 3, "goals_total": 2, "technical_errors": 1},
        2: {"points_total": 4, "goals_total": 2, "technical_errors": 0},
    }
    assert len(collective["critical_warnings"]) == 2

    assert individual[1]["shot_attempts"] == 1
    assert individual[1]["total_conversion"] == 1.0
    assert individual[1]["turnovers"] == 1
    assert individual[1]["technical_errors"] == 1
    assert individual[2]["shot_attempts"] == 3
    assert individual[2]["conversion_by_type"]["two_point"] == 1.0
    assert individual[2]["conversion_by_type"]["specialist"] == 1.0
    assert individual[2]["conversion_by_type"]["shootout"] == 1.0
    assert individual[3]["steals"] == 1
    assert individual[3]["blocks"] == 1
    assert individual[3]["direct_goal_participation"] == 1
    assert individual[4]["saves"] == 1

    assert opponent["preferred_attack_side"] == "center"
    assert opponent["most_frequent_shooter_player_id"] == 99
    assert opponent["top_two_point_scorer_player_id"] == 99
    assert opponent["pressure_error_rate"] == 0.2
    assert opponent["specialist_efficiency"] == 1.0
    assert opponent["transition_vulnerability"] == 0.4
    assert opponent["shootout_efficiency"] == 1.0
    assert len(opponent["critical_warnings"]) == 2


def test_analytics_return_empty_safe_structures() -> None:
    empty_events = pd.DataFrame()
    empty_possessions = pd.DataFrame()

    collective = collective_kpis(empty_events, possessions=empty_possessions)
    individual = individual_kpis(empty_events)
    opponent = opponent_kpis(empty_events, possessions=empty_possessions)

    assert collective["points_total"] == 0
    assert collective["goals_total"] == 0
    assert collective["points_per_possession"] is None
    assert collective["specialist_efficiency"] is None
    assert collective["set_performance"] == {}
    assert individual == {}
    assert opponent["preferred_attack_side"] is None
    assert opponent["specialist_efficiency"] is None
    assert opponent["shootout_efficiency"] is None


def test_individual_specialist_conversion_consolidates_legacy_and_v1_events() -> None:
    events = pd.DataFrame(
        [
            {
                "event_type": "specialist_attempt",
                "player_id": 7,
                "team_side": "team",
                "points_value": 0,
            },
            {
                "event_type": "specialist_goal",
                "player_id": 7,
                "team_side": "team",
                "points_value": 2,
            },
            {
                "event_type": "simple_shot",
                "player_id": 7,
                "team_side": "team",
                "points_value": 0,
                "result_possession": "save",
                "scorer_role": "specialist",
            },
        ]
    )

    individual = individual_kpis(events, taxonomy_status="approved")

    assert individual[7]["conversion_by_type"]["specialist"] == 0.5
    assert individual[7]["conversion_by_type"]["two_point"] == 0.5


def test_opponent_top_two_point_scorer_uses_v1_resolved_points() -> None:
    events = pd.DataFrame(
        [
            {
                "event_type": "simple_shot",
                "player_id": 21,
                "team_side": "opponent",
                "points_value": 2,
                "result_possession": "goal",
                "scorer_role": "specialist",
            },
            {
                "event_type": "six_metre_throw",
                "player_id": 21,
                "team_side": "opponent",
                "points_value": 2,
                "result_possession": "goal",
                "scorer_role": "field_player",
            },
            {
                "event_type": "two_point_goal",
                "player_id": 22,
                "team_side": "opponent",
                "points_value": 2,
            },
        ]
    )

    opponent = opponent_kpis(events, taxonomy_status="approved")

    assert opponent["top_two_point_scorer_player_id"] == 21
