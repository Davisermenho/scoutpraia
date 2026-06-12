from pathlib import Path

from scripts.audit_docs_contract_alignment import (
    AuditReport,
    audit_completion_claims,
    audit_forbidden_codes,
    audit_required_doc_patterns,
    audit_specialist_contract_consistency,
)


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def seed_required_docs(root: Path, taxonomy_text: str) -> None:
    write_file(root / "docs/taxonomy_dictionary.md", taxonomy_text)
    write_file(root / "docs/evidence_matrix.md", "sem codigo legado ativo\n")
    write_file(root / "docs/IMPLEMENTATION_PLAN_EVENTOS_V1.md", "sem codigo legado ativo\n")
    write_file(root / "docs/Contrato_Operacional.md", "sem codigo legado ativo\n")
    write_file(root / "docs/ARCHITECTURE_README.md", "sem codigo legado ativo\n")


def test_flags_legacy_code_when_presented_as_active(tmp_path: Path) -> None:
    seed_required_docs(
        tmp_path,
        "| `specialist_goal` | evento ativo | aprovado para KPI final |\n",
    )

    report = AuditReport()
    audit_forbidden_codes(tmp_path, report)

    assert any(
        finding.severity == "error"
        and finding.code == "forbidden_or_legacy_code_without_context"
        and "specialist_goal" in finding.message
        for finding in report.findings
    )


def test_allows_legacy_code_when_marked_as_migration(tmp_path: Path) -> None:
    seed_required_docs(
        tmp_path,
        "| `specialist_goal` | legado bloqueado em LEGACY_MIGRATION_RULES |\n",
    )

    report = AuditReport()
    audit_forbidden_codes(tmp_path, report)

    assert not report.errors


def test_points_policy_blocks_specialist_misclassification() -> None:
    report = AuditReport()

    audit_specialist_contract_consistency(Path.cwd(), report)

    assert report.ok


def test_required_doc_patterns_detect_missing_architecture_contract(tmp_path: Path) -> None:
    write_file(tmp_path / "docs/ARCHITECTURE_README.md", "Documento incompleto\n")
    write_file(tmp_path / "docs/IMPLEMENTATION_PROGRESS.md", "Documento sem points policy\n")

    report = AuditReport()
    audit_required_doc_patterns(tmp_path, report)

    assert report.errors
    assert any(finding.code == "required_contract_statement_missing" for finding in report.errors)


def test_completion_claims_warns_on_unqualified_completion_claim(tmp_path: Path) -> None:
    write_file(tmp_path / "docs/IMPLEMENTATION_PROGRESS.md", "MVP completo declarado\n")
    write_file(tmp_path / "docs/validation_protocol.md", "G5 aberto; MVP nao pode ser completo\n")
    write_file(tmp_path / "docs/AUDIT_EVIDENCE_VALIDATION.md", "RAG bloqueado\n")
    write_file(tmp_path / "docs/rag_workflow.md", "RAG_liberado: false\n")

    report = AuditReport()
    audit_completion_claims(tmp_path, report)

    assert any(finding.code == "mvp_complete_claim" for finding in report.warnings)
