---
tipo: progresso_execução
status_geral: BASE_TÉCNICA_FUNCIONANDO
fase_atual: "Eventos v1 — EV-009 de shootout_v1 e EV-010 de goalkeeper_v1 registrados sem liberar seed/UI/importação"
testes_passando: 226
event_definitions: 31
última_atualização: 2026-06-11
próxima_ação: "Executar G5 (validação humana); offensive_creation_v1, defensive_v1, shootout_v1 e goalkeeper_v1 seguem sem liberação operacional"
gaps_abertos: ["G5 — validação humana pendente"]
mvp_completo: false
---

# ScoutPraia — Progresso de Implementação e Evidência

Este arquivo registra o estado atual de implementação. Ele deve ser atualizado a cada ciclo.

**Regra:** uma etapa só pode ser marcada como `FUNCIONANDO` quando houver evidência
reproduzível por comando, teste ou arquivo verificável.

**Histórico de ciclos anteriores:** ver `docs/IMPLEMENTATION_LOG.md`.

---

## Sumário executivo

**Status geral:** `BASE TÉCNICA FUNCIONANDO — MVP INCOMPLETO`

**Gate atual:**

```bash
scripts/verify_current_state.sh
# resultado esperado: 226 passed
```

**Estado do workspace no baseline G0:**
- `git status --short` limpo em `2026-06-10`
- `git_head = aa8934c`

**Próxima ação autorizada:**
1. Executar G5: validação humana com vídeo real (ver `docs/validation_protocol.md`)
2. Manter `offensive_creation_v1` e `defensive_v1` somente no registry até G5
3. Manter `shootout_v1` como contrato conceitual validado por teste, sem seed/UI/importação
4. Manter `goalkeeper_v1` como contrato conceitual validado por teste, sem seed/UI/importação
5. Decidir liberação da importação v1 (`import_rule_v1`) apenas depois de G5

---

## Prova reproduzível

```bash
scripts/verify_current_state.sh
```

Verifica: higiene do repo, import do pacote, banco SQLite, seed da taxonomia,
contagem de event_definitions, testes automatizados, `git diff --check`.

**Última execução registrada:**

```text
date_utc=2026-06-11
git_head=aa8934c
taxonomy=ScoutPraia v0.1
taxonomy_status=draft
event_definitions=31
expected_event_definitions=31
226 passed
git_status=clean
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
    verify_current_state: "passed"
    git_status: "clean"
  modules:
    attack_no_shot_v1:
      status: "contrato_validado"
      import_rule_v1: "importar_v1"
      evidence: ["EV-001", "EV-002", "EV-003", "EV-004", "EV-005"]
    finalization_v1:
      status: "contrato_validado"
      import_rule_v1: "nao_importar_v1"
      evidence: ["EV-006"]
    offensive_creation_v1:
      status: "contrato_validado"
      import_rule_v1: "nao_importar_v1"
      evidence: ["EV-007"]
    defensive_v1:
      status: "contrato_validado"
      import_rule_v1: "nao_importar_v1"
      evidence: ["EV-008"]
```

Observação: este baseline registra o estado verde anterior ao ajuste do registry G1. Os ciclos abaixo preservam esse baseline e mantêm `offensive_creation_v1` e `defensive_v1` apenas como contratos bloqueados; a estrutura interna do registry deve seguir a prioridade `SCOUT_DESIGN_TEMPLATE` > `Contrato_Operacional.md` > repositório.

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
| 8 — Testes | `FUNCIONANDO` | 226 passed |
| 9 — Validação operacional com vídeo real | `PARCIAL` | prova automatizada feita; G5 humano pendente |
| 10 — README e operação local | `FUNCIONANDO` | README + scripts documentados |
| Eventos v1 (contrato, serviços, modelo, UI, KPIs) | `IMPLEMENTADO COM EVIDÊNCIA` | baseline G0 fechado; G1 registry realinhado à planilha; importação segue bloqueada |

---

## Detalhe por fase

### Fase 1 — Pré-implementação obrigatória `[CONCLUÍDA]`

- `match_roster` tem um único `player_id` — verificado por script.
- `## 13.1 KPIs coletivos` aparece uma única vez — verificado por script.
- Arquivo: `docs/MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md`

### Fase 2 — Estrutura base do projeto `[CONCLUÍDA]`

- Árvore de diretórios conforme `IMPLEMENTATION_STEPS_AI.md §2.1`
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

- 31 definições de eventos (após adição de `specialist_attempt` e `specialist_goal`)
- Seed idempotente em `scoutpraia/services/taxonomy_service.py`
- Status global da taxonomia: `draft`
- `two_point_goal` promovido para `testing` em 2026-06-09 (G1 fechado)

### Fase 6 — Serviços internos `[CONCLUÍDA COM EVIDÊNCIA]`

| Serviço | Status | Teste principal |
|---------|--------|----------------|
| `video_service.py` | FUNCIONANDO | `test_video_metadata_uses_real_ffprobe` |
| `event_service.py` | FUNCIONANDO | `test_event_service.py` (+ v1 fields) |
| `clip_service.py` | FUNCIONANDO | `test_clip_service.py` |
| `validation_service.py` | FUNCIONANDO | `test_validation_service.py` |
| `analytics_service.py` | FUNCIONANDO | `test_analytics_service.py` |
| `report_service.py` | FUNCIONANDO | `test_report_service.py` |
| `match_service.py` | FUNCIONANDO | `test_match_service.py` |
| `finalization_contract_service.py` | FUNCIONANDO | `test_finalization_contract_service.py` |
| `no_shot_attack_contract_service.py` | FUNCIONANDO | `test_no_shot_attack_contract_service.py` |

### Fase 7 — Interface Streamlit `[CONCLUÍDA COM EVIDÊNCIA]`

Páginas implementadas: Dashboard, Jogos, Marcação, Relatórios, Adversárias

Funcionalidades da página Marcação:
- player de vídeo com `st.video`
- timestamp em MM:SS, HH:MM:SS ou segundos
- botões rápidos com preenchimento automático de pontos
- edição/exclusão de qualquer evento salvo
- edição/exclusão de set e posse
- filtros por set, lado, tipo e busca textual
- navegação rápida entre eventos filtrados
- ajuste fino de timestamp (±0.5s, ±1s)

Pendências da fase 7:
- Verificação visual humana fim a fim ainda não documentada com screenshots

### Fase 8 — Testes `[FUNCIONANDO]`

226 testes passando. Suíte inclui:
- `test_smoke.py`, `test_models.py`, `test_match_service.py`
- `test_event_service.py`, `test_clip_service.py`
- `test_validation_service.py`, `test_analytics_service.py`
- `test_report_service.py`, `test_streamlit_pages.py`
- `test_ui_labels.py`, `test_taxonomy_service.py`
- `test_events_v1_contract_registry.py`, `test_finalization_contract.py`
- `test_finalization_contract_service.py`, `test_no_shot_attack_contract_service.py`
- `test_event_model_v1_fields.py`, `test_tagging_finalization_v1_ui.py`
- `test_tagging_no_shot_attack_v1_ui.py`, `test_reports_events_v1.py`
- `test_real_video_integration.py`

### Fase 9 — Validação operacional com vídeo real `[PARCIAL]`

Concluído:
- Ensaio automatizado com Playwright em `Execução 2` — 3 relatórios gerados pela UI real
- 8 eventos reais persistidos no banco local

Pendente (G5):
- Rodada humana com screenshots documentados
- Protocolo em `docs/validation_protocol.md` — checklist Bloco A–E

### Fase 10 — README e operação local `[CONCLUÍDA]`

- `README.md` documenta instalação, banco, launcher e fallback de virtualenv
- `scripts/run_scout.sh` — launcher com `--port` e `--no-browser`
- `scripts/setup_venv.sh` — fallback para ambientes sem `ensurepip`
- `ScoutPraia.desktop` — lançador gráfico de 1 clique

### Eventos v1 `[IMPLEMENTADO COM EVIDÊNCIA — IMPORTAÇÃO BLOQUEADA]`

| Passo | Arquivo | Status |
|-------|---------|--------|
| 1 — Contrato | `scoutpraia/contracts/events_v1.py` | CONCLUÍDO |
| 1B — Registry G1 | `offensive_creation_v1` + `defensive_v1` reconhecidos no registry com separação núcleo/revisão/futuro | CONCLUÍDO |
| 2 — Serviço Finalização | `finalization_contract_service.py` | CONCLUÍDO |
| 3 — Serviço Ataque sem finalização | `no_shot_attack_contract_service.py` | CONCLUÍDO |
| 4 — Modelo/banco | campos v1 em `event.py` + migração leve | CONCLUÍDO |
| 5 — UI de marcação | blocos v1 em `tagging.py` | CONCLUÍDO |
| 6 — Relatórios/KPIs | métricas v1 em `analytics_service.py` + templates | CONCLUÍDO |
| 6A — Correção KPIs | especialista + 2 pontos adversária | CONCLUÍDO |

Importação bloqueada: `import_rule_v1 = nao_importar_v1`

Registry principal atual:
- `attack_no_shot_v1` — importação ativa (`importar_v1`)
- `finalization_v1` — contrato validado, importação bloqueada
- `offensive_creation_v1` — contrato validado no registry, importação bloqueada
- `defensive_v1` — contrato validado no registry, importação bloqueada
- `shootout_v1` — contrato conceitual validado por teste, sem seed/UI/importação
- `goalkeeper_v1` — contrato conceitual validado por teste, sem seed/UI/importação
- `offensive_creation_v1` — núcleo ativo: `assist_to_finalization`; auxiliares: `assist_to_inflight_shot`, `pivot_feed_to_shot`; revisão: `advantage_pass_to_free_player`, `collective_action_creates_shot`
- `defensive_v1` — núcleo ativo: `line_block_shot`; revisão: `defensive_pressure_forced_error`, `steal_or_interception`; futuro: `defensive_rebound_recovery`

Limite explícito:
- `offensive_creation_v1` e `defensive_v1` ainda não aparecem na UI nem na importação ativa do app
- `shootout_v1` permanece fora do seed operacional, da UI e da importação
- `goalkeeper_v1` permanece fora do seed operacional, da UI e da importação
- este ciclo não altera `tagging.py`, seed, serviços de persistência ou relatórios operacionais

Para liberar: passar todos os testes v1 **E** ter evidência registrada de:
- contrato v1 carregado no código ✓
- serviço de Finalização aprovado ✓
- serviço de Ataque sem finalização aprovado ✓
- UI de marcação aprovada ✓
- modelo/banco aprovado ✓
- relatórios mínimos aprovados ✓
- decisão explícita de promoção em `docs/taxonomy_dictionary.md`

---

## Pendências reais para MVP completo

1. G5: validação humana com screenshots (ver `docs/validation_protocol.md`)
2. Verificação visual fim a fim no navegador documentada
3. Decidir liberação da importação v1 após G5
4. Seed de dados de exemplo ou fixture sintética de jogo completo
5. Expor regra de taxonomia aprovada na UI de relatórios

---

## Definição de não concluído

Não considerar o MVP completo enquanto qualquer item abaixo estiver ausente:

- marcação operacional completa por jogo — **presente**
- geração real de clipes com `ffmpeg` — **presente**
- KPIs completos — **presente**
- fluxo operacional completo de relatórios via interface — **presente**
- validação da taxonomia com vídeo e screenshots humanos — **PENDENTE (G5)**
- testes de fluxo operacional — **presente**

---

## Próxima fase autorizada pelo plano

1. Executar protocolo G5 de validação humana (`docs/validation_protocol.md`)
2. Rodar `scripts/verify_current_state.sh` após qualquer nova mudança relevante
3. Depois de G5: decidir liberação de `import_rule_v1`
4. Não liberar UI/importação de `offensive_creation_v1`, `defensive_v1`, `shootout_v1` ou `goalkeeper_v1` antes desse gate

---

## Governança de agentes

Status: `CONFIGURADO`

- `AGENTS.md` com regras obrigatórias para agentes neste repositório.
- Exigência de prova reproduzível antes de declarar sucesso.
- Exigência de atualização deste arquivo em cada ciclo.
- Proibição explícita de pular fases ou esconder trabalho parcial.
- Restrições de escopo: sem React, FastAPI, PostgreSQL, API pública, auth, deploy, RAG antes do MVP funcional.

---

## Ciclo — G0 baseline + G1 registry

- Fase declarada: `Eventos v1 — fechamento de baseline G0 e ampliação controlada do registry G1`
- O que foi implementado:
  - registro oficial do baseline `G0_BASELINE_EVENTOS_V1_VERDE`
  - inclusão de `offensive_creation_v1` e `defensive_v1` em `scoutpraia/contracts/events_v1.py`
  - atualização de `tests/test_events_v1_contract_registry.py` para o novo snapshot do registry
- O que foi testado:
  - `python3 -m pytest tests/test_events_v1_contract_registry.py -q`
  - `python3 -m pytest tests/test_eventos_sheet_scope.py -q`
  - `python3 -m pytest -q`
  - `scripts/verify_current_state.sh`
  - `git status --short`
- Resultado observado:
  - registry específico: `10 passed`
  - escopo da planilha: `7 passed`
  - suíte completa: `199 passed`
  - `verify_current_state.sh`: verde com `event_definitions=31` e `199 passed`
  - baseline G0 preservado como registro do estado limpo anterior (`git_head=5cf588c`, `git_status=clean`)
- O que ainda não está pronto:
  - `offensive_creation_v1` e `defensive_v1` não foram liberados na UI nem na importação ativa
  - G5 continua pendente
- Limitações, gaps e riscos:
  - este ciclo valida somente reconhecimento contratual no registry; não prova fluxo operacional desses dois módulos no app
  - qualquer liberação futura desses módulos ainda depende de gate posterior e evidência adicional

---

## Ciclo — correção de aderência planilha + contrato

- Fase declarada: `Eventos v1 — correção do registry para espelhar SCOUT_DESIGN_TEMPLATE e Contrato_Operacional`
- O que foi implementado:
  - separação explícita em `scoutpraia/contracts/events_v1.py` entre `primary_events`, `auxiliary_fields`, `review_only_events` e `future_events`
  - realinhamento de `offensive_creation_v1` para núcleo ativo único `assist_to_finalization`
  - realinhamento de `defensive_v1` para núcleo ativo único `line_block_shot`
  - atualização de `tests/test_events_v1_contract_registry.py` para provar que revisão/futuro não contam como núcleo ativo
- O que foi testado:
  - `python3 -m pytest tests/test_events_v1_contract_registry.py -q`
  - `python3 -m pytest -q`
  - `scripts/verify_current_state.sh`
- Resultado observado:
  - registry específico: `10 passed`
  - suíte completa: `199 passed`
  - `verify_current_state.sh`: verde com `event_definitions=31`, `199 passed` e `git diff --check` sem erro
- O que ainda não está pronto:
  - `offensive_creation_v1` e `defensive_v1` continuam fora da UI e da importação ativa
  - G5 continua pendente
- Limitações, gaps e riscos:
  - o registry agora espelha melhor a planilha/contrato, mas isso ainda não representa implementação operacional desses módulos no app
  - qualquer divergência futura deve ser resolvida pela prioridade de fonte definida em `docs/Contrato_Operacional.md`
  - `docs/Contrato_Operacional.md` passa a compor o conjunto versionável de fontes do ciclo

---

## Ciclo — evidência local EV-009 do shootout_v1

- Fase declarada: `Eventos v1 — registro documental da evidência local do contrato conceitual de shootout`
- O que foi implementado:
  - atualização de `docs/Contrato_Operacional.md` para registrar `EV-009`
  - consolidação do estado de `shootout_v1` como `arquitetura_em_definicao_validada_por_teste_conceitual`
  - registro explícito de que seed operacional, UI e importação permanecem inalterados
- O que foi testado:
  - `python3 -m pytest tests/test_shootout_contract.py -q`
  - `python3 -m pytest tests/test_events_v1_contract_registry.py -q`
  - `python3 -m pytest -q`
  - `scripts/verify_current_state.sh`
  - `git diff --check`
  - `git status --short`
- Resultado observado:
  - shootout específico: `10 passed in 0.02s`
  - registry específico: `12 passed in 0.02s`
  - suíte completa: `211 passed in 14.49s`
  - `verify_current_state.sh`: verde com `git_head=c4afac9`, `taxonomy=ScoutPraia v0.1`, `taxonomy_status=draft`, `event_definitions=31` e `211 passed in 13.59s`
  - `git diff --check`: sem saída
  - `git status --short`: limpo antes da atualização documental deste ciclo
- O que ainda não está pronto:
  - `shootout_v1` não foi promovido para seed operacional
  - `shootout_v1` não foi liberado na UI nem na importação
  - G5 continua pendente
- Limitações, gaps e riscos:
  - a evidência fecha apenas o contrato conceitual e sua compatibilidade com a base atual
  - esta validação não prova fluxo operacional de marcação de shoot-out no app
  - qualquer liberação operacional continua bloqueada até gate posterior explícito

---

## Ciclo — evidência local EV-010 do goalkeeper_v1

- Fase declarada: `Eventos v1 — registro documental da evidência local do contrato conceitual de goalkeeper`
- O que foi implementado:
  - atualização de `docs/Contrato_Operacional.md` para registrar `EV-010`
  - consolidação do estado de `goalkeeper_v1` como `arquitetura_em_definicao_validada_por_teste_conceitual`
  - registro explícito de que seed operacional, UI e importação permanecem inalterados
- O que foi testado:
  - `python3 -m pytest tests/test_goalkeeper_contract.py -q`
  - `python3 -m pytest tests/test_events_v1_contract_registry.py -q`
  - `python3 -m pytest -q`
  - `scripts/verify_current_state.sh`
  - `git diff --check`
  - `git status --short`
- Resultado observado:
  - goalkeeper específico: `13 passed in 0.02s`
  - registry específico: `14 passed in 0.02s`
  - suíte completa: `226 passed in 14.19s`
  - `verify_current_state.sh`: verde com `git_head=aa8934c`, `taxonomy=ScoutPraia v0.1`, `taxonomy_status=draft`, `event_definitions=31` e `226 passed in 13.81s`
  - `git diff --check`: sem saída
  - `git status --short`: limpo antes da atualização documental deste ciclo
- O que ainda não está pronto:
  - `goalkeeper_v1` não foi promovido para seed operacional
  - `goalkeeper_v1` não foi liberado na UI nem na importação
  - G5 continua pendente
- Limitações, gaps e riscos:
  - a evidência fecha apenas o contrato conceitual e sua compatibilidade com a base atual
  - esta validação não prova fluxo operacional de marcação de goleira no app
  - qualquer liberação operacional continua bloqueada até gate posterior explícito

---

## Como registrar um novo ciclo

Adicionar ao final deste arquivo:

```markdown
## Ciclo — <nome curto>

Fase atual declarada: `<fase>`

Status: `<status>`

Implementado / executado:

- ...

Comandos executados:

```bash
...
```

Resultado observado:

```text
...
```

O que ainda não está pronto:

- ...

Limitações, gaps e riscos:

- ...
```
