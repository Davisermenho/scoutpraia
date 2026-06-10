---
tipo: progresso_execução
status_geral: BASE_TÉCNICA_FUNCIONANDO
fase_atual: "Eventos v1 — passo 6A concluído; curadoria opponents/relatórios ajustada"
testes_passando: 110
event_definitions: 31
última_atualização: 2026-06-10
próxima_ação: "commit do escopo opponents/relatórios, depois G5 (validação humana)"
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
# resultado esperado: 110 passed
```

**Commits pendentes no workspace:**
- `scoutpraia/pages/opponents.py` — métrica de especialista na página Adversárias
- `tests/test_report_service.py` — cobertura de relatório de adversária com especialista
- `tests/test_streamlit_pages.py` — prova da métrica na página Adversárias
- `scripts/gerar_template_scout.py` — utilitário isolado fora da trilha de produto

**Próxima ação autorizada:**
1. Fazer commit do escopo `opponents/relatórios` curado
2. Executar G5: validação humana com vídeo real (ver `docs/validation_protocol.md`)
3. Decidir liberação da importação v1 (`import_rule_v1`)

---

## Prova reproduzível

```bash
scripts/verify_current_state.sh
```

Verifica: higiene do repo, import do pacote, banco SQLite, seed da taxonomia,
contagem de event_definitions, testes automatizados, `git diff --check`.

**Última execução registrada:**

```text
date_utc=2026-06-10
taxonomy=ScoutPraia v0.1
taxonomy_status=draft
event_definitions=31
expected_event_definitions=31
110 passed
```

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
| 8 — Testes | `FUNCIONANDO` | 110 passed |
| 9 — Validação operacional com vídeo real | `PARCIAL` | prova automatizada feita; G5 humano pendente |
| 10 — README e operação local | `FUNCIONANDO` | README + scripts documentados |
| Eventos v1 (contrato, serviços, modelo, UI, KPIs) | `IMPLEMENTADO COM EVIDÊNCIA` | passos 1–6A concluídos; importação bloqueada |

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

110 testes passando. Suíte inclui:
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
| 2 — Serviço Finalização | `finalization_contract_service.py` | CONCLUÍDO |
| 3 — Serviço Ataque sem finalização | `no_shot_attack_contract_service.py` | CONCLUÍDO |
| 4 — Modelo/banco | campos v1 em `event.py` + migração leve | CONCLUÍDO |
| 5 — UI de marcação | blocos v1 em `tagging.py` | CONCLUÍDO |
| 6 — Relatórios/KPIs | métricas v1 em `analytics_service.py` + templates | CONCLUÍDO |
| 6A — Correção KPIs | especialista + 2 pontos adversária | CONCLUÍDO |

Importação bloqueada: `import_rule_v1 = nao_importar_v1`

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

1. Fazer commit do escopo `opponents/relatórios` curado (já testado)
2. Executar `scripts/verify_current_state.sh` após o commit
3. Executar protocolo G5 de validação humana (`docs/validation_protocol.md`)
4. Depois de G5: decidir liberação de `import_rule_v1`

---

## Governança de agentes

Status: `CONFIGURADO`

- `AGENTS.md` com regras obrigatórias para agentes neste repositório.
- Exigência de prova reproduzível antes de declarar sucesso.
- Exigência de atualização deste arquivo em cada ciclo.
- Proibição explícita de pular fases ou esconder trabalho parcial.
- Restrições de escopo: sem React, FastAPI, PostgreSQL, API pública, auth, deploy, RAG antes do MVP funcional.

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
