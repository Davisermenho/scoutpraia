import pytest

from scoutpraia.contracts.points_policy_v1 import (
    PointsPolicyError,
    derive_points,
    result_allowed,
    validate_points,
)


@pytest.mark.parametrize(
    ("event_code", "result_code", "scorer_role", "expected_points"),
    [
        ("simple_shot", "goal", "field_player", 1),
        ("simple_shot", "goal", "specialist", 2),
        ("spin_shot", "goal", "field_player", 2),
        ("spin_shot", "goal", "specialist", 2),
        ("inflight_shot", "goal", "field_player", 2),
        ("inflight_shot", "goal", "specialist", 2),
        ("goalkeeper_shot", "goal", "goalkeeper", 2),
        ("six_metre_throw", "goal", "field_player", 2),
        ("six_metre_throw", "goal", "specialist", 2),
        ("shootout_attempt", "goal", "field_player", 2),
        ("shootout_attempt", "goal", "specialist", 2),
    ],
)
def test_goal_points_are_derived_by_global_contract(
    event_code: str,
    result_code: str,
    scorer_role: str,
    expected_points: int,
) -> None:
    decision = derive_points(
        event_code=event_code,
        result_code=result_code,
        scorer_role=scorer_role,
    )

    assert decision.points_value == expected_points


@pytest.mark.parametrize(
    ("event_code", "result_code", "scorer_role"),
    [
        ("simple_shot", "save", "specialist"),
        ("simple_shot", "shot_wide", "specialist"),
        ("simple_shot", "shot_blocked", "specialist"),
        ("spin_shot", "save", "field_player"),
        ("inflight_shot", "shot_wide", "specialist"),
        ("goalkeeper_shot", "save", "goalkeeper"),
        ("six_metre_throw", "rebound_live", "field_player"),
        ("six_metre_throw", "execution_invalid_6m", "specialist"),
        ("shootout_attempt", "save", "field_player"),
        ("shootout_attempt", "pass_intercepted", "specialist"),
        ("technical_error_unforced", "lost_possession_no_shot", "field_player"),
        ("bad_substitution_attack", "lost_possession_no_shot", "specialist"),
    ],
)
def test_non_goal_or_no_shot_results_are_zero_when_allowed(
    event_code: str,
    result_code: str,
    scorer_role: str,
) -> None:
    decision = derive_points(
        event_code=event_code,
        result_code=result_code,
        scorer_role=scorer_role,
    )

    assert decision.points_value == 0


@pytest.mark.parametrize(
    ("event_code", "result_code", "scorer_role", "manual_points"),
    [
        ("simple_shot", "goal", "specialist", 1),
        ("spin_shot", "goal", "specialist", 1),
        ("inflight_shot", "goal", "specialist", 1),
        ("six_metre_throw", "goal", "field_player", 1),
        ("goalkeeper_shot", "goal", "goalkeeper", 1),
        ("shootout_attempt", "goal", "field_player", 1),
        ("simple_shot", "save", "field_player", 1),
    ],
)
def test_manual_points_cannot_override_global_contract(
    event_code: str,
    result_code: str,
    scorer_role: str,
    manual_points: int,
) -> None:
    with pytest.raises(PointsPolicyError, match="manual_points_mismatch"):
        validate_points(
            event_code=event_code,
            result_code=result_code,
            scorer_role=scorer_role,
            manual_points=manual_points,
        )


def test_specialist_is_role_not_event_or_position() -> None:
    with pytest.raises(PointsPolicyError, match="forbidden_event_code"):
        validate_points(
            event_code="specialist_shot",
            result_code="goal",
            scorer_role="specialist",
        )

    with pytest.raises(PointsPolicyError, match="forbidden_position_code"):
        validate_points(
            event_code="simple_shot",
            result_code="goal",
            scorer_role="specialist",
            position_code="specialist",
        )

    assert (
        validate_points(
            event_code="simple_shot",
            result_code="goal",
            scorer_role="specialist",
            manual_points=2,
        ).points_value
        == 2
    )


@pytest.mark.parametrize(
    ("event_code", "result_code", "scorer_role"),
    [
        ("simple_shot", "execution_invalid_6m", "field_player"),
        ("spin_shot", "rebound_live", "specialist"),
        ("inflight_shot", "execution_invalid_6m", "specialist"),
        ("goalkeeper_shot", "shot_blocked", "goalkeeper"),
        ("goalkeeper_shot", "goal", "field_player"),
        ("six_metre_throw", "shot_blocked", "field_player"),
        ("shootout_attempt", "shot_blocked", "field_player"),
        ("technical_error_forced", "goal", "field_player"),
    ],
)
def test_invalid_event_result_or_role_combinations_are_blocked(
    event_code: str,
    result_code: str,
    scorer_role: str,
) -> None:
    with pytest.raises(PointsPolicyError):
        derive_points(
            event_code=event_code,
            result_code=result_code,
            scorer_role=scorer_role,
        )


@pytest.mark.parametrize(
    ("event_code", "result_code"),
    [
        ("simple_shot", "goal"),
        ("spin_shot", "shot_blocked"),
        ("inflight_shot", "save"),
        ("goalkeeper_shot", "shot_wide"),
        ("six_metre_throw", "rebound_live"),
        ("shootout_attempt", "defender_foul_6m_awarded"),
        ("turnover_unclassified", "lost_possession_no_shot"),
    ],
)
def test_result_allowed_exposes_global_result_domain(
    event_code: str,
    result_code: str,
) -> None:
    assert result_allowed(event_code, result_code)
