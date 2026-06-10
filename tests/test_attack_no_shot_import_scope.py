from scoutpraia.contracts.events_v1 import (
    IMPORT_RULE_V1_ACTIVE,
    IMPORT_RULE_V1_BLOCKED,
    NO_SHOT_ATTACK_V1,
    all_event_codes,
)


OFFICIAL_ATTACK_NO_SHOT_EVENTS = {
    "technical_error_unforced",
    "technical_error_forced",
    "offensive_foul",
    "goal_area_invasion_attack",
    "passive_play_turnover",
    "bad_substitution_attack",
    "turnover_unclassified",
}


def test_attack_no_shot_module_is_the_only_active_v1_import_scope_in_registry() -> None:
    assert NO_SHOT_ATTACK_V1.module_code == "attack_no_shot_v1"
    assert NO_SHOT_ATTACK_V1.import_rule_v1 == IMPORT_RULE_V1_ACTIVE


def test_only_official_attack_no_shot_primary_events_are_importable() -> None:
    primary_events = set(NO_SHOT_ATTACK_V1.primary_events)
    assert {event.event_code for event in primary_events} == OFFICIAL_ATTACK_NO_SHOT_EVENTS
    assert {event.import_rule_v1 for event in primary_events} == {IMPORT_RULE_V1_ACTIVE}


def test_auxiliary_fields_are_not_importable_as_events() -> None:
    assert {event.event_code for event in NO_SHOT_ATTACK_V1.auxiliary_fields} == {
        "technical_error_subtype",
        "passive_play_subtype",
        "substitution_error_subtype",
    }
    assert {event.import_rule_v1 for event in NO_SHOT_ATTACK_V1.auxiliary_fields} == {
        IMPORT_RULE_V1_BLOCKED
    }


def test_forbidden_old_or_cross_module_codes_are_not_in_attack_scope() -> None:
    forbidden_codes = {
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
    assert forbidden_codes.isdisjoint(all_event_codes("attack_no_shot_v1"))
    assert forbidden_codes.issubset(NO_SHOT_ATTACK_V1.forbidden_event_codes)
