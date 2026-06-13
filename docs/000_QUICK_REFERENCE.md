---
doc_id: QUICK_REF_000
title: "Referência Rápida — ScoutPraia"
status: canonical
category: PLAN
authority_level: 5
owner: Davi Sermenho
created_at: "2026-06-13"
last_updated: "2026-06-13"
repository: Davisermenho/scoutpraia
blocking_policy: "Leia este documento ANTES de qualquer outro. É o ponto de entrada obrigatório do agente."
---

# Referência Rápida — ScoutPraia

## Resumo Executivo

Este documento é o ponto de entrada do agente. Leia-o inteiro antes de qualquer ação. Contém a hierarquia de autoridade, status atual dos módulos, gates ativos e ponteiros para os documentos corretos.

## Objetivo

Reduzir o budget de tokens da leitura obrigatória inicial de ~40.000 tokens para ~800 tokens.

---

## 1. Hierarquia de Autoridade

Quando documentos conflitam, o de maior authority_level vence:

```
001_PLAN_Plano_Mestre_Agente.md   (authority 5) ← leia PRIMEIRO
005_CONT_Operacional_Eventos_v1.md (authority 5)
011_UX_Contrato_Interface.md      (authority 5)
002_SPEC_MVP_Tecnico.md           (authority 5)
AGENTS.md                          (authority 5)
003_PLAN_Passos_Implementacao_IA.md (authority 4)
004_PROG_Progresso_Implementacao.md (authority 4)
007_PROT_Protocolo_Validacao.md   (authority 4)
```

---

## 2. Status dos Módulos v1

Fonte: `docs/SCOUT_DESIGN_TEMPLATE.xlsx` aba `MODULE_INDEX` + `docs/005_CONT_Operacional_Eventos_v1.md`

| Módulo | import_rule_v1 | module_contract_status | ui_status |
|--------|---------------|------------------------|-----------|
| `attack_no_shot_v1` | `importar_v1` ✓ ÚNICO ATIVO | contrato_validado | liberada_conforme_app |
| `finalization_v1` | `nao_importar_v1` ✗ | contrato_validado | nao_liberada |
| `offensive_creation_v1` | `nao_importar_v1` ✗ | contrato_validado | nao_liberada |
| `defensive_v1` | `nao_importar_v1` ✗ | contrato_validado | nao_liberada |
| `shootout_v1` | `nao_importar_v1` ✗ | arquitetura_em_definicao | nao_liberada |
| `goalkeeper_v1` | `nao_importar_v1` ✗ | arquitetura_em_definicao | nao_liberada |
| `transition_v1` | `nao_importar_v1` ✗ | arquitetura_em_definicao | nao_liberada |

---

## 3. Estado Atual do Repositório

```
MVP: COMPLETO — G5 FECHADO em 2026-06-12
Testes: 320 passed
Fase atual: ativação progressiva dos módulos v1 (único ativo: attack_no_shot_v1)
Artefato primário: docs/SCOUT_DESIGN_TEMPLATE.xlsx (62 abas — MODULE_INDEX + SHEET_MAP são entradas obrigatórias)
```

---

## 4. Gates Ativos

- `verify_current_state.sh` deve passar verde antes de qualquer declaração de sucesso
- `python3 -m pytest -q` deve mostrar 311+ passed
- `PYTHONPATH=. python3 scripts/audit_docs_contract_alignment.py` deve passar sem errors

---

## 5. Mapa de Documentos por doc_id

| doc_id | Arquivo | Leia quando |
|--------|---------|-------------|
| PLAN_001 | `docs/001_PLAN_Plano_Mestre_Agente.md` | Antes de qualquer implementação |
| SPEC_002 | `docs/002_SPEC_MVP_Tecnico.md` | Para entender escopo e proibições |
| PLAN_003 | `docs/003_PLAN_Passos_Implementacao_IA.md` | Para entender ordem de fases |
| PROG_004 | `docs/004_PROG_Progresso_Implementacao.md` | Para entender estado atual |
| CONT_005 | `docs/005_CONT_Operacional_Eventos_v1.md` | Para regras semânticas de eventos |
| TAX_006 | `docs/006_TAX_Dicionario_Taxonomia.md` | Para definições de taxonomia |
| PROT_007 | `docs/007_PROT_Protocolo_Validacao.md` | Para critérios de validação humana |
| AUDIT_008 | `docs/008_AUDIT_Matriz_Evidencias.md` | Para rastreabilidade de evidências |
| RAG_009 | `docs/009_RAG_Workflow_Fontes.md` | Para fluxo de fontes RAG (fase 2) |
| AUDIT_010 | `docs/010_AUDIT_Validacao_G5.md` | Para auditoria de G5 (histórico) |
| UX_011 | `docs/011_UX_Contrato_Interface.md` | Para regras de UI/UX da marcação |
| ARCH_012 | `docs/012_ARCH_Agent_View_Design.md` | Para visão do agente do design |
| ARCH_013 | `docs/013_ARCH_Readme.md` | Para arquitetura do template |
| PLAN_014 | `docs/014_PLAN_Eventos_v1.md` | Histórico — plano inicial de eventos |
| PROG_015 | `docs/015_PROG_Log_Implementacao.md` | Log histórico de implementação |
| RAG_016 | `docs/016_RAG_Plano_Organizacao_Fontes.md` | Para organização de fontes |
| AUDIT_017 | `docs/017_AUDIT_Fluxo_MVP_Agente.md` | Para auditoria do fluxo MVP |
| UX_018 | `docs/018_UX_Guia_Preenchimento.md` | Para guia de uso da marcação |
| FLOW_019 | `docs/019_FLOW_Manual_IA_Atacante_Defensor.md` | Para fluxo multi-agente |

---

## 6. Regras Invioláveis

1. Não declarar sucesso sem evidência reproduzível por comando.
2. Scripts MUTANTES requerem confirmação do operador antes de rodar.
3. Não fazer commit ou push sem pedido explícito de Davi.
4. `verify_current_state.sh` deve estar verde antes de qualquer declaração de conclusão.
5. Quando documentos conflitam: o de maior `authority_level` vence.
