from pathlib import Path

from openpyxl import Workbook

from scripts.audit_scout_design_template import (
    audit_workbook,
    registry_module_codes,
    registry_primary_event_codes,
)


def test_audit_reports_missing_required_sheets(tmp_path: Path) -> None:
    workbook_path = tmp_path / "template.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "EVENTOS"
    ws.append(["code"])
    ws.append(["simple_shot"])
    wb.save(workbook_path)

    report = audit_workbook(workbook_path)

    assert not report.ok
    assert "missing sheet: MODULE_INDEX" in report.errors
    assert "EVENTOS missing header: repo_symbol" in report.errors


def test_audit_registry_helpers_expose_expected_contract_surface() -> None:
    assert {
        "finalization_v1",
        "attack_no_shot_v1",
        "shootout_v1",
        "goalkeeper_v1",
        "transition_v1",
    }.issubset(registry_module_codes())
    assert {
        "simple_shot",
        "shootout_attempt",
        "goalkeeper_save",
        "transition_sequence",
    }.issubset(registry_primary_event_codes())
