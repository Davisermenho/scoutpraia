"""Declarative registry for Eventos v1 modules.

This module codifies the validated contract surface. The active application seed
still uses the legacy taxonomy unless a dedicated migration/import gate wires a
module into the app flow.
"""

from __future__ import annotations

from dataclasses import dataclass

IMPORT_RULE_V1_BLOCKED = "nao_importar_v1"
IMPORT_RULE_V1_ACTIVE = "importar_v1"
MODULE_STATUS_VALIDATED = "contrato_validado"
EVENT_STATUS_READY_FOR_TEST = "contrato_pronto_para_teste"
EVENT_STATUS_ACTIVE = "contrato_ativo_v1"
EVENT_STATUS_REVIEW = "revisar"
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


def _primary_event(
    event_code: str,
    *,
    allowed_results: frozenset[str],
    module_contract_status: str = EVENT_STATUS_READY_FOR_TEST,
    import_rule_v1: str = IMPORT_RULE_V1_BLOCKED,
    ui_type: str = "botao_principal",
) -> EventContract:
    return EventContract(
        event_code=event_code,
        ui_type=ui_type,
        module_contract_status=module_contract_status,
        import_rule_v1=import_rule_v1,
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


NO_SHOT_ACTIVE_RESULT = frozenset({NO_SHOT_RESULT})

NO_SHOT_ATTACK_V1 = ModuleContract(
    module_code="attack_no_shot_v1",
    display_name="Ataque sem finalizacao v1.0",
    module_contract_status=MODULE_STATUS_VALIDATED,
    import_rule_v1=IMPORT_RULE_V1_ACTIVE,
    primary_events=(
        _primary_event(
            "technical_error_unforced",
            allowed_results=NO_SHOT_ACTIVE_RESULT,
            module_contract_status=EVENT_STATUS_ACTIVE,
            import_rule_v1=IMPORT_RULE_V1_ACTIVE,
        ),
        _primary_event(
            "technical_error_forced",
            allowed_results=NO_SHOT_ACTIVE_RESULT,
            module_contract_status=EVENT_STATUS_ACTIVE,
            import_rule_v1=IMPORT_RULE_V1_ACTIVE,
        ),
        _primary_event(
            "offensive_foul",
            allowed_results=NO_SHOT_ACTIVE_RESULT,
            module_contract_status=EVENT_STATUS_ACTIVE,
            import_rule_v1=IMPORT_RULE_V1_ACTIVE,
        ),
        _primary_event(
            "goal_area_invasion_attack",
            allowed_results=NO_SHOT_ACTIVE_RESULT,
            module_contract_status=EVENT_STATUS_ACTIVE,
            import_rule_v1=IMPORT_RULE_V1_ACTIVE,
        ),
        _primary_event(
            "passive_play_turnover",
            allowed_results=NO_SHOT_ACTIVE_RESULT,
            module_contract_status=EVENT_STATUS_ACTIVE,
            import_rule_v1=IMPORT_RULE_V1_ACTIVE,
            ui_type="botao_secundario",
        ),
        _primary_event(
            "bad_substitution_attack",
            allowed_results=NO_SHOT_ACTIVE_RESULT,
            module_contract_status=EVENT_STATUS_ACTIVE,
            import_rule_v1=IMPORT_RULE_V1_ACTIVE,
            ui_type="botao_secundario",
        ),
        _primary_event(
            "turnover_unclassified",
            allowed_results=NO_SHOT_ACTIVE_RESULT,
            module_contract_status=EVENT_STATUS_REVIEW,
            import_rule_v1=IMPORT_RULE_V1_ACTIVE,
            ui_type="fallback_revisao",
        ),
    ),
    auxiliary_fields=(
        _auxiliary_field("technical_error_subtype"),
        _auxiliary_field("passive_play_subtype"),
        _auxiliary_field("substitution_error_subtype"),
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
            "ball_control_turnover",
            "offensive_foul_turnover",
            "substitution_error_turnover",
            "turnover_cause_detail",
        }
    ),
    forbidden_results=SHOT_RESULTS,
)


MODULE_CONTRACTS_V1 = {
    FINALIZATION_V1.module_code: FINALIZATION_V1,
    NO_SHOT_ATTACK_V1.module_code: NO_SHOT_ATTACK_V1,
}

# Backward-compatible alias for older code/tests that still import the interim name.
NO_SHOT_ATTACK_LEGACY_ALIAS = "no_shot_attack_v1"
MODULE_ALIASES_V1 = {NO_SHOT_ATTACK_LEGACY_ALIAS: NO_SHOT_ATTACK_V1.module_code}


def get_module_contract(module_code: str) -> ModuleContract:
    canonical_module_code = MODULE_ALIASES_V1.get(module_code, module_code)
    try:
        return MODULE_CONTRACTS_V1[canonical_module_code]
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
