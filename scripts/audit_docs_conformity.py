#!/usr/bin/env python3
"""Verifica conformidade da documentação do ScoutPraia com o padrão de frontmatter.

Escopo:
    - Todos os .md em docs/ têm frontmatter com doc_id, title, status, category, last_updated
    - doc_id segue padrão NNN_CATEG_* e são únicos no conjunto
    - Referências em docs/INDEX.json apontam para arquivos existentes
    - INDEX.json está sincronizado com os arquivos existentes em docs/
    - Nenhum arquivo faz referência a um nome de arquivo que não existe em docs/

Modo: READ-ONLY — não modifica arquivos
Gate/trigger: após qualquer mudança em docs/
Artefatos produzidos: nenhum

Examples:
    PYTHONPATH=. python3 scripts/audit_docs_conformity.py
    PYTHONPATH=. python3 scripts/audit_docs_conformity.py --strict
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
INDEX_PATH = DOCS_DIR / "INDEX.json"

REQUIRED_FRONTMATTER_FIELDS = {"doc_id", "title", "status", "category", "last_updated"}
VALID_STATUSES = {"canonical", "active", "draft", "deprecated", "historical"}
VALID_CATEGORIES = {"CONT", "PLAN", "PROT", "ARCH", "TAX", "SPEC", "AUDIT", "PROG", "UX", "RAG", "REF", "FLOW"}
DOC_ID_PATTERN = re.compile(r"^[A-Z0-9_]+$")

SKIP_DIRS = {"_deprecated", "evidence", "evidence_g5", "__pycache__"}


def _parse_frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---"):
        return None
    end = text.find("---", 3)
    if end == -1:
        return None
    fm_text = text[3:end].strip()
    result: dict[str, str] = {}
    for line in fm_text.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip().strip('"')
    return result


def _md_files(docs_dir: Path) -> Iterable[Path]:
    for path in sorted(docs_dir.rglob("*.md")):
        if any(skip in path.parts for skip in SKIP_DIRS):
            continue
        yield path


@dataclass
class Finding:
    path: str
    severity: str
    code: str
    message: str


@dataclass
class ConformityReport:
    findings: list[Finding] = field(default_factory=list)

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "error"]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "warning"]

    @property
    def ok(self) -> bool:
        return not self.errors

    def add(self, severity: str, code: str, path: str, message: str) -> None:
        self.findings.append(Finding(path=path, severity=severity, code=code, message=message))


def audit_frontmatter(docs_dir: Path, report: ConformityReport) -> dict[str, str]:
    doc_ids: dict[str, str] = {}

    for md_path in _md_files(docs_dir):
        rel = str(md_path.relative_to(REPO_ROOT))
        text = md_path.read_text(encoding="utf-8")
        fm = _parse_frontmatter(text)

        if fm is None:
            report.add("error", "missing_frontmatter", rel, "Arquivo sem frontmatter YAML")
            continue

        missing = REQUIRED_FRONTMATTER_FIELDS - set(fm.keys())
        if missing:
            report.add(
                "error", "missing_frontmatter_fields", rel,
                f"Campos obrigatórios ausentes: {sorted(missing)}"
            )

        doc_id = fm.get("doc_id", "")
        if doc_id:
            if not DOC_ID_PATTERN.match(doc_id):
                report.add(
                    "warning", "nonstandard_doc_id", rel,
                    f"doc_id '{doc_id}' não segue padrão NNN_CATEG_* (somente maiúsculas e underscores)"
                )
            if doc_id in doc_ids:
                report.add(
                    "error", "duplicate_doc_id", rel,
                    f"doc_id '{doc_id}' duplicado — também em {doc_ids[doc_id]}"
                )
            else:
                doc_ids[doc_id] = rel

        status = fm.get("status", "")
        if status and status not in VALID_STATUSES:
            report.add(
                "warning", "unknown_status", rel,
                f"status '{status}' não reconhecido. Válidos: {sorted(VALID_STATUSES)}"
            )

        category = fm.get("category", "")
        if category and category not in VALID_CATEGORIES:
            report.add(
                "warning", "unknown_category", rel,
                f"category '{category}' não reconhecida. Válidas: {sorted(VALID_CATEGORIES)}"
            )

    return doc_ids


def audit_index_sync(docs_dir: Path, index_path: Path, report: ConformityReport) -> None:
    if not index_path.exists():
        report.add("error", "index_missing", str(index_path.relative_to(REPO_ROOT)),
                   "docs/INDEX.json não existe — criar com scripts/audit_docs_conformity.py")
        return

    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        report.add("error", "index_invalid_json", "docs/INDEX.json", f"JSON inválido: {e}")
        return

    indexed_files = {doc["file"] for doc in index.get("documents", [])}

    existing_md = {
        str(p.relative_to(REPO_ROOT))
        for p in _md_files(docs_dir)
    }

    for f in indexed_files:
        if not (REPO_ROOT / f).exists():
            report.add("error", "index_broken_reference", "docs/INDEX.json",
                       f"Arquivo indexado não existe: {f}")

    not_indexed = existing_md - indexed_files - {str(index_path.relative_to(REPO_ROOT))}
    for f in sorted(not_indexed):
        report.add("warning", "file_not_in_index", "docs/INDEX.json",
                   f"Arquivo existe mas não está no INDEX.json: {f}")


def audit_cross_references(docs_dir: Path, report: ConformityReport) -> None:
    """Verifica apenas links Markdown explícitos: [texto](arquivo.md)"""
    all_doc_names = {p.name for p in docs_dir.rglob("*.md")}
    # Adicionar AGENTS.md (está na raiz, não em docs/)
    all_doc_names.add("AGENTS.md")
    # Padrão restrito: links Markdown [texto](caminho.md) — não qualquer menção de .md
    md_link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+\.md[^)]*)\)")

    for md_path in _md_files(docs_dir):
        rel = str(md_path.relative_to(REPO_ROOT))
        text = md_path.read_text(encoding="utf-8")
        for match in md_link_pattern.finditer(text):
            ref_path = match.group(2).strip()
            # Extrair apenas o nome do arquivo (sem âncora #...)
            ref_name = Path(ref_path.split("#")[0]).name
            if not ref_name:
                continue
            if ref_name not in all_doc_names and not ref_name.startswith("_"):
                report.add(
                    "warning", "broken_cross_reference", rel,
                    f"Link quebrado: '{match.group(0)}' → '{ref_name}' não encontrado em docs/"
                )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit ScoutPraia documentation conformity")
    parser.add_argument(
        "--strict", action="store_true",
        help="Tratar warnings como errors (exit 1 se houver warnings)"
    )
    args = parser.parse_args(argv)

    report = ConformityReport()

    audit_frontmatter(DOCS_DIR, report)
    audit_index_sync(DOCS_DIR, INDEX_PATH, report)
    audit_cross_references(DOCS_DIR, report)

    errors = report.errors
    warnings = report.warnings

    for finding in sorted(report.findings, key=lambda f: (f.severity, f.path)):
        marker = "ERROR" if finding.severity == "error" else "WARN "
        print(f"[{marker}] {finding.path}: [{finding.code}] {finding.message}")

    print(f"\nstatus={'ok' if report.ok else 'fail'} errors={len(errors)} warnings={len(warnings)}")

    if errors:
        return 1
    if args.strict and warnings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
