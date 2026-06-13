---
doc_id: DOCS_README
title: "Índice da Documentação — ScoutPraia"
status: canonical
category: PLAN
authority_level: 4
owner: Davi Sermenho
last_updated: "2026-06-13"
repository: Davisermenho/scoutpraia
---

# Documentação — ScoutPraia

## Ponto de entrada

**Leia [`000_QUICK_REFERENCE.md`](000_QUICK_REFERENCE.md) primeiro.** É o resumo executivo de 800 tokens com hierarquia, status dos módulos e mapa de documentos.

Para o índice estruturado em JSON (consulta programática): [`INDEX.json`](INDEX.json).

---

## Hierarquia de Autoridade

Quando documentos conflitam, o de maior `authority_level` vence.

| authority_level | Significado |
|-----------------|-------------|
| 5 | Fonte obrigatória de execução — nunca ignorar |
| 4 | Contrato operacional — bloqueia se violado |
| 3 | Referência ativa — consultar quando relevante |
| 2 | Histórico / suporte — consultar se necessário |
| 1 | Informativo / externo — não guia implementação |

---

## Ordem de Leitura para Agentes

### Leitura obrigatória antes de qualquer tarefa (~2k tokens)
| doc_id | Arquivo | Tokens est. |
|--------|---------|-------------|
| QUICK_REF_000 | [`000_QUICK_REFERENCE.md`](000_QUICK_REFERENCE.md) | ~800 |
| AGENTS_md | [`../AGENTS.md`](../AGENTS.md) | ~900 |

### Leitura obrigatória antes de implementação (~30k tokens adicionais)
| doc_id | Arquivo | Tokens est. | Propósito |
|--------|---------|-------------|-----------|
| PLAN_001 | [`001_PLAN_Plano_Mestre_Agente.md`](001_PLAN_Plano_Mestre_Agente.md) | ~10k | Ordem de execução, gates, dependências |
| SPEC_002 | [`002_SPEC_MVP_Tecnico.md`](002_SPEC_MVP_Tecnico.md) | ~5.3k | Escopo, proibições, requisitos |
| CONT_005 | [`005_CONT_Operacional_Eventos_v1.md`](005_CONT_Operacional_Eventos_v1.md) | ~21k | Regras semânticas e contratos de módulos |
| PROG_004 | [`004_PROG_Progresso_Implementacao.md`](004_PROG_Progresso_Implementacao.md) | ~3.1k | Estado atual e gates |

### Referência sob demanda
| doc_id | Arquivo | Tokens est. | Quando ler |
|--------|---------|-------------|-----------|
| PLAN_003 | [`003_PLAN_Passos_Implementacao_IA.md`](003_PLAN_Passos_Implementacao_IA.md) | ~6k | Para entender fases de implementação |
| TAX_006 | [`006_TAX_Dicionario_Taxonomia.md`](006_TAX_Dicionario_Taxonomia.md) | ~2.8k | Para definições de taxonomia |
| PROT_007 | [`007_PROT_Protocolo_Validacao.md`](007_PROT_Protocolo_Validacao.md) | ~5.6k | Para critérios de validação |
| AUDIT_008 | [`008_AUDIT_Matriz_Evidencias.md`](008_AUDIT_Matriz_Evidencias.md) | ~1.8k | Para rastreabilidade |
| UX_011 | [`011_UX_Contrato_Interface.md`](011_UX_Contrato_Interface.md) | ~7k | Para mudanças de UI |
| ARCH_012 | [`012_ARCH_Agent_View_Design.md`](012_ARCH_Agent_View_Design.md) | ~7.7k | Para visão do agente do design |
| UX_018 | [`018_UX_Guia_Preenchimento.md`](018_UX_Guia_Preenchimento.md) | ~3.9k | Para uso da tela de marcação |

### Histórico / não ler para execução
| doc_id | Arquivo | Motivo |
|--------|---------|--------|
| AUDIT_010 | [`010_AUDIT_Validacao_G5.md`](010_AUDIT_Validacao_G5.md) | Auditoria histórica de G5 |
| PLAN_014 | [`014_PLAN_Eventos_v1.md`](014_PLAN_Eventos_v1.md) | Plano inicial — supersedido por PLAN_001 |
| PROG_015 | [`015_PROG_Log_Implementacao.md`](015_PROG_Log_Implementacao.md) | Log histórico |
| RAG_009 | [`009_RAG_Workflow_Fontes.md`](009_RAG_Workflow_Fontes.md) | Bloqueado — Fase 2 |

### Pular para agentes
| Pasta | Motivo |
|-------|--------|
| `evidence/g5/` | Screenshots PNG — apenas para revisão humana |
| `sources/_deprecated/` | APIs e plataformas depreciadas |

---

## Artefato Central — SCOUT_DESIGN_TEMPLATE.xlsx

**Arquivo:** `docs/SCOUT_DESIGN_TEMPLATE.xlsx`
**Autoridade:** 5 (nível máximo — fonte primária de todos os contratos de módulo)

Este arquivo Excel é o **artefato de design mestre** do ScoutPraia. Contém 62 abas organizadas em camadas:

### Abas obrigatórias para agentes (entrar aqui primeiro)

| Aba | Tipo | Descrição |
|-----|------|-----------|
| `INSTRUÇÕES` | documentation | Frontmatter e metadados do artefato |
| `MODULE_INDEX` | architecture_index | Status de todos os 7 módulos v1: import_rule, ui_status, test_files |
| `SHEET_MAP` | architecture_index | Mapa das 62 abas — scope, módulo, tipo, dependências |
| `EVENTOS` | master_registry | Registro mestre de todos os eventos (não concentra todos os detalhes por módulo) |

### Abas de contratos globais

| Aba | Tipo |
|-----|------|
| `FIELD_RELATIONSHIPS` | governance_contract — relações entre campos e sheets |
| `CROSS_MODULE_BOUNDARIES` | cross_module_contract |
| `AI_USE_POLICY` | ai_governance |
| `FIELD_DICTIONARY_GLOBAL` | dicionário global de campos |
| `DECISION_PRECEDENCE` | precedência de decisão em conflitos |

### Estrutura por módulo v1

Cada módulo tem 3–4 abas próprias:
`CAMPOS_AUXILIARES_<MODULO>` + `RESULTADOS_<MODULO>` + `TESTES_<MODULO>` + `VERSIONAMENTO_<MODULO>`

| Módulo | import_rule_v1 | Abas próprias |
|--------|---------------|---------------|
| `attack_no_shot_v1` | `importar_v1` ✓ | CAMPOS_AUXILIARES_ATAQUE_SEM_FINALIZACAO + 4 |
| `finalization_v1` | `nao_importar_v1` | CAMPOS_AUXILIARES_FINALIZACAO + 4 |
| `offensive_creation_v1` | `nao_importar_v1` | CAMPOS_AUXILIARES_CRIACAO_OFENSIVA + 3 |
| `defensive_v1` | `nao_importar_v1` | CAMPOS_AUXILIARES_DEFENSIVO + 3 |
| `shootout_v1` | `nao_importar_v1` | CAMPOS_AUXILIARES_SHOOTOUT + 3 |
| `goalkeeper_v1` | `nao_importar_v1` | CAMPOS_AUXILIARES_GOLEIRA + 3 |
| `transition_v1` | `nao_importar_v1` | CAMPOS_AUXILIARES_TRANSICAO + 2 |

**Convenção de leitura:** `header_row=7; data_start_row=8` em todas as abas. Linhas 1–6 são frontmatter.

---

## Fontes externas (`sources/`)
| doc_id | Arquivo | Propósito |
|--------|---------|-----------|
| REF_S00 | [`sources/README.md`](sources/README.md) | Índice de fontes |
| REF_S01 | [`sources/REF_S01_Regras_Oficiais_IHF_2026.md`](sources/REF_S01_Regras_Oficiais_IHF_2026.md) | Regras IHF derivadas |
| REF_S02 | [`sources/REF_S02_Fontes_Fortes_Handebol.md`](sources/REF_S02_Fontes_Fortes_Handebol.md) | Curadoria de fontes |
