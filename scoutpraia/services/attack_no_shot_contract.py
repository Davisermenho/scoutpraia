"""Contrato operacional do módulo Ataque sem Finalização v1.0.

Fonte semântica: Contrato_Operacional.md.
Fonte de implementação: SCOUT_DESIGN_TEMPLATE.

Este módulo não implementa scout completo. Ele cobre apenas posses ofensivas que
terminam sem finalização e com perda da posse.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ATTACK_NO_SHOT_RESULT = "lost_possession_no_shot"

AttackNoShotEventCode = Literal[
    "technical_error_unforced",
    "technical_error_forced",
    "offensive_foul",
    "goal_area_invasion_attack",
    "passive_play_turnover",
    "bad_substitution_attack",
    "turnover_unclassified",
]

TECHNICAL_ERROR_SUBTYPES = {
    "three_seconds",
    "steps_violation",
    "double_dribble",
    "pass_error",
    "reception_error",
    "pass_error_foot",
    "pass_error_sideline",
    "pass_error_endline",
    "ground_ball_lost",
    "ball_handling_error",
}

PASSIVE_PLAY_SUBTYPES = {
    "passive_fifth_pass_no_shot",
    "passive_no_shot_after_clear_chance_return",
}

SUBSTITUTION_ERROR_SUBTYPES = {
    "illegal_entry_before_exit",
    "illegal_entry_zone",
    "too_many_players",
    "illegal_goalkeeper_exchange",
    "substitution_violation_other",
}


@dataclass(frozen=True)
class AttackNoShotEventContract:
    code: str
    name_ui: str
    ui_type: str
    require_athlete: bool
    require_court_zone: bool
    require_position: bool
    require_system: bool
    status: str
    validation_source: str
    result_possession_auto: str = ATTACK_NO_SHOT_RESULT


ATTACK_NO_SHOT_EVENTS: dict[str, AttackNoShotEventContract] = {
    "technical_error_unforced": AttackNoShotEventContract(
        code="technical_error_unforced",
        name_ui="Erro Técnico Não Forçado",
        ui_type="botao_principal",
        require_athlete=True,
        require_court_zone=True,
        require_position=True,
        require_system=False,
        status="novo",
        validation_source="IHF_USO_DA_BOLA + DECISAO_OPERACIONAL",
    ),
    "technical_error_forced": AttackNoShotEventContract(
        code="technical_error_forced",
        name_ui="Erro Técnico Forçado",
        ui_type="botao_principal",
        require_athlete=True,
        require_court_zone=True,
        require_position=True,
        require_system=False,
        status="novo",
        validation_source="RAG_DEFESA_PRESSAO + DECISAO_OPERACIONAL",
    ),
    "offensive_foul": AttackNoShotEventContract(
        code="offensive_foul",
        name_ui="Falta de Ataque",
        ui_type="botao_principal",
        require_athlete=True,
        require_court_zone=True,
        require_position=True,
        require_system=False,
        status="novo",
        validation_source="IHF_CONTATO_FALTA_ATAQUE + DECISAO_ARBITRAL",
    ),
    "goal_area_invasion_attack": AttackNoShotEventContract(
        code="goal_area_invasion_attack",
        name_ui="Invasão da Área no Ataque",
        ui_type="botao_principal",
        require_athlete=True,
        require_court_zone=True,
        require_position=True,
        require_system=False,
        status="novo",
        validation_source="IHF_AREA_GOLEIRA",
    ),
    "passive_play_turnover": AttackNoShotEventContract(
        code="passive_play_turnover",
        name_ui="Perda por Jogo Passivo",
        ui_type="botao_secundario",
        require_athlete=False,
        require_court_zone=False,
        require_position=False,
        require_system=True,
        status="novo",
        validation_source="IHF_PASSIVO + FHERJ_PASSIVO",
    ),
    "bad_substitution_attack": AttackNoShotEventContract(
        code="bad_substitution_attack",
        name_ui="Erro de Troca no Ataque",
        ui_type="botao_secundario",
        require_athlete=False,
        require_court_zone=False,
        require_position=False,
        require_system=True,
        status="novo",
        validation_source="IHF_SUBSTITUICAO",
    ),
    "turnover_unclassified": AttackNoShotEventContract(
        code="turnover_unclassified",
        name_ui="Perda de Posse Não Classificada",
        ui_type="fallback_revisao",
        require_athlete=False,
        require_court_zone=False,
        require_position=False,
        require_system=False,
        status="revisar",
        validation_source="QUALIDADE_DADO_VIDEO_INSUFICIENTE",
    ),
}


@dataclass(frozen=True)
class AttackNoShotInput:
    event_code: str
    athlete_id: str | None = None
    court_zone: str | None = None
    position_code: str | None = None
    system_code: str | None = None
    technical_error_subtype: str | None = None
    passive_play_subtype: str | None = None
    substitution_error_subtype: str | None = None
    review_marker: bool = False
    review_reasons: tuple[str, ...] = ()
    finish_type_code: str | None = None
    goal_zone: str | None = None
    points: int | None = None


@dataclass(frozen=True)
class AttackNoShotValidation:
    ok: bool
    errors: tuple[str, ...]
    result_possession_auto: str
    points: int
    review_marker: bool
    defense_forced_error: bool = False


def _has_value(value: str | None) -> bool:
    return value is not None and value.strip() != ""


def validate_attack_no_shot_entry(entry: AttackNoShotInput) -> AttackNoShotValidation:
    errors: list[str] = []

    if entry.event_code not in ATTACK_NO_SHOT_EVENTS:
        return AttackNoShotValidation(
            ok=False,
            errors=(f"Evento fora do módulo Ataque sem Finalização v1.0: {entry.event_code}",),
            result_possession_auto=ATTACK_NO_SHOT_RESULT,
            points=0,
            review_marker=entry.review_marker or bool(entry.review_reasons),
        )

    contract = ATTACK_NO_SHOT_EVENTS[entry.event_code]

    if _has_value(entry.finish_type_code):
        errors.append("tipo_finalizacao_code não é permitido.")
    if _has_value(entry.goal_zone):
        errors.append("zona_gol não é permitida.")
    if entry.points is not None and entry.points != 0:
        errors.append("pontos_jogada deve ser 0.")

    if contract.require_athlete and not _has_value(entry.athlete_id):
        errors.append(f"{entry.event_code} exige atleta principal.")
    if contract.require_court_zone and not _has_value(entry.court_zone):
        errors.append(f"{entry.event_code} exige zona da quadra.")
    if contract.require_position and not _has_value(entry.position_code):
        errors.append(f"{entry.event_code} exige posição/função.")
    if contract.require_system and not _has_value(entry.system_code):
        errors.append(f"{entry.event_code} exige sistema.")

    if entry.event_code in {"technical_error_unforced", "technical_error_forced"}:
        if entry.technical_error_subtype not in TECHNICAL_ERROR_SUBTYPES:
            errors.append(f"{entry.event_code} exige subtipo_erro_tecnico válido.")

    if entry.event_code == "passive_play_turnover":
        if entry.passive_play_subtype not in PASSIVE_PLAY_SUBTYPES:
            errors.append("passive_play_turnover exige subtipo_jogo_passivo válido.")

    if entry.event_code == "bad_substitution_attack":
        if entry.substitution_error_subtype not in SUBSTITUTION_ERROR_SUBTYPES:
            errors.append("bad_substitution_attack exige subtipo_erro_substituicao válido.")

    requires_review = (
        entry.event_code == "turnover_unclassified"
        or entry.substitution_error_subtype == "substitution_violation_other"
        or bool(entry.review_reasons)
    )
    if requires_review and not entry.review_marker:
        errors.append(f"{entry.event_code} exige review_marker = Sim nesta condição.")

    return AttackNoShotValidation(
        ok=not errors,
        errors=tuple(errors),
        result_possession_auto=ATTACK_NO_SHOT_RESULT,
        points=0,
        review_marker=entry.review_marker or requires_review,
        defense_forced_error=entry.event_code == "technical_error_forced",
    )


@dataclass(frozen=True)
class IntraObserverMarking:
    lance_id: str
    first_event_code: str
    second_event_code: str


def evaluate_intra_observer_consistency(
    markings: list[IntraObserverMarking],
    minimum_consistency_percent: float = 85.0,
) -> dict[str, object]:
    total = len(markings)
    divergent_lance_ids = [
        item.lance_id
        for item in markings
        if item.first_event_code != item.second_event_code
    ]
    divergences = len(divergent_lance_ids)
    matches = total - divergences
    consistency_percent = round((matches / total) * 100, 2) if total else 0.0

    return {
        "total": total,
        "matches": matches,
        "divergences": divergences,
        "consistency_percent": consistency_percent,
        "approved": total > 0 and consistency_percent >= minimum_consistency_percent,
        "requires_dictionary_review": total == 0 or consistency_percent < minimum_consistency_percent,
        "divergent_lance_ids": divergent_lance_ids,
    }
