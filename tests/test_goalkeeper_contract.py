from scoutpraia.contracts.events_v1 import (
    GOALKEEPER_V1,
    IMPORT_RULE_V1_BLOCKED,
    all_event_codes,
    list_auxiliary_codes,
    list_primary_event_codes,
)


SAVE_RESULTS = {
    "save_controlled",
    "save_rebound_live",
    "save_out_endline",
    "save_out_sideline",
    "uncertain_review",
}

GOAL_ALLOWED_RESULTS = {"goal_allowed"}

EXCHANGE_RESULTS = {
    "exchange_successful",
    "goalkeeper_late_exit",
    "specialist_late_entry",
    "overlap_violation",
    "empty_goal_risk",
    "exchange_turnover",
    "unknown_review",
}

LINKED_FINALIZATION_CODES = {
    "simple_shot",
    "spin_shot",
    "inflight_shot",
    "goalkeeper_shot",
    "six_metre_throw",
}

REQUIRED_GOALKEEPER_FIELDS = {
    "goalkeeper_id",
    "linked_finalization_id",
    "linked_finalization_event_code",
    "result_goalkeeper",
}

REQUIRED_SAVE_FIELDS = REQUIRED_GOALKEEPER_FIELDS | {"save_type"}

REQUIRED_EXCHANGE_FIELDS = {
    "goalkeeper_id",
    "specialist_id",
    "exchange_phase",
    "exchange_result",
    "court_overlap_detected",
}


def test_goalkeeper_v1_has_three_primary_events() -> None:
    assert list_primary_event_codes("goalkeeper_v1") == (
        "goalkeeper_save",
        "goalkeeper_goal_allowed",
        "goalkeeper_specialist_exchange",
    )
    for event_contract in GOALKEEPER_V1.primary_events:
        assert event_contract.ui_type == "botao_principal"


def test_goalkeeper_v1_is_not_importable_yet() -> None:
    assert GOALKEEPER_V1.import_rule_v1 == IMPORT_RULE_V1_BLOCKED
    for event_contract in GOALKEEPER_V1.event_contracts():
        assert event_contract.import_rule_v1 == IMPORT_RULE_V1_BLOCKED


def test_goalkeeper_primary_result_domains_are_separate() -> None:
    save_event, goal_allowed_event, exchange_event = GOALKEEPER_V1.primary_events

    assert save_event.event_code == "goalkeeper_save"
    assert save_event.allowed_results == SAVE_RESULTS
    assert "goal_allowed" not in save_event.allowed_results

    assert goal_allowed_event.event_code == "goalkeeper_goal_allowed"
    assert goal_allowed_event.allowed_results == GOAL_ALLOWED_RESULTS

    assert exchange_event.event_code == "goalkeeper_specialist_exchange"
    assert exchange_event.allowed_results == EXCHANGE_RESULTS
    assert SAVE_RESULTS.isdisjoint(exchange_event.allowed_results)
    assert GOAL_ALLOWED_RESULTS.isdisjoint(exchange_event.allowed_results)


def test_goalkeeper_v1_uses_auxiliary_fields_not_extra_events() -> None:
    auxiliary_codes = set(list_auxiliary_codes("goalkeeper_v1"))

    assert REQUIRED_SAVE_FIELDS.issubset(auxiliary_codes)
    assert REQUIRED_EXCHANGE_FIELDS.issubset(auxiliary_codes)
    assert {
        "save_body_part",
        "save_zone",
        "shot_goal_zone",
        "goalkeeper_positioning",
        "rebound_result",
        "possession_after_save",
        "restart_after_save",
        "transition_after_save",
        "trajectory_visible",
        "review_marker",
        "punishment_applied",
        "empty_goal_risk",
        "possession_phase",
    }.issubset(auxiliary_codes)
    assert "foot_save" not in all_event_codes("goalkeeper_v1")
    assert "hand_save" not in all_event_codes("goalkeeper_v1")
    assert "body_save" not in all_event_codes("goalkeeper_v1")


def test_goalkeeper_linked_finalizations_include_six_metre_throw() -> None:
    assert LINKED_FINALIZATION_CODES.issubset(set(all_event_codes("finalization_v1")))
    assert "six_metre_throw" in all_event_codes("finalization_v1")
    assert "shootout_attempt" not in LINKED_FINALIZATION_CODES


def test_goalkeeper_save_points_are_never_manual() -> None:
    derived_points = {result: "NA" for result in SAVE_RESULTS}

    assert derived_points == {
        "save_controlled": "NA",
        "save_rebound_live": "NA",
        "save_out_endline": "NA",
        "save_out_sideline": "NA",
        "uncertain_review": "NA",
    }


def test_goalkeeper_goal_allowed_is_required_for_real_efficiency() -> None:
    faced_results = SAVE_RESULTS | GOAL_ALLOWED_RESULTS
    save_count = len(SAVE_RESULTS - {"uncertain_review"})
    goal_allowed_count = 1

    assert "goal_allowed" in faced_results
    assert save_count == 4
    assert goal_allowed_count == 1
    assert GOALKEEPER_V1.primary_events[1].event_code == "goalkeeper_goal_allowed"


def test_goalkeeper_possession_rules_after_save_are_explicit() -> None:
    possession_after_save = {
        "save_controlled": "goalkeeper_team",
        "save_rebound_live": "live_ball",
        "save_out_endline": "goalkeeper_team",
        "save_out_sideline": "opponent_team",
    }
    restart_after_save = {
        "save_rebound_live": "live_play",
        "save_out_endline": "goalkeeper_throw",
        "save_out_sideline": "opponent_throw_in",
    }

    assert possession_after_save["save_out_endline"] == "goalkeeper_team"
    assert restart_after_save["save_out_endline"] == "goalkeeper_throw"
    assert possession_after_save["save_out_sideline"] == "opponent_team"
    assert restart_after_save["save_out_sideline"] == "opponent_throw_in"


def test_goalkeeper_exchange_cycle_is_operational_not_finalization_linked() -> None:
    auxiliary_codes = set(list_auxiliary_codes("goalkeeper_v1"))

    assert REQUIRED_EXCHANGE_FIELDS.issubset(auxiliary_codes)
    assert "goalkeeper_specialist_exchange" in list_primary_event_codes("goalkeeper_v1")
    assert "linked_finalization_id" in auxiliary_codes
    assert "goalkeeper_specialist_exchange" not in all_event_codes("finalization_v1")


def test_goalkeeper_boundaries_do_not_mix_shootout_or_line_block() -> None:
    assert "shootout_attempt" in GOALKEEPER_V1.forbidden_event_codes
    assert "line_block_shot" in GOALKEEPER_V1.forbidden_event_codes
    assert "goalkeeper_save" in all_event_codes("goalkeeper_v1")
    assert "goalkeeper_save" in set(
        __import__("scoutpraia.contracts.events_v1", fromlist=["SHOOTOUT_V1"])
        .SHOOTOUT_V1
        .forbidden_event_codes
    )
    assert "shootout_defender_origin_role" in all_event_codes("shootout_v1")


def test_goalkeeper_blocks_legacy_or_wrong_result_values() -> None:
    assert "goal_allowed_review" in GOALKEEPER_V1.forbidden_results
    assert "result_shootout" in GOALKEEPER_V1.forbidden_results
    assert "lost_possession_no_shot" in GOALKEEPER_V1.forbidden_results
    assert "goal_allowed_review" not in set().union(
        *(event.allowed_results for event in GOALKEEPER_V1.primary_events)
    )


def test_uncertain_review_requires_review_marker_by_contract() -> None:
    auxiliary_codes = set(list_auxiliary_codes("goalkeeper_v1"))

    assert "uncertain_review" in GOALKEEPER_V1.primary_events[0].allowed_results
    assert "review_marker" in auxiliary_codes


def test_overlap_violation_requires_punishment_context_by_contract() -> None:
    auxiliary_codes = set(list_auxiliary_codes("goalkeeper_v1"))
    exchange_results = GOALKEEPER_V1.primary_events[2].allowed_results

    assert "overlap_violation" in exchange_results
    assert "court_overlap_detected" in auxiliary_codes
    assert "punishment_applied" in auxiliary_codes
