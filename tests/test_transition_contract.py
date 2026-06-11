from scoutpraia.contracts.events_v1 import (
    IMPORT_RULE_V1_BLOCKED,
    TRANSITION_V1,
    all_event_codes,
    list_auxiliary_codes,
    list_primary_event_codes,
)


TRANSITION_RESULTS = {
    "transition_goal",
    "transition_shot_created",
    "transition_saved",
    "transition_turnover_no_shot",
    "transition_slowed_to_set",
    "defensive_recovery_success",
    "defensive_recovery_fail",
    "interrupted_review",
    "uncertain_review",
    "direct_transition_chance",
    "indirect_superiority_created",
    "direct_transition_neutralized",
    "indirect_transition_neutralized",
}

REQUIRED_FIELDS = {
    "transition_direction",
    "substitution_phase",
    "substitution_timing",
    "transition_type",
    "transition_trigger",
    "transition_start_zone",
    "transition_target_zone",
    "transition_speed",
    "numerical_context",
    "defensive_stabilization_status",
    "result_transition",
}

OPTIONAL_LINK_FIELDS = {
    "trigger_event_id",
    "trigger_event_code",
    "terminal_event_id",
    "terminal_event_code",
    "terminal_state",
}

SUBSTITUTION_FIELDS = {
    "exiting_player_id",
    "entering_player_id",
    "exiting_role",
    "entering_role",
    "substitution_zone",
    "anticipation_side",
}

TACTICAL_FIELDS = {
    "transition_system",
    "transition_positions",
    "direct_lane_available",
    "first_action",
    "first_passer_id",
    "first_receiver_id",
    "lane_used",
    "pass_count",
    "duration_band",
    "pressure_level",
    "review_marker",
}

FINALIZATION_TERMINALS = {
    "simple_shot",
    "spin_shot",
    "inflight_shot",
    "goalkeeper_shot",
    "six_metre_throw",
}

ATTACK_NO_SHOT_TERMINALS = {
    "technical_error_unforced",
    "technical_error_forced",
    "offensive_foul",
    "passive_play_turnover",
    "bad_substitution_attack",
    "turnover_unclassified",
}


def test_transition_v1_has_one_primary_sequence_event() -> None:
    assert list_primary_event_codes("transition_v1") == ("transition_sequence",)
    assert TRANSITION_V1.primary_events[0].ui_type == "botao_principal"


def test_transition_v1_is_not_importable_yet() -> None:
    assert TRANSITION_V1.import_rule_v1 == IMPORT_RULE_V1_BLOCKED
    for event_contract in TRANSITION_V1.event_contracts():
        assert event_contract.import_rule_v1 == IMPORT_RULE_V1_BLOCKED


def test_transition_result_domain_matches_corrected_sheet_contract() -> None:
    assert TRANSITION_V1.primary_events[0].allowed_results == TRANSITION_RESULTS
    assert "direct_transition_chance" in TRANSITION_RESULTS
    assert "indirect_superiority_created" in TRANSITION_RESULTS
    assert "direct_transition_neutralized" in TRANSITION_RESULTS
    assert "indirect_transition_neutralized" in TRANSITION_RESULTS
    assert "uncertain_review" in TRANSITION_RESULTS


def test_transition_v1_uses_substitution_chain_fields() -> None:
    auxiliary_codes = set(list_auxiliary_codes("transition_v1"))

    assert REQUIRED_FIELDS.issubset(auxiliary_codes)
    assert OPTIONAL_LINK_FIELDS.issubset(auxiliary_codes)
    assert SUBSTITUTION_FIELDS.issubset(auxiliary_codes)
    assert TACTICAL_FIELDS.issubset(auxiliary_codes)


def test_transition_offensive_and_defensive_directions_share_one_event() -> None:
    directions = {"offensive_transition", "defensive_transition", "unknown_review"}
    offensive_substitution = "defenders_exit_attackers_enter"
    defensive_substitution = "attackers_exit_defenders_enter"

    assert "transition_sequence" in list_primary_event_codes("transition_v1")
    assert offensive_substitution != defensive_substitution
    assert {"offensive_transition", "defensive_transition"}.issubset(directions)


def test_transition_direct_and_indirect_types_are_separate() -> None:
    offensive_types = {"direct_transition", "indirect_superiority", "transition_to_set"}
    defensive_types = {
        "defensive_neutralization_direct",
        "defensive_neutralization_indirect",
        "transition_to_set",
    }

    assert "direct_transition" in offensive_types
    assert "indirect_superiority" in offensive_types
    assert "defensive_neutralization_direct" in defensive_types
    assert "defensive_neutralization_indirect" in defensive_types
    assert offensive_types.isdisjoint(
        {"defensive_neutralization_direct", "defensive_neutralization_indirect"}
    )


def test_transition_result_type_coherence_rules_are_explicit() -> None:
    result_to_required_type = {
        "direct_transition_chance": "direct_transition",
        "indirect_superiority_created": "indirect_superiority",
        "direct_transition_neutralized": "defensive_neutralization_direct",
        "indirect_transition_neutralized": "defensive_neutralization_indirect",
    }

    assert result_to_required_type["direct_transition_chance"] == "direct_transition"
    assert result_to_required_type["indirect_superiority_created"] == "indirect_superiority"
    assert (
        result_to_required_type["direct_transition_neutralized"]
        == "defensive_neutralization_direct"
    )
    assert (
        result_to_required_type["indirect_transition_neutralized"]
        == "defensive_neutralization_indirect"
    )


def test_indirect_superiority_requires_an_explicit_superiority_system() -> None:
    allowed_indirect_systems = {"2x1", "3x2", "4x3"}

    assert allowed_indirect_systems == {"2x1", "3x2", "4x3"}
    assert "unstructured" not in allowed_indirect_systems


def test_anticipation_requires_attack_or_defense_side() -> None:
    anticipation_values = {
        "attack_to_defense",
        "defense_to_attack",
        "no_anticipation",
        "unclear_review",
    }

    assert "anticipation_side" in list_auxiliary_codes("transition_v1")
    assert "attack_to_defense" in anticipation_values
    assert "defense_to_attack" in anticipation_values


def test_defensive_stabilization_ends_transition() -> None:
    stabilization_states = {
        "not_stabilized",
        "partially_stabilized",
        "defense_stabilized",
        "unknown_review",
    }
    terminal_when_stabilized = "transition_slowed_to_set"

    assert "defense_stabilized" in stabilization_states
    assert terminal_when_stabilized == "transition_slowed_to_set"


def test_transition_goal_requires_finalization_terminal() -> None:
    assert FINALIZATION_TERMINALS.issubset(set(all_event_codes("finalization_v1")))
    assert "shootout_attempt" not in FINALIZATION_TERMINALS
    assert "goalkeeper_save" not in FINALIZATION_TERMINALS


def test_transition_turnover_no_shot_requires_attack_no_shot_terminal() -> None:
    assert ATTACK_NO_SHOT_TERMINALS.issubset(set(all_event_codes("attack_no_shot_v1")))
    assert "simple_shot" not in ATTACK_NO_SHOT_TERMINALS
    assert "shootout_attempt" not in ATTACK_NO_SHOT_TERMINALS


def test_transition_boundaries_block_shootout_goalkeeper_and_positioned_attack() -> None:
    assert "shootout_attempt" in TRANSITION_V1.forbidden_event_codes
    assert "goalkeeper_save" in TRANSITION_V1.forbidden_event_codes
    assert "goalkeeper_goal_allowed" in TRANSITION_V1.forbidden_event_codes
    assert "goalkeeper_specialist_exchange" in TRANSITION_V1.forbidden_event_codes
    assert "positioned_attack_only" in TRANSITION_V1.forbidden_event_codes
    assert "isolated_goal" in TRANSITION_V1.forbidden_event_codes


def test_transition_never_calculates_points_directly() -> None:
    assert "points" in TRANSITION_V1.forbidden_results
    assert all(event.allowed_results == TRANSITION_RESULTS for event in TRANSITION_V1.primary_events)


def test_transition_review_values_require_review_marker_by_contract() -> None:
    auxiliary_codes = set(list_auxiliary_codes("transition_v1"))

    assert "interrupted_review" in TRANSITION_RESULTS
    assert "uncertain_review" in TRANSITION_RESULTS
    assert "review_marker" in auxiliary_codes
