from __future__ import annotations

import pytest

from scoutpraia.services.no_shot_attack_contract_service import (
    NoShotAttackContractError,
    NoShotAttackRecordInput,
    validate_record,
    validate_record_input,
)


def test_valid_ball_control_turnover_passes() -> None:
    assert (
        validate_record(
            event_code="ball_control_turnover",
            result_possession="lost_possession_no_shot",
            team_in_possession=True,
            turnover_cause_detail="bad_pass",
        )
        == "ball_control_turnover"
    )


def test_area_invasion_is_not_forced_error() -> None:
    with pytest.raises(NoShotAttackContractError, match="area_invasion_not_forced_error"):
        validate_record(
            event_code="ball_control_turnover",
            result_possession="lost_possession_no_shot",
            team_in_possession=True,
            turnover_cause_detail="area_invasion",
        )


def test_specialist_late_is_not_direct_turnover_cause() -> None:
    with pytest.raises(
        NoShotAttackContractError,
        match="specialist_late_not_direct_turnover_cause",
    ):
        validate_record(
            event_code="ball_control_turnover",
            result_possession="lost_possession_no_shot",
            team_in_possession=True,
            turnover_cause_detail="specialist_late",
        )


def test_substitution_error_requires_team_possession_and_turnover() -> None:
    with pytest.raises(
        NoShotAttackContractError,
        match="substitution_error_requires_team_possession",
    ):
        validate_record(
            event_code="substitution_error_turnover",
            result_possession="lost_possession_no_shot",
            team_in_possession=False,
            turnover_cause_detail="illegal_substitution",
        )

    assert (
        validate_record(
            event_code="substitution_error_turnover",
            result_possession="lost_possession_no_shot",
            team_in_possession=True,
            turnover_cause_detail="illegal_substitution",
        )
        == "substitution_error_turnover"
    )


def test_passive_play_accepts_only_approved_subtypes() -> None:
    assert (
        validate_record(
            event_code="passive_play_turnover",
            result_possession="lost_possession_no_shot",
            team_in_possession=True,
            passive_subtype="forewarning_expired",
        )
        == "passive_play_turnover"
    )

    with pytest.raises(NoShotAttackContractError, match="invalid_passive_subtype"):
        validate_record(
            event_code="passive_play_turnover",
            result_possession="lost_possession_no_shot",
            team_in_possession=True,
            passive_subtype="slow_rebuild",
        )


def test_finalization_events_do_not_enter_no_shot_attack() -> None:
    with pytest.raises(NoShotAttackContractError, match="forbidden_event_code"):
        validate_record(
            event_code="simple_shot",
            result_possession="lost_possession_no_shot",
            team_in_possession=True,
        )


def test_offensive_transition_does_not_enter_no_shot_attack() -> None:
    with pytest.raises(NoShotAttackContractError, match="forbidden_event_code"):
        validate_record(
            event_code="fast_break_for",
            result_possession="lost_possession_no_shot",
            team_in_possession=True,
        )


def test_shot_attempted_is_rejected_in_no_shot_attack() -> None:
    with pytest.raises(NoShotAttackContractError, match="shot_not_allowed_in_no_shot_attack"):
        validate_record(
            event_code="ball_control_turnover",
            result_possession="lost_possession_no_shot",
            team_in_possession=True,
            shot_attempted=True,
        )


def test_record_input_shape_is_supported() -> None:
    record = NoShotAttackRecordInput(
        event_code="offensive_foul_turnover",
        result_possession="lost_possession_no_shot",
        team_in_possession=True,
        turnover_cause_detail="area_invasion",
    )

    assert validate_record_input(record) == "offensive_foul_turnover"
