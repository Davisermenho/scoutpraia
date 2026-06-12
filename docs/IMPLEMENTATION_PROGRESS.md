---
tipo: progresso_execução
status_geral: BASE_TÉCNICA_FUNCIONANDO
fase_atual: "Eventos v1 — points_policy_v1 criado; auditor docs x contratos criado; SCOUT_DESIGN_TEMPLATE auditável"
testes_passando: 249
event_definitions: 31
última_atualização: 2026-06-11
próxima_ação: "Validar localmente points_policy_v1 e audit_docs_contract_alignment; depois reconciliar evidence_matrix.md e taxonomy_dictionary.md"
gaps_abertos:
  - "G5 — validação humana com vídeo real e screenshots não executada"
  - "RAG/Chroma/embeddings seguem bloqueados até gate global"
  - "evidence_matrix.md e taxonomy_dictionary.md ainda precisam ser reconciliados com events_v1.py e points_policy_v1"
  - "Proteção/locked copy da planilha ainda dependem de ação no Drive/Sheets"
mvp_completo: false
---

# ScoutPraia — Progresso de Implementação e Evidência

Este arquivo registra o estado atual de implementação. Ele deve ser atualizado a cada ciclo.

**Regra:** uma etapa só pode ser marcada como `FUNCIONANDO` quando houver evidência
reproduzível por comando, teste ou arquivo verificável.

**Histórico de ciclos anteriores:** ver `docs/IMPLEMENTATION_LOG.md` quando existir.

---

## Sumário executivo

**Status geral:** `BASE TÉCNICA FUNCIONANDO — MVP INCOMPLETO`

**Gate atual do repositório:**

```bash
python3 -m pytest tests/test_points_policy_v1.py -q
python3 -m pytest tests/test_docs_contract_alignment_audit.py -q
PYTHONPATH=. python3 scripts/audit_docs_contract_alignment.py
python3 -m pytest tests/test_transition_contract.py -q
python3 -m pytest tests/test_events_v1_contract_registry.py -q
python3 -m pytest -q
scripts/verify_current_state.sh
git diff --check
git status --short
# resultado esperado após pull: 249+ passed
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

Esses arquivos não alteram seed, UI ou importação. Eles centralizam a derivação de pontos e criam um mecanismo para impedir que documentos antigos reativem códigos legados ou regras incompatíveis.

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

## Próximo controle de causa raiz

Depois de validar os novos auditores, reconciliar:

```text
docs/taxonomy_dictionary.md
docs/evidence_matrix.md
```

Objetivo: remover drift conceitual entre taxonomia legada, matriz de evidência e contratos atuais (`events_v1.py`, `points_policy_v1.py`, `SCOUT_DESIGN_TEMPLATE.xlsx`).

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
| 8 — Testes | `FUNCIONANDO` | 249 passed antes dos novos auditores; validar novamente após pull |
| 9 — Validação operacional com vídeo real | `PARCIAL` | prova automatizada feita; G5 humano pendente |
| 10 — README e operação local | `FUNCIONANDO` | README + scripts documentados |
| Eventos v1 (contrato, serviços, modelo, UI, KPIs) | `IMPLEMENTADO COM EVIDÊNCIA PARCIAL` | contratos conceituais; importação segue bloqueada onde aplicável |
| Points policy v1 | `CRIADO — AGUARDA VALIDAÇÃO LOCAL` | `tests/test_points_policy_v1.py` |
| Auditor docs x contratos | `CRIADO — AGUARDA VALIDAÇÃO LOCAL` | `tests/test_docs_contract_alignment_audit.py` |

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

- 31 definições de eventos.
- Seed idempotente em `scoutpraia/services/taxonomy_service.py`.
- Status global da taxonomia: `draft`.
