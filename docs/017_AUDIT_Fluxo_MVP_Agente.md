---
doc_id: AUDIT_017
title: "Auditoria do Fluxo MVP do Agente"
status: active
version: "1.0.0"
authority_level: 3
category: AUDIT
owner: Davi Sermenho
created_at: "2026-06-06"
last_updated: "2026-06-13"
repository: Davisermenho/scoutpraia
tipo: auditoria_fluxo_agente
data_auditoria: 2026-06-06
ordem_execução_para_agente: "003_PLAN_Passos_Implementacao_IA.md — não MVP_TECNICO isolado"
próxima_ação: "G5 — validação humana; depois decidir import_rule_v1"
nota: "Auditoria de 2026-06-06; estado atual tem 110 testes e Eventos v1 implementados"
---

# Auditoria do Fluxo de Implementação do MVP — ScoutPraia

## Resumo Executivo

Auditoria de 2026-06-06 que verificou se os três documentos principais (`002`, `003`, `004`) formam um fluxo correto para implementação do MVP. Veredito: fluxo correto, com ordem obrigatória via `003_PLAN`.

## Objetivo

Avaliar a consistência e completude do trio de documentos de implementação, identificar gaps operacionais e definir a ordem correta de execução para agentes de IA.

## INSTRUÇÕES PARA AGENTES

**Ordem de leitura obrigatória:**
1. `docs/003_PLAN_Passos_Implementacao_IA.md` — contrato de execução com gates sequenciais
2. `docs/002_SPEC_MVP_Tecnico.md` — escopo e arquitetura do produto
3. `docs/004_PROG_Progresso_Implementacao.md` — estado atual provado

**Gate antes de avançar:** `scripts/verify_current_state.sh`

**Fase atual:** G5 — validação humana (ver `docs/007_PROT_Protocolo_Validacao.md`)

---

Data: `2026-06-06`

Objetivo: avaliar se `docs/002_SPEC_MVP_Tecnico.md`, `docs/003_PLAN_Passos_Implementacao_IA.md` e `docs/004_PROG_Progresso_Implementacao.md` formam um fluxo correto para o agente implementar o MVP sem desviar da arquitetura definida.

## Veredito

O fluxo está correto para um agente implementar o MVP, com uma ressalva operacional: a ordem de execução válida para o agente é a de `docs/003_PLAN_Passos_Implementacao_IA.md`, não o roadmap resumido do MVP isoladamente.

Motivo:

- `docs/002_SPEC_MVP_Tecnico.md` define produto, arquitetura, entidades, fluxo operacional e critérios de sucesso.
- `docs/003_PLAN_Passos_Implementacao_IA.md` transforma o MVP em gates técnicos sequenciais e verificáveis.
- `docs/004_PROG_Progresso_Implementacao.md` registra o que já foi provado e o que segue parcial.
- `scripts/verify_current_state.sh` fornece prova reproduzível mínima antes de avançar.

## Evidência executada

Comando:

```bash
scripts/verify_current_state.sh
```

Resultado observado:

```text
date_utc=2026-06-06T11:26:43Z
git_branch=main
git_head=e6f5e85
forbidden_tracked_files=none
collected 15 items
15 passed, 6 warnings
```

Checagens adicionais executadas:

```bash
git ls-files
rg -n -i "react|fastapi|postgres|postgresql|auth|authentication|jwt|deploy|docker|kubernetes" app.py scoutpraia tests requirements.txt README.md .env.example
```

Resultado:

- a árvore obrigatória do plano está presente
- `requirements.txt` contém somente dependências compatíveis com o MVP local
- não há React, FastAPI, PostgreSQL, autenticação, Docker ou deploy implementados no código
- menções a React, FastAPI, PostgreSQL e deploy aparecem no `README.md` como itens proibidos, não como implementação
- vídeos, banco local, clipes, relatórios gerados, `.env`, `.venv`, `tmp/` e binários locais não estão versionados

## Alinhamento entre MVP e plano da IA

| Item | MVP técnico | Plano da IA | Veredito |
| --- | --- | --- | --- |
| arquitetura | monólito local em Python, Streamlit, SQLite e FFmpeg | proíbe React, FastAPI, PostgreSQL, auth, API e deploy | correto |
| fluxo operacional | cadastrar jogo, vídeo, elenco, marcar eventos, gerar clipes, KPIs e relatórios | implementa por fases com serviços antes da UI completa | correto |
| dados | define modelos principais | exige SQLModel para modelos obrigatórios | correto |
| taxonomia | exige dicionário, versionamento e validação | exige seed v0.1 e sincronização com matriz/dicionário | correto |
| serviços | vídeo, evento, clipe, validação, analytics e relatório | separa gates por serviço | correto |
| UI | páginas Streamlit e tela crítica de marcação | vem após serviços internos no plano da IA | correto para agente |
| testes | precisa provar comportamento | define testes mínimos e fixture sintética | correto |
| validação real | 1 jogo completo e divergências | fase 9 exige validação operacional com vídeo real | correto |
| RAG | apenas depois do MVP funcional | plano bloqueia RAG antes do MVP | correto |

## Estado real do repositório

Para o estado atual completo com evidências, ver `docs/010_AUDIT_Validacao_G5.md` e `docs/004_PROG_Progresso_Implementacao.md`.

Resumo (2026-06-10): 110 testes passando; serviços, UI e relatórios implementados; G5 (validação humana) pendente.

## Ponto de atenção

`docs/002_SPEC_MVP_Tecnico.md` traz um roadmap de produto em fases operacionais. `docs/003_PLAN_Passos_Implementacao_IA.md` traz a ordem técnica para agentes.

Essas duas ordens não são idênticas, mas não conflitam:

- o roadmap do MVP descreve a progressão funcional desejada
- o plano da IA prioriza serviços internos testáveis antes de UI completa

Para agentes, a ordem correta com precondição explícita:

| Passo | Ação | Precondição |
| --- | --- | --- |
| 1 | Ler `docs/003_PLAN_Passos_Implementacao_IA.md` completo | sempre — antes de qualquer implementação |
| 2 | Conferir escopo em `docs/002_SPEC_MVP_Tecnico.md` | sempre |
| 3 | Ler `docs/004_PROG_Progresso_Implementacao.md` para estado atual | sempre |
| 4 | Rodar `scripts/verify_current_state.sh` | após qualquer mudança relevante |
| 5 | Atualizar `docs/004_PROG_Progresso_Implementacao.md` | após qualquer mudança |
| 6 | NÃO avançar se o gate falhar | invariante absoluta |

## Conclusão

O fluxo documental é adequado para orientar um agente. Ele impõe escopo local, sequência por gates, prova reproduzível e registro de pendências.

**Estado atual (2026-06-10):** 110 testes passando; Eventos v1 implementados; `import_rule_v1 = nao_importar_v1`; próxima ação: G5 (validação humana).
