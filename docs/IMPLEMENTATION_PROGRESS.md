---
tipo: progresso_execução
status_geral: BASE_TÉCNICA_FUNCIONANDO
fase_atual: "Eventos v1 — EV-011 de transition_v1 registrado; auditoria versionável do SCOUT_DESIGN_TEMPLATE criada"
testes_passando: 247
event_definitions: 31
última_atualização: 2026-06-11
próxima_ação: "Exportar SCOUT_DESIGN_TEMPLATE para XLSX e executar scripts/audit_scout_design_template.py; depois corrigir pendências apontadas na planilha"
gaps_abertos:
  - "Planilha ainda precisa passar no auditor XLSX"
  - "EVENTOS_LEGADOS_FUTUROS precisa existir na planilha ou ter decisão documentada equivalente"
  - "repo_symbol precisa estar nas abas exigidas ou centralização precisa ser formalizada"
  - "proteção/locked copy ainda dependem de ação no Drive/Sheets"
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
python3 -m pytest tests/test_transition_contract.py -q
python3 -m pytest tests/test_events_v1_contract_registry.py -q
python3 -m pytest -q
scripts/verify_current_state.sh
git diff --check
git status --short
```

**Última evidência informada pelo operador:**

```text
git_head=a7b8f97
transition_contract=15 passed
registry_contract=16 passed
pytest=247 passed
verify_current_state.sh=verde
taxonomy=ScoutPraia v0.1
taxonomy_status=draft
event_definitions=31
expected_event_definitions=31
git diff --check=sem saída
git status --short=limpo
```

**Estado após esta atualização no repositório:**

Foram adicionados arquivos versionáveis para fechar a parte do plano que depende do repo:

```text
scripts/audit_scout_design_template.py
tests/test_scout_design_template_audit.py
docs/ARCHITECTURE_README.md
```

Esses arquivos não alteram seed, UI ou importação. Eles criam a base de auditoria para validar o XLSX exportado da planilha contra `scoutpraia/contracts/events_v1.py`.

---

## Auditoria do SCOUT_DESIGN_TEMPLATE

Para validar a planilha exportada:

```bash
python3 scripts/audit_scout_design_template.py caminho/SCOUT_DESIGN_TEMPLATE.xlsx
```

O script deve falhar enquanto houver pendências como:

- ausência de `EVENTOS_LEGADOS_FUTUROS`;
- ausência de `repo_test_file` em `MODULE_INDEX`;
- ausência de `repo_symbol` em `EVENTOS`, `RESULTADOS_*` ou `CAMPOS_AUXILIARES_*`;
- código legado/futuro não bloqueado;
- matriz de validação incompleta;
- regra normalizada ausente.

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
