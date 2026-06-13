---
doc_id: RAG_009
title: "Workflow de Fontes RAG"
status: active
version: "2.0.0"
authority_level: 3
category: RAG
owner: Davi Sermenho
created_at: "2026-06-01"
last_updated: "2026-06-13"
repository: Davisermenho/scoutpraia
tipo: fluxo_rag
fase_atual: 2
RAG_liberado: true
desbloqueio_em: "2026-06-12"
desbloqueio_gate: "G5 aprovado — MVP funcional completo com evidências documentadas"
vector_store: "Chroma local"
source_policy: "responder somente com base em fontes recuperadas; recusar quando não houver base suficiente"
confidence_hierarchy: "A > B > C > D > Rejeitada"
plan_ref: "docs/016_RAG_Plano_Organizacao_Fontes.md"
---

# Fluxo de Fontes, IA e RAG

## Resumo Executivo

Define o fluxo de fontes e RAG do ScoutPraia. **Fase 1 concluída.** G5 aprovado em 2026-06-12 — Fase 2 (RAG local com Chroma) está desbloqueada. Plano detalhado de fontes, coleções e avaliação em [`016_RAG_Plano_Organizacao_Fontes.md`](016_RAG_Plano_Organizacao_Fontes.md).

## Objetivo

Estabelecer quando e como o RAG pode ser ativado no ScoutPraia, garantindo que a camada de IA só seja habilitada após a base operacional estar validada humanamente.

## RESTRIÇÃO CRÍTICA

```
MUST NOT: usar RAG para decidir evento automaticamente durante marcação
MUST NOT: inventar regra de taxonomia sem fonte registrada em docs/sources/README.md
MUST NOT: gerar relatório sem indicar versão da taxonomia usada
MUST NOT: alterar evento approved sem nova versão de taxonomia
MUST NOT: usar fonte metodológica de IA para responder regra, arbitragem, técnica ou tática de Beach Handball
MUST NOT: misturar handebol de quadra com handebol de areia sem fonte explícita
MUST NOT: usar fonte de visão computacional para diagnosticar atleta
MUST NOT: usar artigo científico como regra oficial
```

**RAG está liberado:** SIM — `RAG_liberado: true` (G5 aprovado em 2026-06-12)

---

O RAG não é necessário para a marcação inicial do MVP. No ScoutPraia, ele deve funcionar como camada de auditoria e consulta de fontes.

## Fase 1 — Manual, sem RAG

Usar enquanto há poucas fontes.

1. registrar fontes em `docs/sources/README.md`
2. transformar fonte em decisão na `docs/008_AUDIT_Matriz_Evidencias.md`
3. criar ou ajustar definição em `docs/006_TAX_Dicionario_Taxonomia.md`
4. validar definição em vídeo com `docs/007_PROT_Protocolo_Validacao.md`
5. aprovar apenas campos úteis, observáveis e consistentes

## Fase 2 — RAG local (ATIVA desde 2026-06-12)

**DESBLOQUEADA.** G5 aprovado — todos os critérios atingidos.

### Vector store

**Chroma local.** Coleções separadas por domínio — fonte metodológica de IA, visão computacional e dataset de futebol não entram nas coleções `bh_*`.

### Coleções vetoriais

**Esportivas:**
- `bh_regras` — IHF, CBHb, derivados oficiais
- `bh_tecnico` — EHF técnico/educacional
- `bh_glossario` — glossário interno CEPRAEA
- `bh_playbook_cepraea` — playbook interno
- `bh_scout` — fontes internas de scout
- `bh_ciencia_analise_notacional` — artigos notacionais
- `bh_ciencia_arremessos` — performance de arremessos
- `bh_ciencia_tomada_decisao` — fatores contextuais
- `bh_ciencia_estatisticas_jogo` — estatísticas de jogo
- `bh_ciencia_carga_biomecanica` — carga e biomecânica

**Metodológicas (engenharia do agente):**
- `ai_metodologia_rag`
- `ai_metodologia_reflexao`
- `ai_metodologia_multiagente`
- `ai_metodologia_structured_output`
- `ai_metodologia_avaliacao_agentes`
- `ai_frameworks_notebooks`

**Vídeo e visão computacional:**
- `ai_video_pose_estimation`
- `ai_video_tracking`
- `ai_video_action_spotting`
- `ai_video_representation_learning`
- `ai_sports_multimodal_reasoning`

### Hierarquia de confiabilidade

| Nível | Tipo | Uso |
|-------|------|-----|
| A | IHF oficial; CBHb oficial | fundamentar resposta normativa |
| B | EHF oficial; artigo científico com autoria/periódico | técnica, treino, scout, ciência, engenharia do agente |
| C | CEPRAEA; preprint; poster; dataset; repositório; notebook | método interno, hipótese, protótipo |
| D | Vídeo, tutorial, blog, rede social | não entra no RAG principal sem transcrição e revisão |
| Rejeitada | sem autoria/data/título validado; duplicata; inacessível | não entra no RAG |

### Hierarquia de conflito

1. IHF vigente
2. CBHb vigente para competições brasileiras
3. EHF técnico/educacional
4. Ciência do Beach Handball
5. Documentos internos CEPRAEA (nomenclatura, playbook e scout interno)
6. Fontes metodológicas de IA (engenharia do agente)
7. Fontes de visão computacional (agente de vídeo futuro)

### System instruction do agente textual

```text
Você é um agente textual de apoio ao treinador de handebol de areia.
Responda apenas com base nas fontes recuperadas no contexto.
Toda resposta técnica deve citar source_id, título e organização da fonte.
Quando as fontes não sustentarem a resposta, diga: "Não encontrado nas fontes disponíveis."
Não use conhecimento geral para completar lacunas.
Não misture handebol de quadra com handebol de areia sem fonte explícita.
Não use fonte metodológica de IA para responder regra, arbitragem, técnica ou tática de Beach Handball.
Não use fonte de visão computacional para diagnosticar atleta.
Não use artigo científico como regra oficial.
```

### Chunking

- 500–900 tokens por chunk; sobreposição de 80–120 tokens
- Regra oficial não pode ser quebrada no meio
- Título e explicação ficam no mesmo chunk
- Fontes de domínios diferentes não ficam no mesmo chunk

Tipos: `chunk_normativo` | `chunk_tecnico` | `chunk_cepraea` | `chunk_cientifico_bh` | `chunk_metodologico_ai` | `chunk_video_cv`

### Critérios de recuperação

- 90% das perguntas respondíveis retornam fonte correta no top 3
- 100% das perguntas normativas retornam IHF ou CBHb antes de qualquer outra
- Perguntas sem base retornam baixa confiança ou vazio
- Fonte metodológica não responde regra esportiva
- Fonte rejeitada não é recuperada

### Release gate da Fase 2

```
[ ] fontes_oficiais.md preenchido como registro canônico
[ ] arquivos locais salvos e com checksum SHA-256
[ ] chunks com metadados completos
[ ] teste de recuperação no Chroma aprovado (sem LLM)
[ ] 3 abas de perguntas-teste preenchidas (30 + 10 + 12 = 52 perguntas)
[ ] relatório avaliacoes/eval_mvp_textual_001.md aprovado
[ ] zero alucinação nos critérios definidos
```

Plano detalhado de fontes, source_ids e ordem de execução: [`016_RAG_Plano_Organizacao_Fontes.md`](016_RAG_Plano_Organizacao_Fontes.md)

## Usos corretos da IA/RAG

- verificar se um campo tem fonte suficiente
- identificar conflito entre regra oficial e definição prática
- revisar se um KPI depende de evento ainda em `draft`
- gerar relatório usando apenas dados marcados e definições aprovadas
- sugerir ajustes de taxonomia após divergências de validação

## Usos que devem ser evitados no MVP

- decidir evento automaticamente durante marcação rápida
- inventar regra sem fonte
- transformar hipótese prática em KPI final
- gerar relatório sem apontar versão da taxonomia
- alterar definição aprovada sem nova versão

## Contrato mínimo para prompts

Todo prompt de auditoria deve exigir e retornar:

| Campo obrigatório | Exemplo de saída esperada |
| --- | --- |
| fontes usadas | `SRC-IHF-RULES Rule 9`, `SRC-NOTATIONAL-BH Iannaccone 2022 p.3` |
| itens sem evidência | `spin_shot: fonte presente, sem validação em vídeo` |
| conflitos encontrados | `defensive_breakdown: definição interpretativa conflita com critério de objetividade de SRC-OBS-MEASUREMENT` |
| inferências feitas | `zone atribuída por posição visual — sem confirmação oficial` |
| recomendação | `manter` \| `ajustar definição` \| `fundir com X` \| `dividir em Y/Z` \| `remover` \| `manter como hipótese` |

Prompt de auditoria não deve retornar apenas recomendação sem citar as fontes e conflitos que a sustentam.
