#!/usr/bin/env python3
""" EXPORTADOR PLANILHA - CSV (v.0.2) 

  Uso: python3 scripts/export_scout_design_csv.py

Exporta docs/SCOUT_DESIGN_TEMPLATE.xlsx para um único CSV consolidado:

  docs/SCOUT_DESIGN_CSV.csv

Formato do CSV:

  sheet_index,sheet_name,row_number,column_number,column_letter,value

Regra central:
- SCOUT_DESIGN_TEMPLATE.xlsx é a fonte editável.
- SCOUT_DESIGN_CSV.csv é artefato gerado.
- Nunca corrigir o CSV manualmente.
- Toda correção deve ser feita no XLSX.
- Depois, rodar este script para regenerar o CSV.

Modo: MUTANTE — sobrescreve docs/SCOUT_DESIGN_CSV.csv
Gate/trigger: após modificar abas no XLSX do template
Artefatos produzidos: docs/SCOUT_DESIGN_CSV.csv

Ajuste importante:
- O Excel/XLSX limita nomes físicos de abas a 31 caracteres.
- Por isso, o exportador separa:
  1. physical_sheet_name: nome real da aba no XLSX;
  2. sheet_name: nome canônico do contrato, vindo de SHEET_MAP.sheet_name.
- O CSV usa o nome canônico em sheet_name.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

try:
    from openpyxl import load_workbook
    from openpyxl.utils import get_column_letter
    from openpyxl.utils.cell import range_boundaries
except ImportError as exc:
    raise SystemExit(
        "Dependência ausente: openpyxl.\n"
        "Instale com:\n\n"
        "  pip install openpyxl\n"
    ) from exc


OFFICIAL_COLUMNS = [
    "sheet_index",
    "sheet_name",
    "row_number",
    "column_number",
    "column_letter",
    "value",
]

DEFAULT_SOURCE = "docs/SCOUT_DESIGN_TEMPLATE.xlsx"
DEFAULT_OUT = "docs/SCOUT_DESIGN_CSV.csv"
DEFAULT_MANIFEST = "docs/SCOUT_DESIGN_CSV_MANIFEST.json"
DEFAULT_AUDIT = "docs/SCOUT_DESIGN_CSV_AUDIT.json"

SHEET_MAP_PHYSICAL_NAME = "SHEET_MAP"
SHEET_MAP_CANONICAL_COLUMN = "sheet_name"
XLSX_SHEET_NAME_LIMIT = 31

EXPECTED_IMPORT_SCOPE = {
    "contract_scope": "attack_no_shot_v1",
    "module_contract_status": "contrato_validado",
    "import_rule_v1": "importar_v1",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_value(value: Any) -> str:
    if value is None:
        return ""

    if isinstance(value, datetime):
        return value.isoformat(timespec="seconds")

    if isinstance(value, date):
        return value.isoformat()

    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"

    return str(value)


def load_workbook_safe(path: Path, data_only: bool):
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    return load_workbook(
        filename=path,
        read_only=True,
        data_only=data_only,
    )


def get_sheet_bounds(ws) -> tuple[int, int]:
    """
    Retorna max_row e max_column reais da área usada da aba.

    Em workbooks read_only, ws.max_row/ws.max_column podem vir como None.
    calculate_dimension(force=True) força o cálculo da área usada.
    """
    try:
        dimension = ws.calculate_dimension(force=True)
        min_col, min_row, max_col, max_row = range_boundaries(dimension)
        return max_row, max_col
    except Exception:
        max_row = ws.max_row or 1
        max_col = ws.max_column or 1
        return int(max_row), int(max_col)


def read_sheet_map_canonical_names(wb) -> list[str]:
    """
    Lê SHEET_MAP.sheet_name e retorna a lista de nomes canônicos declarados.

    Importante:
    - Não usa a ordem do SHEET_MAP como ordem física das abas.
    - Usa SHEET_MAP apenas como fonte de nomes canônicos.
    """
    if SHEET_MAP_PHYSICAL_NAME not in wb.sheetnames:
        return []

    ws = wb[SHEET_MAP_PHYSICAL_NAME]

    header: dict[str, int] = {}
    for cell in next(ws.iter_rows(min_row=1, max_row=1), []):
        value = normalize_value(cell.value)
        if value:
            header[value] = cell.column

    sheet_name_col = header.get(SHEET_MAP_CANONICAL_COLUMN)
    if sheet_name_col is None:
        return []

    canonical_names: list[str] = []
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        cell = row[sheet_name_col - 1] if sheet_name_col - 1 < len(row) else None
        value = normalize_value(cell.value if cell is not None else None).strip()
        if value:
            canonical_names.append(value)

    return canonical_names


def resolve_canonical_sheet_names(wb) -> tuple[dict[str, str], list[dict[str, Any]]]:
    """
    Resolve nome físico -> nome canônico.

    Estratégia:
    1. Se o nome físico existe exatamente em SHEET_MAP.sheet_name, usa o mesmo nome.
    2. Se o nome físico tem até 31 caracteres e é prefixo único de um nome canônico,
       usa o nome canônico completo.
       Exemplo:
       physical: VERSIONAMENTO_ATAQUE_SEM_FINALI
       canonical: VERSIONAMENTO_ATAQUE_SEM_FINALIZACAO
    3. Se não resolver, usa fallback para o nome físico, mas a auditoria pode bloquear.
    """
    physical_names = list(wb.sheetnames)
    canonical_candidates = read_sheet_map_canonical_names(wb)
    canonical_set = set(canonical_candidates)

    used_canonical: set[str] = set()
    physical_to_canonical: dict[str, str] = {}
    resolution_report: list[dict[str, Any]] = []

    for physical_name in physical_names:
        source = ""
        canonical_name = ""

        if physical_name in canonical_set and physical_name not in used_canonical:
            canonical_name = physical_name
            source = "exact_sheet_map"

        else:
            prefix_matches = [
                candidate
                for candidate in canonical_candidates
                if candidate not in used_canonical
                and (
                    candidate.startswith(physical_name)
                    or physical_name.startswith(candidate)
                    or candidate[:XLSX_SHEET_NAME_LIMIT] == physical_name
                )
            ]

            if len(prefix_matches) == 1:
                canonical_name = prefix_matches[0]
                source = "prefix_sheet_map"
            elif len(prefix_matches) > 1:
                canonical_name = physical_name
                source = "ambiguous_prefix_fallback"
            else:
                canonical_name = physical_name
                source = "physical_fallback"

        physical_to_canonical[physical_name] = canonical_name
        used_canonical.add(canonical_name)

        resolution_report.append(
            {
                "physical_sheet_name": physical_name,
                "canonical_sheet_name": canonical_name,
                "source": source,
                "is_truncated_physical_name": len(physical_name) >= XLSX_SHEET_NAME_LIMIT,
            }
        )

    return physical_to_canonical, resolution_report


def build_records(source: Path, representation: str, data_only: bool) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    wb = load_workbook_safe(source, data_only=data_only)
    physical_to_canonical, resolution_report = resolve_canonical_sheet_names(wb)
    resolution_by_physical = {
        item["physical_sheet_name"]: item
        for item in resolution_report
    }

    sheets_meta: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []

    for sheet_index, ws in enumerate(wb.worksheets):
        physical_sheet_name = ws.title
        canonical_sheet_name = physical_to_canonical.get(physical_sheet_name, physical_sheet_name)
        resolution = resolution_by_physical.get(physical_sheet_name, {})
        max_row, max_column = get_sheet_bounds(ws)

        sheets_meta.append(
            {
                "sheet_index": sheet_index,
                "sheet_name": canonical_sheet_name,
                "physical_sheet_name": physical_sheet_name,
                "canonical_name_source": resolution.get("source", "unknown"),
                "is_truncated_physical_name": resolution.get("is_truncated_physical_name", False),
                "max_row": max_row,
                "max_column": max_column,
            }
        )

        if representation == "sparse_cell_map":
            for row in ws.iter_rows(
                min_row=1,
                max_row=max_row,
                min_col=1,
                max_col=max_column,
            ):
                for cell in row:
                    value = normalize_value(cell.value)

                    if value == "":
                        continue

                    records.append(
                        {
                            "sheet_index": sheet_index,
                            "sheet_name": canonical_sheet_name,
                            "row_number": cell.row,
                            "column_number": cell.column,
                            "column_letter": get_column_letter(cell.column),
                            "value": value,
                        }
                    )

        elif representation == "dense_used_range":
            for row in ws.iter_rows(
                min_row=1,
                max_row=max_row,
                min_col=1,
                max_col=max_column,
            ):
                for cell in row:
                    value = normalize_value(cell.value)

                    records.append(
                        {
                            "sheet_index": sheet_index,
                            "sheet_name": canonical_sheet_name,
                            "row_number": cell.row,
                            "column_number": cell.column,
                            "column_letter": get_column_letter(cell.column),
                            "value": value,
                        }
                    )

        else:
            raise ValueError(f"representation inválida: {representation}")

    wb.close()

    records.sort(
        key=lambda r: (
            int(r["sheet_index"]),
            int(r["row_number"]),
            int(r["column_number"]),
        )
    )

    return records, sheets_meta


def write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OFFICIAL_COLUMNS)
        writer.writeheader()
        writer.writerows(records)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def reconstruct_sheet(records: list[dict[str, Any]], sheet_index: int) -> dict[int, dict[int, str]]:
    table: dict[int, dict[int, str]] = defaultdict(dict)

    for record in records:
        if int(record["sheet_index"]) != sheet_index:
            continue

        row_number = int(record["row_number"])
        column_number = int(record["column_number"])
        table[row_number][column_number] = str(record["value"])

    return dict(table)


def get_header_map(sheet_table: dict[int, dict[int, str]], header_row: int = 1) -> dict[str, int]:
    header = sheet_table.get(header_row, {})
    return {value: col for col, value in header.items() if value}


def find_sheet_index(sheets_meta: list[dict[str, Any]], sheet_name: str) -> int | None:
    for sheet in sheets_meta:
        if sheet["sheet_name"] == sheet_name:
            return int(sheet["sheet_index"])
    return None


def audit_records(
    records: list[dict[str, Any]],
    sheets_meta: list[dict[str, Any]],
    fail_on_text: list[str],
) -> dict[str, Any]:
    blocking_issues: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    expected_sheet_indices = {int(sheet["sheet_index"]) for sheet in sheets_meta}
    found_sheet_indices = {int(record["sheet_index"]) for record in records}

    if expected_sheet_indices != found_sheet_indices:
        blocking_issues.append(
            {
                "code": "sheet_index_mismatch",
                "expected": sorted(expected_sheet_indices),
                "found": sorted(found_sheet_indices),
                "missing": sorted(expected_sheet_indices - found_sheet_indices),
                "extra": sorted(found_sheet_indices - expected_sheet_indices),
            }
        )

    # Canonical name resolution audit
    canonical_names = [str(sheet["sheet_name"]) for sheet in sheets_meta]
    duplicate_canonical_names = sorted(
        name for name, count in Counter(canonical_names).items() if count > 1
    )

    if duplicate_canonical_names:
        blocking_issues.append(
            {
                "code": "duplicate_canonical_sheet_names",
                "duplicate_canonical_sheet_names": duplicate_canonical_names,
            }
        )

    unresolved_truncated = [
        {
            "sheet_index": sheet["sheet_index"],
            "physical_sheet_name": sheet["physical_sheet_name"],
            "canonical_sheet_name": sheet["sheet_name"],
            "canonical_name_source": sheet["canonical_name_source"],
        }
        for sheet in sheets_meta
        if sheet.get("is_truncated_physical_name")
        and sheet.get("canonical_name_source") in {
            "physical_fallback",
            "ambiguous_prefix_fallback",
            "unknown",
        }
    ]

    if unresolved_truncated:
        blocking_issues.append(
            {
                "code": "unresolved_truncated_sheet_names",
                "message": (
                    "Há abas físicas possivelmente truncadas que não foram resolvidas "
                    "com segurança via SHEET_MAP.sheet_name."
                ),
                "examples": unresolved_truncated,
            }
        )

    physical_fallbacks = [
        {
            "sheet_index": sheet["sheet_index"],
            "physical_sheet_name": sheet["physical_sheet_name"],
            "canonical_sheet_name": sheet["sheet_name"],
            "canonical_name_source": sheet["canonical_name_source"],
        }
        for sheet in sheets_meta
        if sheet.get("canonical_name_source") == "physical_fallback"
    ]

    if physical_fallbacks:
        warnings.append(
            {
                "code": "physical_name_fallback_used",
                "message": (
                    "Algumas abas usaram o nome físico como nome canônico. "
                    "Isso é aceitável para nomes curtos/exatos, mas deve ser monitorado."
                ),
                "examples": physical_fallbacks[:20],
            }
        )

    sheet_name_by_index = {
        int(sheet["sheet_index"]): str(sheet["sheet_name"])
        for sheet in sheets_meta
    }

    seen_coordinates: set[tuple[int, int, int]] = set()
    duplicate_coordinates: list[tuple[int, int, int]] = []
    column_letter_errors: list[dict[str, Any]] = []
    sheet_name_errors: list[dict[str, Any]] = []
    out_of_order_count = 0

    previous_key: tuple[int, int, int] | None = None

    for record in records:
        sheet_index = int(record["sheet_index"])
        row_number = int(record["row_number"])
        column_number = int(record["column_number"])
        key = (sheet_index, row_number, column_number)

        if previous_key is not None and key < previous_key:
            out_of_order_count += 1
        previous_key = key

        if key in seen_coordinates:
            duplicate_coordinates.append(key)
        seen_coordinates.add(key)

        expected_letter = get_column_letter(column_number)
        if record["column_letter"] != expected_letter:
            column_letter_errors.append(
                {
                    "coordinate": key,
                    "found": record["column_letter"],
                    "expected": expected_letter,
                }
            )

        expected_sheet_name = sheet_name_by_index.get(sheet_index)
        if expected_sheet_name and record["sheet_name"] != expected_sheet_name:
            sheet_name_errors.append(
                {
                    "coordinate": key,
                    "found": record["sheet_name"],
                    "expected": expected_sheet_name,
                }
            )

    if duplicate_coordinates:
        blocking_issues.append(
            {
                "code": "duplicate_coordinates",
                "count": len(duplicate_coordinates),
                "examples": duplicate_coordinates[:20],
            }
        )

    if out_of_order_count:
        blocking_issues.append(
            {
                "code": "csv_out_of_order",
                "message": "CSV deve estar ordenado por sheet_index, row_number, column_number.",
                "count": out_of_order_count,
            }
        )

    if column_letter_errors:
        blocking_issues.append(
            {
                "code": "column_letter_mismatch",
                "count": len(column_letter_errors),
                "examples": column_letter_errors[:20],
            }
        )

    if sheet_name_errors:
        blocking_issues.append(
            {
                "code": "sheet_name_mismatch",
                "count": len(sheet_name_errors),
                "examples": sheet_name_errors[:20],
            }
        )

    # Auditoria do SHEET_MAP
    sheet_map_index = find_sheet_index(sheets_meta, "SHEET_MAP")

    if sheet_map_index is None:
        blocking_issues.append(
            {
                "code": "missing_sheet_map",
                "message": "A planilha precisa ter aba SHEET_MAP.",
            }
        )
    else:
        sheet_map = reconstruct_sheet(records, sheet_map_index)
        header = get_header_map(sheet_map)

        if "sheet_name" not in header:
            blocking_issues.append(
                {
                    "code": "sheet_map_missing_sheet_name_column",
                    "message": "SHEET_MAP precisa ter coluna sheet_name.",
                }
            )
        else:
            sheet_name_col = header["sheet_name"]

            mapped_sheet_names = {
                columns.get(sheet_name_col, "")
                for row_number, columns in sheet_map.items()
                if row_number != 1 and columns.get(sheet_name_col, "")
            }

            real_canonical_sheet_names = {str(sheet["sheet_name"]) for sheet in sheets_meta}

            missing_in_sheet_map = sorted(real_canonical_sheet_names - mapped_sheet_names)
            extra_in_sheet_map = sorted(mapped_sheet_names - real_canonical_sheet_names)

            if missing_in_sheet_map:
                blocking_issues.append(
                    {
                        "code": "sheet_map_incomplete",
                        "message": "Existem abas canônicas ausentes no SHEET_MAP.",
                        "missing_in_sheet_map": missing_in_sheet_map,
                    }
                )

            if extra_in_sheet_map:
                blocking_issues.append(
                    {
                        "code": "sheet_map_has_unknown_sheets",
                        "message": "SHEET_MAP contém nomes que não existem como aba canônica real.",
                        "extra_in_sheet_map": extra_in_sheet_map,
                    }
                )

    # Auditoria do escopo de importação em EVENTOS
    eventos_index = find_sheet_index(sheets_meta, "EVENTOS")

    if eventos_index is None:
        blocking_issues.append(
            {
                "code": "missing_eventos_sheet",
                "message": "A planilha precisa ter aba EVENTOS.",
            }
        )
    else:
        eventos = reconstruct_sheet(records, eventos_index)
        header = get_header_map(eventos)

        required_columns = [
            "code",
            "contract_scope",
            "module_contract_status",
            "import_rule_v1",
        ]

        missing_columns = [col for col in required_columns if col not in header]

        if missing_columns:
            blocking_issues.append(
                {
                    "code": "eventos_required_columns_missing",
                    "missing_columns": missing_columns,
                }
            )
        else:
            for row_number, columns in eventos.items():
                if row_number == 1:
                    continue

                import_rule = columns.get(header["import_rule_v1"], "")

                if import_rule != EXPECTED_IMPORT_SCOPE["import_rule_v1"]:
                    continue

                found_scope = {
                    "contract_scope": columns.get(header["contract_scope"], ""),
                    "module_contract_status": columns.get(header["module_contract_status"], ""),
                    "import_rule_v1": import_rule,
                }

                if found_scope != EXPECTED_IMPORT_SCOPE:
                    blocking_issues.append(
                        {
                            "code": "invalid_importable_event_scope",
                            "row_number": row_number,
                            "event_code": columns.get(header["code"], ""),
                            "found": found_scope,
                            "expected": EXPECTED_IMPORT_SCOPE,
                        }
                    )

    # Auditoria do any_event como wildcard
    blocking_rules_index = find_sheet_index(sheets_meta, "EVENT_BLOCKING_RULES")

    if blocking_rules_index is not None:
        rules = reconstruct_sheet(records, blocking_rules_index)
        header = get_header_map(rules)

        if "event_code" in header:
            notes_col = header.get("notes")

            for row_number, columns in rules.items():
                if row_number == 1:
                    continue

                event_code = columns.get(header["event_code"], "")

                if event_code == "any_event":
                    notes = columns.get(notes_col, "") if notes_col else ""

                    if "wildcard" not in notes.lower():
                        blocking_issues.append(
                            {
                                "code": "any_event_without_wildcard_note",
                                "row_number": row_number,
                                "message": "any_event precisa estar documentado como wildcard global, não como evento real.",
                            }
                        )

    # Texto proibido/regressão
    forbidden_hits: list[dict[str, Any]] = []

    for term in fail_on_text:
        if not term:
            continue

        for record in records:
            if term in str(record["value"]):
                forbidden_hits.append(
                    {
                        "term": term,
                        "sheet_index": record["sheet_index"],
                        "sheet_name": record["sheet_name"],
                        "row_number": record["row_number"],
                        "column_letter": record["column_letter"],
                        "value": record["value"],
                    }
                )

    if forbidden_hits:
        blocking_issues.append(
            {
                "code": "forbidden_text_found",
                "count": len(forbidden_hits),
                "examples": forbidden_hits[:30],
            }
        )

    records_by_sheet = Counter(str(record["sheet_name"]) for record in records)

    return {
        "status": "failed" if blocking_issues else "passed",
        "blocking_issues": blocking_issues,
        "warnings": warnings,
        "summary": {
            "sheet_count": len(sheets_meta),
            "record_count": len(records),
            "records_by_sheet": dict(sorted(records_by_sheet.items())),
            "duplicate_coordinate_count": len(duplicate_coordinates),
            "out_of_order_count": out_of_order_count,
            "column_letter_error_count": len(column_letter_errors),
            "sheet_name_error_count": len(sheet_name_errors),
            "canonical_name_sources": dict(
                sorted(Counter(str(sheet["canonical_name_source"]) for sheet in sheets_meta).items())
            ),
            "truncated_physical_sheet_count": sum(
                1 for sheet in sheets_meta if sheet.get("is_truncated_physical_name")
            ),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Gera SCOUT_DESIGN_CSV.csv determinístico a partir de "
            "docs/SCOUT_DESIGN_TEMPLATE.xlsx, usando SHEET_MAP.sheet_name "
            "como nome canônico quando o nome físico da aba estiver truncado."
        )
    )

    parser.add_argument(
        "--source",
        default=DEFAULT_SOURCE,
        help="Caminho da planilha-fonte XLSX.",
    )

    parser.add_argument(
        "--out",
        default=DEFAULT_OUT,
        help="Caminho do CSV gerado.",
    )

    parser.add_argument(
        "--manifest",
        default=DEFAULT_MANIFEST,
        help="Caminho do manifest JSON.",
    )

    parser.add_argument(
        "--audit",
        default=DEFAULT_AUDIT,
        help="Caminho do relatório de auditoria JSON.",
    )

    parser.add_argument(
        "--representation",
        choices=["sparse_cell_map", "dense_used_range"],
        default="sparse_cell_map",
        help=(
            "sparse_cell_map: exporta apenas células preenchidas. "
            "dense_used_range: exporta também células vazias dentro da área usada."
        ),
    )

    parser.add_argument(
        "--data-only",
        action="store_true",
        help=(
            "Se usado, exporta resultados calculados de fórmulas. "
            "Sem isso, exporta a fórmula textual quando houver fórmula."
        ),
    )

    parser.add_argument(
        "--fail-on-text",
        action="append",
        default=["contrato_ativo_v1"],
        help="Texto que, se aparecer no CSV, faz a auditoria falhar. Pode repetir.",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    source_path = Path(args.source)
    out_path = Path(args.out)
    manifest_path = Path(args.manifest)
    audit_path = Path(args.audit)

    records, sheets_meta = build_records(
        source=source_path,
        representation=args.representation,
        data_only=args.data_only,
    )

    write_csv(out_path, records)

    csv_hash = sha256_file(out_path)
    source_hash = sha256_file(source_path)

    audit = audit_records(
        records=records,
        sheets_meta=sheets_meta,
        fail_on_text=args.fail_on_text,
    )

    manifest = {
        "generated_at": now_iso(),
        "generator": {
            "name": "export_scout_design_csv.py",
            "version": "1.1.0",
            "manual_edit_allowed": False,
        },
        "source": {
            "path": str(source_path),
            "sha256": source_hash,
            "type": "xlsx",
        },
        "output": {
            "csv_path": str(out_path),
            "csv_sha256": csv_hash,
            "manifest_path": str(manifest_path),
            "audit_path": str(audit_path),
        },
        "canonical_sheet_name_policy": {
            "source": "SHEET_MAP.sheet_name",
            "physical_sheet_name_limit": XLSX_SHEET_NAME_LIMIT,
            "rule": (
                "CSV.sheet_name usa o nome canônico resolvido por SHEET_MAP.sheet_name. "
                "Quando o nome físico da aba está truncado pelo XLSX, o exportador usa "
                "o match único por prefixo contra SHEET_MAP.sheet_name."
            ),
        },
        "representation": {
            "type": args.representation,
            "official_columns": OFFICIAL_COLUMNS,
            "sort_order": [
                "sheet_index",
                "row_number",
                "column_number",
            ],
            "empty_cell_rule": (
                "missing coordinate means empty cell"
                if args.representation == "sparse_cell_map"
                else "empty cells inside used range are explicit rows with empty value"
            ),
            "data_only": args.data_only,
        },
        "expected_import_scope": EXPECTED_IMPORT_SCOPE,
        "sheets": sheets_meta,
        "audit_status": audit["status"],
    }

    write_json(manifest_path, manifest)
    write_json(audit_path, audit)

    print(f"Fonte XLSX: {source_path}")
    print(f"CSV gerado: {out_path}")
    print(f"Manifest: {manifest_path}")
    print(f"Auditoria: {audit_path}")
    print(f"Status: {audit['status']}")
    print(f"CSV SHA256: {csv_hash}")

    if audit["status"] != "passed":
        print("\nAuditoria falhou. Corrija o XLSX-fonte e rode novamente.")
        print("Problemas bloqueantes:")
        for issue in audit["blocking_issues"]:
            print(f"- {issue['code']}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
