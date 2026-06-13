---
doc_id: AUDIT_010
title: "Auditoria de Evidências e Validação G5"
status: active
version: "1.0.0"
authority_level: 3
category: AUDIT
owner: Davi Sermenho
created_at: "2026-06-06"
last_updated: "2026-06-13"
repository: Davisermenho/scoutpraia
tipo: auditoria_evidência
data_auditoria: 2026-06-06
data_atualização_g5: 2026-06-12
status_base_técnica: FUNCIONANDO_COM_EVIDÊNCIA
mvp_completo: true
testes_no_momento_da_auditoria: 10
testes_atuais: 311
gaps_abertos: []
G5_status: FECHADO
próxima_ação: "Ativação progressiva dos módulos v1 — começar por finalization_v1"
nota: "Auditoria base de 2026-06-06. G5 fechado em 2026-06-12 por Davi Sermenho — 12 eventos marcados, 16 relatórios, 311 testes passando. Ver docs/007_PROT_Protocolo_Validacao.md e docs/evidence_g5/."
---

# Auditoria de Evidências e Validação — ScoutPraia

## Resumo Executivo

Auditoria do estado técnico do ScoutPraia (base em 2026-06-06, G5 fechado em 2026-06-12). MVP declarado completo: 311 testes passando, 12 eventos marcados em vídeo real, 16 relatórios gerados.

## Objetivo

Registrar as evidências de funcionamento do ScoutPraia e o fechamento formal do gate G5 (validação humana), autorizando a ativação progressiva dos módulos v1.

## ATUALIZAÇÃO G5 — 2026-06-12

> **G5 FECHADO — APROVADO.** MVP declarado completo por Davi Sermenho em 2026-06-12.
> 12 eventos marcados, 16 relatórios gerados, 311 testes passando.
> Evidências visuais Playwright em `docs/evidence_g5/`. Ver `docs/007_PROT_Protocolo_Validacao.md`.

O texto abaixo é a auditoria original de 2026-06-06 e reflete o estado **antes** do fechamento de G5. Mantido como registro histórico.

---

## VEREDITO RÁPIDO PARA AGENTES

**AUTORIZADO declarar:**
- MVP do ScoutPraia está implementado e validado humanamente (`mvp_completo: true`)
- base técnica implementada e funcionando
- banco, taxonomia, seed, metadados de vídeo e testes automatizados provados
- serviços internos (evento, clipe, validação, analytics, relatório) funcionam — 311 testes passando
- UI Streamlit validada humanamente com screenshots Playwright (`docs/evidence_g5/`)

**NÃO AUTORIZADO declarar:**
- taxonomia v0.1 aprovada para KPI final estável (segue `draft`; v1 endereça)

**Gate atual:** ativação progressiva dos módulos v1 — começar por `finalization_v1`

---

Data: `2026-06-06`

Objetivo: verificar se as provas geradas por `scripts/verify_current_state.sh` e pelos testes automatizados sustentam corretamente as afirmações de implementação do ScoutPraia.

## Veredito executivo

As provas atuais garantem que a base técnica implementada está funcionando dentro do escopo testado:

- contrato documental mínimo corrigido
- pacote Python importável
- banco SQLite inicializável
- seed idempotente da taxonomia `ScoutPraia v0.1`
- extração de metadados por `ffprobe`
- persistência de metadados de vídeo em `Match`
- integração com vídeo real local em `storage/videos/`, quando presente
- ausência de diretório legado `Videos-Jogos/`
- ausência de arquivos gerados/proibidos versionados
- ausência de problemas de whitespace no diff

As provas atuais não garantem MVP completo. Elas não provam marcação operacional de eventos, geração real de clipes, analytics completo, relatórios finais, validação observacional da taxonomia, confiabilidade intra/interobservador ou verificação visual completa da UI Streamlit.

## Fontes usadas na auditoria

| Fonte | Código | Uso na auditoria |
| --- | --- | --- |
| pytest | — | `assert` verifica expectativas; `tmp_path` isola banco de teste |
| Python `subprocess` | — | `check=True` falha em código de saída diferente de zero |
| ffprobe | — | `-show_format`, `-show_streams` e saída JSON para metadados |
| SQLModel | — | modelos `table=True`, SQLite URL, `create_all(engine)` |
| Streamlit `st.video` | — | aceita caminho local de vídeo; não prova UI sem execução visual |
| Observational Measurement / IRR | `SRC-OBS-MEASUREMENT` | scout observacional exige confiabilidade por codificação |

Links de referência completos: ver `docs/sources/README.md` para todos os `SRC-*`.

## Prova executada

Comando:

```bash
scripts/verify_current_state.sh
```

Resultado observado:

```text
== ScoutPraia current-state verification ==
date_utc=2026-06-06T07:45:56Z
cwd=/home/davis/SCOUT
git_branch=main
git_head=13914ea

== Repository hygiene checks ==
canonical_video_dir=storage/videos
legacy_video_dir_absent=Videos-Jogos
forbidden_tracked_files=none

== Required MVP doc checks ==
match_roster_player_id_count=1
kpi_13_1_title_count=1

== Python import ==
ScoutPraia local beach handball scouting app.

== Database init and taxonomy seed ==
Banco inicializado em data/scoutpraia.db
taxonomy=ScoutPraia v0.1
taxonomy_status=draft
event_definitions=29
expected_event_definitions=29

== Tests ==
collected 10 items
tests/test_match_service.py .                                            [ 10%]
tests/test_real_video_integration.py ..                                  [ 30%]
tests/test_smoke.py .......                                              [100%]
10 passed

== Git whitespace check ==
sem erros
```

## Validação do script de prova

| Checagem | Critério | O que prova | Veredito |
| --- | --- | --- | --- |
| diretório canônico | `storage/videos` existe e tem `.gitkeep` | local correto de vídeo conforme MVP | correto |
| legado removido | `Videos-Jogos/` não existe e não há path versionado nesse diretório | legado não continua como fonte operacional | correto |
| arquivos proibidos | `git ls-files` não contém mídia, banco, `.env`, `.venv`, `tmp/`, `bin/` ou gerados | dados locais não estão versionados | correto |
| doc MVP | `player_id` em `match_roster` aparece 1 vez | correção obrigatória do contrato foi aplicada | correto |
| doc MVP | `## 13.1 KPIs coletivos` aparece 1 vez | título duplicado foi corrigido | correto |
| import | `python3 -c "import scoutpraia"` passa | pacote está importável | correto |
| banco | `python3 -m scoutpraia.core.database` passa | banco e seed inicial executam sem erro fatal | correto |
| taxonomia | número persistido igual a `len(EVENT_DEFINITIONS)` | seed cadastra todas as definições previstas no código | correto |
| pytest | `python3 -m pytest` passa | testes automatizados cobertos estão verdes | correto |
| whitespace | `git diff --check` passa | diff não tem erro básico de whitespace | correto |

Limite: o script é um gate de estado atual. Ele prova condições técnicas objetivas, mas não prova sozinho comportamento não coberto por testes.

## Validação dos testes

### `tests/test_smoke.py`

| Teste | O que prova | Critério está correto? | Limite |
| --- | --- | --- | --- |
| `test_package_imports` | pacote importável e docstring esperada | sim | não testa app Streamlit |
| `test_database_initializes` | banco local é criado | sim | não testa todas as tabelas individualmente |
| `test_taxonomy_seed_is_idempotent` | seed não duplica definições e mantém eventos esperados | sim | não valida a taxonomia no vídeo |
| `test_paths_are_safe` | slug básico e join seguro simples | parcial | falta testar path traversal explicitamente |
| `test_timecode_helpers` | conversão básica de tempo | sim | poucos casos de borda |
| `test_clip_window_protects_negative_start` | janela de clipe não começa negativa | sim | não gera clipe real com `ffmpeg` |
| `test_video_metadata_uses_real_ffprobe` | MP4 sintético real é gerado com `ffmpeg` e lido com `ffprobe` | sim | vídeo sintético não substitui jogo real |

### `tests/test_match_service.py`

| Teste | O que prova | Critério está correto? | Limite |
| --- | --- | --- | --- |
| `test_create_match_with_video_persists_metadata` | adversária, atleta e jogo são criados; metadados do vídeo são extraídos e persistidos em SQLite temporário | sim | não testa UI, roster, edição/exclusão ou validação visual |

O uso de `tmp_path` é adequado porque isola o banco de teste e evita depender do banco local real.

### `tests/test_real_video_integration.py`

| Teste | O que prova | Critério está correto? | Limite |
| --- | --- | --- | --- |
| `test_real_video_metadata_is_extracted_when_available` | vídeo real local em `storage/videos/` tem metadados extraíveis | sim | pula em ambientes sem vídeo real |
| `test_real_video_metadata_can_be_persisted_when_available` | metadados de vídeo real persistem em `Match` com SQLite temporário | sim | não prova marcação ou relatório sobre esse vídeo |

O `skip` é correto para CI/repo porque vídeos reais são dados locais ignorados pelo Git. Para uma validação final de produto, o skip não basta: deve existir uma fixture de vídeo controlada ou um procedimento manual documentado.

## O que está comprovado como funcionando

| Área | Arquivos principais | Prova |
| --- | --- | --- |
| contrato documental | `docs/002_SPEC_MVP_Tecnico.md` | contadores no script |
| higiene de repo | `.gitignore`, `scripts/verify_current_state.sh` | ausência de mídia/banco/legado versionado |
| banco e modelos base | `scoutpraia/core/database.py`, `scoutpraia/models/*` | init de DB e criação de tabelas |
| taxonomia inicial | `scoutpraia/services/taxonomy_service.py` | seed idempotente com 29 definições |
| vídeo/metadados | `scoutpraia/services/video_service.py` | `ffmpeg` + `ffprobe` reais em teste sintético |
| cadastro base de jogo | `scoutpraia/services/match_service.py` | persistência em SQLite temporário |
| vídeo real local | `tests/test_real_video_integration.py` | metadados extraídos e persistidos quando há arquivo em `storage/videos/` |

## O que não está comprovado

*Nota: estado desta auditoria é de 2026-06-06. Serviços internos, UI e relatórios foram implementados desde então (226 testes). O bloqueio atual é G5.*

| Área | Motivo | Próximo gate |
| --- | --- | --- |
| UI Streamlit completa | não houve `streamlit run app.py` com verificação visual/browser | G5 — `docs/007_PROT_Protocolo_Validacao.md` |
| marcação de eventos (validação humana) | prova automatizada existe; falta validação humana com screenshots | G5 — `docs/007_PROT_Protocolo_Validacao.md` |
| validação observacional | não há duas codificações comparadas nem amostra intra/interobservador | G5 — Bloco C de `docs/007_PROT_Protocolo_Validacao.md` |
| taxonomia aprovada | taxonomia está `draft`; vídeo real não validou definição operacional | G1/G5 — `docs/006_TAX_Dicionario_Taxonomia.md` + `docs/007_PROT_Protocolo_Validacao.md` |
| importação de Eventos v1 | `import_rule_v1 = nao_importar_v1` | G5 aprovado + decisão em `docs/006_TAX_Dicionario_Taxonomia.md` |
| MVP completo | G5 pendente | G5 fechado → declarar MVP |

## Veredito sobre `AGENTS.md`

O fluxo de `AGENTS.md` está correto para reduzir fuga do agente porque exige:

- leitura de contratos antes de implementar
- execução por fase
- teste/prova após mudança relevante
- atualização de progresso
- registro explícito de pendências
- proibição de declarar sucesso sem evidência
- proibição de versionar dados locais e binários

Limite: `AGENTS.md` não é prova técnica por si só. Ele força comportamento quando obedecido, mas a garantia real vem da combinação entre `AGENTS.md`, testes específicos, script de validação e auditoria humana/técnica.

## Conclusão

As provas atuais são válidas e corretamente calibradas para afirmar:

> A base inicial do ScoutPraia está implementada e funcionando para importação, banco, seed de taxonomia, extração/persistência de metadados de vídeo e higiene do repositório.

As provas atuais não autorizam afirmar:

> O ScoutPraia MVP completo está implementado.

Para poder declarar MVP completo, os próximos gates precisam incluir pelo menos:

1. teste de path traversal em `safe_join`
2. teste de criação/validação de eventos reais contra taxonomia
3. teste de geração real de clipe com `ffmpeg`
4. teste de analytics/KPIs com fixture controlada
5. teste de relatório HTML salvo em `storage/reports/`
6. teste ou verificação visual da UI Streamlit
7. validação com vídeo real conforme `docs/007_PROT_Protocolo_Validacao.md`
8. comparação intra/interobservador para campos críticos
