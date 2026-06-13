"""Tests for P0_006 — QUICK_EVENT_TYPES must not expose forbidden event codes.

Verifies that tagging.py QUICK_EVENT_TYPES is derived from the ui/contracts registry
and does not contain specialist_goal, specialist_attempt, shootout_goal, or any other
event code blocked by the UX contract (UX_011).
"""

import importlib

import pytest

import scoutpraia.pages.tagging as tagging_module
from scoutpraia.ui.contracts import FORBIDDEN_EVENT_CODES, get_active_quick_event_codes


@pytest.fixture
def quick_event_types() -> list[str]:
    return list(tagging_module.QUICK_EVENT_TYPES)


# --- Forbidden codes absent ---


def test_specialist_attempt_not_in_quick_event_types(quick_event_types):
    assert "specialist_attempt" not in quick_event_types


def test_specialist_goal_not_in_quick_event_types(quick_event_types):
    assert "specialist_goal" not in quick_event_types


def test_shootout_goal_not_in_quick_event_types(quick_event_types):
    assert "shootout_goal" not in quick_event_types


def test_shot_attempt_legacy_not_in_quick_event_types(quick_event_types):
    assert "shot_attempt" not in quick_event_types


def test_goal_scored_legacy_not_in_quick_event_types(quick_event_types):
    assert "goal_scored" not in quick_event_types


def test_no_explicitly_prohibited_code_in_quick_event_types(quick_event_types):
    # These codes are prohibited across all modules and must never appear as buttons.
    explicitly_prohibited = {"specialist_attempt", "specialist_goal", "shootout_goal", "specialist_shot", "shootout_attempt"}
    overlap = [code for code in quick_event_types if code in explicitly_prohibited]
    assert overlap == [], f"Prohibited codes in QUICK_EVENT_TYPES: {overlap}"


# --- Active codes present ---


def test_quick_event_types_equals_registry(quick_event_types):
    assert quick_event_types == get_active_quick_event_codes()


def test_simple_shot_in_quick_event_types(quick_event_types):
    assert "simple_shot" in quick_event_types


def test_technical_error_unforced_in_quick_event_types(quick_event_types):
    assert "technical_error_unforced" in quick_event_types


# --- Non-empty ---


def test_quick_event_types_not_empty(quick_event_types):
    assert len(quick_event_types) > 0
