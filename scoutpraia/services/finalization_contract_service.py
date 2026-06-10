"""Validation and scoring service for Finalizacao v1.0.

This service remains isolated from the active app flow until the later gates
explicitly wire it into tagging, persistence, and reporting.
"""

from __future__ import annotations

from dataclasses import dataclass

from scoutpraia.contracts.events_v1 import FINALIZATION_V1

VALID_SCORER_ROLES = frozenset({"field_player", "specialist", "goalkeeper"})
FORBIDDEN_POSITION_CODES = frozenset({"specialist"})
ALLOWED_RESULTS_BY_EVENT = {
    event_contract.event_code: event_contract.allowed_results
    for event_contract in FINALIZATION_V1.primary_events
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


class FinalizationContractError(ValueError):
    """Raised when a Finalizacao v1.0 contract rule is violated."""


@dataclass(frozen=True)
class FinalizationRecordInput:
    event_code: str
    result_possession: str
    scorer_role: str
    position_code: str | None = None
    manual_points: int | None = None


def result_allowed(event_code: str, result_possession: str) -> bool:
    allowed_results = ALLOWED_RESULTS_BY_EVENT.get(event_code)
    return allowed_results is not None and result_possession in allowed_results


def derive_points(event_code: str, result_possession: str, scorer_role: str) -> int:
    _validate_event_code(event_code)
    if scorer_role not in VALID_SCORER_ROLES:
        raise FinalizationContractError("invalid_scorer_role")
    if not result_allowed(event_code, result_possession):
        raise FinalizationContractError("result_not_allowed_for_event")

    exact_key = (event_code, result_possession, scorer_role)
    wildcard_key = (event_code, result_possession, "any_valid")
    if exact_key in POINT_RULES:
        return POINT_RULES[exact_key]
    if wildcard_key in POINT_RULES:
        return POINT_RULES[wildcard_key]
    raise FinalizationContractError("no_points_rule_match")


def validate_record(
    *,
    event_code: str,
    result_possession: str,
    scorer_role: str,
    position_code: str | None = None,
    manual_points: int | None = None,
) -> int:
    _validate_event_code(event_code)
    if event_code in FINALIZATION_V1.forbidden_event_codes:
        raise FinalizationContractError("forbidden_event_code")
    if position_code in FORBIDDEN_POSITION_CODES:
        raise FinalizationContractError("forbidden_position_code")
    if result_possession in FINALIZATION_V1.forbidden_results:
        raise FinalizationContractError("lost_possession_no_shot_forbidden")
    if event_code == "goalkeeper_shot" and scorer_role != "goalkeeper":
        raise FinalizationContractError("goalkeeper_shot_requires_goalkeeper_role")

    derived_points = derive_points(event_code, result_possession, scorer_role)
    if manual_points is not None and manual_points != derived_points:
        raise FinalizationContractError("manual_points_mismatch")
    return derived_points


def validate_record_input(record: FinalizationRecordInput) -> int:
    return validate_record(
        event_code=record.event_code,
        result_possession=record.result_possession,
        scorer_role=record.scorer_role,
        position_code=record.position_code,
        manual_points=record.manual_points,
    )


def _validate_event_code(event_code: str) -> None:
    if event_code in FINALIZATION_V1.forbidden_event_codes:
        return
    if event_code not in ALLOWED_RESULTS_BY_EVENT:
        raise FinalizationContractError("invalid_event_code")
