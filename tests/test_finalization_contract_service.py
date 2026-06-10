from __future__ import annotations

import pytest

from scoutpraia.services.finalization_contract_service import (
    FinalizationContractError,
    FinalizationRecordInput,
    derive_points,
    result_allowed,
    validate_record,
    validate_record_input,
)


@pytest.mark.parametrize(
    ("event_code", "result_possession", "scorer_role", "expected_points"),
    [
        ("simple_shot", "goal", "field_player", 1),
        ("simple_shot", "goal", "specialist", 2),
        ("simple_shot", "save", "specialist", 0),
        ("six_metre_throw", "rebound_live", "field_player", 0),
    ],
)
def test_derive_points_matches_required_contract_cases(
    event_code: str,
    result_possession: str,
    scorer_role: str,
    expected_points: int,
) -> None:
    assert derive_points(event_code, result_possession, scorer_role) == expected_points


def test_result_matrix_accepts_six_metre_throw_specific_results() -> None:
    assert result_allowed("six_metre_throw", "goal")
    assert result_allowed("six_metre_throw", "save")
    assert result_allowed("six_metre_throw", "shot_wide")
    assert result_allowed("six_metre_throw", "rebound_live")
    assert result_allowed("six_metre_throw", "execution_invalid_6m")


@pytest.mark.parametrize(
    ("event_code", "result_possession"),
    [
        ("six_metre_throw", "shot_blocked"),
        ("goalkeeper_shot", "shot_blocked"),
    ],
)
def test_service_blocks_results_forbidden_by_contract(
    event_code: str,
    result_possession: str,
) -> None:
    with pytest.raises(FinalizationContractError, match="result_not_allowed_for_event"):
        derive_points(event_code, result_possession, "goalkeeper")


def test_service_blocks_manual_points_divergent_from_derived_points() -> None:
    with pytest.raises(FinalizationContractError, match="manual_points_mismatch"):
        validate_record(
            event_code="simple_shot",
            result_possession="goal",
            scorer_role="specialist",
            manual_points=1,
        )


def test_service_blocks_specialist_position_code() -> None:
    with pytest.raises(FinalizationContractError, match="forbidden_position_code"):
        validate_record(
            event_code="simple_shot",
            result_possession="goal",
            scorer_role="specialist",
            position_code="specialist",
        )


def test_service_blocks_specialist_shot_event_code() -> None:
    with pytest.raises(FinalizationContractError, match="forbidden_event_code"):
        validate_record(
            event_code="specialist_shot",
            result_possession="goal",
            scorer_role="specialist",
        )


def test_service_blocks_lost_possession_without_shot() -> None:
    with pytest.raises(FinalizationContractError, match="lost_possession_no_shot_forbidden"):
        validate_record(
            event_code="simple_shot",
            result_possession="lost_possession_no_shot",
            scorer_role="field_player",
        )


def test_service_requires_goalkeeper_role_for_goalkeeper_shot() -> None:
    with pytest.raises(
        FinalizationContractError,
        match="goalkeeper_shot_requires_goalkeeper_role",
    ):
        validate_record(
            event_code="goalkeeper_shot",
            result_possession="goal",
            scorer_role="field_player",
        )


def test_validate_record_input_supports_real_service_call_shape() -> None:
    record = FinalizationRecordInput(
        event_code="simple_shot",
        result_possession="goal",
        scorer_role="field_player",
        manual_points=1,
    )

    assert validate_record_input(record) == 1
