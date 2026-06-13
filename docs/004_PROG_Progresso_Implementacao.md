---
doc_id: PROG_004
title: "Progresso de Implementação"
status: active
version: "1.0.0"
authority_level: 4
category: PROG
owner: Davi Sermenho
created_at: "2026-06-01"
last_updated: "2026-06-13"
repository: Davisermenho/scoutpraia
blocking_policy: "Não declarar trabalho concluído sem cumprir os critérios aqui definidos."
tipo: progresso_execução
status_geral: MVP_COMPLETO
fase_atual: "finalization_v1 ativo — QUICK_EVENT_TYPES derivado do registry (P0_005/P0_006 completos); UI registry sem eventos bloqueados"
testes_passando: 352
event_definitions: 35
próxima_ação: "Validar merge com origin/main; testar gerador/auditor full extraction; gerar JSON da planilha"
gaps_abertos:
  - "Taxonomia v0.1 ainda em draft — não sustenta KPI final estável (previsto; v1 endereça)"
  - "RAG/Chroma/embeddings seguem bloqueados até gate de Fase 2"
  - "008_AUDIT_Matriz_Evidencias.md e 006_TAX_Dicionario_Taxonomia.md a reconciliar com events_v1.py (pós-MVP)"
  - "SCOUT_DESIGN_TEMPLATE_FULL_EXTRACTION.json/jsonl ainda precisa ser gerado localmente a partir das abas da planilha"
  - "Proteção/locked copy da planilha dependem de ação no Drive/Sheets"
mvp_completo: true
---

# ScoutPraia — Progresso de Implementação e Evidência

## Resumo Executivo

Registro do estado atual de implementação do ScoutPraia. MVP completo com G5 aprovado; finalization_v1 ativo e ativação progressiva de módulos v1 em curso.

## Objetivo

Rastrear o progresso real de implementação com evidência reproduzível por fase, servindo como fonte de verdade sobre o que está funcionando, o que está pendente e qual é a próxima ação.

Este arquivo registra o estado atual de implementação. Ele deve ser atualizado a cada ciclo.

**Regra:** uma etapa só pode ser marcada como `FUNCIONANDO` quando houver evidência
reproduzível por comando, teste ou arquivo verificável.

**Histórico de ciclos anteriores:** ver `docs/015_PROG_Log_Implementacao.md` quando existir.

---

## Sumário executivo

**Status geral:** `BASE TÉCNICA FUNCIONANDO — MVP INCOMPLETO`

**Gate atual do repositório:**

```bash
python3 -m pytest tests/test_points_policy_v1.py -q
python3 -m pytest tests/test_docs_contract_alignment_audit.py -q
python3 -m pytest tests/test_scout_design_template_full_extraction_audit.py -q
PYTHONPATH=. python3 scripts/audit_docs_contract_alignment.py
PYTHONPATH=. python3 scripts/audit_scout_design_template.py docs/SCOUT_DESIGN_TEMPLATE.xlsx
# quando existir o JSON full extraction local:
# PYTHONPATH=. python3 scripts/audit_scout_design_template_full_extraction.py --chunks docs/SCOUT_DESIGN_TEMPLATE_FULL_EXTRACTION.json --xlsx docs/SCOUT_DESIGN_TEMPLATE.xlsx --full-extraction
python3 -m pytest tests/test_transition_contract.py -q
python3 -m pytest tests/test_events_v1_contract_registry.py -q
python3 -m pytest -q
scripts/verify_current_state.sh
git diff --check
git status --short
# resultado esperado após pull: 300+ passed
```

**Última evidência informada pelo operador:**

```text
date_utc=2026-06-11T22:48:16Z
git_head=7de34ec
pytest=249 passed
verify_current_state.sh=verde
taxonomy=ScoutPraia v0.1
taxonomy_status=draft
event_definitions=31
expected_event_definitions=31
SCOUT_DESIGN_TEMPLATE audit=status=ok errors=0 warnings=4
```

**Estado após esta atualização no repositório:**

Foram adicionados arquivos versionáveis para fechar a causa raiz da pontuação como contrato executável global:

```text
scoutpraia/contracts/points_policy_v1.py
tests/test_points_policy_v1.py
scoutpraia/contracts/__init__.py
```

Também foi criado um auditor semântico para detectar drift entre documentação e contratos:

```text
scripts/audit_docs_contract_alignment.py
tests/test_docs_contract_alignment_audit.py
```

Também foi criado um auditor da extração completa do `SCOUT_DESIGN_TEMPLATE`:

```text
scripts/audit_scout_design_template_full_extraction.py
tests/test_scout_design_template_full_extraction_audit.py
```

Esse auditor valida arquivos JSON/JSONL de chunks exportados da planilha. Ele verifica:

```text
chunk_id único;
campos obrigatórios do chunk;
conteúdo não vazio;
prioridade válida;
cobertura de abas do XLSX quando --xlsx é informado;
cobertura de todas as abas quando --full-extraction é usado;
presença de regras críticas como specialist não ser event_code/position_code, Shoot-out não virar goalkeeper_save, goalkeeper_save exigir finalização vinculada e transição não calcular pontos.
```

Esses arquivos não alteram seed, UI ou importação. Eles centralizam a derivação de pontos e criam mecanismos para impedir que documentos antigos, planilha binária ou chunks incompletos orientem implementação errada.

Regras críticas cobertas pelo contrato de pontuação:

```text
specialist não é event_code nem position_code; é scorer_role.
specialist_shot é código proibido.
scorer_role=specialist + result=goal em finalização válida deriva 2 pontos.
simple_shot + field_player + goal deriva 1 ponto.
spin_shot, inflight_shot, goalkeeper_shot, six_metre_throw e shootout_attempt convertidos derivam 2 pontos.
resultados não convertidos ou perda sem finalização derivam 0 quando permitidos.
manual_points divergente deve gerar erro.
resultado incompatível com evento deve gerar erro.
```

Regras críticas cobertas pelo auditor docs x contratos:

```text
specialist_shot, specialist_attempt e specialist_goal não podem aparecer como evento ativo/KPI final.
save_shootout, goal_conceded, fast_break_against e recovery legados precisam aparecer apenas como legado/bloqueio/migração.
docs precisam preservar a afirmação de que SCOUT_DESIGN_TEMPLATE é contrato de arquitetura, não banco de lances.
docs não podem declarar MVP/RAG/taxonomia como completos sem contexto de bloqueio/negação.
```

---

## Auditoria do SCOUT_DESIGN_TEMPLATE

Para validar a planilha exportada:

```bash
PYTHONPATH=. python3 scripts/audit_scout_design_template.py docs/SCOUT_DESIGN_TEMPLATE.xlsx
```

O auditor já foi executado localmente pelo operador com:

```text
status=ok
errors=0
warnings=4
```

Warnings remanescentes:

```text
specialist_shot ausente de EVENTOS porque é legado/bloqueado, não evento ativo.
ARCHITECTURE_README/SOURCE_REGISTER/VALIDATION_MATRIX sem proteção no XLSX exportado.
```

---

## Auditoria da extração completa em chunks

Para validar uma extração completa futura das abas:

```bash
PYTHONPATH=. python3 scripts/audit_scout_design_template_full_extraction.py \
  --chunks docs/SCOUT_DESIGN_TEMPLATE_FULL_EXTRACTION.json \
  --xlsx docs/SCOUT_DESIGN_TEMPLATE.xlsx \
  --full-extraction
```

Para validar apenas uma visão sintética de agente:

```bash
PYTHONPATH=. python3 scripts/audit_scout_design_template_full_extraction.py \
  --chunks docs/SCOUT_DESIGN_TEMPLATE_AGENT_VIEW_CHUNKS.json
```

Diferença:

```text
Agent View sintético: pode não ter sheet_name em cada chunk e pode gerar warnings sem falhar.
Full extraction: precisa de sheet_name, chunk_type, row_range e cobertura das abas do XLSX.
```

---

## Próximo controle de causa raiz

Depois de validar os novos auditores, gerar:

```text
docs/SCOUT_DESIGN_TEMPLATE_FULL_EXTRACTION.json ou .jsonl
```

Objetivo: extrair todas as abas relevantes da planilha em chunks auditáveis e reconciliar:

```text
docs/006_TAX_Dicionario_Taxonomia.md
docs/008_AUDIT_Matriz_Evidencias.md
```

com os contratos atuais:

```text
events_v1.py
points_policy_v1.py
SCOUT_DESIGN_TEMPLATE.xlsx
```

---

## Baseline oficial G0

```yaml
baseline:
  id: "G0_BASELINE_EVENTOS_V1_VERDE"
  git_head: "5cf588c"
  date: "2026-06-10"
  tests:
    pytest: "196 passed"
```

Observação: este baseline registra o estado verde anterior ao ajuste do registry G1. Os ciclos abaixo preservam esse baseline e mantêm `offensive_creation_v1` e `defensive_v1` apenas como contratos bloqueados; a estrutura interna do registry deve seguir a prioridade `SCOUT_DESIGN_TEMPLATE` > `005_CONT_Operacional_Eventos_v1.md` > repositório.

---

## Checklist por fase

| Fase | Status | Testes |
|------|--------|--------|
| 1 — Pré-implementação obrigatória | `FUNCIONANDO` | gate documental ok |
| 2 — Estrutura base do projeto | `FUNCIONANDO` | import ok |
| 3 — Configuração, paths e banco | `FUNCIONANDO` | banco inicializa |
| 4 — Modelos de dados iniciais | `FUNCIONANDO COMO BASE` | criação de tabelas ok |
| 5 — Taxonomia v0.1 | `FUNCIONANDO` | 31 definições, seed idempotente |
| 6 — Serviços internos | `FUNCIONANDO COM EVIDÊNCIA` | event, clip, validation, analytics, report |
| 7 — Interface Streamlit | `FUNCIONANDO COM EVIDÊNCIA` | Dashboard, Jogos, Marcação, Relatórios, Adversárias |
| 8 — Testes | `FUNCIONANDO` | 249 passed antes dos novos auditores; validar novamente após pull |
| 9 — Validação operacional com vídeo real | `PARCIAL` | prova automatizada feita; G5 humano pendente |
| 10 — README e operação local | `FUNCIONANDO` | README + scripts documentados |
| Eventos v1 (contrato, serviços, modelo, UI, KPIs) | `IMPLEMENTADO COM EVIDÊNCIA PARCIAL` | contratos conceituais; importação segue bloqueada onde aplicável |
| Points policy v1 | `CRIADO — AGUARDA VALIDAÇÃO LOCAL` | `tests/test_points_policy_v1.py` |
| Auditor docs x contratos | `CRIADO — AGUARDA VALIDAÇÃO LOCAL` | `tests/test_docs_contract_alignment_audit.py` |
| Auditor full extraction template | `CRIADO — AGUARDA VALIDAÇÃO LOCAL` | `tests/test_scout_design_template_full_extraction_audit.py` |

---

## Detalhe por fase

### Fase 1 — Pré-implementação obrigatória `[CONCLUÍDA]`

- `match_roster` tem um único `player_id` — verificado por script.
- `## 13.1 KPIs coletivos` aparece uma única vez — verificado por script.
- Arquivo: `docs/002_SPEC_MVP_Tecnico.md`

### Fase 2 — Estrutura base do projeto `[CONCLUÍDA]`

- Árvore de diretórios conforme `003_PLAN_Passos_Implementacao_IA.md §2.1`
- `requirements.txt` com versões fixas provadas no ambiente local
- `python3 -c "import scoutpraia"` passa

### Fase 3 — Configuração, paths e banco `[CONCLUÍDA]`

- `scoutpraia/core/config.py`, `paths.py`, `database.py`
- `python3 -m scoutpraia.core.database` cria `data/scoutpraia.db`
- `data/*.db` ignorado pelo Git

### Fase 4 — Modelos de dados iniciais `[CONCLUÍDA COMO BASE]`

Modelos implementados: `Team`, `Player`, `Opponent`, `Match`, `MatchRoster`,
`SetSegment`, `Possession`, `TaxonomyVersion`, `EventDefinition`, `Event`,
`CodingSession`, `CodingAgreement`, `Clip`, `Report`

Limite: ainda faltam testes individuais para todos os modelos.

### Fase 5 — Taxonomia v0.1 `[CONCLUÍDA]`

- 31 definições de eventos.
- Seed idempotente em `scoutpraia/services/taxonomy_service.py`.
- Status global da taxonomia: `draft`.

---

## Ciclo — G5: validação humana com vídeo real (fechamento oficial do MVP)

- Fase declarada: `Fase 9 — validação operacional com vídeo real — CONCLUÍDA`
- O que foi executado:
  - rodada humana completa no navegador real por Davi Sermenho
  - 12 eventos marcados no match-1 (adversária: Campinas 360)
  - vídeo real: `jogo_x6ppOlG0XlQ_2h19m44s_2h52m31s_720p_h264.mp4`
  - 3 tipos de relatório gerados pela UI: coletivo, individual (Fernanda Campbell), adversária (Campinas 360)
  - screenshots registrados em `docs/prints.png`
  - protocolo Blocos A–E preenchido em `docs/007_PROT_Protocolo_Validacao.md`
- O que foi testado:
  - `scripts/verify_current_state.sh` verde antes do ensaio
  - `python3 -m pytest -q` com venv ativo
- Resultado observado:
```text
date_utc=2026-06-12T04:34:46Z
git_head=2f3b7f6
pytest=300 passed in 16.68s
new_events_count=12
final_report_count=5
decision=APROVADO
```
- Limitações registradas (escopo de v0.1, não falha de plataforma):
  - posições ofensivas e defensivas não coletadas
  - papel da especialista não coletado
  - defesa da goleira sem módulo ativo
  - resultados de eventos incompletos (campos v1 não ativados)
  - todas as lacunas são endereçadas pelos contratos v1 bloqueados até este gate
- Status final:
  - `G5`: **FECHADO — APROVADO**
  - `mvp_completo`: **true**
  - próxima fase autorizada: ativação progressiva dos módulos v1 (começar por `finalization_v1`)

---

## Ciclo — Ativação finalization_v1

- Data: `2026-06-12`
- O que foi alterado:
  - `scoutpraia/contracts/events_v1.py`: `FINALIZATION_V1.import_rule_v1` → `IMPORT_RULE_V1_ACTIVE`; todos os 5 primary_events → `EVENT_STATUS_ACTIVE` + `IMPORT_RULE_V1_ACTIVE`
  - `scoutpraia/services/taxonomy_service.py`: adicionados 4 eventos ausentes — `simple_shot`, `inflight_shot`, `goalkeeper_shot`, `six_metre_throw` (total: 35 definições)
  - `tests/test_events_v1_contract_registry.py`: assertion de import_rule atualizada para `IMPORT_RULE_V1_ACTIVE` em primary_events de `finalization_v1`
  - `docs/005_CONT_Operacional_Eventos_v1.md`: seção 2-bis e gate_de_leitura atualizados
- Resultado esperado:
  - botões "Finalização v1.0" aparecem na UI de marcação (simple_shot, spin_shot, inflight_shot, goalkeeper_shot, six_metre_throw)
  - pontos derivados automaticamente pelo contrato (não manual)
  - scorer_role obrigatório nos formulários de finalização
- Verificação:
  ```bash
  source .venv/bin/activate && python3 -m pytest -q
  ```

---

## Ciclo — P0_005 + P0_006: UI Registry + QUICK_EVENT_TYPES derivado do contrato

- Data: `2026-06-13`
- Contexto: P1_001 (conflito finalization_v1) resolvido. P0_005 e P0_006 implementados.
- O que foi alterado:
  - `scoutpraia/ui/__init__.py`: criado (pacote ui)
  - `scoutpraia/ui/contracts.py`: criado — `get_active_quick_event_codes()`, `FORBIDDEN_EVENT_CODES`, `is_blocked_event()` derivados de `events_v1.py`
  - `scoutpraia/pages/tagging.py`: `QUICK_EVENT_TYPES` agora é `get_active_quick_event_codes()` (remove hardcoded legacy/proibidos); default do session_state usa `QUICK_EVENT_TYPES[0]` em vez de `"shot_attempt"`
  - `tests/test_ui_contract_registry.py`: criado — 22 testes provam que specialist_goal/specialist_attempt/shootout_goal estão fora do registry e que finalization+attack_no_shot estão presentes
  - `tests/test_tagging_no_blocked_quick_buttons.py`: criado — 10 testes provam que QUICK_EVENT_TYPES não expõe eventos proibidos
  - `tests/test_streamlit_pages.py`: dois testes atualizados para simular corretamente a troca de tipo de evento antes de preencher campos dependentes
  - `docs/005_CONT_Operacional_Eventos_v1.md`: seções 2-bis, 3, 7 e 11 — finalization_v1 corrigido para `importar_v1`
  - `docs/000_QUICK_REFERENCE.md`: tabela e seção 3 atualizados (finalization_v1 ativo)
  - `docs/001_PLAN_Plano_Mestre_Agente.md`: module_effective_status.finalization_v1 → `effective_status: "active"`, P1_001 → `status: completed`
  - memória `project_contract_g1fix.md`: atualizada para refletir dois módulos ativos
- Resultado:
  - `QUICK_EVENT_TYPES` não contém mais: `specialist_attempt`, `specialist_goal`, `shootout_goal`, `shot_attempt`, `goal_scored`, `two_point_goal`, etc.
  - UI expõe apenas eventos de módulos com `IMPORT_RULE_V1_ACTIVE`
  - 352 testes passando (32 novos testes adicionados)
- Verificação:
  ```bash
  source .venv/bin/activate && python3 -m pytest -q
  bash scripts/verify_current_state.sh
  ```
