"""UI contracts derived from the events_v1 registry.

Single source of truth for which event codes may appear in quick-event buttons.
No UI surface may expose a code not returned by get_active_quick_event_codes().
"""

from __future__ import annotations

from scoutpraia.contracts.events_v1 import (
    DEFENSIVE_V1,
    FINALIZATION_V1,
    GOALKEEPER_V1,
    IMPORT_RULE_V1_ACTIVE,
    NO_SHOT_ATTACK_V1,
    OFFENSIVE_CREATION_V1,
    SHOOTOUT_V1,
    TRANSITION_V1,
    ModuleContract,
)

_ALL_MODULES: tuple[ModuleContract, ...] = (
    FINALIZATION_V1,
    NO_SHOT_ATTACK_V1,
    OFFENSIVE_CREATION_V1,
    DEFENSIVE_V1,
    SHOOTOUT_V1,
    GOALKEEPER_V1,
    TRANSITION_V1,
)


def get_active_modules() -> tuple[ModuleContract, ...]:
    return tuple(m for m in _ALL_MODULES if m.import_rule_v1 == IMPORT_RULE_V1_ACTIVE)


def get_active_quick_event_codes() -> list[str]:
    """Return primary event codes from all IMPORT_RULE_V1_ACTIVE modules, in module order."""
    codes: list[str] = []
    for module in get_active_modules():
        for event in module.primary_events:
            if event.import_rule_v1 == IMPORT_RULE_V1_ACTIVE:
                codes.append(event.event_code)
    return codes


FORBIDDEN_EVENT_CODES: frozenset[str] = frozenset().union(
    *(m.forbidden_event_codes for m in _ALL_MODULES)
)


def is_blocked_event(event_code: str) -> bool:
    """Return True if event_code must not appear in any quick-event UI surface."""
    return event_code not in get_active_quick_event_codes()
