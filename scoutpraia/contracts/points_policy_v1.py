"""Global points policy for ScoutPraia event contracts.

This module centralizes point derivation so UI, importers, reports and future
agents do not infer scoring from labels or free text.

It intentionally does not enable any module import in the app. It only exposes a
pure contract function and validation errors for staged integration.
"""

from __future__ import annotations

from dataclasses import dataclass


class PointsPolicyError(ValueError):
    """Raised when a scoring rule violates the ScoutPraia points contract."""


VALID_SCORER_ROLES = frozenset({"field_player", "specialist", "goalkeeper"})
FORBIDDEN_EVENT_CODES = frozenset({"specialist_shot"})
FORBIDDEN_POSITION_CODES = frozenset({"specialist"})

ZERO_POINT_RESULTS = frozenset(
    {
        "save",
        "shot_wide",
        "shot_blocked",
        "rebound_live",
        "execution_invalid_6m",
        "attacker_execution_error",
        "launch_ground_contact",
        "pass_intercepted",
        "defender_foul_6m_awarded",
        "save_controlled",
        "save_rebound_live",
        "save_out_endline",
        "save_out_sideline",
        "uncertain_review",
        "lost_possession_no_shot",
    }
)

ALLOWED_RESULTS_BY_EVENT = {
    "simple_shot": frozenset({"goal", "save", "shot_wide", "shot_blocked"}),
    "spin_shot": frozenset({"goal", "save", "shot_wide", "shot_blocked"}),
    "inflight_shot": frozenset({"goal", "save", "shot_wide", "shot_blocked"}),
    "goalkeeper_shot": frozenset({"goal", "save", "shot_wide"}),
    "six_metre_throw": frozenset(
        {"goal", "save", "shot_wide", "rebound_live", "execution_invalid_6m"}
    ),
    "shootout_attempt": frozenset(
        {
            "goal",
            "save",
            "shot_wide",
            "attacker_execution_error",
            "launch_ground_contact",
            "pass_intercepted",
            "defender_foul_6m_awarded",
        }
    ),
    "technical_error_unforced": frozenset({"lost_possession_no_shot"}),
    "technical_error_forced": frozenset({"lost_possession_no_shot"}),
    "offensive_foul": frozenset({"lost_possession_no_shot"}),
    "goal_area_invasion_attack": frozenset({"lost_possession_no_shot"}),
    "passive_play_turnover": frozenset({"lost_possession_no_shot"}),
    "bad_substitution_attack": frozenset({"lost_possession_no_shot"}),
    "turnover_unclassified": frozenset({"lost_possession_no_shot"}),
}

POINT_RULES = {
    ("simple_shot", "goal", "field_player"): 1,
    ("simple_shot", "goal", "specialist"): 2,
    ("spin_shot", "goal", "any_valid"): 2,
    ("inflight_shot", "goal", "any_valid"): 2,
    ("goalkeeper_shot", "goal", "goalkeeper"): 2,
    ("six_metre_throw", "goal", "any_valid"): 2,
    ("shootout_attempt", "goal", "any_valid"): 2,
}


@dataclass(frozen=True)
class PointsDecision:
    event_code: str
    result_code: str
    scorer_role: str
    points_value: int
    rule_source: str


def result_allowed(event_code: str, result_code: str) -> bool:
    """Return whether a result belongs to the event result domain."""

    return result_code in ALLOWED_RESULTS_BY_EVENT.get(event_code, frozenset())


def _validate_identity_codes(
    *,
    event_code: str,
    scorer_role: str,
    position_code: str | None,
) -> None:
    if event_code in FORBIDDEN_EVENT_CODES:
        raise PointsPolicyError("forbidden_event_code")
    if position_code in FORBIDDEN_POSITION_CODES:
        raise PointsPolicyError("forbidden_position_code")
    if scorer_role not in VALID_SCORER_ROLES:
        raise PointsPolicyError("invalid_scorer_role")
    if event_code == "goalkeeper_shot" and scorer_role != "goalkeeper":
        raise PointsPolicyError("goalkeeper_shot_requires_goalkeeper_role")


def derive_points(
    *,
    event_code: str,
    result_code: str,
    scorer_role: str,
    position_code: str | None = None,
) -> PointsDecision:
    """Derive points from the global scoring contract.

    Points must be derived, not inferred from UI labels or entered freely.
    Specialist is a dynamic role, not an event code or position code.
    """

    _validate_identity_codes(
        event_code=event_code,
        scorer_role=scorer_role,
        position_code=position_code,
    )

    if not result_allowed(event_code, result_code):
        raise PointsPolicyError("result_not_allowed_for_event")

    if result_code in ZERO_POINT_RESULTS:
        return PointsDecision(
            event_code=event_code,
            result_code=result_code,
            scorer_role=scorer_role,
            points_value=0,
            rule_source="zero_point_terminal_result",
        )

    exact_key = (event_code, result_code, scorer_role)
    wildcard_key = (event_code, result_code, "any_valid")
    if exact_key in POINT_RULES:
        points_value = POINT_RULES[exact_key]
        return PointsDecision(
            event_code=event_code,
            result_code=result_code,
            scorer_role=scorer_role,
            points_value=points_value,
            rule_source="exact_event_result_role_rule",
        )
    if wildcard_key in POINT_RULES:
        points_value = POINT_RULES[wildcard_key]
        return PointsDecision(
            event_code=event_code,
            result_code=result_code,
            scorer_role=scorer_role,
            points_value=points_value,
            rule_source="event_result_any_valid_role_rule",
        )

    raise PointsPolicyError("no_points_rule_match")


def validate_points(
    *,
    event_code: str,
    result_code: str,
    scorer_role: str,
    manual_points: int | None = None,
    position_code: str | None = None,
) -> PointsDecision:
    """Validate optional manual points against derived points.

    Use this as the boundary for UI/import/report integrations: manual points may
    be displayed or supplied for review, but they cannot override the contract.
    """

    decision = derive_points(
        event_code=event_code,
        result_code=result_code,
        scorer_role=scorer_role,
        position_code=position_code,
    )
    if manual_points is not None and manual_points != decision.points_value:
        raise PointsPolicyError("manual_points_mismatch")
    return decision
