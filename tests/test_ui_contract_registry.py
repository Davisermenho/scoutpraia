"""Tests for scoutpraia/ui/contracts.py — UX_011 enforcement.

Proves that:
- Forbidden event codes (specialist_goal, specialist_attempt, shootout_goal) are not
  in the active quick-event code list.
- All finalization_v1 and attack_no_shot_v1 primary events ARE present.
- FORBIDDEN_EVENT_CODES detects blocked events correctly.
"""

import pytest

from scoutpraia.ui.contracts import (
    FORBIDDEN_EVENT_CODES,
    get_active_quick_event_codes,
    get_active_modules,
    is_blocked_event,
)
from scoutpraia.contracts.events_v1 import (
    FINALIZATION_V1,
    NO_SHOT_ATTACK_V1,
    IMPORT_RULE_V1_ACTIVE,
)


@pytest.fixture
def active_codes() -> list[str]:
    return get_active_quick_event_codes()


# --- Active modules ---


def test_exactly_two_active_modules():
    modules = get_active_modules()
    module_codes = {m.module_code for m in modules}
    assert module_codes == {"finalization_v1", "attack_no_shot_v1"}


# --- Forbidden codes absent from active list ---


def test_specialist_attempt_not_in_active_codes(active_codes):
    assert "specialist_attempt" not in active_codes


def test_specialist_goal_not_in_active_codes(active_codes):
    assert "specialist_goal" not in active_codes


def test_shootout_goal_not_in_active_codes(active_codes):
    assert "shootout_goal" not in active_codes


def test_specialist_shot_not_in_active_codes(active_codes):
    assert "specialist_shot" not in active_codes


def test_shootout_attempt_not_in_active_codes(active_codes):
    assert "shootout_attempt" not in active_codes


# --- Finalization events present ---


def test_finalization_primary_events_in_active_codes(active_codes):
    for event in FINALIZATION_V1.primary_events:
        if event.import_rule_v1 == IMPORT_RULE_V1_ACTIVE:
            assert event.event_code in active_codes, f"{event.event_code} missing"


def test_simple_shot_in_active_codes(active_codes):
    assert "simple_shot" in active_codes


def test_spin_shot_in_active_codes(active_codes):
    assert "spin_shot" in active_codes


def test_inflight_shot_in_active_codes(active_codes):
    assert "inflight_shot" in active_codes


def test_goalkeeper_shot_in_active_codes(active_codes):
    assert "goalkeeper_shot" in active_codes


def test_six_metre_throw_in_active_codes(active_codes):
    assert "six_metre_throw" in active_codes


# --- Attack no-shot events present ---


def test_no_shot_primary_events_in_active_codes(active_codes):
    for event in NO_SHOT_ATTACK_V1.primary_events:
        if event.import_rule_v1 == IMPORT_RULE_V1_ACTIVE:
            assert event.event_code in active_codes, f"{event.event_code} missing"


def test_technical_error_unforced_in_active_codes(active_codes):
    assert "technical_error_unforced" in active_codes


def test_offensive_foul_in_active_codes(active_codes):
    assert "offensive_foul" in active_codes


# --- FORBIDDEN_EVENT_CODES ---


def test_forbidden_codes_is_frozenset():
    assert isinstance(FORBIDDEN_EVENT_CODES, frozenset)


def test_specialist_shot_is_forbidden():
    assert "specialist_shot" in FORBIDDEN_EVENT_CODES


def test_shootout_attempt_is_forbidden():
    assert "shootout_attempt" in FORBIDDEN_EVENT_CODES


def test_is_blocked_event_specialist_shot():
    assert is_blocked_event("specialist_shot") is True


def test_is_blocked_event_shootout_attempt():
    assert is_blocked_event("shootout_attempt") is True


def test_is_blocked_event_simple_shot_is_false():
    assert is_blocked_event("simple_shot") is False


def test_is_blocked_event_technical_error_unforced_is_false():
    assert is_blocked_event("technical_error_unforced") is False
