"""Contract tests for the Criação ofensiva v1.0 scout module.

These tests intentionally model the spreadsheet/operational-contract rules in a
small in-memory structure. They do not enable import of the module in the app.
Their purpose is to lock the current offensive-creation taxonomy decisions before
implementation.
"""

from __future__ import annotations

import pytest


OFFENSIVE_CREATION_EVENTS = {
    "assist_to_finalization": {
        "ui_type": "botao_principal",
        "module_contract_status": "arquitetura_em_definicao",
        "import_rule_v1": "nao_importar_v1",
    },
    "assist_to_inflight_shot": {
        "ui_type": "campo_auxiliar",
        "module_contract_status": "reclassificado_auxiliar",
        "import_rule_v1": "nao_importar_v1",
        "maps_to": "assist_to_finalization",
    },
    "pivot_feed_to_shot": {
        "ui_type": "campo_auxiliar",
        "module_contract_status": "reclassificado_auxiliar",
        "import_rule_v1": "nao_importar_v1",
        "maps_to": "assist_to_finalization",
    },
    "advantage_pass_to_free_player": {
        "ui_type": "botao_secundario_revisao",
        "module_contract_status": "arquitetura_em_revisao",
        "import_rule_v1": "nao_importar_v1",
    },
    "collective_action_creates_shot": {
        "ui_type": "fallback_revisao",
        "module_contract_status": "arquitetura_em_revisao",
        "import_rule_v1": "nao_importar_v1",
    },
}

ACTIVE_CORE_CREATION_TYPES = {
    "direct_assist": {
        "allowed_with": "assist_to_finalization",
        "required_result_creation": "shot_created",
        "requires_review_marker": False,
    },
    "inflight_setup": {
        "allowed_with": "assist_to_finalization",
        "required_result_creation": "shot_created",
        "requires_review_marker": False,
        "required_created_finalization_type": "inflight_shot",
    },
    "pivot_feed": {
        "allowed_with": "assist_to_finalization",
        "required_result_creation": "shot_created",
        "requires_review_marker": False,
    },
}

REVIEW_CREATION_TYPES = {
    "free_player_pass_review": {
        "allowed_with": "advantage_pass_to_free_player",
        "required_result_creation": "clear_chance_created",
        "requires_review_marker": True,
        "requires_created_advantage": True,
    },
    "defense_shift_creation_review": {
        "allowed_with": "collective_action_creates_shot",
        "allowed_result_creation": {"shot_created", "clear_chance_created"},
        "requires_review_marker": True,
    },
    "planned_collective_action_review": {
        "allowed_with": "collective_action_creates_shot",
        "allowed_result_creation": {"shot_created", "clear_chance_created"},
        "requires_review_marker": True,
    },
}

ALL_CREATION_TYPES = {**ACTIVE_CORE_CREATION_TYPES, **REVIEW_CREATION_TYPES}

ACTIVE_RESULT_CREATIONS = {
    "shot_created",
    "clear_chance_created",
    "advantage_lost_no_turnover",
    "no_clear_advantage_review",
}

FORBIDDEN_FIELDS = {
    "points",
    "goal_zone",
    "shot_origin_depth",
}

TACTICAL_POSITION_SOURCE = "POSIÇÕES"
COURT_ZONE_SOURCE = "ZONAS_QUADRA"
FORBIDDEN_ACTIVE_RESULTS = {"turnover_after_creation_error"}


class ContractError(ValueError):
    """Raised when an Offensive Creation v1.0 contract rule is violated."""


def validate_creation_record(
    *,
    event_code: str,
    creation_type: str,
    result_creation: str,
    passer_id: str | None = "athlete_passer",
    receiver_id: str | None = "athlete_receiver",
    system_code: str | None = "AT_3X1",
    created_finalization_type: str | None = "simple_shot",
    review_marker: bool = False,
    created_advantage: str | None = None,
    pass_origin_position: str | None = "Central",
    receiver_position: str | None = "Lateral Direita",
    pass_origin_zone: str | None = "lane_3_central_axis",
    receiver_zone: str | None = "depth_3_near_area",
    linked_finalization_id: str | None = None,
    extra_fields: dict[str, object] | None = None,
) -> None:
    if event_code not in OFFENSIVE_CREATION_EVENTS:
        raise ContractError("unknown_event_code")

    event_config = OFFENSIVE_CREATION_EVENTS[event_code]
    if event_config["import_rule_v1"] != "nao_importar_v1":
        raise ContractError("import_must_stay_blocked")

    if event_code in {"assist_to_inflight_shot", "pivot_feed_to_shot"}:
        raise ContractError("reclassified_event_cannot_be_active")

    if creation_type not in ALL_CREATION_TYPES:
        raise ContractError("unknown_creation_type")

    if result_creation in FORBIDDEN_ACTIVE_RESULTS:
        raise ContractError("turnover_result_forbidden")

    if result_creation not in ACTIVE_RESULT_CREATIONS:
        raise ContractError("unknown_result_creation")

    if extra_fields:
        forbidden_present = FORBIDDEN_FIELDS.intersection(extra_fields)
        if forbidden_present:
            raise ContractError("forbidden_field_for_creation")
        if "result_possession" in extra_fields and linked_finalization_id is None:
            raise ContractError("result_possession_requires_linked_finalization")

    type_config = ALL_CREATION_TYPES[creation_type]
    if type_config["allowed_with"] != event_code:
        raise ContractError("creation_type_used_with_wrong_event")

    if type_config.get("requires_review_marker") and not review_marker:
        raise ContractError("review_marker_required")

    expected_result = type_config.get("required_result_creation")
    allowed_results = type_config.get("allowed_result_creation")
    if expected_result and result_creation != expected_result:
        raise ContractError("invalid_result_for_creation_type")
    if allowed_results and result_creation not in allowed_results:
        raise ContractError("invalid_result_for_creation_type")

    required_finalization_type = type_config.get("required_created_finalization_type")
    if required_finalization_type and created_finalization_type != required_finalization_type:
        raise ContractError("invalid_created_finalization_type")

    if result_creation == "shot_created" and not created_finalization_type:
        raise ContractError("created_finalization_type_required")

    if event_code in {"assist_to_finalization", "advantage_pass_to_free_player"}:
        if not passer_id or not receiver_id or not system_code:
            raise ContractError("pass_based_core_fields_required")
        if not (pass_origin_position or pass_origin_zone):
            raise ContractError("pass_origin_location_required")
        if not (receiver_position or receiver_zone):
            raise ContractError("receiver_location_required")

    if event_code == "advantage_pass_to_free_player" and not created_advantage:
        raise ContractError("created_advantage_required")

    if event_code == "collective_action_creates_shot":
        if not system_code:
            raise ContractError("system_code_required")
        if not review_marker:
            raise ContractError("review_marker_required")



def test_offensive_creation_v1_keeps_import_blocked() -> None:
    assert {
        event_code
        for event_code, config in OFFENSIVE_CREATION_EVENTS.items()
        if config["ui_type"] == "botao_principal"
    } == {"assist_to_finalization"}

    for config in OFFENSIVE_CREATION_EVENTS.values():
        assert config["import_rule_v1"] == "nao_importar_v1"


@pytest.mark.parametrize(
    "event_code",
    ["assist_to_inflight_shot", "pivot_feed_to_shot"],
)
def test_reclassified_events_are_not_active_buttons(event_code: str) -> None:
    with pytest.raises(ContractError, match="reclassified_event_cannot_be_active"):
        validate_creation_record(
            event_code=event_code,
            creation_type="direct_assist",
            result_creation="shot_created",
        )


@pytest.mark.parametrize(
    ("creation_type", "created_finalization_type"),
    [
        ("direct_assist", "simple_shot"),
        ("inflight_setup", "inflight_shot"),
        ("pivot_feed", "spin_shot"),
    ],
)
def test_core_assist_to_finalization_accepts_only_active_creation_types(
    creation_type: str,
    created_finalization_type: str,
) -> None:
    validate_creation_record(
        event_code="assist_to_finalization",
        creation_type=creation_type,
        result_creation="shot_created",
        created_finalization_type=created_finalization_type,
    )


@pytest.mark.parametrize(
    "creation_type",
    [
        "free_player_pass_review",
        "defense_shift_creation_review",
        "planned_collective_action_review",
    ],
)
def test_review_creation_types_cannot_be_used_in_core_assist_event(
    creation_type: str,
) -> None:
    with pytest.raises(ContractError, match="creation_type_used_with_wrong_event"):
        validate_creation_record(
            event_code="assist_to_finalization",
            creation_type=creation_type,
            result_creation="shot_created",
        )


def test_inflight_setup_requires_inflight_finalization_type() -> None:
    with pytest.raises(ContractError, match="invalid_created_finalization_type"):
        validate_creation_record(
            event_code="assist_to_finalization",
            creation_type="inflight_setup",
            result_creation="shot_created",
            created_finalization_type="simple_shot",
        )


@pytest.mark.parametrize(
    "extra_fields",
    [
        {"points": 2},
        {"goal_zone": "high_left"},
        {"shot_origin_depth": "depth_3_near_area"},
    ],
)
def test_creation_forbids_finalization_fields(extra_fields: dict[str, object]) -> None:
    with pytest.raises(ContractError, match="forbidden_field_for_creation"):
        validate_creation_record(
            event_code="assist_to_finalization",
            creation_type="direct_assist",
            result_creation="shot_created",
            extra_fields=extra_fields,
        )


def test_result_possession_requires_linked_finalization() -> None:
    with pytest.raises(ContractError, match="result_possession_requires_linked_finalization"):
        validate_creation_record(
            event_code="assist_to_finalization",
            creation_type="direct_assist",
            result_creation="shot_created",
            extra_fields={"result_possession": "goal"},
        )

    validate_creation_record(
        event_code="assist_to_finalization",
        creation_type="direct_assist",
        result_creation="shot_created",
        linked_finalization_id="evt-finalization-001",
        extra_fields={"result_possession": "goal"},
    )


def test_turnover_after_creation_error_is_not_active_creation_result() -> None:
    with pytest.raises(ContractError, match="turnover_result_forbidden"):
        validate_creation_record(
            event_code="assist_to_finalization",
            creation_type="direct_assist",
            result_creation="turnover_after_creation_error",
        )


def test_pass_based_events_require_origin_and_receiver_location() -> None:
    with pytest.raises(ContractError, match="pass_origin_location_required"):
        validate_creation_record(
            event_code="assist_to_finalization",
            creation_type="direct_assist",
            result_creation="shot_created",
            pass_origin_position=None,
            pass_origin_zone=None,
        )

    with pytest.raises(ContractError, match="receiver_location_required"):
        validate_creation_record(
            event_code="assist_to_finalization",
            creation_type="direct_assist",
            result_creation="shot_created",
            receiver_position=None,
            receiver_zone=None,
        )


def test_tactical_positions_and_court_zones_have_distinct_sources() -> None:
    assert TACTICAL_POSITION_SOURCE == "POSIÇÕES"
    assert COURT_ZONE_SOURCE == "ZONAS_QUADRA"
    assert TACTICAL_POSITION_SOURCE != COURT_ZONE_SOURCE


def test_advantage_pass_stays_under_review_with_required_marker() -> None:
    with pytest.raises(ContractError, match="review_marker_required"):
        validate_creation_record(
            event_code="advantage_pass_to_free_player",
            creation_type="free_player_pass_review",
            result_creation="clear_chance_created",
            created_advantage="free_player",
        )

    with pytest.raises(ContractError, match="created_advantage_required"):
        validate_creation_record(
            event_code="advantage_pass_to_free_player",
            creation_type="free_player_pass_review",
            result_creation="clear_chance_created",
            review_marker=True,
        )

    validate_creation_record(
        event_code="advantage_pass_to_free_player",
        creation_type="free_player_pass_review",
        result_creation="clear_chance_created",
        created_advantage="free_player",
        review_marker=True,
    )


@pytest.mark.parametrize(
    "creation_type",
    ["defense_shift_creation_review", "planned_collective_action_review"],
)
def test_collective_action_stays_fallback_with_review_marker(
    creation_type: str,
) -> None:
    with pytest.raises(ContractError, match="review_marker_required"):
        validate_creation_record(
            event_code="collective_action_creates_shot",
            creation_type=creation_type,
            result_creation="shot_created",
        )

    validate_creation_record(
        event_code="collective_action_creates_shot",
        creation_type=creation_type,
        result_creation="shot_created",
        review_marker=True,
    )
