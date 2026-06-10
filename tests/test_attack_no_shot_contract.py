import pytest

from scoutpraia.services.no_shot_attack_contract_service import (
    NoShotAttackContractError,
    validate_record,
)


BASE_KWARGS = {
    "result_possession": "lost_possession_no_shot",
    "team_in_possession": True,
    "athlete_id": "athlete_1",
    "court_lane": "lane_3_central_axis",
    "court_depth": "depth_2_mid",
    "position_code": "pos_central",
    "system_code": "AT_3X1",
}


@pytest.mark.parametrize(
    ("event_code", "extra_kwargs"),
    [
        ("technical_error_unforced", {"technical_error_subtype": "bad_pass"}),
        ("technical_error_forced", {"technical_error_subtype": "bad_reception"}),
        ("offensive_foul", {}),
        ("goal_area_invasion_attack", {}),
        ("passive_play_turnover", {"passive_play_subtype": "forewarning_expired"}),
        ("bad_substitution_attack", {"substitution_error_subtype": "early_entry"}),
        ("turnover_unclassified", {"review_marker": True}),
    ],
)
def test_accepts_official_attack_no_shot_events(event_code: str, extra_kwargs: dict[str, object]) -> None:
    assert validate_record(event_code=event_code, **BASE_KWARGS, **extra_kwargs) == event_code


@pytest.mark.parametrize(
    "event_code",
    [
        "simple_shot",
        "spin_shot",
        "inflight_shot",
        "goalkeeper_shot",
        "six_metre_throw",
        "shootout_attempt",
        "fast_break_for",
    ],
)
def test_blocks_finalization_shootout_and_transition_events(event_code: str) -> None:
    with pytest.raises(NoShotAttackContractError, match="forbidden_event_code"):
        validate_record(event_code=event_code, **BASE_KWARGS)


@pytest.mark.parametrize(
    "legacy_code",
    [
        "ball_control_turnover",
        "offensive_foul_turnover",
        "substitution_error_turnover",
        "turnover_cause_detail",
    ],
)
def test_blocks_old_interim_event_codes(legacy_code: str) -> None:
    with pytest.raises(NoShotAttackContractError, match="forbidden_event_code|invalid_event_code"):
        validate_record(event_code=legacy_code, **BASE_KWARGS)


def test_requires_lost_possession_no_shot_result() -> None:
    with pytest.raises(NoShotAttackContractError, match="turnover_result_required"):
        validate_record(
            event_code="technical_error_unforced",
            **{**BASE_KWARGS, "result_possession": "goal"},
            technical_error_subtype="bad_pass",
        )


def test_blocks_shot_attempted_and_offensive_transition() -> None:
    with pytest.raises(NoShotAttackContractError, match="shot_not_allowed_in_no_shot_attack"):
        validate_record(
            event_code="technical_error_unforced",
            **BASE_KWARGS,
            technical_error_subtype="bad_pass",
            shot_attempted=True,
        )

    with pytest.raises(NoShotAttackContractError, match="offensive_transition_forbidden"):
        validate_record(
            event_code="technical_error_unforced",
            **BASE_KWARGS,
            technical_error_subtype="bad_pass",
            is_offensive_transition=True,
        )


def test_technical_errors_require_subtype_and_location() -> None:
    with pytest.raises(NoShotAttackContractError, match="technical_error_subtype_required"):
        validate_record(event_code="technical_error_unforced", **BASE_KWARGS)

    with pytest.raises(NoShotAttackContractError, match="court_lane_required"):
        validate_record(
            event_code="technical_error_unforced",
            **{**BASE_KWARGS, "court_lane": None},
            technical_error_subtype="bad_pass",
        )


def test_passive_play_requires_approved_subtype() -> None:
    with pytest.raises(NoShotAttackContractError, match="invalid_passive_subtype"):
        validate_record(
            event_code="passive_play_turnover",
            **BASE_KWARGS,
            passive_play_subtype="slow_attack_only",
        )


def test_substitution_error_requires_possession_and_review_for_other() -> None:
    with pytest.raises(NoShotAttackContractError, match="substitution_error_requires_team_possession"):
        validate_record(
            event_code="bad_substitution_attack",
            **{**BASE_KWARGS, "team_in_possession": False},
            substitution_error_subtype="early_entry",
        )

    with pytest.raises(NoShotAttackContractError, match="review_marker_required"):
        validate_record(
            event_code="bad_substitution_attack",
            **BASE_KWARGS,
            substitution_error_subtype="substitution_violation_other",
        )

    validate_record(
        event_code="bad_substitution_attack",
        **BASE_KWARGS,
        substitution_error_subtype="substitution_violation_other",
        review_marker=True,
    )


def test_turnover_unclassified_requires_review_marker() -> None:
    with pytest.raises(NoShotAttackContractError, match="review_marker_required"):
        validate_record(event_code="turnover_unclassified", **BASE_KWARGS)


def test_points_must_be_zero() -> None:
    with pytest.raises(NoShotAttackContractError, match="points_must_be_zero"):
        validate_record(
            event_code="technical_error_unforced",
            **BASE_KWARGS,
            technical_error_subtype="bad_pass",
            points=1,
        )
