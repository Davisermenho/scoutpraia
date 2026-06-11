from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


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

ALLOWED_STATUS = {
    "ativo",
    "ativo_com_ressalva",
    "bloqueado",
    "bloqueado_visual",
    "deprecated",
}

ALLOWED_METHODS = {
    "curadoria_legada_convertida",
    "janela_unica_sem_split",
    "janela_paragrafos_com_overlap",
    "placeholder_deprecated",
}

REQUIRED_KEYS = {
    "chunk_id",
    "registro_id_origem",
    "source_id",
    "tema",
    "subtema",
    "organizacao",
    "versao",
    "confiabilidade",
    "arquivo_origem",
    "status",
    "metodo_chunking",
    "uso_no_agente",
    "token_count_aprox",
    "overlap_tokens_aprox",
    "texto",
}


def token_count(text: str) -> int:
    return len(re.findall(r"\S+", text))


def test_stage4_chunk_inventory_is_structured_and_separated() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    chunks_path = (
        repo_root / "beach_handball_ai/fontes/05_processado/chunks_jsonl/CHUNKS_ETAPA_4_CORPUS.jsonl"
    )

    records = [
        json.loads(line)
        for line in chunks_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    assert records
    assert len({record["chunk_id"] for record in records}) == len(records)

    statuses = Counter()
    generated_active = []

    for record in records:
        assert REQUIRED_KEYS.issubset(record)
        assert record["tema"] in ALLOWED_TEMAS
        assert record["status"] in ALLOWED_STATUS
        assert record["metodo_chunking"] in ALLOWED_METHODS

        source_path = repo_root / record["arquivo_origem"]
        assert source_path.exists(), record["arquivo_origem"]

        statuses[record["status"]] += 1

        counted_tokens = token_count(record["texto"])
        assert abs(counted_tokens - int(record["token_count_aprox"])) <= 3

        if record["status"] == "deprecated":
            assert record["metodo_chunking"] == "placeholder_deprecated"
            assert "_rascunhos/" in record["arquivo_origem"]
            continue

        assert record["source_id"]
        assert record["confiabilidade"]
        assert counted_tokens > 0
        assert record["uso_no_agente"]

        if record["status"] in {"ativo", "ativo_com_ressalva"} and record["chunk_id"].startswith("ETAPA4_"):
            generated_active.append(record)

        if record["tema"] == "cepraea_playbook":
            assert record["source_id"] == "PLAYBOOK_CEPRAEA"
            assert record["organizacao"] == "CEPRAEA"

        if record["tema"] == "regra":
            assert record["organizacao"] != "CEPRAEA"

    assert statuses["ativo"] > 0
    assert statuses["ativo_com_ressalva"] > 0
    assert statuses["deprecated"] > 0
    assert statuses["bloqueado"] > 0

    assert generated_active
    within_recommended = [
        record
        for record in generated_active
        if 500 <= int(record["token_count_aprox"]) <= 900
    ]
    assert len(within_recommended) / len(generated_active) >= 0.75

    for record in generated_active:
        assert int(record["token_count_aprox"]) <= 1100
        if record["metodo_chunking"] == "janela_paragrafos_com_overlap":
            assert 0 <= int(record["overlap_tokens_aprox"]) <= 100
