# Auditoria do Fluxo de Implementação do MVP — ScoutPraia

Data: `2026-06-06`

Objetivo: avaliar se `docs/MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md`, `docs/IMPLEMENTATION_STEPS_AI.md` e `docs/IMPLEMENTATION_PROGRESS.md` formam um fluxo correto para o agente implementar o MVP sem desviar da arquitetura definida.

## Veredito

O fluxo está correto para um agente implementar o MVP, com uma ressalva operacional: a ordem de execução válida para o agente é a de `docs/IMPLEMENTATION_STEPS_AI.md`, não o roadmap resumido do MVP isoladamente.

Motivo:

- `docs/MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md` define produto, arquitetura, entidades, fluxo operacional e critérios de sucesso.
- `docs/IMPLEMENTATION_STEPS_AI.md` transforma o MVP em gates técnicos sequenciais e verificáveis.
- `docs/IMPLEMENTATION_PROGRESS.md` registra o que já foi provado e o que segue parcial.
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

Comprovado por teste ou script:

- estrutura base do projeto
- configuração, paths e SQLite
- modelos SQLModel principais
- seed idempotente da taxonomia `ScoutPraia v0.1`
- cadastro básico de adversária, atleta e jogo com metadados de vídeo
- associação de roster ao jogo
- CRUD de eventos no serviço
- validação de taxonomia, zona e `points_value`
- geração real de clipe com `ffmpeg` sobre vídeo sintético
- extração de metadados com `ffprobe`
- higiene de repositório

Ainda não comprovado como MVP:

- tela de marcação operacional com `st.video`, histórico, edição e exclusão
- dashboard real com KPIs
- analytics completo coletivo, individual e adversária
- relatório HTML salvo com registro `Report`
- validação operacional com jogo real completo
- comparação intra/interobservador persistida em `CodingAgreement`
- verificação visual do Streamlit
- README final de operação do MVP completo

## Ponto de atenção

`docs/MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md` traz um roadmap de produto em fases operacionais. `docs/IMPLEMENTATION_STEPS_AI.md` traz a ordem técnica para agentes.

Essas duas ordens não são idênticas, mas não conflitam:

- o roadmap do MVP descreve a progressão funcional desejada
- o plano da IA prioriza serviços internos testáveis antes de UI completa

Para agentes, a ordem correta é:

1. seguir `docs/IMPLEMENTATION_STEPS_AI.md`
2. conferir o escopo contra `docs/MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md`
3. atualizar `docs/IMPLEMENTATION_PROGRESS.md`
4. rodar `scripts/verify_current_state.sh`
5. não avançar se o gate falhar

## Próxima fase correta

Como `event_service.py` e `clip_service.py` já têm prova automatizada, a próxima ação técnica correta é:

1. completar `validation_service.py`
2. persistir `CodingAgreement`
3. testar divergência artificial por evento, atleta, zona e pontos
4. só depois avançar para analytics, relatórios e UI completa

## Conclusão

O fluxo documental é adequado para orientar um agente. Ele impõe escopo local, sequência por gates, prova reproduzível e registro de pendências. O MVP técnico é coerente com o objetivo do ScoutPraia.

O MVP ainda não deve ser declarado completo. O estado atual autoriza continuar a implementação pela Fase 6.4 do plano da IA: `validation_service.py`.
