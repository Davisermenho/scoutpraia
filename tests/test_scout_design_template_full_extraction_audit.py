import json
from pathlib import Path

from openpyxl import Workbook

from scripts.audit_scout_design_template_full_extraction import CRITICAL_SHEETS, audit_extraction

CRITICAL_SHEETS_LIST = sorted(CRITICAL_SHEETS)

REQUIRED_RULE_TEXT = " ".join(
    [
        "specialist não é event_code; event_code=specialist_shot proibido",
        "specialist não é position_code; position_code=specialist proibido",
        "simple_shot goal specialist 2 pontos",
        "shootout save não goalkeeper_save",
        "goalkeeper_save linked_finalization_id obrigatório",
        "transition_sequence não calcula pontos",
        "transition_goal exige terminal de Finalização",
        "G5 pendente; MVP completo não pode ser declarado",
        "RAG não decide lance automaticamente",
    ]
)


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_xlsx(path: Path, sheet_names: list[str]) -> None:
    workbook = Workbook()
    default = workbook.active
    default.title = sheet_names[0]
    for sheet_name in sheet_names[1:]:
        workbook.create_sheet(sheet_name)
    workbook.save(path)
    workbook.close()


def make_full_workbook(path: Path, extra_sheets: list[str] | None = None) -> None:
    sheets = CRITICAL_SHEETS_LIST + (extra_sheets or [])
    workbook = Workbook()
    workbook.active.title = sheets[0]
    for name in sheets[1:]:
        workbook.create_sheet(name)
    workbook.save(path)
    workbook.close()


def make_chunk(chunk_id: str, sheet_name: str, content: str | None = None) -> dict:
    return {
        "chunk_id": chunk_id,
        "title": f"Chunk {sheet_name}",
        "theme": "test",
        "priority": "critical",
        "agent_use": "test_audit",
        "sheet_name": sheet_name,
        "chunk_type": "contract_table",
        "row_range": "1-10",
        "content": content or f"Conteúdo de {sheet_name}. {REQUIRED_RULE_TEXT}",
    }


def _make_dict_chunk(chunk_id: str, sheet_name: str, headers: list[str], rows: list[dict]) -> dict:
    chunk = make_chunk(chunk_id, sheet_name)
    chunk["content"] = {"headers": headers, "rows": rows}
    return chunk


def test_full_extraction_audit_passes_when_all_sheets_and_rules_are_covered(tmp_path: Path) -> None:
    xlsx_path = tmp_path / "template.xlsx"
    chunks_path = tmp_path / "chunks.json"
    make_full_workbook(xlsx_path)
    write_json(
        chunks_path,
        {
            "expected_sheet_count": len(CRITICAL_SHEETS_LIST),
            "chunks": [
                make_chunk(f"SDT-SHEET-{i:04d}", sheet)
                for i, sheet in enumerate(CRITICAL_SHEETS_LIST, start=1)
            ],
        },
    )

    report = audit_extraction(chunks_path=chunks_path, xlsx_path=xlsx_path, full_extraction=True)

    assert report.ok, f"errors={[f.code for f in report.errors]}"


def test_full_extraction_audit_fails_when_xlsx_sheet_is_missing_from_chunks(tmp_path: Path) -> None:
    xlsx_path = tmp_path / "template.xlsx"
    chunks_path = tmp_path / "chunks.json"
    write_xlsx(xlsx_path, ["EVENTOS", "MODULE_INDEX"])
    write_json(
        chunks_path,
        {
            "expected_sheet_count": 2,
            "chunks": [make_chunk("SDT-SHEET-0001", "EVENTOS")],
        },
    )

    report = audit_extraction(
        chunks_path=chunks_path,
        xlsx_path=xlsx_path,
        full_extraction=True,
    )

    assert not report.ok
    assert any(finding.code == "missing_sheet_coverage" for finding in report.errors)


def test_full_extraction_audit_fails_when_required_rule_is_missing(tmp_path: Path) -> None:
    xlsx_path = tmp_path / "template.xlsx"
    chunks_path = tmp_path / "chunks.json"
    write_xlsx(xlsx_path, ["EVENTOS"])
    write_json(
        chunks_path,
        {
            "expected_sheet_count": 1,
            "chunks": [
                make_chunk(
                    "SDT-SHEET-0001",
                    "EVENTOS",
                    content="Conteúdo incompleto sem regras críticas.",
                )
            ],
        },
    )

    report = audit_extraction(
        chunks_path=chunks_path,
        xlsx_path=xlsx_path,
        full_extraction=True,
    )

    assert not report.ok
    assert any(finding.code == "missing_required_rule" for finding in report.errors)


def test_synthetic_agent_view_can_warn_about_missing_sheet_metadata_without_failing(tmp_path: Path) -> None:
    chunks_path = tmp_path / "chunks.json"
    write_json(
        chunks_path,
        {
            "chunks": [
                {
                    "chunk_id": "SDT-AGENT-0001",
                    "title": "Síntese",
                    "theme": "governance",
                    "priority": "critical",
                    "agent_use": "orientation",
                    "content": REQUIRED_RULE_TEXT,
                }
            ]
        },
    )

    report = audit_extraction(chunks_path=chunks_path, full_extraction=False)

    assert report.ok
    assert any(finding.code == "no_sheet_level_metadata" for finding in report.warnings)


def test_critical_sheet_with_empty_sheet_flag_is_error(tmp_path: Path) -> None:
    chunks_path = tmp_path / "chunks.json"
    chunk = make_chunk("SDT-SHEET-0001", "EVENTOS")
    chunk["content"] = {"headers": [], "rows": [], "empty_sheet": True}
    write_json(chunks_path, {"chunks": [chunk]})

    report = audit_extraction(chunks_path=chunks_path, full_extraction=False)

    assert not report.ok
    assert any(f.code == "critical_sheet_empty" for f in report.errors)


def test_event_code_without_field_rules_generates_warning(tmp_path: Path) -> None:
    chunks_path = tmp_path / "chunks.json"
    write_json(
        chunks_path,
        {
            "chunks": [
                _make_dict_chunk(
                    "SDT-SHEET-0001",
                    "EVENTOS",
                    ["event_code"],
                    [{"_sheet_row": 2, "event_code": "orphan_event"}],
                ),
                _make_dict_chunk(
                    "SDT-SHEET-0002",
                    "EVENT_REQUIRED_FIELDS",
                    ["event_code", "field_code"],
                    [{"_sheet_row": 2, "event_code": "other_event", "field_code": "athlete_id"}],
                ),
            ]
        },
    )

    report = audit_extraction(chunks_path=chunks_path, full_extraction=False)

    assert any(f.code == "event_code_without_field_rules" for f in report.warnings)


def test_cross_reference_to_missing_sheet_generates_warning(tmp_path: Path) -> None:
    chunks_path = tmp_path / "chunks.json"
    chunk = make_chunk("SDT-SHEET-0001", "EVENTOS")
    chunk["cross_reference_sheets"] = ["SHEET_INEXISTENTE"]
    write_json(chunks_path, {"chunks": [chunk]})

    report = audit_extraction(chunks_path=chunks_path, full_extraction=False)

    assert any(f.code == "cross_reference_sheet_missing" for f in report.warnings)
