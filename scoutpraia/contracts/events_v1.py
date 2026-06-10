"""Declarative registry for Eventos v1 modules.

This module intentionally does not integrate with the active taxonomy seed, UI,
or persistence layer yet. It only codifies the validated contract surface that
must remain blocked from import until the later gates pass.
"""

from __future__ import annotations

from dataclasses import dataclass

IMPORT_RULE_V1_BLOCKED = "nao_importar_v1"
MODULE_STATUS_VALIDATED = "contrato_validado"
EVENT_STATUS_READY_FOR_TEST = "contrato_pronto_para_teste"
EVENT_STATUS_AUXILIARY = "reclassificado_auxiliar"

SHOT_RESULTS = frozenset(
    {
        "goal",
        "save",
        "shot_wide",
        "shot_blocked",
        "rebound_live",
        "execution_invalid_6m",
    }
)
NO_SHOT_RESULT = "lost_possession_no_shot"


@dataclass(frozen=True)
class EventContract:
    event_code: str
    ui_type: str
    module_contract_status: str
    import_rule_v1: str
    allowed_results: frozenset[str]


@dataclass(frozen=True)
class ModuleContract:
    module_code: str
    display_name: str
    module_contract_status: str
    import_rule_v1: str
    primary_events: tuple[EventContract, ...]
    auxiliary_fields: tuple[EventContract, ...]
    forbidden_event_codes: frozenset[str]
    forbidden_results: frozenset[str]

    def event_contracts(self) -> tuple[EventContract, ...]:
        return self.primary_events + self.auxiliary_fields


def _primary_event(event_code: str, *, allowed_results: frozenset[str]) -> EventContract:
    return EventContract(
        event_code=event_code,
        ui_type="botao_principal",
        module_contract_status=EVENT_STATUS_READY_FOR_TEST,
        import_rule_v1=IMPORT_RULE_V1_BLOCKED,
        allowed_results=allowed_results,
    )


def _auxiliary_field(event_code: str) -> EventContract:
    return EventContract(
        event_code=event_code,
        ui_type="campo_auxiliar",
        module_contract_status=EVENT_STATUS_AUXILIARY,
        import_rule_v1=IMPORT_RULE_V1_BLOCKED,
        allowed_results=frozenset(),
    )


FINALIZATION_V1 = ModuleContract(
    module_code="finalization_v1",
    display_name="Finalizacao v1.0",
    module_contract_status=MODULE_STATUS_VALIDATED,
    import_rule_v1=IMPORT_RULE_V1_BLOCKED,
    primary_events=(
        _primary_event(
            "simple_shot",
            allowed_results=frozenset({"goal", "save", "shot_wide", "shot_blocked"}),
        ),
        _primary_event(
            "spin_shot",
            allowed_results=frozenset({"goal", "save", "shot_wide", "shot_blocked"}),
        ),
        _primary_event(
            "inflight_shot",
            allowed_results=frozenset({"goal", "save", "shot_wide", "shot_blocked"}),
        ),
        _primary_event(
            "goalkeeper_shot",
            allowed_results=frozenset({"goal", "save", "shot_wide"}),
        ),
        _primary_event(
            "six_metre_throw",
            allowed_results=frozenset(
                {"goal", "save", "shot_wide", "rebound_live", "execution_invalid_6m"}
            ),
        ),
    ),
    auxiliary_fields=(
        _auxiliary_field("specialist_finish_role"),
    ),
    forbidden_event_codes=frozenset({"specialist_shot", "shootout_attempt"}),
    forbidden_results=frozenset({NO_SHOT_RESULT}),
)


# Conservative coding names for the no-shot module. They stay local to the
# contract registry until the later migration and taxonomy gates define the
# persistent representation.
NO_SHOT_ATTACK_V1 = ModuleContract(
    module_code="no_shot_attack_v1",
    display_name="Ataque sem finalizacao v1.0",
    module_contract_status=MODULE_STATUS_VALIDATED,
    import_rule_v1=IMPORT_RULE_V1_BLOCKED,
    primary_events=(
        _primary_event(
            "ball_control_turnover",
            allowed_results=frozenset({NO_SHOT_RESULT}),
        ),
        _primary_event(
            "offensive_foul_turnover",
            allowed_results=frozenset({NO_SHOT_RESULT}),
        ),
        _primary_event(
            "passive_play_turnover",
            allowed_results=frozenset({NO_SHOT_RESULT}),
        ),
        _primary_event(
            "substitution_error_turnover",
            allowed_results=frozenset({NO_SHOT_RESULT}),
        ),
    ),
    auxiliary_fields=(
        _auxiliary_field("turnover_cause_detail"),
    ),
    forbidden_event_codes=frozenset(
        {
            "simple_shot",
            "spin_shot",
            "inflight_shot",
            "goalkeeper_shot",
            "six_metre_throw",
            "shootout_attempt",
            "fast_break_for",
        }
    ),
    forbidden_results=SHOT_RESULTS,
)


MODULE_CONTRACTS_V1 = {
    FINALIZATION_V1.module_code: FINALIZATION_V1,
    NO_SHOT_ATTACK_V1.module_code: NO_SHOT_ATTACK_V1,
}


def get_module_contract(module_code: str) -> ModuleContract:
    try:
        return MODULE_CONTRACTS_V1[module_code]
    except KeyError as exc:
        raise ValueError(f"Modulo de contrato v1 nao encontrado: {module_code}") from exc


def list_primary_event_codes(module_code: str) -> tuple[str, ...]:
    return tuple(
        event_contract.event_code
        for event_contract in get_module_contract(module_code).primary_events
    )


def list_auxiliary_codes(module_code: str) -> tuple[str, ...]:
    return tuple(
        event_contract.event_code
        for event_contract in get_module_contract(module_code).auxiliary_fields
    )


def all_event_codes(module_code: str) -> tuple[str, ...]:
    module_contract = get_module_contract(module_code)
    return tuple(
        event_contract.event_code for event_contract in module_contract.event_contracts()
    )
