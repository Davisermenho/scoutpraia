"""Contracts for staged event modules not yet imported into the app."""

from scoutpraia.contracts.events_v1 import (
    GOALKEEPER_V1,
    IMPORT_RULE_V1_BLOCKED,
    MODULE_CONTRACTS_V1,
    SHOOTOUT_V1,
    EventContract,
    ModuleContract,
    all_event_codes,
    get_module_contract,
    list_auxiliary_codes,
    list_future_event_codes,
    list_primary_event_codes,
    list_review_event_codes,
)

__all__ = [
    "GOALKEEPER_V1",
    "IMPORT_RULE_V1_BLOCKED",
    "MODULE_CONTRACTS_V1",
    "SHOOTOUT_V1",
    "EventContract",
    "ModuleContract",
    "all_event_codes",
    "get_module_contract",
    "list_auxiliary_codes",
    "list_future_event_codes",
    "list_primary_event_codes",
    "list_review_event_codes",
]
