from __future__ import annotations

import csv
from pathlib import Path


def test_stage1_stage2_registry_and_pdf_conversion_coverage() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    registry_path = repo_root / "beach_handball_ai/fontes/00_registro/fontes_oficiais.csv"
    rows = list(csv.DictReader(registry_path.open(encoding="utf-8")))

    assert rows
    assert len({row["source_id"] for row in rows}) == len(rows)

    registered_paths = {row["arquivo_local"] for row in rows}
    required_files = []
    for root in [repo_root / "docs/sources", repo_root / "beach_handball_ai/fontes"]:
        for path in root.rglob("*"):
            if path.is_file():
                required_files.append(str(path.relative_to(repo_root)))

    assert sorted(required_files) == sorted(registered_paths)

    for row in rows:
        assert row["organização"], row["source_id"]
        assert row["tema"], row["source_id"]
        assert row["nível_de_confiabilidade"], row["source_id"]
        assert row["arquivo_local"], row["source_id"]
        assert row["data"] or row["versão"], row["source_id"]
        assert (repo_root / row["arquivo_local"]).exists(), row["arquivo_local"]

        confidence = row["nível_de_confiabilidade"].lower()
        if confidence.startswith("d") or "rejeitada" in confidence:
            assert "permitido_quando_fase2_liberada" not in row["uso_rag_fase2"]

        if row["arquivo_local"].lower().endswith(".pdf"):
            processed = (
                repo_root
                / "beach_handball_ai/fontes/05_processado/documentos_markdown"
                / f"MD_PROCESSADO__{row['source_id']}.md"
            )
            assert processed.exists(), row["source_id"]
            text = processed.read_text(encoding="utf-8")
            assert f"source_id: {row['source_id']}" in text

    critical_anchors = {
        "IHF_RULES_BH_2026_EN": [
            "Rule 7 – Playing the Ball, Passive Play",
            "Clarifications to the Rules of the Game",
            "Substitution Area Regulations",
            "Athlete Uniform Regulations",
        ],
        "IHF_RULES_BH_2026_WORKING_COPY": [
            "Rule 7 – Playing the Ball, Passive Play",
            "Clarifications to the Rules of the Game",
            "Substitution Area Regulations",
            "Athlete Uniform Regulations",
        ],
        "IHF_RULES_BH_2026_PT_TRANSLATION": [
            "Regra 7 - Jogando a Bola e Jogo Passivo",
            "Regulamento da Área de Substituição",
            "Regulamento do Uniforme dos Atletas",
        ],
        "FHERJ_MUDANCAS_REGRAS_BH_2026": [
            "Após a advertência, a equipe terá o limite máximo de quatro passes",
            "Últimos 15 (quinze) segundos",
            "cabeça do goleiro",
        ],
        "FHERJ_ESCLARECIMENTOS_REGRAS_2025": [
            "JOGO PASSIVO:",
            "SHOOT OUT:",
            "PUNIÇÕES:",
        ],
        "CBHB_REGULAMENTO_BH_2026": [
            "CAPÍTULO VIII",
            "Art. 20.",
        ],
        "REFEREEING_BEACH_HANDBALL": [
            "PHYSICAL DEMANDS OF BEACH HANDBALL REFEREES",
            "Figure 1:",
        ],
        "IHF_RULES_BH_2026_DE": [
            "Regel 7 – Spielen des Balles, passives Spiel",
            "Erläuterungen zu den Spielregeln",
            "Auswechselraum-Reglement",
            "Bestimmungen für Spielkleidung",
        ],
        "IHF_RULES_BH_2026_FR": [
            "Règle 7 – Le maniement du ballon, le jeu passif",
            "Interprétations des Règles de jeu",
            "Règlement des zones de changement",
            "Règlement de la tenue de jeu des athlètes",
        ],
        "SHOOTOUT_PSYCHOLOGICAL_PRESSURE": [
            "WHY ARE SHOOTOUTS SO PSYCHOLOGICALLY DEMANDING?",
            "WHAT PSYCHOLOGICAL FACTORS ARE AT PLAY?",
        ],
        "SRC_NOTATIONAL_BH_IANNACCONE_2022": [
            "Abstract",
            "Table 1. Classification of the types of shots used in beach handball",
            "Table 6. Absolute (n) and relative",
            "Conclusions",
        ],
        "SRC_RAG_STRUCTURED_FILE": [
            "Abstract",
            "3   Methodology",
            "Table 5:",
            "6   Conclusion",
        ],
        "SRC_WOMENS_BH_STATISTICS_2022": [
            "Abstract:",
            "Table 1. Definitions of game-related statistics",
            "Table 4. Discriminant analysis by match outcome",
            "Discussion and conclusions",
        ],
        "ULTIMATE_SCHOOL_HANDBALL_2025": [
            "1. INTRODUCTION",
            "BEACH HANDBALL AND INDOOR HANDBALL AT SCHOOL",
        ],
        "MINI_BEACH_HANDBALL_INFO_SHEET": [
            "Recommendations for Mini Beach Handball",
            "Scoring System in Mini Beach Handball",
        ],
    }
    for source_id, anchors in critical_anchors.items():
        processed = (
            repo_root
            / "beach_handball_ai/fontes/05_processado/documentos_markdown"
            / f"MD_PROCESSADO__{source_id}.md"
        )
        text = processed.read_text(encoding="utf-8")
        for anchor in anchors:
            assert anchor in text, (source_id, anchor)
