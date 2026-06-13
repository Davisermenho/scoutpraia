"""Audit docs against executable ScoutPraia contracts.

This script detects semantic drift between documentation and executable contracts.
It does not modify files. It exits with code 1 when a blocking drift is found.

Intended use:
    PYTHONPATH=. python3 scripts/audit_docs_contract_alignment.py

Scope:
    - specialist must be a role/field, never an active event or position;
    - legacy/future codes must not appear as active KPI/event guidance;
    - points policy must be present as the global scoring authority;
    - docs must not claim MVP/RAG completion while gates remain blocked.

Modo: READ-ONLY — não modifica arquivos
Gate/trigger: antes de declarar MVP ou contrato como fechado
Artefatos produzidos: nenhum
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from scoutpraia.contracts.points_policy_v1 import (
    FORBIDDEN_EVENT_CODES as POINTS_FORBIDDEN_EVENT_CODES,
    FORBIDDEN_POSITION_CODES as POINTS_FORBIDDEN_POSITION_CODES,
    POINT_RULES,
)


FORBIDDEN_ACTIVE_EVENT_CODES = frozenset(
    {
        "specialist_shot",
        "specialist_attempt",
        "specialist_goal",
        "save_shootout",
        "goal_conceded",
        "empty_goal_conceded",
        "fast_break_against",
        "transition_recovery_good",
        "transition_recovery_bad",
    }
)

LEGACY_ALLOWED_CONTEXT_MARKERS = (
    "legacy",
    "legado",
    "deprecated",
    "bloqueado",
    "forbidden",
    "proibido",
    "migration",
    "migração",
    "migracao",
    "EVENTOS_LEGADOS_FUTUROS",
    "LEGACY_MIGRATION_RULES",
    "forbidden_event_codes",
    "forbidden_event_code",
    "não usar",
    "nao_usar",
    "não entra",
    "nao entra",
    "substituído",
    "substituido",
)

ACTIVE_STATUS_MARKERS = (
    "approved",
    "contrato_ativo",
    "contrato_ativo_v1",
    "evento ativo",
    "botao_principal",
    "botão principal",
    "KPI final",
    "kpi final",
)

DOC_PATHS_TO_SCAN = (
    "docs/006_TAX_Dicionario_Taxonomia.md",
    "docs/008_AUDIT_Matriz_Evidencias.md",
    "docs/014_PLAN_Eventos_v1.md",
    "docs/005_CONT_Operacional_Eventos_v1.md",
    "docs/013_ARCH_Readme.md",
)

REQUIRED_DOC_PATTERNS = {
    "docs/013_ARCH_Readme.md": [
        r"SCOUT_DESIGN_TEMPLATE.*contrato de arquitetura",
        r"events_v1\.py.*registry executável|events_v1\.py.*registry executavel",
        r"não é banco oficial de lances|nao e banco oficial de lances",
    ],
    "docs/004_PROG_Progresso_Implementacao.md": [
        r"points_policy_v1",
        r"não alteram seed, UI ou importação|nao alteram seed, UI ou importacao",
    ],
}


@dataclass
class Finding:
    path: str
    line_no: int
    severity: str
    code: str
    message: str
    line: str


@dataclass
class AuditReport:
    findings: list[Finding] = field(default_factory=list)

    @property
    def errors(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.severity == "error"]

    @property
    def warnings(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.severity == "warning"]

    @property
    def ok(self) -> bool:
        return not self.errors

    def add(
        self,
        *,
        path: str,
        line_no: int,
        severity: str,
        code: str,
        message: str,
        line: str,
    ) -> None:
        self.findings.append(
            Finding(
                path=path,
                line_no=line_no,
                severity=severity,
                code=code,
                message=message,
                line=line.strip(),
            )
        )


def normalize(text: str) -> str:
    return text.lower()


def line_has_legacy_allowed_context(line: str) -> bool:
    normalized = normalize(line)
    return any(marker.lower() in normalized for marker in LEGACY_ALLOWED_CONTEXT_MARKERS)


def line_has_active_marker(line: str) -> bool:
    normalized = normalize(line)
    return any(marker.lower() in normalized for marker in ACTIVE_STATUS_MARKERS)


def iter_file_lines(repo_root: Path, relative_path: str) -> Iterable[tuple[int, str]]:
    path = repo_root / relative_path
    if not path.exists():
        return []
    return enumerate(path.read_text(encoding="utf-8").splitlines(), start=1)


def audit_forbidden_codes(repo_root: Path, report: AuditReport) -> None:
    for relative_path in DOC_PATHS_TO_SCAN:
        path = repo_root / relative_path
        if not path.exists():
            report.add(
                path=relative_path,
                line_no=0,
                severity="warning",
                code="missing_doc",
                message="Documento esperado não existe para auditoria de alinhamento.",
                line="",
            )
            continue

        for line_no, line in iter_file_lines(repo_root, relative_path):
            for event_code in FORBIDDEN_ACTIVE_EVENT_CODES:
                if event_code not in line:
                    continue

                if line_has_legacy_allowed_context(line):
                    continue

                severity = "error" if line_has_active_marker(line) else "warning"
                report.add(
                    path=relative_path,
                    line_no=line_no,
                    severity=severity,
                    code="forbidden_or_legacy_code_without_context",
                    message=(
                        f"{event_code} aparece sem contexto claro de legado/bloqueio; "
                        "pode reativar código antigo no agente."
                    ),
                    line=line,
                )


def audit_specialist_contract_consistency(repo_root: Path, report: AuditReport) -> None:
    points_forbidden = POINTS_FORBIDDEN_EVENT_CODES | POINTS_FORBIDDEN_POSITION_CODES
    if "specialist_shot" not in points_forbidden:
        report.add(
            path="scoutpraia/contracts/points_policy_v1.py",
            line_no=0,
            severity="error",
            code="specialist_shot_not_forbidden",
            message="points_policy_v1 não bloqueia specialist_shot como evento/posição.",
            line="",
        )

    specialist_goal_rule = POINT_RULES.get(("simple_shot", "goal", "specialist"))
    if specialist_goal_rule != 2:
        report.add(
            path="scoutpraia/contracts/points_policy_v1.py",
            line_no=0,
            severity="error",
            code="specialist_goal_not_two_points",
            message="simple_shot + goal + specialist precisa derivar 2 pontos.",
            line="",
        )


def audit_required_doc_patterns(repo_root: Path, report: AuditReport) -> None:
    for relative_path, patterns in REQUIRED_DOC_PATTERNS.items():
        path = repo_root / relative_path
        if not path.exists():
            report.add(
                path=relative_path,
                line_no=0,
                severity="error",
                code="required_doc_missing",
                message="Documento obrigatório ausente.",
                line="",
            )
            continue

        text = path.read_text(encoding="utf-8")
        for pattern in patterns:
            if re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL):
                continue
            report.add(
                path=relative_path,
                line_no=0,
                severity="error",
                code="required_contract_statement_missing",
                message=f"Padrão obrigatório ausente: {pattern}",
                line="",
            )


def audit_completion_claims(repo_root: Path, report: AuditReport) -> None:
    risky_patterns = {
        "MVP completo": "mvp_complete_claim",
        "RAG liberado": "rag_released_claim",
        "Chroma implementado": "chroma_complete_claim",
        "taxonomia aprovada": "taxonomy_approved_claim",
    }
    allowed_context = (
        "não",
        "nao",
        "blocked",
        "bloqueado",
        "não pode",
        "nao pode",
        "false",
        "pendente",
        "aberto",
        "não executada",
        "nao executada",
    )

    for relative_path in (
        "docs/004_PROG_Progresso_Implementacao.md",
        "docs/007_PROT_Protocolo_Validacao.md",
        "docs/010_AUDIT_Validacao_G5.md",
        "docs/009_RAG_Workflow_Fontes.md",
    ):
        path = repo_root / relative_path
        if not path.exists():
            continue
        for line_no, line in iter_file_lines(repo_root, relative_path):
            normalized = normalize(line)
            for phrase, finding_code in risky_patterns.items():
                if phrase.lower() not in normalized:
                    continue
                if any(marker in normalized for marker in allowed_context):
                    continue
                report.add(
                    path=relative_path,
                    line_no=line_no,
                    severity="warning",
                    code=finding_code,
                    message=(
                        f"A frase '{phrase}' aparece sem negação/bloqueio claro; "
                        "pode sugerir conclusão indevida."
                    ),
                    line=line,
                )


def audit_repo(repo_root: Path) -> AuditReport:
    report = AuditReport()
    audit_specialist_contract_consistency(repo_root, report)
    audit_forbidden_codes(repo_root, report)
    audit_required_doc_patterns(repo_root, report)
    audit_completion_claims(repo_root, report)
    return report


def format_report(report: AuditReport) -> str:
    lines = [
        "== docs x contracts semantic alignment audit ==",
        f"status={'ok' if report.ok else 'failed'}",
        f"errors={len(report.errors)}",
        f"warnings={len(report.warnings)}",
    ]

    for severity, findings in (("errors", report.errors), ("warnings", report.warnings)):
        if not findings:
            continue
        lines.append(f"\n-- {severity} --")
        for finding in findings:
            lines.append(
                f"- {finding.path}:{finding.line_no} [{finding.code}] {finding.message}"
            )
            if finding.line:
                lines.append(f"  line: {finding.line}")

    return "\n".join(lines)


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audita alinhamento semântico entre docs e contratos")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Raiz do repositório. Padrão: diretório atual.",
    )
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    report = audit_repo(args.repo_root)
    print(format_report(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
