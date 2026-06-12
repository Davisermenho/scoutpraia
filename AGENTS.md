# AGENTS.md — ScoutPraia

Estas instruções são obrigatórias para qualquer agente trabalhando neste repositório.

## Regra central

Não declarar trabalho como concluído sem prova reproduzível. Toda afirmação de implementação deve ser sustentada por arquivo, teste, comando executado ou evidência registrada.

## Arquivos de contrato

Antes de implementar qualquer coisa, leia:

- `docs/MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md`
- `docs/IMPLEMENTATION_STEPS_AI.md`
- `docs/IMPLEMENTATION_PROGRESS.md`
- `docs/sources/README.md`
- `docs/evidence_matrix.md`
- `docs/taxonomy_dictionary.md`
- `docs/validation_protocol.md`
- `docs/rag_workflow.md`
- `docs/AUDIT_EVIDENCE_VALIDATION.md`

Se algum desses arquivos não existir, registre a ausência em `docs/IMPLEMENTATION_PROGRESS.md` antes de prosseguir.

## Ordem de execução

Siga a ordem definida em `docs/IMPLEMENTATION_STEPS_AI.md`. Não pule fases.

Para cada ciclo de trabalho:

1. declarar a fase atual
2. implementar somente o escopo dessa fase
3. adicionar ou atualizar testes
4. rodar prova reproduzível
5. atualizar `docs/IMPLEMENTATION_PROGRESS.md`
6. registrar pendências reais sem suavizar

## Prova obrigatória

Após qualquer mudança relevante, rode:

```bash
scripts/verify_current_state.sh
```

Se o script falhar:

- não declarar sucesso
- explicar exatamente qual checagem falhou
- corrigir a causa raiz ou registrar o bloqueio

Também rode comandos específicos quando a mudança exigir, por exemplo:

- `python3 -m pytest`
- `python3 -m scoutpraia.core.database`
- `git diff --check`
- testes específicos do serviço alterado

## Registro de progresso

Atualize `docs/IMPLEMENTATION_PROGRESS.md` em toda entrega.

O registro deve conter:

- o que foi implementado
- o que foi testado
- comando executado
- resultado observado
- o que ainda não está pronto
- limitações, gaps e riscos

Não use termos como “funcionando”, “completo” ou “validado” sem evidência no próprio arquivo de progresso.

## Escopo técnico do MVP

O ScoutPraia é um monólito local em Python.

Não implementar no MVP:

- React
- FastAPI
- API pública
- PostgreSQL
- autenticação
- multiusuário
- deploy
- automação visual avançada antes do fluxo manual funcionar
- RAG antes do MVP funcional

Stack prevista:

- Python
- Streamlit
- SQLite
- SQLModel ou `sqlite3`
- Pandas
- FFmpeg/ffprobe
- Jinja2
- Plotly
- pytest

## Evidência, fontes e taxonomia

Toda decisão de taxonomia, KPI ou regra de scout deve respeitar:

- regra oficial quando aplicável
- matriz de evidência
- dicionário operacional
- validação em vídeo quando for campo crítico

Não transformar hipótese prática em KPI final.

Não alterar taxonomia aprovada silenciosamente; criar nova versão.

## Honestidade sobre estado parcial

Se uma funcionalidade está parcial, diga `PARCIAL`.

Exemplos:

- placeholder de UI não é tela funcional
- função que calcula janela de clipe não é geração real de clipe
- seed de taxonomia não é validação da taxonomia
- smoke test não é teste operacional completo
- relatório template não é relatório final validado

## Git

Não fazer commit ou push sem pedido explícito do usuário.

Antes de commit:

- rodar `scripts/verify_current_state.sh`
- rodar `git status --short`
- garantir que vídeos, banco, clipes, relatórios gerados, `.env`, `.venv`, `tmp/` e binários locais não entram no Git

## Ambiente

Use `python3` como comando padrão.

Se `.venv` não puder ser criado por falta de `python3-venv` ou `ensurepip`, registre isso em `docs/IMPLEMENTATION_PROGRESS.md`. Não ocultar instalação feita fora da `.venv`.

## Critério de MVP completo

O MVP só pode ser chamado de completo quando todos os critérios em `docs/IMPLEMENTATION_STEPS_AI.md` e `docs/IMPLEMENTATION_PROGRESS.md` estiverem satisfeitos e provados por comando.

## Scripts disponíveis

Ver [`scripts/README.md`](scripts/README.md) para o índice completo de scripts, seus modos (read-only vs. mutante), gates de uso e exemplos de comando.
