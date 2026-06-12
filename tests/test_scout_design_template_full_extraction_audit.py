import json
from pathlib import Path

from openpyxl import Workbook

from scripts.audit_scout_design_template_full_extraction import audit_extraction


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


def test_full_extraction_audit_passes_when_all_sheets_and_rules_are_covered(tmp_path: Path) -> None:
    xlsx_path = tmp_path / "template.xlsx"
    chunks_path = tmp_path / "chunks.json"
    sheets = ["EVENTOS", "MODULE_INDEX", "FIELD_DICTIONARY_GLOBAL"]
    write_xlsx(xlsx_path, sheets)
    write_json(
        chunks_path,
        {
            "expected_sheet_count": 3,
            "chunks": [make_chunk("SDT-SHEET-0001", sheet) for sheet in sheets],
        },
    )

    report = audit_extraction(
        chunks_path=chunks_path,
        xlsx_path=xlsx_path,
        full_extraction=True,
    )

    assert report.ok


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
