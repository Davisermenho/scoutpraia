"""Contract tests for the Finalização v1.0 scout module.

These tests intentionally model the spreadsheet/operational-contract rules in a
small in-memory structure. They do not enable import of the module in the app.
Their purpose is to lock the approved taxonomy decisions before implementation.
"""

from __future__ import annotations

import pytest


FINALIZATION_EVENTS = {
    "simple_shot": {
        "ui_type": "botao_principal",
        "module_contract_status": "contrato_pronto_para_teste",
        "import_rule_v1": "nao_importar_v1",
    },
    "spin_shot": {
        "ui_type": "botao_principal",
        "module_contract_status": "contrato_pronto_para_teste",
        "import_rule_v1": "nao_importar_v1",
    },
    "inflight_shot": {
        "ui_type": "botao_principal",
        "module_contract_status": "contrato_pronto_para_teste",
        "import_rule_v1": "nao_importar_v1",
    },
    "goalkeeper_shot": {
        "ui_type": "botao_principal",
        "module_contract_status": "contrato_pronto_para_teste",
        "import_rule_v1": "nao_importar_v1",
    },
    "six_metre_throw": {
        "ui_type": "botao_principal",
        "module_contract_status": "contrato_pronto_para_teste",
        "import_rule_v1": "nao_importar_v1",
    },
    "specialist_finish_role": {
        "ui_type": "campo_auxiliar",
        "module_contract_status": "reclassificado_auxiliar",
        "import_rule_v1": "nao_importar_v1",
    },
}

SCORER_ROLES = {"field_player", "specialist", "goalkeeper"}

ALLOWED_RESULTS_BY_EVENT = {
    "simple_shot": {"goal", "save", "shot_wide", "shot_blocked"},
    "spin_shot": {"goal", "save", "shot_wide", "shot_blocked"},
    "inflight_shot": {"goal", "save", "shot_wide", "shot_blocked"},
    "goalkeeper_shot": {"goal", "save", "shot_wide"},
    "six_metre_throw": {
        "goal",
        "save",
        "shot_wide",
        "rebound_live",
        "execution_invalid_6m",
    },
}

POINT_RULES = {
    ("simple_shot", "goal", "field_player"): 1,
    ("simple_shot", "goal", "specialist"): 2,
    ("simple_shot", "save", "any_valid"): 0,
    ("simple_shot", "shot_wide", "any_valid"): 0,
    ("simple_shot", "shot_blocked", "any_valid"): 0,
    ("spin_shot", "goal", "any_valid"): 2,
    ("spin_shot", "save", "any_valid"): 0,
    ("spin_shot", "shot_wide", "any_valid"): 0,
    ("spin_shot", "shot_blocked", "any_valid"): 0,
    ("inflight_shot", "goal", "any_valid"): 2,
    ("inflight_shot", "save", "any_valid"): 0,
    ("inflight_shot", "shot_wide", "any_valid"): 0,
    ("inflight_shot", "shot_blocked", "any_valid"): 0,
    ("goalkeeper_shot", "goal", "goalkeeper"): 2,
    ("goalkeeper_shot", "save", "goalkeeper"): 0,
    ("goalkeeper_shot", "shot_wide", "goalkeeper"): 0,
    ("six_metre_throw", "goal", "field_player"): 2,
    ("six_metre_throw", "goal", "specialist"): 2,
    ("six_metre_throw", "save", "any_valid"): 0,
    ("six_metre_throw", "shot_wide", "any_valid"): 0,
    ("six_metre_throw", "rebound_live", "any_valid"): 0,
    ("six_metre_throw", "execution_invalid_6m", "any_valid"): 0,
}

FORBIDDEN_EVENT_CODES = {"specialist_shot"}
FORBIDDEN_POSITION_CODES = {"specialist"}


class ContractError(ValueError):
    """Raised when a Finalização v1.0 contract rule is violated."""


def result_allowed(event_code: str, result_possession: str) -> bool:
    return result_possession in ALLOWED_RESULTS_BY_EVENT.get(event_code, set())


def derive_points(event_code: str, result_possession: str, scorer_role: str) -> int:
    if scorer_role not in SCORER_ROLES:
        raise ContractError("invalid_scorer_role")
    if not result_allowed(event_code, result_possession):
        raise ContractError("result_not_allowed_for_event")

    exact_key = (event_code, result_possession, scorer_role)
    wildcard_key = (event_code, result_possession, "any_valid")
    if exact_key in POINT_RULES:
        return POINT_RULES[exact_key]
    if wildcard_key in POINT_RULES:
        return POINT_RULES[wildcard_key]
    raise ContractError("no_points_rule_match")


def validate_record(
    *,
    event_code: str,
    result_possession: str,
    scorer_role: str,
    position_code: str | None = None,
    manual_points: int | None = None,
) -> int:
    if event_code in FORBIDDEN_EVENT_CODES:
        raise ContractError("forbidden_event_code")
    if position_code in FORBIDDEN_POSITION_CODES:
        raise ContractError("forbidden_position_code")
    if result_possession == "lost_possession_no_shot":
        raise ContractError("lost_possession_no_shot_forbidden")
    if event_code == "goalkeeper_shot" and scorer_role != "goalkeeper":
        raise ContractError("goalkeeper_shot_requires_goalkeeper_role")

    derived_points = derive_points(event_code, result_possession, scorer_role)
    if manual_points is not None and manual_points != derived_points:
        raise ContractError("manual_points_mismatch")
    return derived_points


def test_finalization_v1_keeps_import_blocked_until_acceptance() -> None:
    assert {
        event_code
        for event_code, config in FINALIZATION_EVENTS.items()
        if config["ui_type"] == "botao_principal"
    } == {
        "simple_shot",
        "spin_shot",
        "inflight_shot",
        "goalkeeper_shot",
        "six_metre_throw",
    }

    for event_code in {
        "simple_shot",
        "spin_shot",
        "inflight_shot",
        "goalkeeper_shot",
        "six_metre_throw",
    }:
        assert FINALIZATION_EVENTS[event_code]["module_contract_status"] == (
            "contrato_pronto_para_teste"
        )
        assert FINALIZATION_EVENTS[event_code]["import_rule_v1"] == "nao_importar_v1"


def test_specialist_finish_role_is_auxiliary_not_a_button() -> None:
    specialist = FINALIZATION_EVENTS["specialist_finish_role"]

    assert specialist["ui_type"] == "campo_auxiliar"
    assert specialist["module_contract_status"] == "reclassificado_auxiliar"
    assert specialist["import_rule_v1"] == "nao_importar_v1"
    assert "specialist_shot" not in FINALIZATION_EVENTS


@pytest.mark.parametrize(
    ("event_code", "result_possession", "scorer_role", "expected_points"),
    [
        ("simple_shot", "goal", "field_player", 1),
        ("simple_shot", "goal", "specialist", 2),
        ("simple_shot", "save", "specialist", 0),
        ("spin_shot", "goal", "specialist", 2),
        ("inflight_shot", "goal", "specialist", 2),
        ("goalkeeper_shot", "goal", "goalkeeper", 2),
        ("six_metre_throw", "goal", "field_player", 2),
        ("six_metre_throw", "rebound_live", "field_player", 0),
        ("six_metre_throw", "execution_invalid_6m", "specialist", 0),
    ],
)
def test_points_are_derived_from_event_result_and_scorer_role(
    event_code: str,
    result_possession: str,
    scorer_role: str,
    expected_points: int,
) -> None:
    assert derive_points(event_code, result_possession, scorer_role) == expected_points


@pytest.mark.parametrize(
    ("event_code", "result_possession"),
    [
        ("simple_shot", "goal"),
        ("simple_shot", "shot_blocked"),
        ("spin_shot", "shot_blocked"),
        ("inflight_shot", "shot_blocked"),
        ("goalkeeper_shot", "save"),
        ("six_metre_throw", "rebound_live"),
        ("six_metre_throw", "execution_invalid_6m"),
    ],
)
def test_result_matrix_accepts_only_allowed_event_results(
    event_code: str,
    result_possession: str,
) -> None:
    assert result_allowed(event_code, result_possession)


@pytest.mark.parametrize(
    ("event_code", "result_possession", "scorer_role"),
    [
        ("simple_shot", "execution_invalid_6m", "field_player"),
        ("spin_shot", "rebound_live", "specialist"),
        ("inflight_shot", "execution_invalid_6m", "specialist"),
        ("goalkeeper_shot", "shot_blocked", "goalkeeper"),
        ("goalkeeper_shot", "rebound_live", "goalkeeper"),
        ("six_metre_throw", "shot_blocked", "field_player"),
    ],
)
def test_result_matrix_blocks_invalid_event_results(
    event_code: str,
    result_possession: str,
    scorer_role: str,
) -> None:
    with pytest.raises(ContractError, match="result_not_allowed_for_event"):
        derive_points(event_code, result_possession, scorer_role)


def test_blocks_specialist_as_event_or_position() -> None:
    with pytest.raises(ContractError, match="forbidden_event_code"):
        validate_record(
            event_code="specialist_shot",
            result_possession="goal",
            scorer_role="specialist",
        )

    with pytest.raises(ContractError, match="forbidden_position_code"):
        validate_record(
            event_code="simple_shot",
            result_possession="goal",
            scorer_role="specialist",
            position_code="specialist",
        )


def test_blocks_lost_possession_no_shot_in_finalization() -> None:
    with pytest.raises(ContractError, match="lost_possession_no_shot_forbidden"):
        validate_record(
            event_code="six_metre_throw",
            result_possession="lost_possession_no_shot",
            scorer_role="field_player",
        )


def test_goalkeeper_shot_requires_goalkeeper_scorer_role() -> None:
    with pytest.raises(ContractError, match="goalkeeper_shot_requires_goalkeeper_role"):
        validate_record(
            event_code="goalkeeper_shot",
            result_possession="goal",
            scorer_role="field_player",
        )


def test_blocks_manual_points_that_diverge_from_derived_points() -> None:
    with pytest.raises(ContractError, match="manual_points_mismatch"):
        validate_record(
            event_code="simple_shot",
            result_possession="goal",
            scorer_role="specialist",
            manual_points=1,
        )

    with pytest.raises(ContractError, match="manual_points_mismatch"):
        validate_record(
            event_code="spin_shot",
            result_possession="goal",
            scorer_role="specialist",
            manual_points=1,
        )


def test_accepts_manual_points_only_when_matching_derived_points() -> None:
    assert (
        validate_record(
            event_code="simple_shot",
            result_possession="goal",
            scorer_role="field_player",
            manual_points=1,
        )
        == 1
    )
    assert (
        validate_record(
            event_code="simple_shot",
            result_possession="goal",
            scorer_role="specialist",
            manual_points=2,
        )
        == 2
    )