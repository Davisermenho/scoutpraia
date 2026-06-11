from __future__ import annotations

import json
from pathlib import Path


REQUIRED_KEYS = {
    "registro_id",
    "source_id",
    "tema",
    "subtema",
    "organizacao",
    "versao",
    "confiabilidade",
    "arquivo",
    "pronto_para_chunking",
    "status_pre_chunking",
}

ALLOWED_TEMAS = {
    "regra",
    "arbitragem",
    "tecnica",
    "tatica",
    "treino",
    "scout",
    "nomenclatura",
    "analise_de_adversario",
    "cepraea_playbook",
}


def test_stage3_thematic_metadata_inventory_is_consistent() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    metadata_path = (
        repo_root
        / "beach_handball_ai/fontes/05_processado/chunks_jsonl/METADADOS_TEMATICOS_ETAPA_3.jsonl"
    )

    records = [
        json.loads(line)
        for line in metadata_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    assert records
    assert len({record["registro_id"] for record in records}) == len(records)

    temas = set()
    ready_records = 0
    pending_records = 0

    for record in records:
        assert REQUIRED_KEYS.issubset(record)
        assert record["tema"] in ALLOWED_TEMAS
        assert isinstance(record["pronto_para_chunking"], bool)

        target_path = repo_root / record["arquivo"]
        assert target_path.exists(), record["arquivo"]

        temas.add(record["tema"])

        if record["pronto_para_chunking"]:
            ready_records += 1
            assert record["status_pre_chunking"] == "ready_for_chunking"
        else:
            pending_records += 1
            assert record["status_pre_chunking"] == "pendente_etapa_2_conversao_texto"

    assert ready_records > 0
    assert ready_records + pending_records == len(records)
    assert ALLOWED_TEMAS.issubset(temas)
