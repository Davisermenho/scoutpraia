# ScoutPraia — Progresso de Implementação e Evidência

Este arquivo acompanha o que foi implementado, o que foi verificado e o que ainda não está pronto. Ele deve ser atualizado a cada ciclo de implementação.

Regra: uma etapa só pode ser marcada como `FUNCIONANDO` quando houver evidência reproduzível por comando, teste ou arquivo verificável.

---

## Estado atual

Última atualização: `2026-06-06`

Status geral: `BASE TÉCNICA INICIAL FUNCIONANDO`

Importante: o MVP completo ainda **não** está pronto. A base de projeto, banco, modelos iniciais, seed de taxonomia, serviços iniciais de eventos e geração real de clipe com `ffmpeg` em teste sintético estão funcionando dentro do escopo testado. Marcação real na UI, upload/cadastro de jogos completo, analytics completo e relatórios finais ainda não foram implementados.

---

## Prova reproduzível

Rodar na raiz do projeto:

```bash
scripts/verify_current_state.sh
```

Esse script verifica:

- duplicação obrigatória corrigida no MVP documental
- importação do pacote `scoutpraia`
- inicialização do banco SQLite
- seed da taxonomia `ScoutPraia v0.1`
- quantidade esperada de definições de eventos
- testes automatizados
- `git diff --check`
- estado atual da working tree

Arquivo do script: `scripts/verify_current_state.sh`

---

## Última execução da prova

Comando executado:

```bash
scripts/verify_current_state.sh
```

Resultado observado:

```text
== ScoutPraia current-state verification ==
date_utc=2026-06-06T11:21:28Z
cwd=/home/davis/SCOUT
git_branch=main
git_head=a13e9c6

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
collected 15 items
tests/test_clip_service.py .                                             [  6%]
tests/test_event_service.py ..                                           [ 20%]
tests/test_match_service.py ..                                           [ 33%]
tests/test_models.py .                                                   [ 40%]
tests/test_real_video_integration.py ..                                  [ 53%]
tests/test_smoke.py .......                                              [100%]
15 passed, 6 warnings

== Git whitespace check ==
sem erros
```

Interpretação: a base técnica atual está validada para seguir para a próxima fase. Isso **não** prova que o MVP completo está pronto.

---

## Checklist por fase

### Fase 1 — Pré-implementação obrigatória

Status: `FUNCIONANDO`

Evidência:

- `match_roster` tem um único `player_id`.
- `## 13.1 KPIs coletivos` aparece uma única vez.
- Verificado por `scripts/verify_current_state.sh`.

Arquivos relacionados:

- `MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md`
- `docs/IMPLEMENTATION_STEPS_AI.md`

### Fase 2 — Estrutura base do projeto

Status: `FUNCIONANDO`

Implementado:

- `app.py`
- `requirements.txt`
- `README.md`
- `.env.example`
- `data/.gitkeep`
- `storage/videos/.gitkeep`
- `storage/clips/.gitkeep`
- `storage/reports/.gitkeep`
- `storage/thumbnails/.gitkeep`
- pacote `scoutpraia/`
- diretórios `core`, `models`, `services`, `pages`, `templates`, `utils`
- diretório `tests/`

Evidência:

- `python3 -c "import scoutpraia; print(scoutpraia.__doc__)"` passa.
- `python3 -m pytest` passa.

### Fase 3 — Configuração, paths e banco

Status: `FUNCIONANDO`

Implementado:

- `scoutpraia/core/config.py`
- `scoutpraia/core/paths.py`
- `scoutpraia/core/database.py`

Evidência:

- `python3 -m scoutpraia.core.database` cria/inicializa `data/scoutpraia.db`.
- `data/*.db` está ignorado pelo Git.
- `git diff --check` passa.

Observação:

- O ambiente local não tinha `python3-venv/ensurepip`, então as dependências foram instaladas com `python3 -m pip install --user --break-system-packages -r requirements.txt` para validar. Para operação limpa, instalar `python3.12-venv` e recriar `.venv`.

### Fase 4 — Modelos de dados iniciais

Status: `FUNCIONANDO COMO BASE`

Implementado:

- `Team`
- `Player`
- `Opponent`
- `Match`
- `MatchRoster`
- `SetSegment`
- `Possession`
- `TaxonomyVersion`
- `EventDefinition`
- `Event`
- `CodingSession`
- `CodingAgreement`
- `Clip`
- `Report`

Evidência:

- `SQLModel.metadata.create_all(engine)` executa sem erro.
- Banco inicializa no teste `test_database_initializes`.

Limite atual:

- Ainda faltam testes de criação/consulta para todos os modelos individualmente.

### Fase 5 — Taxonomia v0.1

Status: `FUNCIONANDO`

Implementado:

- `scoutpraia/services/taxonomy_service.py`
- seed idempotente de `ScoutPraia v0.1`
- 29 definições de eventos

Evidência:

- `event_definitions=29`
- `expected_event_definitions=29`
- teste `test_taxonomy_seed_is_idempotent` passa.

Limite atual:

- Taxonomia está com status `draft`, como previsto. Ainda não foi validada com vídeo real.

### Fase 6 — Serviços internos iniciais

Status: `PARCIAL`

Implementado parcialmente:

- `video_service.py`: validação de arquivo/extensão e extração real de metadados com `ffprobe`
- `event_service.py`: criação, listagem por jogo, edição e exclusão de evento com validação contra taxonomia, zona e regra prática de `points_value`
- `clip_service.py`: cálculo de janela, nome de clipe, execução real de `ffmpeg` e persistência de `Clip`
- `validation_service.py`: cálculo simples de concordância
- `analytics_service.py`: KPIs coletivos mínimos
- `report_service.py`: renderização Jinja básica
- `match_service.py`: associação idempotente de atletas ao `match_roster`, listagem e remoção

Evidência:

- `clip_window` e `probe_video_metadata` testados em `tests/test_smoke.py`.
- `match_roster` testado em `tests/test_match_service.py`.
- CRUD de eventos e falhas esperadas de validação testados em `tests/test_event_service.py`.
- Geração real de clipe com `ffmpeg` e persistência de `Clip` testadas em `tests/test_clip_service.py`.

Pendências:

- `analytics_service.py` ainda não cobre todos os KPIs do MVP.
- `report_service.py` ainda não salva relatório nem cria registro `Report`.
- `validation_service.py` ainda não persiste `CodingAgreement`.

### Fase 7 — Interface Streamlit

Status: `PARCIAL`

Implementado:

- `app.py` com navegação local simples.
- página de Jogos com cadastro básico real.
- página de Jogos com associação básica de atletas disponíveis ao jogo via `match_roster`.
- Dashboard, Marcação, Relatórios e Adversárias ainda são placeholders.

Evidência:

- importação do app e pacote passa indiretamente nos testes.

Pendências:

- Ainda não foi feita verificação visual com `streamlit run app.py`.
- Tela real de marcação ainda não implementada.
- Relatórios na UI ainda não implementados.

### Fase 8 — Testes

Status: `FUNCIONANDO COMO SMOKE TESTS`

Implementado:

- `tests/test_smoke.py`
- `tests/test_clip_service.py`
- `tests/test_event_service.py`
- `tests/test_match_service.py`
- `tests/test_models.py`
- 15 testes passando

Evidência:

- `python3 -m pytest` retorna `15 passed`.

Limite atual:

- A cobertura aumentou para modelos principais, roster, eventos e clipe real sintético, mas ainda faltam testes de fixture de jogo sintético completo, KPIs completos e relatórios completos.

---

## Pendências reais para MVP completo

O ScoutPraia ainda precisa de:

1. Mais testes completos de serviços.
2. Seed de dados de exemplo ou fixture sintética de jogo.
3. evoluir cadastro de atletas, adversárias e jogos com edição/exclusão.
4. Tela de marcação real com criação/edição/exclusão de eventos.
5. Analytics completo conforme o MVP.
6. Relatórios HTML completos e persistidos.
7. Validação operacional com vídeo real.
8. Verificação visual do Streamlit.
9. README operacional completo após a implementação funcional.
10. Commit das mudanças atuais quando o ciclo for aprovado.

---

## Definição de não concluído

Não considerar o MVP completo enquanto qualquer item abaixo estiver ausente:

- marcação real de eventos por jogo
- geração real de clipes com `ffmpeg`
- KPIs completos
- relatórios HTML completos
- validação da taxonomia com vídeo
- testes de fluxo operacional

---

## Próxima fase autorizada pelo plano

Próximo trabalho técnico recomendado:

1. implementar testes de criação/consulta dos modelos principais
2. associar elenco disponível ao jogo com `match_roster`
3. implementar edição/exclusão de adversária/jogo/atleta
4. implementar tela de marcação funcional


---

## Governança de agentes

Status: `CONFIGURADO`

Implementado:

- `AGENTS.md` com regras obrigatórias para agentes neste repositório.
- Exigência de prova reproduzível antes de declarar sucesso.
- Exigência de atualização de `docs/IMPLEMENTATION_PROGRESS.md` em cada ciclo.
- Proibição explícita de pular fases ou esconder trabalho parcial.
- Restrições de escopo do MVP para evitar React, FastAPI, PostgreSQL, API pública, autenticação, deploy e RAG antes do MVP funcional.

Evidência:

- `AGENTS.md` existe e não está vazio.
- `git diff --check` passou após criação do arquivo.
- `scripts/verify_current_state.sh` deve continuar passando após esta atualização.

---

## Ciclo — Serviço real de vídeo com ffprobe

Status: `FUNCIONANDO`

Fase atual: serviço de vídeo.

Implementado:

- `scoutpraia/services/video_service.py` agora resolve binários configurados, binários no `PATH` ou fallback local em `bin/`.
- `probe_video_metadata()` valida `.mp4`/`.mov`, executa `ffprobe`, lê JSON e retorna duração, largura, altura, FPS e codec.
- `VideoMetadata` registra os metadados extraídos.

Teste adicionado:

- `tests/test_smoke.py::test_video_metadata_uses_real_ffprobe`

Evidência executada:

```bash
python3 -m pytest tests/test_smoke.py -q
```

Resultado observado:

```text
7 passed in 1.09s
```

O teste gera um MP4 mínimo com `ffmpeg` real e valida os metadados com `ffprobe` real. Isso prova extração real de metadados, não mock.

Pendências remanescentes da fase de vídeo:

- integrar `probe_video_metadata()` à tela de cadastro de jogos
- persistir metadados no registro `Match`
- tratar exibição de erro na UI Streamlit


---

## Auditoria — AGENTS.md e prova real

Status: `AUDITADO`

Escopo da auditoria:

- verificar se `AGENTS.md` obriga leitura de contrato, prova reproduzível, atualização de progresso e registro de pendências reais
- verificar se o teste atual prova a extração real de metadados de vídeo
- verificar se o critério do teste é adequado ao que foi implementado
- verificar se o fluxo impede declarar MVP completo sem evidência

Evidência executada:

```bash
scripts/verify_current_state.sh
```

Resultado observado:

```text
collected 8 items
tests/test_match_service.py . [ 12%]
tests/test_smoke.py ....... [100%]
8 passed in 0.50s
```

Conclusão da auditoria:

- O teste de vídeo prova extração real de metadados com `ffprobe` para um MP4 sintético gerado por `ffmpeg` real.
- O teste de cadastro prova persistência de metadados em `Match` usando banco SQLite temporário.
- Os testes não provam verificação visual da UI, associação de roster, edição/exclusão, tratamento visual de erro ou funcionamento com vídeos reais de jogo.
- O `AGENTS.md` reduz brechas ao exigir prova reproduzível, progresso atualizado e pendências explícitas, mas não substitui testes específicos de cada nova funcionalidade.
- O fluxo atual é correto para impedir declarações amplas sem evidência, desde que toda entrega rode `scripts/verify_current_state.sh` e adicione testes específicos do escopo alterado.


---

## Ciclo — Cadastro básico de jogos com metadados persistidos

Status: `FUNCIONANDO COMO BASE`

Fase atual: cadastro de jogos e persistência de metadados de vídeo.

Implementado:

- `Match` recebeu `video_width`, `video_height`, `video_fps` e `video_codec`.
- `MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md` foi atualizado para refletir esses campos.
- `scoutpraia/services/match_service.py` cadastra adversária, atleta e jogo.
- `create_match_with_video()` executa `ffprobe` via `probe_video_metadata()` e persiste metadados em `Match`.
- `scoutpraia/pages/matches.py` agora tem cadastro básico real de adversárias, atletas e jogos.
- `scoutpraia/core/database.py` tem migração leve para adicionar colunas novas de metadados ao SQLite local existente.

Teste adicionado:

- `tests/test_match_service.py::test_create_match_with_video_persists_metadata`

Evidência executada:

```bash
python3 -m pytest
```

Resultado observado:

```text
collected 8 items
tests/test_match_service.py . [ 12%]
tests/test_smoke.py ....... [100%]
8 passed in 1.15s
```

O teste cria um banco SQLite temporário, gera um MP4 real com `ffmpeg`, cadastra adversária, atleta e jogo, executa `ffprobe`, persiste metadados no `Match` e consulta os dados gravados. Isso prova persistência de metadados de vídeo no serviço, não apenas extração isolada.

Limitações reais:

- A página Streamlit de Jogos ainda não foi verificada visualmente no navegador.
- O cadastro ainda não associa elenco disponível ao jogo via `match_roster`.
- Ainda não há edição/exclusão pela UI.
- A tela de marcação ainda não cria eventos reais.

---

## Ciclo — Validação com vídeo real em storage/videos

Status: `FUNCIONANDO COM VÍDEO REAL`

Fase atual: prova de extração e persistência de metadados usando vídeo real local no diretório canônico do MVP.

Vídeos reais detectados:

- `storage/videos/jogo_x6ppOlG0XlQ_2h19m44s_2h52m31s.mp4`
- `storage/videos/jogo_x6ppOlG0XlQ_2h19m44s_2h52m31s_720p_h264.mp4`

Metadados observados com `probe_video_metadata()`:

```text
storage/videos/jogo_x6ppOlG0XlQ_2h19m44s_2h52m31s.mp4
VideoMetadata(duration_seconds=1967.0, width=640, height=360, fps=30.0, codec='h264')

storage/videos/jogo_x6ppOlG0XlQ_2h19m44s_2h52m31s_720p_h264.mp4
VideoMetadata(duration_seconds=1967.033, width=1280, height=720, fps=60.0, codec='h264')
```

Teste adicionado:

- `tests/test_real_video_integration.py::test_real_video_metadata_is_extracted_when_available`
- `tests/test_real_video_integration.py::test_real_video_metadata_can_be_persisted_when_available`

Evidência executada:

```bash
python3 -m pytest tests/test_real_video_integration.py -q
```

Resultado observado:

```text
2 passed in 0.76s
```

O teste usa arquivo real em `storage/videos/` quando disponível. Se a pasta ou vídeo não existir em outro ambiente, o teste fica `skip`, porque vídeos reais são dados locais ignorados pelo Git.

Limitações reais:

- Isso prova leitura e persistência de metadados com vídeo real local.
- Isso ainda não prova marcação de eventos no vídeo real.
- Isso ainda não prova geração de clipes com `ffmpeg`.
- Isso ainda não prova operação visual completa no Streamlit.


---

## Ciclo — Remoção do diretório legado de vídeos

Status: `ALINHADO AO MVP`

Motivo:

- O MVP define `storage/videos/` como diretório canônico de vídeos.
- a pasta local antiga estava fora da estrutura prevista.

Implementado:

- vídeos reais copiados para `storage/videos/`
- testes de integração atualizados para procurar vídeos reais em `storage/videos/`
- `.gitignore` removeu a referência ao diretório legado
- `docs/IMPLEMENTATION_PROGRESS.md` atualizado para usar apenas `storage/videos/`

Limites:

- os vídeos continuam ignorados pelo Git por `storage/videos/*`
- apenas `storage/videos/.gitkeep` deve ser versionado

---

## Auditoria — Validação das provas atuais

Status: `AUDITADO COM GATE REFORÇADO`

Escopo:

- verificar se o script e os testes provam corretamente o que está implementado
- separar prova técnica real de afirmações ainda não cobertas
- validar o critério dos testes contra fontes técnicas e metodologia observacional
- reforçar o gate contra versionamento indevido de mídia, banco, `.env`, `.venv`, `tmp/`, `bin/` e gerados
- reforçar o gate contra retorno do diretório legado `Videos-Jogos/`

Implementado:

- `docs/AUDIT_EVIDENCE_VALIDATION.md` criado com veredito técnico.
- `scripts/verify_current_state.sh` agora checa higiene de repositório.
- `AGENTS.md` passa a exigir leitura do arquivo de auditoria.

Evidência executada:

```bash
scripts/verify_current_state.sh
```

Resultado observado:

```text
== Repository hygiene checks ==
canonical_video_dir=storage/videos
legacy_video_dir_absent=Videos-Jogos
forbidden_tracked_files=none

== Tests ==
collected 10 items
tests/test_match_service.py .                                            [ 10%]
tests/test_real_video_integration.py ..                                  [ 30%]
tests/test_smoke.py .......                                              [100%]
10 passed
```

Conclusão:

- As provas atuais sustentam a base técnica inicial: importação, banco, seed de taxonomia, extração/persistência de metadados de vídeo e higiene do repo.
- As provas atuais não sustentam declarar MVP completo.
- Permanecem não comprovados: UI completa, marcação real, geração real de clipes, analytics completo, relatórios finais, validação observacional e confiabilidade intra/interobservador.

---

## Ciclo — Roster de jogo e testes de modelos

Fase atual declarada: `Fase 6 — Serviços internos` com reforço de `Fase 8 — Testes`.

Status: `PARCIAL COM EVIDÊNCIA`

Implementado:

- `scoutpraia/services/match_service.py` recebeu associação idempotente de atleta ao jogo via `MatchRoster`.
- `scoutpraia/services/match_service.py` recebeu listagem e remoção de atleta do roster do jogo.
- `scoutpraia/pages/matches.py` recebeu seção básica para adicionar atletas disponíveis ao elenco do jogo.
- `tests/test_match_service.py` passou a testar adicionar, atualizar, listar e remover roster.
- `tests/test_models.py` criado para testar criação e consulta dos modelos principais.

Comandos executados:

```bash
python3 -m pytest tests/test_match_service.py tests/test_models.py
scripts/verify_current_state.sh
```

Resultado observado:

```text
tests/test_match_service.py ..                                           [ 66%]
tests/test_models.py .                                                   [100%]
3 passed, 3 warnings

scripts/verify_current_state.sh
date_utc=2026-06-06T10:40:30Z
collected 12 items
tests/test_match_service.py ..                                           [ 16%]
tests/test_models.py .                                                   [ 25%]
tests/test_real_video_integration.py ..                                  [ 41%]
tests/test_smoke.py .......                                              [100%]
12 passed, 3 warnings
```

Limitações, gaps e riscos:

- A tela de roster é básica e ainda não tem edição visual de titularidade nem remoção pela UI.
- Os avisos são de depreciação de `datetime.utcnow()` disparados pelos modelos com `default_factory`; não quebram a execução, mas devem ser tratados em ciclo específico.
- A marcação real de eventos, geração real de clipes, analytics completo e relatórios persistidos continuam `PARCIAL` ou ausentes conforme pendências acima.

---

## Ciclo — Serviço de eventos com CRUD e validação

Fase atual declarada: `Fase 6 — Serviços internos`.

Status: `PARCIAL COM EVIDÊNCIA`

Implementado:

- `scoutpraia/services/event_service.py` agora lista eventos por jogo.
- `scoutpraia/services/event_service.py` agora edita eventos existentes com campos permitidos.
- `scoutpraia/services/event_service.py` agora exclui eventos existentes.
- `scoutpraia/services/event_service.py` valida existência de jogo, set, posse e atletas referenciadas.
- `scoutpraia/services/event_service.py` valida `points_value` de forma conservadora conforme dicionário: `two_point_goal` exige `2`, eventos de gol exigem valor maior que `0` e eventos não pontuadores exigem `0`.
- `tests/test_event_service.py` cobre criação, listagem, edição, exclusão e falhas por taxonomia, zona e pontos inválidos.

Comandos executados:

```bash
python3 -m pytest tests/test_event_service.py
scripts/verify_current_state.sh
```

Resultado observado:

```text
tests/test_event_service.py ..                                           [100%]
2 passed, 2 warnings

scripts/verify_current_state.sh
date_utc=2026-06-06T10:46:57Z
collected 14 items
tests/test_event_service.py ..                                           [ 14%]
tests/test_match_service.py ..                                           [ 28%]
tests/test_models.py .                                                   [ 35%]
tests/test_real_video_integration.py ..                                  [ 50%]
tests/test_smoke.py .......                                              [100%]
14 passed, 5 warnings
```

Limitações, gaps e riscos:

- A validação de `points_value` é prática e conservadora; ela não torna a taxonomia `approved`.
- A tela de marcação ainda não usa esse serviço.
- Os warnings de `datetime.utcnow()` continuam presentes e registrados como pendência técnica.

---

## Ciclo — Geração real de clipes com FFmpeg

Fase atual declarada: `Fase 6 — Serviços internos`.

Status: `PARCIAL COM EVIDÊNCIA`

Implementado:

- `scoutpraia/services/clip_service.py` agora busca evento, jogo, set e atleta para montar o contexto do clipe.
- `scoutpraia/services/clip_service.py` agora valida o vídeo de origem associado ao jogo.
- `scoutpraia/services/clip_service.py` agora gera nome previsível com jogo, set, timestamp, tipo de evento e atleta.
- `scoutpraia/services/clip_service.py` agora executa `ffmpeg` real com janela calculada pelo tipo de evento.
- `scoutpraia/services/clip_service.py` agora captura erro do `ffmpeg` em `ClipGenerationError`.
- `scoutpraia/services/clip_service.py` agora salva registro `Clip` com caminho, janela, evento e atleta.
- `tests/test_clip_service.py` gera MP4 sintético real, cria evento, gera clipe real, lê metadados com `ffprobe` e confirma persistência em SQLite temporário.

Comandos executados:

```bash
python3 -m pytest tests/test_clip_service.py
scripts/verify_current_state.sh
```

Resultado observado:

```text
tests/test_clip_service.py .                                             [100%]
1 passed, 1 warning

scripts/verify_current_state.sh
date_utc=2026-06-06T11:21:28Z
collected 15 items
tests/test_clip_service.py .                                             [  6%]
tests/test_event_service.py ..                                           [ 20%]
tests/test_match_service.py ..                                           [ 33%]
tests/test_models.py .                                                   [ 40%]
tests/test_real_video_integration.py ..                                  [ 53%]
tests/test_smoke.py .......                                              [100%]
15 passed, 6 warnings
```

Limitações, gaps e riscos:

- A prova usa vídeo sintético gerado por `ffmpeg`; ainda falta validação operacional de clipes em jogo real completo.
- A UI de marcação ainda não aciona geração de clipes.
- Não há rotina de remoção/limpeza de clipes órfãos.
- Os warnings de `datetime.utcnow()` continuam presentes e devem ser tratados em ciclo específico.
