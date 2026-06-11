from scoutpraia.contracts.events_v1 import (
    IMPORT_RULE_V1_BLOCKED,
    SHOOTOUT_V1,
    all_event_codes,
    list_auxiliary_codes,
    list_primary_event_codes,
)


SHOOTOUT_RESULTS = {
    "goal",
    "save",
    "shot_wide",
    "attacker_execution_error",
    "launch_ground_contact",
    "pass_intercepted",
    "defender_" + "foul_6m_awarded",
}

REQUIRED_FIELDS = {
    "shooter_id",
    "shootout_launcher_id",
    "shootout_launcher_role",
    "shootout_defender_id",
    "shootout_defender_role",
    "shootout_phase",
    "attempt_order",
    "pre_launch_defensive_behavior",
    "launch_type",
    "launch_result",
    "defensive_trap_type",
    "result_shootout",
}

FORBIDDEN_EVENT_CODES = {
    "shootout_goal",
    "shootout_miss",
    "shootout_spin",
    "shootout_double_spin",
    "shootout_inflight",
    "shootout_interception",
    "goalkeeper_id",
    "launcher_goalkeeper_id",
    "defender_goalkeeper_id",
    "defender_goalkeeper_role",
    "retry_linked_attempt_id",
    "legacy_retry_linked_attempt_id",
    "six_metre_throw",
}

FORBIDDEN_RESULTS = {
    "defender_infraction_retry",
    "goalkeeper_violation_retry",
    "retry_ordered",
    "lost_possession_no_shot",
}


def test_shootout_v1_has_one_primary_event() -> None:
    assert list_primary_event_codes("shootout_v1") == ("shootout_attempt",)
    assert SHOOTOUT_V1.primary_events[0].ui_type == "botao_principal"
    assert SHOOTOUT_V1.primary_events[0].import_rule_v1 == IMPORT_RULE_V1_BLOCKED


def test_shootout_v1_is_not_importable_yet() -> None:
    assert SHOOTOUT_V1.import_rule_v1 == IMPORT_RULE_V1_BLOCKED
    for event_contract in SHOOTOUT_V1.event_contracts():
        assert event_contract.import_rule_v1 == IMPORT_RULE_V1_BLOCKED


def test_shootout_results_match_sheet_contract() -> None:
    assert SHOOTOUT_V1.primary_events[0].allowed_results == SHOOTOUT_RESULTS


def test_shootout_points_are_derived_from_result() -> None:
    derived_points = {
        result: 2 if result == "goal" else 0 for result in SHOOTOUT_RESULTS
    }

    assert derived_points["goal"] == 2
    assert derived_points["save"] == 0
    assert derived_points["shot_wide"] == 0
    assert derived_points["attacker_execution_error"] == 0
    assert derived_points["launch_ground_contact"] == 0
    assert derived_points["pass_intercepted"] == 0
    assert derived_points["defender_" + "foul_6m_awarded"] == 0


def test_shootout_uses_functional_roles_instead_of_fixed_goalkeeper_position() -> None:
    auxiliary_codes = set(list_auxiliary_codes("shootout_v1"))

    assert REQUIRED_FIELDS.issubset(auxiliary_codes)
    assert "shootout_launcher_id" in auxiliary_codes
    assert "shootout_launcher_role" in auxiliary_codes
    assert "shootout_defender_id" in auxiliary_codes
    assert "shootout_defender_role" in auxiliary_codes
    assert "goalkeeper_id" not in auxiliary_codes
    assert "launcher_goalkeeper_id" not in auxiliary_codes
    assert "defender_goalkeeper_id" not in auxiliary_codes
    assert "defender_goalkeeper_role" not in auxiliary_codes


def test_shootout_blocks_legacy_events_and_retry_logic() -> None:
    assert FORBIDDEN_EVENT_CODES.issubset(SHOOTOUT_V1.forbidden_event_codes)
    assert FORBIDDEN_RESULTS.issubset(SHOOTOUT_V1.forbidden_results)
    assert FORBIDDEN_EVENT_CODES.isdisjoint(all_event_codes("shootout_v1"))


def test_shootout_keeps_six_metre_throw_as_follow_up_not_primary_event() -> None:
    assert "six_metre_throw" in SHOOTOUT_V1.forbidden_event_codes
    assert "six_metre_throw" not in all_event_codes("shootout_v1")
    assert "six_metre_throw" in all_event_codes("finalization_v1")


def test_ground_contact_and_legal_interception_are_lost_attempt_results() -> None:
    assert "launch_ground_contact" in SHOOTOUT_RESULTS
    assert "pass_intercepted" in SHOOTOUT_RESULTS
    assert "defender_infraction_retry" not in SHOOTOUT_RESULTS
    assert "goalkeeper_violation_retry" not in SHOOTOUT_RESULTS


def test_shootout_technical_action_is_auxiliary_not_a_separate_event() -> None:
    auxiliary_codes = set(list_auxiliary_codes("shootout_v1"))

    assert "shootout_action_type" in auxiliary_codes
    assert "shootout_spin" not in all_event_codes("shootout_v1")
    assert "shootout_double_spin" not in all_event_codes("shootout_v1")
    assert "shootout_inflight" not in all_event_codes("shootout_v1")


def test_shootout_attempt_stays_out_of_finalization_and_no_shot_attack() -> None:
    assert "shootout_attempt" not in all_event_codes("finalization_v1")
    assert "shootout_attempt" not in all_event_codes("attack_no_shot_v1")
