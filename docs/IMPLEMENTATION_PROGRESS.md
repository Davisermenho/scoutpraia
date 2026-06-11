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

## Ciclo — padronização do `plano_de_acao.md`

- Fase declarada: `Fase 9 — documentação operacional auxiliar (sem alterar comportamento do MVP)`
- O que foi implementado:
  - reestruturação completa de `plano_de_acao.md` para Markdown hierárquico consistente
  - remoção de headings redundantes em `# **...**` e padronização para títulos Markdown nativos
  - conversão de exemplos soltos para blocos de código (`csv`, `text`, `json`, `md`)
  - conversão de listas com quebra manual em listas Markdown reais
  - correção de inconsistências de hierarquia, especialmente nos exemplos internos de glossário e relatório
- O que foi testado:
  - `git diff --check`
  - `scripts/verify_current_state.sh`
  - `git status --short`
- Resultado observado:
  - `git diff --check`: sem saída
  - `verify_current_state.sh`: verde com `git_head=63624c2`, `taxonomy=ScoutPraia v0.1`, `taxonomy_status=draft`, `event_definitions=31` e `226 passed in 13.96s`
  - `git status --short`: `?? beach_handball_ai/` e `?? plano_de_acao.md`
- O que ainda não está pronto:
  - G5 continua pendente
  - o conteúdo de `plano_de_acao.md` segue como plano auxiliar e não substitui os contratos canônicos do repositório
- Limitações, gaps e riscos:
  - a validação executada prova higiene do diff e integridade do estado atual do repositório, não qualidade semântica do plano além da padronização estrutural
  - `plano_de_acao.md` permanece não rastreado no Git neste estado
  - havia um diretório não rastreado pré-existente (`beach_handball_ai/`) no workspace durante a validação

---

## Ciclo — registro unificado de fontes fortes

- Fase declarada: `Fase 9 — organização manual de fontes e rastreabilidade documental (sem liberar RAG)`
- O que foi implementado:
  - atualização de `beach_handball_ai/plano_de_acao.md` para declarar `docs/sources/` como entrada obrigatória junto com `beach_handball_ai/fontes/`
  - substituição dos `.md` vazios em `beach_handball_ai/fontes/04_fontes_proprias_cepraea/` e `beach_handball_ai/fontes/05_processado/IHF_RULES_BH_2026_PT_TRANSLATION.md` por placeholders explícitos de status
  - geração de `beach_handball_ai/fontes/00_registro/fontes_oficiais.csv` com 46 linhas inventariadas e colunas extras de rastreabilidade (`source_code_repo`, `origem_catalogo`, `papel_documento`, `fonte_primaria_relacionada`, `uso_mvp`, `uso_rag_fase2`)
  - atualização de `beach_handball_ai/fontes/00_registro/fontes_oficiais.xlsx` para refletir o registro unificado e adicionar sheets auxiliares de crosswalk e resumo de status
  - geração de `beach_handball_ai/fontes/05_processado/manifest_checksums.json` com checksums SHA-256 para `docs/sources/` e `beach_handball_ai/fontes/`
- O que foi testado:
  - `python3` inline para reconstruir o registro unificado, recalcular checksums e regravar `csv`/`xlsx`/`json`
  - `python3` inline para validar `source_id` único, existência de arquivo, checksum preenchido e zero-byte somente em status de placeholder
  - `git diff --check`
  - `scripts/verify_current_state.sh`
  - `git status --short`
- Resultado observado:
  - registro unificado: `46` linhas, `46` `source_id` únicos, nenhum arquivo ausente, nenhum checksum em branco
  - pendências explícitas restantes: `4` PDFs EHF continuam `0 bytes` com status `placeholder_vazio_pendente_download`
  - `manifest_checksums.json` passou a registrar os dois acervos (`docs/sources` e `beach_handball_ai/fontes`)
  - `verify_current_state.sh`: verde com `git_head=63624c2`, `taxonomy=ScoutPraia v0.1`, `taxonomy_status=draft`, `event_definitions=31` e `226 passed`
  - `git diff --check`: sem saída
  - `git status --short`: ` M docs/IMPLEMENTATION_PROGRESS.md` e `?? beach_handball_ai/`
- O que ainda não está pronto:
  - RAG continua bloqueado por contrato até G5 e fase 2
  - os 4 PDFs EHF previstos no corpus operacional ainda não foram obtidos
  - as fontes próprias CEPRAEA continuam como `pendente_elaboracao`; agora sem ambiguidade de placeholder vazio
- Limitações, gaps e riscos:
  - este ciclo fecha o inventário e a rastreabilidade do item 1, mas não valida o conteúdo semântico das fontes próprias ainda não escritas
  - os artefatos em `beach_handball_ai/fontes/05_processado/documentos_markdown/` continuam derivados intermediários (`.docx`), não markdown consolidado final
  - a presença de fontes de IA em `docs/sources/` não altera o bloqueio de uso operacional do RAG no ScoutPraia

---

## Ciclo — obtenção dos 4 PDFs EHF previstos no registro

- Fase declarada: `Fase 9 — organização manual de fontes e fechamento de placeholders EHF`
- O que foi implementado:
  - substituição dos 4 placeholders vazios em `beach_handball_ai/fontes/02_ehf_tecnico/` pelos PDFs oficiais reais da página EHF Beach Handball Publications
  - atualização do registro em `beach_handball_ai/fontes/00_registro/fontes_oficiais.csv` e `fontes_oficiais.xlsx` com links oficiais EHF, checksums e status `obtido_oficial_ehf_pendente_leitura`
  - atualização de `beach_handball_ai/fontes/05_processado/manifest_checksums.json` para refletir os novos arquivos e o novo resumo de status
- O que foi testado:
  - `python3` inline para localizar e baixar os 4 PDFs a partir dos links oficiais da página EHF
  - `python3` inline para atualizar `csv`/`xlsx`/`manifest` com links, checksums e status
  - verificação de tamanho dos arquivos em `beach_handball_ai/fontes/02_ehf_tecnico`
  - verificação de ausência de arquivos `0 bytes` restantes em `beach_handball_ai/fontes/`
  - `git diff --check`
  - `scripts/verify_current_state.sh`
  - `git status --short`
- Resultado observado:
  - `refereeing_beach_handball.pdf`: `2967257` bytes
  - `shootout_psychological_pressure.pdf`: `1702276` bytes
  - `ultimate_school_handball_2025.pdf`: `11374314` bytes
  - `mini_beach_handball_info_sheet.pdf`: `2225349` bytes
  - não restaram arquivos `0 bytes` em `beach_handball_ai/fontes/`
  - `verify_current_state.sh`: verde com `git_head=63624c2`, `taxonomy=ScoutPraia v0.1`, `taxonomy_status=draft`, `event_definitions=31` e `226 passed`
  - `git diff --check`: sem saída
  - `git status --short`: ` M docs/IMPLEMENTATION_PROGRESS.md` e `?? beach_handball_ai/`
- O que ainda não está pronto:
  - os 4 PDFs EHF foram obtidos, mas seguem `pendente_leitura` no registro; o conteúdo semântico ainda não foi resumido/classificado em profundidade
  - as fontes próprias CEPRAEA continuam `pendente_elaboracao`
  - os artefatos `.docx` de `05_processado/documentos_markdown/` continuam derivados intermediários
- Limitações, gaps e riscos:
  - a obtenção dos PDFs prova disponibilidade local e rastreabilidade oficial EHF, não leitura técnica integral do conteúdo
  - o arquivo `Understanding Psyhological Pressure...` preserva a grafia do link oficial EHF (`Psyhological`)
  - o bloqueio de RAG permanece inalterado; obter os PDFs não libera fase 2

---

## Ciclo — classificação semântica dos 4 PDFs EHF

- Fase declarada: `Fase 9 — organização manual de fontes e classificação temática de apoio`
- O que foi implementado:
  - leitura local dos 4 PDFs EHF com extração de texto por `pdftotext`
  - conferência de metadata por `pdfinfo` para registrar datas de criação/versão quando disponíveis
  - atualização de `beach_handball_ai/fontes/00_registro/fontes_oficiais.csv` e `fontes_oficiais.xlsx` para trocar `obtido_oficial_ehf_pendente_leitura` por `validado_tecnico_educacional_ehf`
  - refinamento semântico de tema, observação e uso final para cada publicação:
    - `Refereeing in Beach Handball` → arbitragem, preparação física e estresse térmico
    - `Understanding Psychological Pressure in Beach Handball Shootouts` → psicologia do esporte e preparação mental para shoot-out
    - `Ultimate School Handball 2025` → ensino escolar, metodologia e iniciação
    - `Mini Beach Handball Info Sheet 2020` → iniciação infantil e regras adaptadas
  - atualização do resumo de status em `beach_handball_ai/fontes/05_processado/manifest_checksums.json`
- O que foi testado:
  - `pdftotext` nos 4 PDFs EHF
  - `pdfinfo` nos 4 PDFs EHF
  - `python3` inline para atualizar `csv`/`xlsx`/`manifest`
  - inspeção das 4 linhas EHF no registro final
  - `git diff --check`
  - `scripts/verify_current_state.sh`
  - `git status --short`
- Resultado observado:
  - as 4 entradas EHF passaram a `validado_tecnico_educacional_ehf`
  - `manifest_checksums.json` agora resume `4` itens nesse status
  - `verify_current_state.sh`: verde com `git_head=63624c2`, `taxonomy=ScoutPraia v0.1`, `taxonomy_status=draft`, `event_definitions=31` e `226 passed`
  - `git diff --check`: sem saída
  - `git status --short`: ` M docs/IMPLEMENTATION_PROGRESS.md` e `?? beach_handball_ai/`
- O que ainda não está pronto:
  - as fontes próprias CEPRAEA continuam `pendente_elaboracao`
  - os artefatos `.docx` de `05_processado/documentos_markdown/` continuam derivados intermediários
  - o uso das fontes EHF continua sendo de apoio técnico/educacional, não normativo
- Limitações, gaps e riscos:
  - a classificação feita aqui é suficiente para catalogação e uso orientado, mas não substitui leitura integral futura se alguma publicação passar a sustentar decisão crítica específica
  - o bloqueio de RAG permanece inalterado; classificar semanticamente as fontes não libera fase 2

---

## Ciclo — elaboração das 4 fontes próprias CEPRAEA

- Fase declarada: `Fase 9 — consolidação de fontes internas de apoio`
- O que foi implementado:
  - substituição dos placeholders por conteúdo base nas 4 fontes próprias em `beach_handball_ai/fontes/04_fontes_proprias_cepraea/`
  - elaboração de `glossario_tecnico_cepraea.md` com distinção entre termos operacionais já alinhados ao app e convenções internas ainda pendentes
  - elaboração de `playbook_cepraea.md` com hierarquia de decisão, blocos de leitura e fluxo treinador-video-relatorio
  - elaboração de `scout_schema.md` com o schema funcional do ScoutPraia v0.1 baseado no modelo `Event`, labels e KPIs atuais
  - elaboração de `criterios_taticos_cepraea.md` com critérios internos para transformar evento e KPI em leitura de treino/jogo
  - atualização do registro em `beach_handball_ai/fontes/00_registro/fontes_oficiais.csv` e `fontes_oficiais.xlsx` para promover as 4 fontes de `pendente_elaboracao` para `base_interna_elaborada_v0`
  - atualização de `beach_handball_ai/fontes/05_processado/manifest_checksums.json` com os novos checksums e resumo de status
- O que foi testado:
  - inspeção dos 4 arquivos gerados
  - `python3` inline para atualizar `csv`/`xlsx`/`manifest`
  - verificação de status e checksum das 4 entradas no registro
  - verificação de ausência de arquivos `0 bytes` em `beach_handball_ai/fontes/`
  - `git diff --check`
  - `scripts/verify_current_state.sh`
  - `git status --short`
- Resultado observado:
  - as 4 entradas internas passaram a `base_interna_elaborada_v0`
  - os 4 arquivos internos deixaram de ser vazios: `4965` a `11177` bytes
  - não restaram arquivos `0 bytes` em `beach_handball_ai/fontes/`
  - `verify_current_state.sh`: verde com `git_head=63624c2`, `taxonomy=ScoutPraia v0.1`, `taxonomy_status=draft`, `event_definitions=31` e `226 passed`
  - `git diff --check`: sem saída
  - `git status --short`: ` M docs/IMPLEMENTATION_PROGRESS.md` e `?? beach_handball_ai/`
- O que ainda não está pronto:
  - as 4 fontes próprias estão em base `v0`, não em ontologia tática final congelada
  - termos internos como `3:0`, `2:1`, `4:0` e `devolucao` continuam explicitamente marcados como convenção pendente de formalização
  - os artefatos `.docx` de `05_processado/documentos_markdown/` continuam derivados intermediários
- Limitações, gaps e riscos:
  - essas fontes internas foram ancoradas no estado atual do app e da documentação, não em validação humana G5 concluída
  - o objetivo aqui foi remover lacuna documental e alinhar linguagem interna ao que já existe no ScoutPraia, não congelar doutrina tática definitiva
  - o bloqueio de RAG permanece inalterado

---

## Ciclo — consolidação dos artefatos processados em Markdown

- Fase declarada: `Fase 9 — saneamento dos derivados de processamento para uso futuro no plano`
- O que foi implementado:
  - comparação entre os `.docx` e os `.md` correspondentes em `beach_handball_ai/fontes/05_processado/`
  - promoção do melhor conteúdo para `.md` em 17 pares de artefatos
  - limpeza dos escapes indevidos de Markdown (`\\#`, `\\_`, `\\---`) nos `.md` preservados
  - criação de `chunks_jsonl/CHUNKS_FINAIS_RAG_IHF_RULES_BH_2026_PT.md` a partir do `.docx` que não tinha equivalente `.md`
  - transformação de `IHF_RULES_BH_2026_PT_TRANSLATION.md` em índice dos `.md` consolidados
  - remoção de todos os `.docx` intermediários de `05_processado/`
  - atualização do registro em `fontes_oficiais.csv`/`xlsx` e do `manifest_checksums.json` para refletir somente os `.md` consolidados
- O que foi testado:
  - extração local de texto dos `.docx` com `python3` e leitura de `word/document.xml`
  - inspeção manual de pares representativos (`MD_PROCESSADO__IHF_UPDATE_BH_2026_04`, `MD_PROCESSADO__IHF_PAGE_BH_RULES_2026`, `REVISAO_CHUNKING_*`)
  - busca residual por `.docx` em `05_processado/`, no `csv` e no `manifest`
  - verificação de existência de `.docx` via `find` e `rglob`
  - `git diff --check`
  - `scripts/verify_current_state.sh`
  - `git status --short`
- Resultado observado:
  - `docx_exists False`
  - `05_processado/` ficou apenas com `.md` e `manifest_checksums.json`
  - `fontes_oficiais.csv` ficou sem referências residuais a `.docx`
  - resumo de status passou a registrar `18` itens como `derivado_markdown_consolidado`
  - `verify_current_state.sh`: verde com `git_head=63624c2`, `taxonomy=ScoutPraia v0.1`, `taxonomy_status=draft`, `event_definitions=31` e `226 passed`
  - `git diff --check`: sem saída
  - `git status --short`: ` M docs/IMPLEMENTATION_PROGRESS.md` e `?? beach_handball_ai/`
- O que ainda não está pronto:
  - os artefatos processados continuam derivados de apoio, não fontes normativas primárias
  - eventual uso futuro desses `.md` em fase 2 ainda depende do desbloqueio formal de RAG
- Limitações, gaps e riscos:
  - a comparação privilegiou o conteúdo semanticamente mais completo e a formatação Markdown mais utilizável, não equivalência bit a bit com o `.docx`
  - o índice `IHF_RULES_BH_2026_PT_TRANSLATION.md` aponta para os melhores `.md` consolidados, mas a regra normativa continua sendo o PDF IHF oficial em inglês
  - o bloqueio de RAG permanece inalterado

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

---

## Ciclo — fusao das fontes internas CEPRAEA e remocao dos duplicados `*2`

- Fase declarada: `Fase 9 — consolidacao semantica das fontes internas de apoio`
- O que foi implementado:
  - fusao do conteudo util de `glossario_tecnico_cepraea2.md` em `beach_handball_ai/fontes/04_fontes_proprias_cepraea/glossario_tecnico_cepraea.md`
  - formalizacao no glossario dos termos internos `3:0`, `2:1`, `4:0`, `devolucao` e `ultimos 15 segundos`, mantendo o status de convencao interna e sem promover esses itens a evento ou KPI
  - fusao do conteudo util de `playbook_cepraea2.md` em `beach_handball_ai/fontes/04_fontes_proprias_cepraea/playbook_cepraea.md`, com secao propria para sistemas e protocolos internos (`4:0`, `3:1`, `3:0`, `2:1`, `slide`, jogo passivo, ultimos 15 segundos e shoot-out)
  - fusao do conteudo util de `criterios_taticos_cepraea2.md` em `beach_handball_ai/fontes/04_fontes_proprias_cepraea/criterios_taticos_cepraea.md`, reescrevendo as diretrizes como criterio interno condicional e nao como regra oficial ou KPI validado
  - remocao dos arquivos duplicados `glossario_tecnico_cepraea2.md`, `playbook_cepraea2.md` e `criterios_taticos_cepraea2.md`
- O que foi testado:
  - inspecao manual dos trechos fundidos nos 3 arquivos canonicos
  - verificacao de ausencia dos arquivos `*2` via `find`
  - `git diff --check`
  - `scripts/verify_current_state.sh`
  - `git status --short`
- Comandos executados:
```bash
find beach_handball_ai/fontes/04_fontes_proprias_cepraea -maxdepth 1 -type f | sort
git diff --check
scripts/verify_current_state.sh
git status --short
```
- Resultado observado:
```text
find: permaneceram apenas criterios_taticos_cepraea.md, glossario_tecnico_cepraea.md, playbook_cepraea.md e scout_schema.md
git diff --check: sem saida
verify_current_state.sh: verde com git_head=63624c2, taxonomy=ScoutPraia v0.1, taxonomy_status=draft, event_definitions=31 e 226 passed
git status --short:  M docs/IMPLEMENTATION_PROGRESS.md e ?? beach_handball_ai/
```
- O que ainda nao esta pronto:
  - os termos internos fundidos continuam como nomenclatura e playbook interno; nao viraram evento, KPI ou automacao do ScoutPraia
  - a validacao humana G5 continua pendente e segue bloqueando qualquer liberacao de RAG
  - o conteudo fundido ainda nao congela ontologia tatica final da equipe
- Limitacoes, gaps e riscos:
  - a fusao privilegiou o contrato metodologico do ScoutPraia e rebaixou afirmacoes absolutas dos arquivos `*2` para linguagem de convencao interna
  - metas numericas rigidas e gatilhos automaticos dos arquivos `*2` nao foram canonizados como criterio estavel por falta de validacao observacional no repositorio
  - o resultado melhora a consistencia documental do corpus CEPRAEA, mas nao substitui revisao tecnica humana da comissao para fechar doutrina interna definitiva

---

## Ciclo — auditoria do corpus `beach_handball_ai/` para segundo commit controlado

- Fase declarada: `Fase 9 — saneamento e versionamento controlado do corpus documental`
- O que foi implementado:
  - auditoria do restante de `beach_handball_ai/` ainda fora do Git apos o primeiro commit das fontes internas canonicas
  - verificacao de que o corpus remanescente contem apenas plano, registros, fontes normativas/tecnicas, processados markdown e schema documental
  - decisao de versionar controladamente o restante do corpus, incluindo PDFs oficiais, `fontes_oficiais.csv`/`.xlsx`, `manifest_checksums.json`, `scout_schema.md`, markdowns processados e `plano_de_acao.md`
- O que foi testado:
  - listagem completa de arquivos com tamanho em bytes
  - busca negativa por extensoes proibidas ou indevidas para o repositório (`.db`, `.sqlite`, `.mp4`, `.mov`, `.avi`, `.mkv`, `.env`, `.pyc`, `.zip`, `.tar`, `.gz`, `.bin`)
  - busca por referencias residuais a `*2` no corpus
  - `git status --short`
- Comandos executados:
```bash
find beach_handball_ai -type f -printf '%P\t%s bytes\n' | sort
find beach_handball_ai -type f | rg '\.(db|sqlite|sqlite3|mp4|mov|avi|mkv|env|pyc|zip|tar|gz|bin)$' -n || true
rg -n "cepraea2|playbook_cepraea2|glossario_tecnico_cepraea2|criterios_taticos_cepraea2" beach_handball_ai docs -S
git status --short
```
- Resultado observado:
```text
nenhum arquivo proibido encontrado em beach_handball_ai/
restante do corpus composto por fontes PDF oficiais, registro tabular, markdowns processados, schema documental e plano
referencias a `*2` restaram apenas no historico de docs/IMPLEMENTATION_PROGRESS.md
git status --short mostrou apenas itens documentais de beach_handball_ai/ ainda nao rastreados
```
- O que ainda nao esta pronto:
  - o versionamento do corpus nao libera RAG nem substitui validacao humana G5
  - os markdowns de `05_processado/` continuam derivados de apoio, nao fontes normativas primarias
- Limitacoes, gaps e riscos:
  - este ciclo decide apenas sobre versionamento seguro do corpus; nao revalida o merito tecnico individual de cada PDF ou markdown
  - o corpus inclui binarios documentais legitimos (`.pdf` e `.xlsx`), o que aumenta o peso do repositório mas foi considerado aceitavel por serem fontes de trabalho do projeto
