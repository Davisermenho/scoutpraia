# Auditoria Etapa 4

gerado_em: 2026-06-11
arquivo_jsonl: beach_handball_ai/fontes/05_processado/chunks_jsonl/CHUNKS_ETAPA_4_CORPUS.jsonl
chunks_totais: 173

## Status

- ativo: 101
- ativo_com_ressalva: 61
- bloqueado: 4
- bloqueado_visual: 1
- deprecated: 6

## Temas

- analise_de_adversario: 8
- arbitragem: 16
- cepraea_playbook: 1
- nomenclatura: 3
- regra: 90
- scout: 22
- tatica: 2
- tecnica: 23
- treino: 8

## Regras operacionais

- chunks derivados de `_rascunhos/` ficam com `status=deprecated` e nao entram na ingestao principal.
- chunks normativos IHF convertidos do artefato legado continuam separados de CEPRAEA por `tema`, `organizacao` e `source_id`.
- a Etapa 4 continua documental; embeddings/Chroma seguem bloqueados ate o gate global do ScoutPraia.
