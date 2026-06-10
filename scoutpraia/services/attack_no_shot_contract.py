"""Contrato operacional executável do módulo Ataque sem Finalização v1.0.

Fonte humana: Contrato_Operacional.md.
Fonte estruturada de máquina: contracts/attack_no_shot_v1.json.

Este módulo não implementa scout completo. Ele cobre apenas posses ofensivas que
terminam sem finalização e com perda da posse.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

CONTRACT_PATH = Path(__file__).resolve().parents[2] / "contracts" / "attack_no_shot_v1.json"
ATTACK_NO_SHOT_RESULT = "lost_possession_no_shot"


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


@dataclass(frozen=True)
class IntraObserverMarking:
    lance_id: str
    first_event_code: str
    second_event_code: str


def _has_value(value: str | None) -> bool:
    return value is not None and value.strip() != ""


@lru_cache(maxsize=1)
def load_attack_no_shot_contract() -> dict[str, Any]:
    """Load the machine-readable contract from the repository."""
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def _field_is_required(event: dict[str, Any], field_name: str) -> bool:
    return field_name in set(event.get("required_fields", []))


def _events_by_code() -> dict[str, dict[str, Any]]:
    contract = load_attack_no_shot_contract()
    return {event["code"]: event for event in contract["events"]}


def _controlled_values(name: str) -> set[str]:
    contract = load_attack_no_shot_contract()
    return set(contract["controlled_values"][name])


def _build_public_event_contracts() -> dict[str, AttackNoShotEventContract]:
    events: dict[str, AttackNoShotEventContract] = {}
    for code, event in _events_by_code().items():
        required_fields = set(event.get("required_fields", []))
        events[code] = AttackNoShotEventContract(
            code=code,
            name_ui=event["name_ui"],
            ui_type=event["ui_type"],
            require_athlete="athlete_id" in required_fields,
            require_court_zone="court_zone" in required_fields,
            require_position="position_code" in required_fields,
            require_system="system_code" in required_fields,
            status=event["status"],
            validation_source=event["validation_source"],
            result_possession_auto=event["derived_fields"]["result_possession_auto"],
        )
    return events


ATTACK_NO_SHOT_EVENTS: dict[str, AttackNoShotEventContract] = _build_public_event_contracts()
TECHNICAL_ERROR_SUBTYPES = _controlled_values("technical_error_subtype")
PASSIVE_PLAY_SUBTYPES = _controlled_values("passive_play_subtype")
SUBSTITUTION_ERROR_SUBTYPES = _controlled_values("substitution_error_subtype")


def validate_attack_no_shot_entry(entry: AttackNoShotInput) -> AttackNoShotValidation:
    errors: list[str] = []
    events_by_code = _events_by_code()

    if entry.event_code not in events_by_code:
        return AttackNoShotValidation(
            ok=False,
            errors=(f"Evento fora do módulo Ataque sem Finalização v1.0: {entry.event_code}",),
            result_possession_auto=ATTACK_NO_SHOT_RESULT,
            points=0,
            review_marker=entry.review_marker or bool(entry.review_reasons),
        )

    event = events_by_code[entry.event_code]
    forbidden_fields = set(event.get("forbidden_fields", []))

    if "finish_type_code" in forbidden_fields and _has_value(entry.finish_type_code):
        errors.append("tipo_finalizacao_code não é permitido.")
    if "goal_zone" in forbidden_fields and _has_value(entry.goal_zone):
        errors.append("zona_gol não é permitida.")
    if entry.points is not None and entry.points != event["derived_fields"]["points"]:
        errors.append("pontos_jogada deve ser 0.")

    if _field_is_required(event, "athlete_id") and not _has_value(entry.athlete_id):
        errors.append(f"{entry.event_code} exige atleta principal.")
    if _field_is_required(event, "court_zone") and not _has_value(entry.court_zone):
        errors.append(f"{entry.event_code} exige zona da quadra.")
    if _field_is_required(event, "position_code") and not _has_value(entry.position_code):
        errors.append(f"{entry.event_code} exige posição/função.")
    if _field_is_required(event, "system_code") and not _has_value(entry.system_code):
        errors.append(f"{entry.event_code} exige sistema.")

    if _field_is_required(event, "technical_error_subtype"):
        if entry.technical_error_subtype not in TECHNICAL_ERROR_SUBTYPES:
            errors.append(f"{entry.event_code} exige subtipo_erro_tecnico válido.")

    if _field_is_required(event, "passive_play_subtype"):
        if entry.passive_play_subtype not in PASSIVE_PLAY_SUBTYPES:
            errors.append("passive_play_turnover exige subtipo_jogo_passivo válido.")

    if _field_is_required(event, "substitution_error_subtype"):
        if entry.substitution_error_subtype not in SUBSTITUTION_ERROR_SUBTYPES:
            errors.append("bad_substitution_attack exige subtipo_erro_substituicao válido.")

    requires_review = (
        _field_is_required(event, "review_marker")
        or entry.substitution_error_subtype == "substitution_violation_other"
        or bool(entry.review_reasons)
    )
    if requires_review and not entry.review_marker:
        errors.append(f"{entry.event_code} exige review_marker = Sim nesta condição.")

    derived_fields = event["derived_fields"]
    return AttackNoShotValidation(
        ok=not errors,
        errors=tuple(errors),
        result_possession_auto=derived_fields["result_possession_auto"],
        points=derived_fields["points"],
        review_marker=entry.review_marker or requires_review,
        defense_forced_error=bool(derived_fields.get("defense_forced_error", False)),
    )


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
