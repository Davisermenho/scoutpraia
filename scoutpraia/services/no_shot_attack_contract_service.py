"""Validation service for Ataque sem finalizacao v1.0.

This module remains isolated from the app flow until later migration, UI, and
taxonomy gates are completed.
"""

from __future__ import annotations

from dataclasses import dataclass

from scoutpraia.contracts.events_v1 import NO_SHOT_ATTACK_V1

PASSIVE_PLAY_APPROVED_SUBTYPES = frozenset(
    {
        "forewarning_expired",
        "clear_chance_refused",
    }
)
ALLOWED_CAUSE_DETAILS_BY_EVENT = {
    "ball_control_turnover": frozenset(
        {
            "bad_pass",
            "bad_reception",
            "travelling",
            "double_dribble",
            "foot_fault",
        }
    ),
    "offensive_foul_turnover": frozenset(
        {
            "area_invasion",
            "offensive_foul",
            "line_violation",
        }
    ),
    "passive_play_turnover": PASSIVE_PLAY_APPROVED_SUBTYPES,
    "substitution_error_turnover": frozenset(
        {
            "illegal_substitution",
            "extra_attacker_entry_error",
        }
    ),
}
FORBIDDEN_DIRECT_TURNOVER_CAUSES = frozenset(
    {
        "specialist_late",
        "forced_error",
    }
)


class NoShotAttackContractError(ValueError):
    """Raised when an Ataque sem finalizacao v1.0 rule is violated."""


@dataclass(frozen=True)
class NoShotAttackRecordInput:
    event_code: str
    result_possession: str
    team_in_possession: bool
    turnover_cause_detail: str | None = None
    passive_subtype: str | None = None
    shot_attempted: bool = False
    is_offensive_transition: bool = False


def validate_record(
    *,
    event_code: str,
    result_possession: str,
    team_in_possession: bool,
    turnover_cause_detail: str | None = None,
    passive_subtype: str | None = None,
    shot_attempted: bool = False,
    is_offensive_transition: bool = False,
) -> str:
    if event_code in NO_SHOT_ATTACK_V1.forbidden_event_codes:
        raise NoShotAttackContractError("forbidden_event_code")
    if event_code not in ALLOWED_CAUSE_DETAILS_BY_EVENT:
        raise NoShotAttackContractError("invalid_event_code")
    if is_offensive_transition:
        raise NoShotAttackContractError("offensive_transition_forbidden")
    if shot_attempted:
        raise NoShotAttackContractError("shot_not_allowed_in_no_shot_attack")
    if result_possession not in {"lost_possession_no_shot"}:
        raise NoShotAttackContractError("turnover_result_required")
    if turnover_cause_detail in FORBIDDEN_DIRECT_TURNOVER_CAUSES:
        if turnover_cause_detail == "specialist_late":
            raise NoShotAttackContractError("specialist_late_not_direct_turnover_cause")
        raise NoShotAttackContractError("forced_error_not_allowed")

    allowed_cause_details = ALLOWED_CAUSE_DETAILS_BY_EVENT[event_code]
    if turnover_cause_detail is not None and turnover_cause_detail not in allowed_cause_details:
        if event_code == "ball_control_turnover" and turnover_cause_detail == "area_invasion":
            raise NoShotAttackContractError("area_invasion_not_forced_error")
        raise NoShotAttackContractError("turnover_cause_not_allowed_for_event")

    if event_code == "passive_play_turnover":
        if passive_subtype not in PASSIVE_PLAY_APPROVED_SUBTYPES:
            raise NoShotAttackContractError("invalid_passive_subtype")
        if turnover_cause_detail is None:
            turnover_cause_detail = passive_subtype
    elif passive_subtype is not None:
        raise NoShotAttackContractError("passive_subtype_only_for_passive_play")

    if event_code == "substitution_error_turnover":
        if not team_in_possession:
            raise NoShotAttackContractError("substitution_error_requires_team_possession")
        if result_possession != "lost_possession_no_shot":
            raise NoShotAttackContractError("substitution_error_requires_turnover")

    return event_code


def validate_record_input(record: NoShotAttackRecordInput) -> str:
    return validate_record(
        event_code=record.event_code,
        result_possession=record.result_possession,
        team_in_possession=record.team_in_possession,
        turnover_cause_detail=record.turnover_cause_detail,
        passive_subtype=record.passive_subtype,
        shot_attempted=record.shot_attempted,
        is_offensive_transition=record.is_offensive_transition,
    )
