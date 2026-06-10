"""Validation service for Ataque sem finalizacao v1.0.

The service uses the official event codes from SCOUT_DESIGN_TEMPLATE. It remains
safe to call independently from the legacy app seed.
"""

from __future__ import annotations

from dataclasses import dataclass

from scoutpraia.contracts.events_v1 import NO_SHOT_ATTACK_V1

NO_SHOT_RESULT = "lost_possession_no_shot"
TECHNICAL_ERROR_SUBTYPES = frozenset(
    {
        "bad_pass",
        "bad_reception",
        "travelling",
        "double_dribble",
        "foot_or_leg_contact",
        "ball_handling_error",
        "ball_out_by_attack",
        "three_seconds",
    }
)
PASSIVE_PLAY_APPROVED_SUBTYPES = frozenset(
    {
        "forewarning_expired",
        "clear_chance_refused",
    }
)
SUBSTITUTION_ERROR_SUBTYPES = frozenset(
    {
        "early_entry",
        "wrong_substitution_zone",
        "extra_player",
        "goalkeeper_specialist_exchange_error",
        "substitution_violation_other",
    }
)
ALLOWED_SUBTYPES_BY_EVENT = {
    "technical_error_unforced": TECHNICAL_ERROR_SUBTYPES,
    "technical_error_forced": TECHNICAL_ERROR_SUBTYPES,
    "offensive_foul": frozenset({"offensive_contact", "illegal_screen", "charge", "push_off"}),
    "goal_area_invasion_attack": frozenset(
        {
            "area_step_with_ball",
            "area_touch_with_ball",
            "area_entry_advantage",
            "ball_recovered_inside_area",
            "fall_inside_area_before_release",
        }
    ),
    "passive_play_turnover": PASSIVE_PLAY_APPROVED_SUBTYPES,
    "bad_substitution_attack": SUBSTITUTION_ERROR_SUBTYPES,
    "turnover_unclassified": frozenset({"unknown_video_quality", "unknown_obstructed_view"}),
}
FORBIDDEN_DIRECT_CAUSES = frozenset(
    {
        "specialist_late",
        "forced_error",
        "finish_type_code",
        "goal_zone",
        "shot_origin_depth",
    }
)


class NoShotAttackContractError(ValueError):
    """Raised when an Ataque sem finalizacao v1.0 rule is violated."""


@dataclass(frozen=True)
class NoShotAttackRecordInput:
    event_code: str
    result_possession: str
    team_in_possession: bool
    athlete_id: str | None = None
    court_lane: str | None = None
    court_depth: str | None = None
    position_code: str | None = None
    system_code: str | None = None
    technical_error_subtype: str | None = None
    passive_play_subtype: str | None = None
    substitution_error_subtype: str | None = None
    review_marker: bool = False
    shot_attempted: bool = False
    is_offensive_transition: bool = False
    points: int = 0


def validate_record(
    *,
    event_code: str,
    result_possession: str,
    team_in_possession: bool,
    athlete_id: str | None = None,
    court_lane: str | None = None,
    court_depth: str | None = None,
    position_code: str | None = None,
    system_code: str | None = None,
    technical_error_subtype: str | None = None,
    passive_play_subtype: str | None = None,
    substitution_error_subtype: str | None = None,
    review_marker: bool = False,
    shot_attempted: bool = False,
    is_offensive_transition: bool = False,
    points: int = 0,
) -> str:
    if event_code in NO_SHOT_ATTACK_V1.forbidden_event_codes:
        raise NoShotAttackContractError("forbidden_event_code")
    if event_code not in ALLOWED_SUBTYPES_BY_EVENT:
        raise NoShotAttackContractError("invalid_event_code")
    if is_offensive_transition:
        raise NoShotAttackContractError("offensive_transition_forbidden")
    if shot_attempted:
        raise NoShotAttackContractError("shot_not_allowed_in_no_shot_attack")
    if result_possession != NO_SHOT_RESULT:
        raise NoShotAttackContractError("turnover_result_required")
    if points != 0:
        raise NoShotAttackContractError("points_must_be_zero")

    if event_code in {"technical_error_unforced", "technical_error_forced"}:
        _require_technical_error_fields(
            athlete_id=athlete_id,
            court_lane=court_lane,
            court_depth=court_depth,
            position_code=position_code,
            technical_error_subtype=technical_error_subtype,
        )
        if technical_error_subtype in FORBIDDEN_DIRECT_CAUSES:
            raise NoShotAttackContractError("technical_error_subtype_forbidden")
        if technical_error_subtype not in TECHNICAL_ERROR_SUBTYPES:
            raise NoShotAttackContractError("invalid_technical_error_subtype")

    if event_code == "technical_error_unforced" and technical_error_subtype == "forced_error":
        raise NoShotAttackContractError("forced_error_not_unforced")

    if event_code == "technical_error_forced":
        if technical_error_subtype == "area_invasion":
            raise NoShotAttackContractError("area_invasion_not_forced_error")

    if event_code in {"offensive_foul", "goal_area_invasion_attack"}:
        _require_core_location_fields(
            athlete_id=athlete_id,
            court_lane=court_lane,
            court_depth=court_depth,
            position_code=position_code,
        )

    if event_code == "passive_play_turnover":
        if not system_code:
            raise NoShotAttackContractError("system_code_required")
        if passive_play_subtype not in PASSIVE_PLAY_APPROVED_SUBTYPES:
            raise NoShotAttackContractError("invalid_passive_subtype")

    if event_code == "bad_substitution_attack":
        if not team_in_possession:
            raise NoShotAttackContractError("substitution_error_requires_team_possession")
        if not system_code:
            raise NoShotAttackContractError("system_code_required")
        if substitution_error_subtype not in SUBSTITUTION_ERROR_SUBTYPES:
            raise NoShotAttackContractError("invalid_substitution_error_subtype")
        if substitution_error_subtype == "substitution_violation_other" and not review_marker:
            raise NoShotAttackContractError("review_marker_required")

    if event_code == "turnover_unclassified":
        if not review_marker:
            raise NoShotAttackContractError("review_marker_required")

    return event_code


def validate_record_input(record: NoShotAttackRecordInput) -> str:
    return validate_record(
        event_code=record.event_code,
        result_possession=record.result_possession,
        team_in_possession=record.team_in_possession,
        athlete_id=record.athlete_id,
        court_lane=record.court_lane,
        court_depth=record.court_depth,
        position_code=record.position_code,
        system_code=record.system_code,
        technical_error_subtype=record.technical_error_subtype,
        passive_play_subtype=record.passive_play_subtype,
        substitution_error_subtype=record.substitution_error_subtype,
        review_marker=record.review_marker,
        shot_attempted=record.shot_attempted,
        is_offensive_transition=record.is_offensive_transition,
        points=record.points,
    )


def _require_technical_error_fields(
    *,
    athlete_id: str | None,
    court_lane: str | None,
    court_depth: str | None,
    position_code: str | None,
    technical_error_subtype: str | None,
) -> None:
    _require_core_location_fields(
        athlete_id=athlete_id,
        court_lane=court_lane,
        court_depth=court_depth,
        position_code=position_code,
    )
    if not technical_error_subtype:
        raise NoShotAttackContractError("technical_error_subtype_required")


def _require_core_location_fields(
    *,
    athlete_id: str | None,
    court_lane: str | None,
    court_depth: str | None,
    position_code: str | None,
) -> None:
    if not athlete_id:
        raise NoShotAttackContractError("athlete_id_required")
    if not court_lane:
        raise NoShotAttackContractError("court_lane_required")
    if not court_depth:
        raise NoShotAttackContractError("court_depth_required")
    if not position_code:
        raise NoShotAttackContractError("position_code_required")
