"""Contract tests for the Defensivo v1.0 scout module.

These tests model the spreadsheet/operational-contract rules in memory. They do
not enable import of the defensive module in the app. The goal is to lock the
current taxonomy decisions before implementation.
"""

from __future__ import annotations

import pytest


DEFENSIVE_EVENTS = {
    "line_block_shot": {
        "ui_type": "botao_principal",
        "module_contract_status": "arquitetura_em_definicao",
        "import_rule_v1": "nao_importar_v1",
    },
    "defensive_pressure_forced_error": {
        "ui_type": "botao_secundario_revisao",
        "module_contract_status": "arquitetura_em_revisao",
        "import_rule_v1": "nao_importar_v1",
    },
    "steal_or_interception": {
        "ui_type": "botao_secundario_revisao",
        "module_contract_status": "arquitetura_em_revisao",
        "import_rule_v1": "nao_importar_v1",
    },
    "defensive_rebound_recovery": {
        "ui_type": "future_module",
        "module_contract_status": "rascunho_modulo_futuro",
        "import_rule_v1": "nao_importar_v1",
    },
}

DEFENSIVE_POSITIONS_BY_SYSTEM = {
    "DEF_3X0": {
        "def_3x0_cobertura",
        "def_3x0_base",
        "def_3x0_solta",
    },
    "DEF_2X1": {
        "def_2x1_cobertura",
        "def_2x1_avancada",
        "def_2x1_solta",
    },
}

ALLOWED_LINKED_FINALIZATION_EVENTS_FOR_BLOCK = {
    "simple_shot",
    "spin_shot",
    "inflight_shot",
}

FORBIDDEN_LINKED_FINALIZATION_EVENTS_FOR_BLOCK = {
    "six_metre_throw",
    "goalkeeper_shot",
}

DEFENSIVE_RESULTS = {
    "shot_blocked_linked": "ativo_nucleo",
    "forced_error_linked": "revisar",
    "possession_won": "revisar_futuro_transicao",
    "rebound_recovered": "futuro",
    "pressure_no_turnover_review": "bloqueado_v1",
}

FORBIDDEN_FIELDS = {
    "points",
    "goal_zone",
    "scorer_role",
    "shot_origin_depth",
}

NAME_UI_VALUES_THAT_ARE_NOT_POSITION_CODES = {
    "Cobertura",
    "Base",
    "Solta",
    "Avançada",
}


class ContractError(ValueError):
    """Raised when a Defensivo v1.0 contract rule is violated."""


def validate_defensive_record(
    *,
    event_code: str,
    result_defense: str,
    defender_id: str | None = "athlete_defender",
    defensive_system_code: str | None = "DEF_3X0",
    defensive_position_code: str | None = "def_3x0_base",
    court_lane: str | None = "lane_3_central_axis",
    court_depth: str | None = "depth_3_near_area",
    linked_finalization_id: str | None = "evt-finalization-001",
    linked_finalization_event_code: str | None = "simple_shot",
    linked_attack_no_shot_id: str | None = None,
    review_marker: bool = False,
    defensive_control_clear: bool = False,
    goalkeeper_action: bool = False,
    imported_v1: bool = False,
    extra_fields: dict[str, object] | None = None,
) -> None:
    if event_code not in DEFENSIVE_EVENTS:
        raise ContractError("unknown_event_code")

    event_config = DEFENSIVE_EVENTS[event_code]
    if event_config["import_rule_v1"] != "nao_importar_v1":
        raise ContractError("import_must_stay_blocked")

    if imported_v1 and event_config["ui_type"] in {"botao_secundario_revisao", "future_module"}:
        raise ContractError("review_or_future_event_cannot_be_imported")

    if goalkeeper_action:
        raise ContractError("goalkeeper_out_of_defensive_v1")

    if result_defense not in DEFENSIVE_RESULTS:
        raise ContractError("unknown_result_defense")

    if extra_fields:
        if FORBIDDEN_FIELDS.intersection(extra_fields):
            raise ContractError("forbidden_field_for_defensive")
        if "result_possession" in extra_fields:
            raise ContractError("result_possession_belongs_to_linked_event")

    if not defender_id:
        raise ContractError("defender_id_required")
    if defensive_system_code not in DEFENSIVE_POSITIONS_BY_SYSTEM:
        raise ContractError("invalid_defensive_system")
    if not defensive_position_code:
        raise ContractError("defensive_position_required")
    if defensive_position_code in NAME_UI_VALUES_THAT_ARE_NOT_POSITION_CODES:
        raise ContractError("position_code_required_not_name_ui")
    if defensive_position_code not in DEFENSIVE_POSITIONS_BY_SYSTEM[defensive_system_code]:
        raise ContractError("defensive_position_incompatible_with_system")

    if event_code == "line_block_shot":
        if result_defense != "shot_blocked_linked":
            raise ContractError("line_block_requires_shot_blocked_linked")
        if not linked_finalization_id:
            raise ContractError("linked_finalization_required")
        if linked_finalization_event_code in FORBIDDEN_LINKED_FINALIZATION_EVENTS_FOR_BLOCK:
            raise ContractError("linked_finalization_event_forbidden_for_block")
        if linked_finalization_event_code not in ALLOWED_LINKED_FINALIZATION_EVENTS_FOR_BLOCK:
            raise ContractError("linked_finalization_event_not_allowed_for_block")
        if not court_lane or not court_depth:
            raise ContractError("court_location_required")

    if event_code == "defensive_pressure_forced_error":
        if result_defense != "forced_error_linked":
            raise ContractError("pressure_requires_forced_error_linked")
        if not linked_attack_no_shot_id:
            raise ContractError("linked_attack_no_shot_required")
        if not review_marker:
            raise ContractError("review_marker_required")

    if event_code == "steal_or_interception":
        if result_defense != "possession_won":
            raise ContractError("steal_requires_possession_won")
        if not defensive_control_clear:
            raise ContractError("defensive_control_required")
        if not review_marker:
            raise ContractError("review_marker_required")

    if event_code == "defensive_rebound_recovery":
        raise ContractError("future_module_not_active")



def test_defensive_v1_keeps_import_blocked_and_single_core_button() -> None:
    assert {
        event_code
        for event_code, config in DEFENSIVE_EVENTS.items()
        if config["ui_type"] == "botao_principal"
    } == {"line_block_shot"}

    for config in DEFENSIVE_EVENTS.values():
        assert config["import_rule_v1"] == "nao_importar_v1"


def test_line_block_shot_accepts_allowed_finalization_links() -> None:
    for linked_event in ALLOWED_LINKED_FINALIZATION_EVENTS_FOR_BLOCK:
        validate_defensive_record(
            event_code="line_block_shot",
            result_defense="shot_blocked_linked",
            linked_finalization_event_code=linked_event,
        )


@pytest.mark.parametrize(
    "linked_event",
    ["six_metre_throw", "goalkeeper_shot"],
)
def test_line_block_shot_rejects_forbidden_finalization_links(linked_event: str) -> None:
    with pytest.raises(ContractError, match="linked_finalization_event_forbidden_for_block"):
        validate_defensive_record(
            event_code="line_block_shot",
            result_defense="shot_blocked_linked",
            linked_finalization_event_code=linked_event,
        )


def test_line_block_shot_requires_linked_finalization() -> None:
    with pytest.raises(ContractError, match="linked_finalization_required"):
        validate_defensive_record(
            event_code="line_block_shot",
            result_defense="shot_blocked_linked",
            linked_finalization_id=None,
        )


def test_line_block_shot_accepts_only_core_result() -> None:
    with pytest.raises(ContractError, match="line_block_requires_shot_blocked_linked"):
        validate_defensive_record(
            event_code="line_block_shot",
            result_defense="forced_error_linked",
        )


@pytest.mark.parametrize(
    ("system_code", "position_code"),
    [
        ("DEF_3X0", "def_3x0_cobertura"),
        ("DEF_3X0", "def_3x0_base"),
        ("DEF_3X0", "def_3x0_solta"),
        ("DEF_2X1", "def_2x1_cobertura"),
        ("DEF_2X1", "def_2x1_avancada"),
        ("DEF_2X1", "def_2x1_solta"),
    ],
)
def test_defensive_positions_are_valid_when_compatible_with_system(
    system_code: str,
    position_code: str,
) -> None:
    validate_defensive_record(
        event_code="line_block_shot",
        result_defense="shot_blocked_linked",
        defensive_system_code=system_code,
        defensive_position_code=position_code,
    )


@pytest.mark.parametrize(
    ("system_code", "position_code"),
    [
        ("DEF_3X0", "def_2x1_avancada"),
        ("DEF_2X1", "def_3x0_base"),
    ],
)
def test_defensive_positions_are_restricted_by_system(
    system_code: str,
    position_code: str,
) -> None:
    with pytest.raises(ContractError, match="defensive_position_incompatible_with_system"):
        validate_defensive_record(
            event_code="line_block_shot",
            result_defense="shot_blocked_linked",
            defensive_system_code=system_code,
            defensive_position_code=position_code,
        )


@pytest.mark.parametrize("name_ui", ["Cobertura", "Base", "Solta", "Avançada"])
def test_defensive_position_code_must_not_use_name_ui(name_ui: str) -> None:
    with pytest.raises(ContractError, match="position_code_required_not_name_ui"):
        validate_defensive_record(
            event_code="line_block_shot",
            result_defense="shot_blocked_linked",
            defensive_position_code=name_ui,
        )


@pytest.mark.parametrize(
    "extra_fields",
    [
        {"points": 2},
        {"goal_zone": "high_left"},
        {"scorer_role": "field_player"},
        {"shot_origin_depth": "depth_3_near_area"},
    ],
)\def test_defensive_forbids_offensive_and_finalization_fields(extra_fields: dict[str, object]) -> None:
    with pytest.raises(ContractError, match="forbidden_field_for_defensive"):
        validate_defensive_record(
            event_code="line_block_shot",
            result_defense="shot_blocked_linked",
            extra_fields=extra_fields,
        )


def test_result_possession_belongs_to_linked_event_not_defensive_record() -> None:
    with pytest.raises(ContractError, match="result_possession_belongs_to_linked_event"):
        validate_defensive_record(
            event_code="line_block_shot",
            result_defense="shot_blocked_linked",
            extra_fields={"result_possession": "shot_blocked"},
        )


def test_goalkeeper_actions_are_out_of_defensive_v1() -> None:
    with pytest.raises(ContractError, match="goalkeeper_out_of_defensive_v1"):
        validate_defensive_record(
            event_code="line_block_shot",
            result_defense="shot_blocked_linked",
            goalkeeper_action=True,
        )


def test_defensive_pressure_forced_error_stays_under_review_with_link() -> None:
    with pytest.raises(ContractError, match="linked_attack_no_shot_required"):
        validate_defensive_record(
            event_code="defensive_pressure_forced_error",
            result_defense="forced_error_linked",
            linked_attack_no_shot_id=None,
            review_marker=True,
        )

    with pytest.raises(ContractError, match="review_marker_required"):
        validate_defensive_record(
            event_code="defensive_pressure_forced_error",
            result_defense="forced_error_linked",
            linked_attack_no_shot_id="evt-attack-no-shot-001",
            review_marker=False,
        )

    validate_defensive_record(
        event_code="defensive_pressure_forced_error",
        result_defense="forced_error_linked",
        linked_attack_no_shot_id="evt-attack-no-shot-001",
        review_marker=True,
    )


def test_steal_or_interception_stays_review_future_with_control() -> None:
    with pytest.raises(ContractError, match="defensive_control_required"):
        validate_defensive_record(
            event_code="steal_or_interception",
            result_defense="possession_won",
            defensive_control_clear=False,
            review_marker=True,
        )

    with pytest.raises(ContractError, match="review_marker_required"):
        validate_defensive_record(
            event_code="steal_or_interception",
            result_defense="possession_won",
            defensive_control_clear=True,
            review_marker=False,
        )

    validate_defensive_record(
        event_code="steal_or_interception",
        result_defense="possession_won",
        defensive_control_clear=True,
        review_marker=True,
    )


def test_defensive_rebound_recovery_is_future_module() -> None:
    with pytest.raises(ContractError, match="future_module_not_active"):
        validate_defensive_record(
            event_code="defensive_rebound_recovery",
            result_defense="rebound_recovered",
            review_marker=True,
        )


def test_review_or_future_events_cannot_be_imported_in_v1() -> None:
    with pytest.raises(ContractError, match="review_or_future_event_cannot_be_imported"):
        validate_defensive_record(
            event_code="steal_or_interception",
            result_defense="possession_won",
            defensive_control_clear=True,
            review_marker=True,
            imported_v1=True,
        )
