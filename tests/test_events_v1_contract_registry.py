from scoutpraia.contracts.events_v1 import (
    DEFENSIVE_V1,
    FINALIZATION_V1,
    GOALKEEPER_V1,
    IMPORT_RULE_V1_ACTIVE,
    IMPORT_RULE_V1_BLOCKED,
    MODULE_CONTRACTS_V1,
    NO_SHOT_ATTACK_V1,
    OFFENSIVE_CREATION_V1,
    SHOOTOUT_V1,
    all_event_codes,
    get_module_contract,
    list_auxiliary_codes,
    list_future_event_codes,
    list_primary_event_codes,
    list_review_event_codes,
)


def test_contract_registry_exposes_v1_modules() -> None:
    assert set(MODULE_CONTRACTS_V1) == {
        "finalization_v1",
        "attack_no_shot_v1",
        "offensive_creation_v1",
        "defensive_v1",
        "shootout_v1",
        "goalkeeper_v1",
    }
    assert get_module_contract("finalization_v1") is FINALIZATION_V1
    assert get_module_contract("attack_no_shot_v1") is NO_SHOT_ATTACK_V1
    assert get_module_contract("offensive_creation_v1") is OFFENSIVE_CREATION_V1
    assert get_module_contract("defensive_v1") is DEFENSIVE_V1
    assert get_module_contract("shootout_v1") is SHOOTOUT_V1
    assert get_module_contract("goalkeeper_v1") is GOALKEEPER_V1
    assert get_module_contract("no_shot_attack_v1") is NO_SHOT_ATTACK_V1


def test_finalization_primary_events_match_the_validated_contract() -> None:
    assert list_primary_event_codes("finalization_v1") == (
        "simple_shot",
        "spin_shot",
        "inflight_shot",
        "goalkeeper_shot",
        "six_metre_throw",
    )


def test_attack_no_shot_primary_events_match_sheet_contract() -> None:
    assert list_primary_event_codes("attack_no_shot_v1") == (
        "technical_error_unforced",
        "technical_error_forced",
        "offensive_foul",
        "goal_area_invasion_attack",
        "passive_play_turnover",
        "bad_substitution_attack",
        "turnover_unclassified",
    )


def test_offensive_creation_primary_events_match_contract_snapshot() -> None:
    assert list_primary_event_codes("offensive_creation_v1") == ("assist_to_finalization",)


def test_defensive_primary_events_match_contract_snapshot() -> None:
    assert list_primary_event_codes("defensive_v1") == ("line_block_shot",)


def test_shootout_primary_event_matches_contract_snapshot() -> None:
    assert list_primary_event_codes("shootout_v1") == ("shootout_attempt",)


def test_goalkeeper_primary_events_match_contract_snapshot() -> None:
    assert list_primary_event_codes("goalkeeper_v1") == (
        "goalkeeper_save",
        "goalkeeper_goal_allowed",
        "goalkeeper_specialist_exchange",
    )


def test_auxiliary_codes_are_not_exposed_as_primary_buttons() -> None:
    finalization_primary = set(list_primary_event_codes("finalization_v1"))
    finalization_auxiliary = set(list_auxiliary_codes("finalization_v1"))
    attack_primary = set(list_primary_event_codes("attack_no_shot_v1"))
    attack_auxiliary = set(list_auxiliary_codes("attack_no_shot_v1"))
    offensive_creation_primary = set(list_primary_event_codes("offensive_creation_v1"))
    offensive_creation_auxiliary = set(list_auxiliary_codes("offensive_creation_v1"))
    offensive_creation_review = set(list_review_event_codes("offensive_creation_v1"))
    offensive_creation_future = set(list_future_event_codes("offensive_creation_v1"))
    defensive_primary = set(list_primary_event_codes("defensive_v1"))
    defensive_auxiliary = set(list_auxiliary_codes("defensive_v1"))
    defensive_review = set(list_review_event_codes("defensive_v1"))
    defensive_future = set(list_future_event_codes("defensive_v1"))
    shootout_primary = set(list_primary_event_codes("shootout_v1"))
    shootout_auxiliary = set(list_auxiliary_codes("shootout_v1"))
    goalkeeper_primary = set(list_primary_event_codes("goalkeeper_v1"))
    goalkeeper_auxiliary = set(list_auxiliary_codes("goalkeeper_v1"))

    assert finalization_auxiliary == {"specialist_finish_role"}
    assert finalization_primary.isdisjoint(finalization_auxiliary)
    assert "specialist_finish_role" not in finalization_primary
    assert "shootout_attempt" not in all_event_codes("finalization_v1")

    assert attack_auxiliary == {
        "technical_error_subtype",
        "passive_play_subtype",
        "substitution_error_subtype",
    }
    assert attack_primary.isdisjoint(attack_auxiliary)

    assert offensive_creation_auxiliary == {
        "assist_to_inflight_shot",
        "pivot_feed_to_shot",
    }
    assert offensive_creation_review == {
        "advantage_pass_to_free_player",
        "collective_action_creates_shot",
    }
    assert offensive_creation_future == set()
    assert offensive_creation_primary.isdisjoint(offensive_creation_auxiliary)
    assert offensive_creation_primary.isdisjoint(offensive_creation_review)
    assert "assist_to_inflight_shot" not in offensive_creation_primary
    assert "pivot_feed_to_shot" not in offensive_creation_primary
    assert "advantage_pass_to_free_player" not in offensive_creation_primary
    assert "collective_action_creates_shot" not in offensive_creation_primary

    assert defensive_auxiliary == set()
    assert defensive_primary == {"line_block_shot"}
    assert defensive_review == {
        "defensive_pressure_forced_error",
        "steal_or_interception",
    }
    assert defensive_future == {"defensive_rebound_recovery"}

    assert shootout_primary == {"shootout_attempt"}
    assert shootout_primary.isdisjoint(shootout_auxiliary)
    assert {
        "shootout_launcher_id",
        "shootout_launcher_role",
        "shootout_defender_id",
        "shootout_defender_role",
        "shootout_defender_origin_role",
        "launch_result",
        "result_shootout",
    }.issubset(shootout_auxiliary)

    assert goalkeeper_primary == {
        "goalkeeper_save",
        "goalkeeper_goal_allowed",
        "goalkeeper_specialist_exchange",
    }
    assert goalkeeper_primary.isdisjoint(goalkeeper_auxiliary)
    assert {
        "goalkeeper_id",
        "linked_finalization_id",
        "linked_finalization_event_code",
        "result_goalkeeper",
        "possession_after_save",
        "restart_after_save",
        "specialist_id",
        "exchange_phase",
        "exchange_result",
        "court_overlap_detected",
        "punishment_applied",
    }.issubset(goalkeeper_auxiliary)


def test_import_rules_match_module_activation_policy() -> None:
    assert FINALIZATION_V1.import_rule_v1 == IMPORT_RULE_V1_BLOCKED
    for event_contract in FINALIZATION_V1.event_contracts():
        assert event_contract.import_rule_v1 == IMPORT_RULE_V1_BLOCKED

    assert NO_SHOT_ATTACK_V1.import_rule_v1 == IMPORT_RULE_V1_ACTIVE
    for event_contract in NO_SHOT_ATTACK_V1.primary_events:
        assert event_contract.import_rule_v1 == IMPORT_RULE_V1_ACTIVE
    for event_contract in NO_SHOT_ATTACK_V1.auxiliary_fields:
        assert event_contract.import_rule_v1 == IMPORT_RULE_V1_BLOCKED

    assert OFFENSIVE_CREATION_V1.import_rule_v1 == IMPORT_RULE_V1_BLOCKED
    for event_contract in OFFENSIVE_CREATION_V1.event_contracts():
        assert event_contract.import_rule_v1 == IMPORT_RULE_V1_BLOCKED

    assert DEFENSIVE_V1.import_rule_v1 == IMPORT_RULE_V1_BLOCKED
    for event_contract in DEFENSIVE_V1.event_contracts():
        assert event_contract.import_rule_v1 == IMPORT_RULE_V1_BLOCKED

    assert SHOOTOUT_V1.import_rule_v1 == IMPORT_RULE_V1_BLOCKED
    for event_contract in SHOOTOUT_V1.event_contracts():
        assert event_contract.import_rule_v1 == IMPORT_RULE_V1_BLOCKED

    assert GOALKEEPER_V1.import_rule_v1 == IMPORT_RULE_V1_BLOCKED
    for event_contract in GOALKEEPER_V1.event_contracts():
        assert event_contract.import_rule_v1 == IMPORT_RULE_V1_BLOCKED


def test_no_shot_attack_and_finalization_keep_result_domains_separate() -> None:
    finalization_results = set().union(
        *(event.allowed_results for event in FINALIZATION_V1.primary_events)
    )
    no_shot_results = set().union(
        *(event.allowed_results for event in NO_SHOT_ATTACK_V1.primary_events)
    )

    assert no_shot_results == {"lost_possession_no_shot"}
    assert "lost_possession_no_shot" not in finalization_results
    assert finalization_results == NO_SHOT_ATTACK_V1.forbidden_results
    assert finalization_results.isdisjoint(no_shot_results)


def test_registry_adds_offensive_creation_and_defensive_without_exposing_app_import() -> None:
    offensive_creation_results = set().union(
        *(event.allowed_results for event in OFFENSIVE_CREATION_V1.primary_events)
    )
    offensive_creation_review_results = set().union(
        *(event.allowed_results for event in OFFENSIVE_CREATION_V1.review_only_events)
    )
    defensive_results = set().union(
        *(event.allowed_results for event in DEFENSIVE_V1.primary_events)
    )
    defensive_review_results = set().union(
        *(event.allowed_results for event in DEFENSIVE_V1.review_only_events)
    )
    defensive_future_results = set().union(
        *(event.allowed_results for event in DEFENSIVE_V1.future_events)
    )

    assert offensive_creation_results == {"shot_created"}
    assert offensive_creation_review_results == {"shot_created", "clear_chance_created"}
    assert defensive_results == {"shot_blocked_linked"}
    assert defensive_review_results == {"forced_error_linked", "possession_won"}
    assert defensive_future_results == {"rebound_recovered"}
    assert OFFENSIVE_CREATION_V1.forbidden_results == {"turnover_after_creation_error"}
    assert DEFENSIVE_V1.forbidden_results == {"pressure_no_turnover_review"}


def test_shootout_contract_is_registered_without_app_import() -> None:
    shootout_results = set().union(
        *(event.allowed_results for event in SHOOTOUT_V1.primary_events)
    )

    expected_6m_result = "defender_" + "foul_6m_awarded"
    assert shootout_results == {
        "goal",
        "save",
        "shot_wide",
        "attacker_execution_error",
        "launch_ground_contact",
        "pass_intercepted",
        expected_6m_result,
    }
    assert SHOOTOUT_V1.import_rule_v1 == IMPORT_RULE_V1_BLOCKED
    assert SHOOTOUT_V1.forbidden_results == {
        "defender_infraction_retry",
        "goalkeeper_violation_retry",
        "retry_ordered",
        "lost_possession_no_shot",
    }
    assert "six_metre_throw" in SHOOTOUT_V1.forbidden_event_codes
    assert "goalkeeper_save" in SHOOTOUT_V1.forbidden_event_codes
    assert "shootout_attempt" not in all_event_codes("finalization_v1")


def test_goalkeeper_contract_is_registered_without_app_import() -> None:
    goalkeeper_results = set().union(
        *(event.allowed_results for event in GOALKEEPER_V1.primary_events)
    )

    assert goalkeeper_results == {
        "save_controlled",
        "save_rebound_live",
        "save_out_endline",
        "save_out_sideline",
        "uncertain_review",
        "goal_allowed",
        "exchange_successful",
        "goalkeeper_late_exit",
        "specialist_late_entry",
        "overlap_violation",
        "empty_goal_risk",
        "exchange_turnover",
        "unknown_review",
    }
    assert GOALKEEPER_V1.import_rule_v1 == IMPORT_RULE_V1_BLOCKED
    assert "shootout_attempt" in GOALKEEPER_V1.forbidden_event_codes
    assert "line_block_shot" in GOALKEEPER_V1.forbidden_event_codes
    assert "goal_allowed_review" in GOALKEEPER_V1.forbidden_results
    assert "six_metre_throw" in all_event_codes("finalization_v1")


def test_old_interim_attack_event_codes_are_not_active() -> None:
    assert {
        "ball_control_turnover",
        "offensive_foul_turnover",
        "substitution_error_turnover",
        "turnover_cause_detail",
    }.isdisjoint(all_event_codes("attack_no_shot_v1"))
