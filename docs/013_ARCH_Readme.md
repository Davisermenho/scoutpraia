---
doc_id: ARCH_013
title: "Architecture README"
status: active
version: "1.0.0"
authority_level: 2
category: ARCH
owner: Davi Sermenho
created_at: "2026-06-01"
last_updated: "2026-06-13"
repository: Davisermenho/scoutpraia
---

# SCOUT_DESIGN_TEMPLATE — Architecture README

## Resumo Executivo

Este documento registra a função arquitetural do `SCOUT_DESIGN_TEMPLATE` e separa o que é contrato, o que é dado observacional e o que precisa de auditoria automática.

## Objetivo

Definir as regras de governança da planilha `SCOUT_DESIGN_TEMPLATE`, incluindo abas obrigatórias, política de importação/UI e critério de implementação completa.

Este documento registra a funcao arquitetural do `SCOUT_DESIGN_TEMPLATE` e separa o que e contrato, o que e dado observacional e o que precisa de auditoria automatica.

## Regra central

O `SCOUT_DESIGN_TEMPLATE` e contrato de arquitetura e governanca do scout. Ele nao e banco oficial de lances, nao deve receber dados de jogo por atleta, rodada, treino ou competicao, e nao libera UI/importacao por si so.

## Fontes de verdade

1. `scoutpraia/contracts/events_v1.py` e o registry executavel dos contratos v1.
2. `docs/005_CONT_Operacional_Eventos_v1.md` e o registro historico das decisoes, evidencias EV e bloqueios.
3. `SCOUT_DESIGN_TEMPLATE` e a visao humana/operacional do contrato.
4. `pytest` e `scripts/verify_current_state.sh` sao a evidencia executavel.

## Abas de governanca da planilha

- `MODULE_INDEX`: indice mestre dos modulos, eventos principais, status, importacao, UI e politica de IA.
- `SHEET_MAP`: mapa das abas, seus tipos, donos, dependencias e funcao.
- `VALIDATION_MATRIX`: matriz de validacao ligando modulos, testes, evidencias, git_head, UI, importacao e seed.
- `SOURCE_REGISTER`: registro de fontes fortes, internas e executaveis.
- `AI_USE_POLICY`: politica do que a IA pode sugerir, importar, revisar ou bloquear.
- `CROSS_MODULE_BOUNDARIES`: fronteiras entre modulos para evitar dupla contagem e mistura de conceitos.
- `LEGACY_MIGRATION_RULES`: regras de migracao, contexto ou bloqueio para codigos antigos/futuros.

## Abas de contrato por modulo

As abas `CAMPOS_AUXILIARES_*`, `RESULTADOS_*`, `TESTES_*` e `VERSIONAMENTO_*` sao metadados/contrato do modulo. Elas nao devem receber lances observados de jogos.

## Abas normalizadas para auditoria

- `EVENT_REQUIRED_FIELDS`
- `EVENT_OPTIONAL_FIELDS`
- `EVENT_FORBIDDEN_FIELDS`
- `EVENT_BLOCKING_RULES`

Essas abas existem para transformar regras longas separadas por ponto-e-virgula em linhas auditaveis por script. Enquanto a normalizacao nao cobrir 100% das regras, a aba `EVENTOS` permanece como visao humana, e as abas normalizadas funcionam como camada de auditoria incremental.

## Convencao de nomes

1. Abas globais usam nomes explicitos em ingles tecnico, como `MODULE_INDEX`, `SHEET_MAP`, `SOURCE_REGISTER` e `VALIDATION_MATRIX`.
2. Abas especificas de modulo devem seguir uma das formas:
   - `CAMPOS_AUXILIARES_<MODULO>`
   - `RESULTADOS_<MODULO>`
   - `TESTES_<MODULO>`
   - `VERSIONAMENTO_<MODULO>`
3. Abas de dominio global podem usar nomes curtos, como `POSIÇÕES`, `ZONAS_QUADRA`, `ZONAS_GOL` e `SISTEMAS`.

## Politica de importacao/UI

Nenhum modulo com `import_rule_v1=nao_importar_v1` pode ser exposto na UI ou importado sem:

1. teste especifico no repositorio;
2. `python3 -m pytest -q` verde;
3. `scripts/verify_current_state.sh` verde;
4. evidencia EV registrada no Contrato Operacional;
5. alteracao explicita do contrato de importacao/UI.

## Auditoria automatica

Para auditar um XLSX exportado da planilha contra o registry v1:

```bash
python3 scripts/audit_scout_design_template.py caminho/SCOUT_DESIGN_TEMPLATE.xlsx
```

O script retorna codigo 1 quando encontra pendencias bloqueantes, como:

- aba obrigatoria ausente;
- coluna critica ausente;
- evento primario do registry ausente em `EVENTOS`;
- codigo legado sem bloqueio;
- `repo_symbol` ausente em abas que precisam comparar com o repo;
- matriz de validacao sem evidencias esperadas.

## Criterio para considerar o plano totalmente implementado

O plano so deve ser considerado 100% implementado quando:

1. a planilha contiver todas as abas obrigatorias;
2. `MODULE_INDEX` contiver `repo_test_file`;
3. `EVENTOS`, `RESULTADOS_*` e `CAMPOS_AUXILIARES_*` contiverem `repo_symbol` quando forem fontes de contrato;
4. existir `EVENTOS_LEGADOS_FUTUROS` ou decisao documentada equivalente;
5. as regras normalizadas cobrirem 100% dos campos criticos ou houver excecao documentada;
6. o script `scripts/audit_scout_design_template.py` passar contra o XLSX exportado;
7. houver versao travada/backup do template antes de novas mudancas estruturais.
