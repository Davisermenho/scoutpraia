#!/usr/bin/env python3
"""
Fase 1 — Auditoria automatizada do corpus Beach Handball AI.
Varre todos os .md em documentos_markdown/ e produz AUDITORIA_CORPUS_2026-06-11.json.
"""

import json
import re
from pathlib import Path

# ── Configuração ───────────────────────────────────────────────────────────────

MD_DIR = Path(__file__).parent / "documentos_markdown"
OUTPUT = Path(__file__).parent / "AUDITORIA_CORPUS_2026-06-11.json"

# Seções esperadas por source_id (texto que deve aparecer no corpo como substantivo)
EXPECTED_SECTIONS: dict[str, list[str]] = {
    "IHF_RULES_BH_2026_EN": [
        "### Rule 1", "### Rule 2", "### Rule 3", "### Rule 4", "### Rule 5",
        "### Rule 6", "### Rule 7", "### Rule 8", "### Rule 9", "### Rule 10",
        "### Rule 11", "### Rule 12", "### Rule 13", "### Rule 14", "### Rule 15",
        "### Rule 16", "### Rule 17", "### Rule 18",
        "### Referee Hand Signals",
        "### Clarifications to the Rules of the Game",
        "### Substitution Area Regulations",
        "### Athlete Uniform Regulations",
        "### Sand Quality and Lighting Regulations",
    ],
    "IHF_RULES_BH_2026_WORKING_COPY": [
        "### Rule 1", "### Rule 2", "### Rule 3", "### Rule 4", "### Rule 5",
        "### Rule 6", "### Rule 7", "### Rule 8", "### Rule 9", "### Rule 10",
        "### Rule 11", "### Rule 12", "### Rule 13", "### Rule 14", "### Rule 15",
        "### Rule 16", "### Rule 17", "### Rule 18",
        "### Referee Hand Signals",
        "### Clarifications to the Rules of the Game",
        "### Substitution Area Regulations",
        "### Athlete Uniform Regulations",
        "### Sand Quality and Lighting Regulations",
    ],
    "IHF_RULES_BH_2026_DE": [
        "### Handzeichen der Schiedsrichter",
        "Regel 1", "Regel 2", "Regel 16", "Regel 17", "Regel 18",
        "LACUNA DE EXTRAÇÃO",
    ],
    "IHF_RULES_BH_2026_FR": [
        "### Gestes des arbitres",
        "Règle 1", "Règle 2", "Règle 16", "Règle 17", "Règle 18",
        "LACUNA DE EXTRAÇÃO",
    ],
    "IHF_RULES_BH_2026_PT_TRANSLATION": [
        "### Regra 1", "### Regra 2", "### Regra 3", "### Regra 4", "### Regra 5",
        "### Regra 6", "### Regra 7", "### Regra 8", "### Regra 9", "### Regra 10",
        "### Regra 11", "### Regra 12", "### Regra 13", "### Regra 14", "### Regra 15",
        "### Regra 16", "### Regra 17", "### Regra 18",
        "### Os Sinais Manuais dos Árbitros",
        "### Esclarecimentos sobre as Regras do Jogo",
        "### Regulamento da Área de Substituição",
        "### Regulamento da Qualidade da Areia e da Iluminação",
    ],
    "CBHB_REGULAMENTO_BH_2026": [
        "### CAPÍTULO I", "### CAPÍTULO II", "### CAPÍTULO III",
        "### CAPÍTULO IV", "### CAPÍTULO V", "### CAPÍTULO VI",
        "### CAPÍTULO VII", "### CAPÍTULO VIII", "### CAPÍTULO IX",
        "### CAPÍTULO X", "### CAPÍTULO XI",
    ],
    "FHERJ_ESCLARECIMENTOS_REGRAS_2025": [
        "Regra", "esclarecimento",
    ],
    "FHERJ_MUDANCAS_REGRAS_BH_2026": [
        "Regra", "2026",
    ],
    "REFEREEING_BEACH_HANDBALL": [
        "referee", "signal",
    ],
    "SRC_IHF_RULES_FILE": [],  # nivel C / Arquivo historico — extracao corrompida, sem verificacao de secoes
    "SHOOTOUT_PSYCHOLOGICAL_PRESSURE": [
        "shoot-out", "psychological",
    ],
    "MINI_BEACH_HANDBALL_INFO_SHEET": [
        "mini", "beach handball",
    ],
    "SRC_NOTATIONAL_BH_IANNACCONE_2022": [
        "notation", "match",
    ],
    "SRC_RAG_STRUCTURED_FILE": [
        "retrieval", "hallucination",
    ],
    "SRC_WOMENS_BH_STATISTICS_2022": [
        "statistics", "women",
    ],
    "ULTIMATE_SCHOOL_HANDBALL_2025": [
        "school", "handball",
    ],
}

# Source IDs onde blank runs são artefatos do pdftotext (separadores de página), não conteúdo perdido.
# Limiar elevado para suprimir falsos ALTO por separadores de página em documentos grandes.
PDFTOTEXT_LARGE_DOCS = {
    "IHF_RULES_BH_2026_EN",
    "IHF_RULES_BH_2026_WORKING_COPY",
    "IHF_RULES_BH_2026_DE",
    "IHF_RULES_BH_2026_FR",
    "IHF_RULES_BH_2026_PT_TRANSLATION",
    "CBHB_REGULAMENTO_BH_2026",
    "FHERJ_MUDANCAS_REGRAS_BH_2026",
    "FHERJ_ESCLARECIMENTOS_REGRAS_2025",
    "REFEREEING_BEACH_HANDBALL",
    "SHOOTOUT_PSYCHOLOGICAL_PRESSURE",
    "SRC_NOTATIONAL_BH_IANNACCONE_2022",
    "SRC_IHF_RULES_FILE",
    "SRC_WOMENS_BH_STATISTICS_2022",
    "ULTIMATE_SCHOOL_HANDBALL_2025",
}

# Tipos que indicam metadado/navegação — não pertencem ao corpus normativo
TIPOS_NAO_CORPUS = {
    "artefato_processado",
    "metadado_de_navegacao",
    "indice_historico_arquivado",
}

# Combinações nivel_de_confiabilidade+tipo suspeitas
SUSPICIOUS_COMBOS = [
    # (nivel, tipo, motivo)
    ("B operacional / apoio em português", "Regra oficial",
     "Tradução classificada como 'Regra oficial' — deve ser 'Tradução técnica'"),
    ("C", "Regra oficial",
     "Documento nível C classificado como 'Regra oficial'"),
]

# ── Parsing ────────────────────────────────────────────────────────────────────

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extrai YAML frontmatter e retorna (meta, body)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    yaml_block = text[3:end].strip()
    body = text[end + 4:].lstrip("\n")
    meta = {}
    for line in yaml_block.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
    return meta, body


def count_blank_run_gt3(body: str) -> int:
    """Conta quantas vezes há 3+ linhas em branco consecutivas (proxy de imagem perdida)."""
    count = 0
    run = 0
    for line in body.splitlines():
        if line.strip() == "":
            run += 1
        else:
            if run >= 3:
                count += 1
            run = 0
    if run >= 3:
        count += 1
    return count


def count_table_cells(body: str) -> int:
    """Conta linhas de tabela markdown (linhas que começam com |, exceto separadores)."""
    return sum(
        1 for line in body.splitlines()
        if line.strip().startswith("|") and not re.match(r"^\s*\|[-| ]+\|\s*$", line)
    )


def check_sections(source_id: str, body: str) -> dict[str, bool]:
    """Verifica presença de cada seção esperada para o source_id."""
    expected = EXPECTED_SECTIONS.get(source_id, [])
    result = {}
    body_lower = body.lower()
    for section in expected:
        # Correspondência insensível a maiúsculas para seções textuais simples
        if section.startswith("###"):
            result[section] = section in body
        else:
            result[section] = section.lower() in body_lower
    return result


def find_lacunas_documentadas(body: str) -> list[str]:
    """Retorna todas as lacunas de extração documentadas no arquivo."""
    return re.findall(r"\[LACUNA DE EXTRAÇÃO[^\]]*\]", body)


def body_substantive_lines(body: str) -> int:
    """Conta linhas com conteúdo não-vazio e não-separador."""
    separators = re.compile(r"^[_\-=]{5,}$|^\s*[0-9]+\s+IX\.")
    return sum(
        1 for line in body.splitlines()
        if line.strip() and not separators.match(line.strip())
    )


# ── Análise por arquivo ────────────────────────────────────────────────────────

def audit_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)

    source_id = meta.get("source_id", path.stem)
    nivel = meta.get("nivel_de_confiabilidade", "N/A")
    tipo = meta.get("tipo", "N/A")
    status = meta.get("status", "N/A")
    org = meta.get("organizacao", "N/A")

    blank_runs = count_blank_run_gt3(body)
    table_cells = count_table_cells(body)
    substantive_lines = body_substantive_lines(body)
    total_lines = len(text.splitlines())
    sections = check_sections(source_id, body)
    lacunas = find_lacunas_documentadas(body)

    missing_sections = [s for s, present in sections.items() if not present]
    present_sections = [s for s, present in sections.items() if present]

    # Flags de problema
    flags = []

    is_large_pdf = source_id in PDFTOTEXT_LARGE_DOCS
    blank_runs_threshold_alto = 200 if is_large_pdf else 5
    blank_runs_threshold_medio = 50 if is_large_pdf else 2
    if blank_runs >= blank_runs_threshold_alto:
        flags.append(f"ALTO: {blank_runs} blocos com 3+ linhas em branco — possível conteúdo visual perdido")
    elif blank_runs >= blank_runs_threshold_medio:
        flags.append(f"MEDIO: {blank_runs} blocos com 3+ linhas em branco — verificar (artefato pdftotext esperado)")
    elif blank_runs >= 2 and not is_large_pdf:
        flags.append(f"MEDIO: {blank_runs} blocos com 3+ linhas em branco — verificar")

    if table_cells == 0 and tipo in ("Regra oficial", "Publicação técnica oficial", "Esclarecimento regional"):
        flags.append("SEM_TABELAS: nenhuma tabela markdown detectada em documento normativo")

    if missing_sections:
        flags.append(f"SECOES_AUSENTES: {len(missing_sections)} seção(ões) esperada(s) não encontrada(s)")

    if tipo.lower() in TIPOS_NAO_CORPUS:
        flags.append(f"TIPO_NAO_CORPUS: arquivo de metadado/navegação dentro do corpus (tipo='{tipo}')")

    for nivel_check, tipo_check, motivo in SUSPICIOUS_COMBOS:
        if nivel == nivel_check and tipo == tipo_check:
            flags.append(f"COMBO_SUSPEITO: {motivo}")

    if status == "texto_extraido_layout_pendente_revisao_manual_tabelas":
        flags.append("STATUS_PENDENTE: revisão manual de tabelas ainda não realizada")

    # Classificação de papel no corpus
    if "REVISAO_CHUNKING" in path.name or "PARTE_" in path.name:
        flags.append("RASCUNHO: arquivo de trabalho intermediário — candidato a mover para _rascunhos/")

    severidade = "OK"
    if any(f.startswith("ALTO:") for f in flags):
        severidade = "ALTO"
    elif any(f.startswith(("MEDIO:", "SECOES_AUSENTES", "SEM_TABELAS", "STATUS_PENDENTE", "RASCUNHO")) for f in flags):
        severidade = "MEDIO"
    elif flags:
        severidade = "BAIXO"

    return {
        "arquivo": path.name,
        "source_id": source_id,
        "organizacao": org,
        "tipo": tipo,
        "nivel_de_confiabilidade": nivel,
        "status": status,
        "metricas": {
            "total_linhas": total_lines,
            "linhas_substantivas": substantive_lines,
            "blocos_branco_3mais": blank_runs,
            "celulas_tabela_markdown": table_cells,
            "lacunas_documentadas": len(lacunas),
        },
        "secoes": {
            "esperadas": len(sections),
            "presentes": len(present_sections),
            "ausentes": missing_sections,
        },
        "lacunas_doc": lacunas,
        "flags": flags,
        "severidade": severidade,
    }


# ── Órfãos fora do corpus estruturado ─────────────────────────────────────────

def detect_orphan_mds() -> list[dict]:
    """Detecta arquivos .md na raiz de 05_processado/ — fora de documentos_markdown/."""
    orphans = sorted(MD_DIR.parent.glob("*.md"))
    if not orphans:
        return []
    return [{
        "tipo_alerta": "ORFAOS_FORA_DO_CORPUS",
        "descricao": (
            f"{len(orphans)} arquivo(s) .md encontrado(s) fora de documentos_markdown/. "
            "Verificar se é corpus, metadado mal posicionado ou rascunho."
        ),
        "arquivos": [str(p.relative_to(MD_DIR.parent.parent.parent)) for p in orphans],
        "recomendacao": (
            "Mover para documentos_markdown/ se for corpus, para _rascunhos/ se for rascunho, "
            "ou deletar se for metadado obsoleto."
        ),
    }]


# ── Análise de duplicatas ──────────────────────────────────────────────────────

_LANG_SUFFIXES = {"_EN", "_DE", "_FR", "_PT_TRANSLATION", "_PT", "_ES"}


def _strip_lang(source_id: str) -> str:
    """Remove sufixo de idioma para agrupar versões do mesmo documento."""
    for suffix in _LANG_SUFFIXES:
        if source_id.endswith(suffix):
            return source_id[: -len(suffix)]
    return source_id


def detect_duplicates(resultados: list[dict]) -> list[dict]:
    """Identifica grupos de archivos nivel-A com source_id de mesma base (duplicatas reais)."""
    nivel_a_oficiais = [
        r for r in resultados
        if r["nivel_de_confiabilidade"] == "A" and r["tipo"] == "Regra oficial"
    ]

    # Agrupa por (base, idioma) — mesma base E mesmo idioma = duplicata real
    from collections import defaultdict

    def lang_suffix(source_id: str) -> str:
        for s in _LANG_SUFFIXES:
            if source_id.endswith(s):
                return s
        return "_NENHUM"

    grupos: dict[tuple, list[dict]] = defaultdict(list)
    for r in nivel_a_oficiais:
        key = (_strip_lang(r["source_id"]), lang_suffix(r["source_id"]))
        grupos[key].append(r)

    alertas = []
    for (base, lang), grupo in grupos.items():
        if len(grupo) < 2:
            continue
        alertas.append({
            "tipo_alerta": "DUPLICATAS_POTENCIAIS",
            "descricao": (
                f"{len(grupo)} arquivo(s) com base='{base}' e idioma='{lang}', "
                f"tipo='Regra oficial' e nivel='A'. Verificar qual é canônico."
            ),
            "arquivos": [r["arquivo"] for r in grupo],
            "recomendacao": (
                "Rebaixar arquivos redundantes para nivel 'A-auxiliar' e adicionar "
                "campo 'observacao' e 'fonte_canonica' no frontmatter."
            ),
        })
    return alertas


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    md_files = sorted(MD_DIR.glob("*.md"))
    print(f"Auditando {len(md_files)} arquivo(s) em {MD_DIR}...\n")

    resultados = []
    for path in md_files:
        r = audit_file(path)
        resultados.append(r)
        sev_icon = {"OK": "✓", "BAIXO": "·", "MEDIO": "!", "ALTO": "!!!"}.get(r["severidade"], "?")
        print(f"  [{sev_icon}] {r['arquivo']:<65} sev={r['severidade']}")
        for flag in r["flags"]:
            print(f"       → {flag}")

    alertas_globais = detect_duplicates(resultados)
    alertas_globais += detect_orphan_mds()

    # Resumo
    por_sev = {}
    for r in resultados:
        por_sev[r["severidade"]] = por_sev.get(r["severidade"], 0) + 1

    total_flags = sum(len(r["flags"]) for r in resultados)
    sem_tabelas = [r["arquivo"] for r in resultados if r["metricas"]["celulas_tabela_markdown"] == 0
                   and r["tipo"] in ("Regra oficial", "Publicação técnica oficial", "Esclarecimento regional", "Circular regional")]
    status_pendente = [r["arquivo"] for r in resultados
                       if r["status"] == "texto_extraido_layout_pendente_revisao_manual_tabelas"]

    resumo = {
        "data_auditoria": "2026-06-11",
        "total_arquivos": len(resultados),
        "por_severidade": por_sev,
        "total_flags": total_flags,
        "documentos_sem_tabelas_markdown": sem_tabelas,
        "documentos_status_pendente": status_pendente,
        "alertas_globais": alertas_globais,
    }

    output = {
        "resumo": resumo,
        "arquivos": resultados,
    }

    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nRelatório salvo em: {OUTPUT}")
    print(f"\nResumo: {json.dumps(por_sev)} — {total_flags} flag(s) total")
    print(f"Sem tabelas MD (normativos): {len(sem_tabelas)}")
    print(f"Status ainda pendente: {len(status_pendente)}")
    if alertas_globais:
        print(f"Alertas globais: {len(alertas_globais)}")
        for a in alertas_globais:
            print(f"  [{a['tipo_alerta']}] {a['descricao']}")


if __name__ == "__main__":
    main()
