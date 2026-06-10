from scoutpraia.contracts.events_v1 import (
    IMPORT_RULE_V1_BLOCKED,
    FINALIZATION_V1,
    MODULE_CONTRACTS_V1,
    NO_SHOT_ATTACK_V1,
    all_event_codes,
    get_module_contract,
    list_auxiliary_codes,
    list_primary_event_codes,
)


def test_contract_registry_exposes_both_v1_modules() -> None:
    assert set(MODULE_CONTRACTS_V1) == {"finalization_v1", "no_shot_attack_v1"}
    assert get_module_contract("finalization_v1") is FINALIZATION_V1
    assert get_module_contract("no_shot_attack_v1") is NO_SHOT_ATTACK_V1


def test_finalization_primary_events_match_the_validated_contract() -> None:
    assert list_primary_event_codes("finalization_v1") == (
        "simple_shot",
        "spin_shot",
        "inflight_shot",
        "goalkeeper_shot",
        "six_metre_throw",
    )


def test_auxiliary_codes_are_not_exposed_as_primary_buttons() -> None:
    finalization_primary = set(list_primary_event_codes("finalization_v1"))
    finalization_auxiliary = set(list_auxiliary_codes("finalization_v1"))

    assert finalization_auxiliary == {"specialist_finish_role"}
    assert finalization_primary.isdisjoint(finalization_auxiliary)
    assert "specialist_finish_role" not in finalization_primary
    assert "shootout_attempt" not in all_event_codes("finalization_v1")


def test_import_rule_remains_blocked_for_every_v1_contract_item() -> None:
    for module_contract in MODULE_CONTRACTS_V1.values():
        assert module_contract.import_rule_v1 == IMPORT_RULE_V1_BLOCKED
        for event_contract in module_contract.event_contracts():
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
