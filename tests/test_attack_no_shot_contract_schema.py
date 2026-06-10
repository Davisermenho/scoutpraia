import json
from pathlib import Path

from scoutpraia.services.attack_no_shot_contract import (
    ATTACK_NO_SHOT_EVENTS,
    ATTACK_NO_SHOT_RESULT,
    load_attack_no_shot_contract,
)

CONTRACT_PATH = Path("contracts/attack_no_shot_v1.json")
SCHEMA_PATH = Path("contracts/attack_no_shot_v1.schema.json")

REQUIRED_TOP_LEVEL_KEYS = {
    "contract_id",
    "project",
    "module",
    "version",
    "status",
    "semantic_source",
    "implementation_source",
    "runtime_source",
    "test_source",
    "module_rule",
    "controlled_values",
    "events",
}

REQUIRED_EVENT_KEYS = {
    "code",
    "name_ui",
    "category",
    "definition",
    "include_when",
    "exclude_when",
    "decision_rule",
    "allowed_points",
    "required_fields",
    "optional_fields",
    "derived_fields",
    "forbidden_fields",
    "blocking_rules",
    "ui_type",
    "validation_source",
    "status",
    "positive_example",
    "negative_example",
    "common_error",
    "acceptance_tests",
}

EXPECTED_EVENT_CODES = {
    "technical_error_unforced",
    "technical_error_forced",
    "offensive_foul",
    "goal_area_invasion_attack",
    "passive_play_turnover",
    "bad_substitution_attack",
    "turnover_unclassified",
}


def test_machine_contract_file_is_valid_json():
    parsed = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    assert parsed["contract_id"] == "attack_no_shot_v1"
    assert parsed["module"] == "Ataque sem Finalização"


def test_schema_file_is_valid_json_and_declares_required_contract_shape():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    assert schema["type"] == "object"
    assert set(schema["required"]) == REQUIRED_TOP_LEVEL_KEYS
    assert "event" in schema["$defs"]
    assert set(schema["$defs"]["event"]["required"]) == REQUIRED_EVENT_KEYS


def test_machine_contract_has_required_top_level_keys():
    contract = load_attack_no_shot_contract()
    assert set(contract) == REQUIRED_TOP_LEVEL_KEYS


def test_machine_contract_has_exactly_the_approved_seven_events():
    contract = load_attack_no_shot_contract()
    event_codes = {event["code"] for event in contract["events"]}
    assert event_codes == EXPECTED_EVENT_CODES
    assert len(contract["events"]) == 7


def test_every_event_is_ia_readable_and_contract_driven():
    contract = load_attack_no_shot_contract()
    for event in contract["events"]:
        assert REQUIRED_EVENT_KEYS.issubset(event)
        assert event["category"] == "Ataque sem finalização"
        assert event["include_when"]
        assert event["exclude_when"]
        assert event["definition"]
        assert event["decision_rule"]
        assert event["positive_example"]
        assert event["negative_example"]
        assert event["common_error"]
        assert event["acceptance_tests"]
        assert event["derived_fields"]["result_possession_auto"] == ATTACK_NO_SHOT_RESULT
        assert event["derived_fields"]["points"] == 0
        assert "finish_type_code" in event["forbidden_fields"]
        assert "goal_zone" in event["forbidden_fields"]
        assert event["blocking_rules"]


def test_runtime_contract_is_loaded_from_machine_contract():
    contract = load_attack_no_shot_contract()
    machine_event_codes = {event["code"] for event in contract["events"]}
    runtime_event_codes = set(ATTACK_NO_SHOT_EVENTS)
    assert runtime_event_codes == machine_event_codes


def test_controlled_values_match_contract_requirements():
    contract = load_attack_no_shot_contract()
    controlled_values = contract["controlled_values"]
    assert "technical_error_subtype" in controlled_values
    assert "pass_error" in controlled_values["technical_error_subtype"]
    assert "passive_play_subtype" in controlled_values
    assert "passive_fifth_pass_no_shot" in controlled_values["passive_play_subtype"]
    assert "substitution_error_subtype" in controlled_values
    assert "substitution_violation_other" in controlled_values["substitution_error_subtype"]
