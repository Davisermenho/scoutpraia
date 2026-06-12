from scoutpraia.contracts.events_v1 import (
    FINALIZATION_V1,
    IMPORT_RULE_V1_ACTIVE,
    IMPORT_RULE_V1_BLOCKED,
    NO_SHOT_ATTACK_V1,
    all_event_codes,
    list_primary_event_codes,
)


SHEET_ATTACK_NO_SHOT_EVENTS = (
    "technical_error_unforced",
    "technical_error_forced",
    "offensive_foul",
    "goal_area_invasion_attack",
    "passive_play_turnover",
    "bad_substitution_attack",
    "turnover_unclassified",
)

SHEET_FINALIZATION_EVENTS = (
    "simple_shot",
    "spin_shot",
    "inflight_shot",
    "goalkeeper_shot",
    "six_metre_throw",
)


def test_registry_matches_sheet_attack_no_shot_event_codes() -> None:
    assert list_primary_event_codes("attack_no_shot_v1") == SHEET_ATTACK_NO_SHOT_EVENTS


def test_registry_matches_sheet_finalization_event_codes() -> None:
    assert list_primary_event_codes("finalization_v1") == SHEET_FINALIZATION_EVENTS


def test_attack_no_shot_import_scope_matches_sheet_import_rule() -> None:
    assert NO_SHOT_ATTACK_V1.import_rule_v1 == IMPORT_RULE_V1_ACTIVE
    for event_contract in NO_SHOT_ATTACK_V1.primary_events:
        assert event_contract.import_rule_v1 == IMPORT_RULE_V1_ACTIVE


def test_finalization_import_rule_is_active() -> None:
    assert FINALIZATION_V1.import_rule_v1 == IMPORT_RULE_V1_ACTIVE
    for event_contract in FINALIZATION_V1.primary_events:
        assert event_contract.import_rule_v1 == IMPORT_RULE_V1_ACTIVE
    for event_contract in FINALIZATION_V1.auxiliary_fields:
        assert event_contract.import_rule_v1 == IMPORT_RULE_V1_BLOCKED


def test_event_domains_are_disjoint_between_attack_no_shot_and_finalization() -> None:
    assert set(all_event_codes("attack_no_shot_v1")).isdisjoint(
        set(all_event_codes("finalization_v1"))
    )


def test_attack_no_shot_uses_only_lost_possession_no_shot_result() -> None:
    assert {
        result
        for event_contract in NO_SHOT_ATTACK_V1.primary_events
        for result in event_contract.allowed_results
    } == {"lost_possession_no_shot"}


def test_finalization_does_not_use_lost_possession_no_shot_result() -> None:
    assert "lost_possession_no_shot" not in {
        result
        for event_contract in FINALIZATION_V1.primary_events
        for result in event_contract.allowed_results
    }
