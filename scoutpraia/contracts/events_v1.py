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
EVENT_STATUS_FUTURE = "rascunho_modulo_futuro"

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
    review_only_events: tuple[EventContract, ...]
    future_events: tuple[EventContract, ...]
    forbidden_event_codes: frozenset[str]
    forbidden_results: frozenset[str]

    def event_contracts(self) -> tuple[EventContract, ...]:
        return (
            self.primary_events
            + self.auxiliary_fields
            + self.review_only_events
            + self.future_events
        )


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


def _review_event(
    event_code: str,
    *,
    allowed_results: frozenset[str],
    ui_type: str = "botao_secundario_revisao",
) -> EventContract:
    return EventContract(
        event_code=event_code,
        ui_type=ui_type,
        module_contract_status=EVENT_STATUS_REVIEW,
        import_rule_v1=IMPORT_RULE_V1_BLOCKED,
        allowed_results=allowed_results,
    )


def _future_event(
    event_code: str,
    *,
    allowed_results: frozenset[str],
) -> EventContract:
    return EventContract(
        event_code=event_code,
        ui_type="future_module",
        module_contract_status=EVENT_STATUS_FUTURE,
        import_rule_v1=IMPORT_RULE_V1_BLOCKED,
        allowed_results=allowed_results,
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
    review_only_events=(),
    future_events=(),
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
    review_only_events=(),
    future_events=(),
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

OFFENSIVE_CREATION_V1 = ModuleContract(
    module_code="offensive_creation_v1",
    display_name="Criacao ofensiva v1.0",
    module_contract_status=MODULE_STATUS_VALIDATED,
    import_rule_v1=IMPORT_RULE_V1_BLOCKED,
    primary_events=(
        _primary_event(
            "assist_to_finalization",
            allowed_results=frozenset({"shot_created"}),
        ),
    ),
    auxiliary_fields=(
        _auxiliary_field("assist_to_inflight_shot"),
        _auxiliary_field("pivot_feed_to_shot"),
    ),
    review_only_events=(
        _review_event(
            "advantage_pass_to_free_player",
            allowed_results=frozenset({"clear_chance_created"}),
        ),
        _review_event(
            "collective_action_creates_shot",
            allowed_results=frozenset({"shot_created", "clear_chance_created"}),
            ui_type="fallback_revisao",
        ),
    ),
    future_events=(),
    forbidden_event_codes=frozenset(),
    forbidden_results=frozenset({"turnover_after_creation_error"}),
)

DEFENSIVE_V1 = ModuleContract(
    module_code="defensive_v1",
    display_name="Defensivo v1.0",
    module_contract_status=MODULE_STATUS_VALIDATED,
    import_rule_v1=IMPORT_RULE_V1_BLOCKED,
    primary_events=(
        _primary_event(
            "line_block_shot",
            allowed_results=frozenset({"shot_blocked_linked"}),
        ),
    ),
    auxiliary_fields=(),
    review_only_events=(
        _review_event(
            "defensive_pressure_forced_error",
            allowed_results=frozenset({"forced_error_linked"}),
        ),
        _review_event(
            "steal_or_interception",
            allowed_results=frozenset({"possession_won"}),
        ),
    ),
    future_events=(
        _future_event(
            "defensive_rebound_recovery",
            allowed_results=frozenset({"rebound_recovered"}),
        ),
    ),
    forbidden_event_codes=frozenset(),
    forbidden_results=frozenset({"pressure_no_turnover_review"}),
)


MODULE_CONTRACTS_V1 = {
    FINALIZATION_V1.module_code: FINALIZATION_V1,
    NO_SHOT_ATTACK_V1.module_code: NO_SHOT_ATTACK_V1,
    OFFENSIVE_CREATION_V1.module_code: OFFENSIVE_CREATION_V1,
    DEFENSIVE_V1.module_code: DEFENSIVE_V1,
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


def list_review_event_codes(module_code: str) -> tuple[str, ...]:
    return tuple(
        event_contract.event_code
        for event_contract in get_module_contract(module_code).review_only_events
    )


def list_future_event_codes(module_code: str) -> tuple[str, ...]:
    return tuple(
        event_contract.event_code
        for event_contract in get_module_contract(module_code).future_events
    )


def all_event_codes(module_code: str) -> tuple[str, ...]:
    module_contract = get_module_contract(module_code)
    return tuple(
        event_contract.event_code for event_contract in module_contract.event_contracts()
    )
