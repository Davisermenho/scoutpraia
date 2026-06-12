# Scripts — ScoutPraia

## Como usar

Todos os scripts Python requerem `PYTHONPATH=.` a partir da raiz do repositório.
Scripts shell devem ser executados a partir da raiz.

---

## Scripts de auditoria (READ-ONLY — seguros para rodar a qualquer momento)

| Script | Propósito | Comando mínimo |
|--------|-----------|----------------|
| `audit_docs_contract_alignment.py` | Detecta drift semântico entre docs e contratos | `PYTHONPATH=. python3 scripts/audit_docs_contract_alignment.py` |
| `audit_scout_design_template.py` | Audita XLSX contra registry v1 | `PYTHONPATH=. python3 scripts/audit_scout_design_template.py docs/SCOUT_DESIGN_TEMPLATE.xlsx` |
| `audit_scout_design_template_full_extraction.py` | Valida chunks JSON/JSONL exportados | `PYTHONPATH=. python3 scripts/audit_scout_design_template_full_extraction.py --chunks docs/SCOUT_DESIGN_TEMPLATE_FULL_EXTRACTION.json --xlsx docs/SCOUT_DESIGN_TEMPLATE.xlsx --full-extraction` |

---

## Scripts de exportação/geração (MUTANTES — modificam arquivos)

| Script | Propósito | Artefato gerado | Comando mínimo |
|--------|-----------|-----------------|----------------|
| `export_scout_design_csv.py` | XLSX → CSV consolidado | `docs/SCOUT_DESIGN_CSV.csv` | `python3 scripts/export_scout_design_csv.py` |
| `export_scout_design_template_full_extraction.py` | XLSX → chunks JSON/JSONL para agentes/RAG | `docs/SCOUT_DESIGN_TEMPLATE_FULL_EXTRACTION.json` | `PYTHONPATH=. python3 scripts/export_scout_design_template_full_extraction.py --xlsx docs/SCOUT_DESIGN_TEMPLATE.xlsx --output docs/SCOUT_DESIGN_TEMPLATE_FULL_EXTRACTION.json --verify` |
| `gerar_template_scout.py` | Gera/regenera o XLSX do template do zero | `docs/SCOUT_DESIGN_TEMPLATE.xlsx` | `python3 scripts/gerar_template_scout.py` |
| `refresh_fontes_registry_and_processados.py` | Sincroniza registro RAG completo (CSV + XLSX + JSONL + Markdown) | `beach_handball_ai/fontes/` | `python3 scripts/refresh_fontes_registry_and_processados.py` |

---

## Scripts shell

| Script | Propósito | Comando |
|--------|-----------|---------|
| `verify_current_state.sh` | Gate obrigatório — valida estado do repositório | `bash scripts/verify_current_state.sh` |
| `run_scout.sh` | Sobe o app Streamlit localmente | `bash scripts/run_scout.sh` |
| `setup_venv.sh` | Cria venv quando ensurepip não está disponível | `bash scripts/setup_venv.sh` |

---

## Regras para agentes

1. **Scripts READ-ONLY** são seguros para rodar sem confirmação do operador.
2. **Scripts MUTANTES** requerem confirmação do operador antes de rodar.
3. `verify_current_state.sh` deve ser rodado após qualquer mudança relevante.
4. Nunca declarar trabalho concluído se `verify_current_state.sh` falhar.
5. Cada script declara seu `Modo:`, `Gate/trigger:` e `Artefatos produzidos:` na docstring — leia-os antes de rodar.
