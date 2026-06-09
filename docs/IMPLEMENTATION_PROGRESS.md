# ScoutPraia — Progresso de Implementação e Evidência

Este arquivo acompanha o que foi implementado, o que foi verificado e o que ainda não está pronto. Ele deve ser atualizado a cada ciclo de implementação.

Regra: uma etapa só pode ser marcada como `FUNCIONANDO` quando houver evidência reproduzível por comando, teste ou arquivo verificável.

---

## Estado atual

Última atualização: `2026-06-08`

Status geral: `BASE TÉCNICA INICIAL FUNCIONANDO`

Importante: o MVP completo ainda **não** está pronto. A base de projeto, banco, modelos iniciais, seed de taxonomia, serviços de eventos, validação de concordância, geração real de clipe com `ffmpeg` em teste sintético, analytics com fixture controlada, geração local de relatórios HTML persistidos e o núcleo da UI Streamlit para Dashboard, Jogos, Marcação, Relatórios e Adversárias estão funcionando dentro do escopo testado. A página `Marcação` já cobre criação, edição e exclusão de `set`, `posse` e qualquer `evento` salvo, com filtros, navegação rápida no editor e sem a falha de `session_state` tardio nos formulários de criação. Validação observacional, verificação visual humana do fluxo completo e operação com vídeo real ainda não foram implementadas integralmente.

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
date_utc=2026-06-08T12:20:15Z
cwd=/home/davis/SCOUT
git_branch=main
git_head=bfd5f51

== Repository hygiene checks ==
canonical_video_dir=storage/videos
legacy_video_dir_absent=Videos-Jogos
forbidden_tracked_files=none

== Required MVP doc checks ==
match_roster_player_id_count=1
kpi_13_1_title_count=1
mvp_doc_path=docs/MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md
legacy_root_mvp_doc_absent=yes

== Python import ==
ScoutPraia local beach handball scouting app.

== Database init and taxonomy seed ==
Banco inicializado em data/scoutpraia.db
taxonomy=ScoutPraia v0.1
taxonomy_status=draft
event_definitions=29
expected_event_definitions=29

== Tests ==
collected 41 items
tests/test_analytics_service.py ..                                       [  4%]
tests/test_clip_service.py .                                             [  7%]
tests/test_event_service.py ..                                           [ 12%]
tests/test_match_service.py .....                                        [ 24%]
tests/test_models.py ..                                                  [ 29%]
tests/test_real_video_integration.py ..                                  [ 34%]
tests/test_report_service.py ..                                          [ 39%]
tests/test_smoke.py .........                                            [ 60%]
tests/test_streamlit_pages.py ...........                                [ 87%]
tests/test_ui_labels.py ...                                              [ 95%]
tests/test_validation_service.py ..                                      [100%]

============================== 41 passed in 6.02s ==============================

== Git whitespace check ==
== Working tree summary ==
 M AGENTS.md
 D MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md
 M docs/AUDIT_EVIDENCE_VALIDATION.md
 M docs/AUDIT_MVP_AGENT_FLOW.md
 M docs/IMPLEMENTATION_PROGRESS.md
 M docs/IMPLEMENTATION_STEPS_AI.md
 T docs/MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md
 M scripts/verify_current_state.sh
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

- `docs/MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md`
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

Status: `FUNCIONANDO COM EVIDÊNCIA`

Implementado parcialmente:

- `video_service.py`: validação de arquivo/extensão e extração real de metadados com `ffprobe`
- `event_service.py`: criação, listagem por jogo, edição e exclusão de evento com validação contra taxonomia, zona e regra prática de `points_value`
- `clip_service.py`: cálculo de janela, nome de clipe, execução real de `ffmpeg` e persistência de `Clip`
- `validation_service.py`: listagem de definições sem base operacional mínima, validação de taxonomia aprovada e persistência de `CodingAgreement` com divergências em JSON
- `analytics_service.py`: KPIs coletivos, individuais e por adversária com aviso para taxonomia não aprovada
- `report_service.py`: payload coletivo, individual e de adversária, renderização Jinja, exportação HTML e persistência de `Report`
- `match_service.py`: CRUD seguro parcial para adversárias, atletas e jogos, além de associação idempotente ao `match_roster`

Evidência:

- `clip_window` e `probe_video_metadata` testados em `tests/test_smoke.py`.
- `match_roster` testado em `tests/test_match_service.py`.
- CRUD de eventos e falhas esperadas de validação testados em `tests/test_event_service.py`.
- Geração real de clipe com `ffmpeg` e persistência de `Clip` testadas em `tests/test_clip_service.py`.
- Persistência de `CodingAgreement`, divergência artificial e aprovação de taxonomia testadas em `tests/test_validation_service.py`.
- KPIs coletivos, individuais e por adversária com fixture controlada testados em `tests/test_analytics_service.py`.
- Geração de relatórios HTML, links relativos de clipes e persistência de `Report` testadas em `tests/test_report_service.py`.
- Atualização/exclusão segura de cadastros e guardas de dependência testadas em `tests/test_match_service.py`.

Pendências:

- O fluxo de taxonomia aprovada na UI ainda depende de evolução explícita da interface.

### Fase 7 — Interface Streamlit

Status: `FUNCIONANDO COM EVIDÊNCIA`

Implementado:

- `app.py` com navegação local simples.
- página de Jogos com cadastro básico real.
- página de Jogos com edição/exclusão segura de jogos, adversárias e atletas.
- página de Jogos com associação e remoção de atletas no `match_roster`.
- página de Marcação com seleção de jogo/taxonomia, vídeo local, botões rápidos, timestamp manual, escolha de atleta/zona/set/posse, histórico lateral, edição/exclusão de `set` e `posse`, e editor de qualquer evento salvo com filtros/navegação.
- página de Relatórios com seleção de jogo, prévia de KPIs, geração de relatório coletivo/individual/adversária e ações para download/abrir HTML gerado.
- Dashboard com métricas operacionais, jogos recentes, atalhos e resumo de KPIs recentes.
- página Adversárias com cadastro, edição/exclusão, histórico de jogos, tendências calculadas e plano manual editável.
- `streamlit run app.py --server.headless true --server.port 8511` inicializa sem erro no ambiente atual.

Evidência:

- `tests/test_streamlit_pages.py` cobre estado vazio da página de Marcação.
- `tests/test_streamlit_pages.py` cobre criação, edição e exclusão de qualquer evento selecionado via página de Marcação.
- `tests/test_streamlit_pages.py` cobre edição/exclusão de `set` e `posse` via página de Marcação.
- `tests/test_streamlit_pages.py` cobre filtros e navegação rápida do editor de eventos.
- `tests/test_streamlit_pages.py` cobre geração de relatório coletivo via página de Relatórios.
- `tests/test_streamlit_pages.py` cobre renderização do Dashboard com métricas.
- `tests/test_streamlit_pages.py` cobre renderização da página Adversárias com histórico e tendências.
- `streamlit run app.py --server.headless true --server.port 8511` subiu e expôs `Local URL: http://localhost:8511`.

Pendências:

- A interface ainda não foi validada visualmente por navegação humana fim a fim no navegador.
- O fluxo completo com vídeo real, marcação extensa e geração de relatórios ainda não foi ensaiado operacionalmente.
- A política de exigir taxonomia aprovada para relatório final ainda não está exposta como decisão explícita na UI.

### Fase 8 — Testes

Status: `FUNCIONANDO COMO SMOKE TESTS`

Implementado:

- `tests/test_smoke.py`
- `tests/test_clip_service.py`
- `tests/test_event_service.py`
- `tests/test_match_service.py`
- `tests/test_models.py`
- `tests/test_validation_service.py`
- `tests/test_analytics_service.py`
- `tests/test_report_service.py`
- `tests/test_streamlit_pages.py`
- 28 testes passando

Evidência:

- `python3 -m pytest` retorna `28 passed`.

Limite atual:

- A cobertura aumentou para modelos principais, roster, eventos, clipe real sintético, validação de concordância, KPIs com fixture controlada, relatórios HTML persistidos, Dashboard, Adversárias e fluxo básico das páginas críticas do Streamlit, mas ainda faltam testes do fluxo operacional completo com vídeo real.

---

## Pendências reais para MVP completo

O ScoutPraia ainda precisa de:

1. Mais testes completos de serviços.
2. Seed de dados de exemplo ou fixture sintética de jogo.
3. Validação operacional com vídeo real.
4. Verificação visual do fluxo completo do Streamlit.
5. Expor decisão de taxonomia aprovada na UI de relatórios.
6. README operacional completo após a implementação funcional.

---

## Definição de não concluído

Não considerar o MVP completo enquanto qualquer item abaixo estiver ausente:

- marcação operacional completa por jogo
- geração real de clipes com `ffmpeg`
- KPIs completos
- fluxo operacional completo de relatórios via interface
- validação da taxonomia com vídeo
- testes de fluxo operacional

---

## Próxima fase autorizada pelo plano

Próximo trabalho técnico recomendado:

1. executar verificação visual do fluxo completo no navegador
2. iniciar validação operacional com vídeo real
3. expor regra de taxonomia aprovada na UI de relatórios
4. consolidar README operacional do MVP


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
- `docs/MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md` foi atualizado para refletir esses campos.
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

---

## Auditoria — Fluxo do MVP para agentes

Status: `AUDITADO`

Escopo:

- ler `docs/MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md`
- ler `docs/IMPLEMENTATION_STEPS_AI.md`
- ler `docs/IMPLEMENTATION_PROGRESS.md`
- avaliar se o fluxo documental é correto para um agente implementar o MVP
- auditar estrutura do repositório e restrições de stack

Implementado:

- `docs/AUDIT_MVP_AGENT_FLOW.md` criado com veredito e evidência.
- bloco `Próxima fase autorizada pelo plano` atualizado para `validation_service.py`, conforme Fase 6.4.

Comandos executados:

```bash
scripts/verify_current_state.sh
git ls-files
rg -n -i "react|fastapi|postgres|postgresql|auth|authentication|jwt|deploy|docker|kubernetes" app.py scoutpraia tests requirements.txt README.md .env.example
```

Resultado observado:

```text
date_utc=2026-06-06T11:28:28Z
git_head=e6f5e85
forbidden_tracked_files=none
collected 15 items
15 passed, 6 warnings
```

Conclusão:

- O fluxo correto para agentes é seguir `docs/IMPLEMENTATION_STEPS_AI.md` como ordem executável.
- `docs/MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md` permanece como contrato de produto e critério de escopo.
- `docs/IMPLEMENTATION_PROGRESS.md` deve continuar registrando prova, pendências e bloqueios.
- O próximo trabalho técnico autorizado é completar `report_service.py`.

---

## Ciclo — Validation service com persistência de CodingAgreement

Fase atual declarada: `Fase 6 — Serviços internos`.

Status: `PARCIAL COM EVIDÊNCIA`

Implementado:

- `scoutpraia/services/validation_service.py` agora lista definições sem base operacional mínima.
- `scoutpraia/services/validation_service.py` agora valida se a taxonomia está aprovada para relatório final.
- `scoutpraia/services/validation_service.py` agora compara duas sessões por `event_type`, atleta, zona e `points_value`.
- `scoutpraia/services/validation_service.py` agora calcula concordância percentual simples considerando divergências e ausências.
- `scoutpraia/services/validation_service.py` agora persiste `CodingAgreement` com divergências em JSON.
- `tests/test_validation_service.py` cobre divergência artificial, persistência do agreement e aprovação de taxonomia.

Comandos executados:

```bash
python3 -m pytest tests/test_validation_service.py
scripts/verify_current_state.sh
```

Resultado observado:

```text
tests/test_validation_service.py ..                                      [100%]
2 passed, 4 warnings

scripts/verify_current_state.sh
date_utc=2026-06-06T11:35:10Z
collected 17 items
tests/test_clip_service.py .                                             [  5%]
tests/test_event_service.py ..                                           [ 17%]
tests/test_match_service.py ..                                           [ 29%]
tests/test_models.py .                                                   [ 35%]
tests/test_real_video_integration.py ..                                  [ 47%]
tests/test_smoke.py .......                                              [ 88%]
tests/test_validation_service.py ..                                      [100%]
17 passed, 10 warnings
```

Limitações, gaps e riscos:

- O contrato atual não relaciona `Event` diretamente a `CodingSession`; a comparação persiste o vínculo entre sessões dentro do `disagreements_json`.
- A comparação usa listas de eventos fornecidas explicitamente; a UI ainda não gera essas sessões operacionais.
- A taxonomia segue `draft` no estado padrão; a aprovação testada é controlada em fixture.
- Os warnings de `datetime.utcnow()` continuam presentes e devem ser tratados em ciclo específico.

---

## Ciclo — Analytics service com fixture controlada

Fase atual declarada: `Fase 6 — Serviços internos`.

Status: `PARCIAL COM EVIDÊNCIA`

Implementado:

- `scoutpraia/services/analytics_service.py` agora calcula KPIs coletivos.
- `scoutpraia/services/analytics_service.py` agora calcula KPIs individuais por atleta.
- `scoutpraia/services/analytics_service.py` agora calcula KPIs por adversária.
- `scoutpraia/services/analytics_service.py` agora retorna aviso quando a taxonomia não está aprovada.
- `scoutpraia/services/analytics_service.py` agora sinaliza uso de eventos práticos/hipotéticos em KPI crítico quando esses eventos aparecem na amostra.
- `tests/test_analytics_service.py` cobre fixture controlada com eventos, posses e sets previsíveis.

Comandos executados:

```bash
python3 -m pytest tests/test_analytics_service.py
scripts/verify_current_state.sh
```

Resultado observado:

```text
tests/test_analytics_service.py ..                                       [100%]
2 passed

scripts/verify_current_state.sh
date_utc=2026-06-06T11:55:06Z
collected 19 items
tests/test_analytics_service.py ..                                       [ 10%]
tests/test_clip_service.py .                                             [ 15%]
tests/test_event_service.py ..                                           [ 26%]
tests/test_match_service.py ..                                           [ 36%]
tests/test_models.py .                                                   [ 42%]
tests/test_real_video_integration.py ..                                  [ 52%]
tests/test_smoke.py .......                                              [ 89%]
tests/test_validation_service.py ..                                      [100%]
19 passed, 10 warnings
```

Limitações, gaps e riscos:

- Os KPIs usam fixture controlada; ainda falta validação operacional sobre jogo real completo.
- O estado padrão da taxonomia continua `draft`, então os avisos críticos seguem aparecendo por desenho.
- `report_service.py` ainda não consome esses payloads.
- Os warnings de `datetime.utcnow()` continuam presentes e devem ser tratados em ciclo específico.

---

## Ciclo — Correção raiz dos timestamps UTC

Fase atual declarada: `Fase 6 — Serviços internos`.

Status: `PARCIAL COM EVIDÊNCIA`

Implementado:

- `scoutpraia/utils/datetime.py` centraliza a geração de timestamp UTC com `datetime.now(timezone.utc)`.
- `scoutpraia/models/taxonomy.py` substitui `datetime.utcnow()` por `utc_now`.
- `scoutpraia/models/validation.py` substitui `datetime.utcnow()` por `utc_now`.
- `scoutpraia/models/report.py` substitui `datetime.utcnow()` por `utc_now`.
- `tests/test_models.py` agora cobre regressão para garantir ausência de `DeprecationWarning` e presença de `tzinfo` nos campos padrão.

Comandos executados:

```bash
python3 -m pytest tests/test_models.py tests/test_validation_service.py -W error::DeprecationWarning
git diff --check
scripts/verify_current_state.sh
```

Resultado observado:

```text
tests/test_models.py ..                                                  [ 50%]
tests/test_validation_service.py ..                                      [100%]
4 passed in 1.54s

git diff --check
sem erros

scripts/verify_current_state.sh
date_utc=2026-06-06T22:26:43Z
git_head=216fbad
collected 20 items
20 passed
```

Limitações, gaps e riscos:

- A correção remove o warning de depreciação na origem dos modelos cobertos, mas ainda não implementa migração explícita de dados legados com timestamps sem fuso já persistidos em SQLite.
- `report_service.py` continua `PARCIAL` e permanece como próxima fase autorizada do plano.
- A taxonomia padrão continua `draft`; relatórios finais ainda dependem da validação/aprovação já tratada em serviço separado.

---

## Ciclo — Report service com payload, HTML e persistência

Fase atual declarada: `Fase 6 — Serviços internos`.

Status: `PARCIAL COM EVIDÊNCIA`

Implementado:

- `scoutpraia/services/report_service.py` agora monta payload coletivo.
- `scoutpraia/services/report_service.py` agora monta payload individual por atleta.
- `scoutpraia/services/report_service.py` agora monta payload de adversária.
- `scoutpraia/services/report_service.py` agora renderiza HTML via Jinja, exporta para diretório configurável e persiste `Report` com `payload_json`.
- `scoutpraia/services/report_service.py` agora rejeita relatório sem taxonomia inequívoca quando o jogo mistura versões.
- `scoutpraia/templates/report_collective.html`, `scoutpraia/templates/report_individual.html` e `scoutpraia/templates/report_opponent.html` agora exibem versão da taxonomia, KPIs e links relativos para clipes existentes.
- `README.md` agora declara explicitamente que PDF ainda não foi implementado neste MVP.
- `tests/test_report_service.py` cobre geração de HTML, persistência de `Report`, versão da taxonomia e links relativos de clipes.

Comandos executados:

```bash
python3 -m pytest tests/test_report_service.py tests/test_models.py tests/test_validation_service.py -W error::DeprecationWarning
git diff --check
scripts/verify_current_state.sh
```

Resultado observado:

```text
tests/test_report_service.py ..                                          [ 33%]
tests/test_models.py ..                                                  [ 66%]
tests/test_validation_service.py ..                                      [100%]
6 passed in 3.44s

git diff --check
sem erros

scripts/verify_current_state.sh
date_utc=2026-06-06T22:43:38Z
git_head=216fbad
collected 22 items
22 passed
```

Limitações, gaps e riscos:

- A geração de relatório está comprovada em serviço e teste, mas ainda não está conectada à interface Streamlit.
- O fluxo de relatório final com taxonomia aprovada depende de quem chamar `require_approved_taxonomy=True`; o estado padrão do seed continua `draft`.
- Ainda falta verificação visual com `streamlit run app.py` e fluxo manual completo de marcação até relatório.

---

## Ciclo — Páginas críticas de Marcação e Relatórios no Streamlit

Fase atual declarada: `Fase 7 — Interface Streamlit`.

Status: `PARCIAL COM EVIDÊNCIA`

Implementado:

- `scoutpraia/pages/tagging.py` agora oferece seleção de jogo e taxonomia.
- `scoutpraia/pages/tagging.py` agora exibe vídeo local com `st.video` quando o jogo possui `video_path`.
- `scoutpraia/pages/tagging.py` agora registra eventos com timestamp manual, botões rápidos, atleta, zona, set e posse.
- `scoutpraia/pages/tagging.py` agora mostra histórico recente e permite localizar, editar e excluir qualquer evento salvo.
- `scoutpraia/pages/reports.py` agora mostra prévia de KPIs por jogo.
- `scoutpraia/pages/reports.py` agora gera relatório coletivo, individual e de adversária chamando `report_service.py`.
- `scoutpraia/pages/reports.py` agora lista arquivos gerados com ação de download e tentativa de abertura local.
- `tests/test_streamlit_pages.py` cobre renderização vazia, marcação via página e geração de relatório via página.

Comandos executados:

```bash
python3 -m pytest tests/test_streamlit_pages.py tests/test_event_service.py tests/test_report_service.py tests/test_validation_service.py tests/test_models.py -W error::DeprecationWarning
scripts/verify_current_state.sh
streamlit run app.py --server.headless true --server.port 8510
```

Resultado observado:

```text
tests/test_streamlit_pages.py ...                                        [ 27%]
tests/test_event_service.py ..                                           [ 45%]
tests/test_report_service.py ..                                          [ 63%]
tests/test_validation_service.py ..                                      [ 81%]
tests/test_models.py ..                                                  [100%]
11 passed in 4.93s

scripts/verify_current_state.sh
date_utc=2026-06-06T23:10:10Z
git_head=216fbad
collected 25 items
25 passed

streamlit run app.py --server.headless true --server.port 8510
Uvicorn server started on 0.0.0.0:8510
Local URL: http://localhost:8510
```

Limitações, gaps e riscos:

- O player nativo do Streamlit continua limitado a timestamp manual; não há sincronização fina do tempo de reprodução no HTML player.
- A página de Relatórios usa o fluxo padrão da taxonomia seed `draft`; exigir taxonomia aprovada na UI ainda depende de evolução explícita de UX/regra.
- A página Adversárias continua parcial e ainda não há verificação visual do fluxo completo em navegador com interação humana.

---

## Ciclo — Dashboard, Adversárias e CRUD seguro em Jogos

Fase atual declarada: `Fase 7 — Interface Streamlit`.

Status: `PARCIAL COM EVIDÊNCIA`

Implementado:

- `scoutpraia/services/match_service.py` agora atualiza e exclui adversárias com guarda de dependência.
- `scoutpraia/services/match_service.py` agora atualiza e exclui atletas com guarda de dependência.
- `scoutpraia/services/match_service.py` agora atualiza e exclui jogos com guarda de dependência e releitura de metadados do vídeo.
- `scoutpraia/pages/dashboard.py` agora exibe métricas operacionais, jogos recentes e resumo de KPIs recentes.
- `scoutpraia/pages/opponents.py` agora exibe cadastro, histórico, tendências calculadas e plano manual editável por adversária.
- `scoutpraia/pages/matches.py` agora permite editar/excluir jogos, atletas e adversárias, além de remover atletas do elenco do jogo.
- `tests/test_match_service.py` agora cobre atualização/exclusão segura e mensagens de bloqueio por dependência.
- `tests/test_streamlit_pages.py` agora cobre Dashboard e Adversárias.

Comandos executados:

```bash
python3 -m pytest tests/test_match_service.py tests/test_streamlit_pages.py tests/test_report_service.py tests/test_models.py -W error::DeprecationWarning
scripts/verify_current_state.sh
streamlit run app.py --server.headless true --server.port 8511
```

Resultado observado:

```text
tests/test_match_service.py ...                                          [ 25%]
tests/test_streamlit_pages.py .....                                      [ 66%]
tests/test_report_service.py ..                                          [ 83%]
tests/test_models.py ..                                                  [100%]
12 passed in 7.62s

scripts/verify_current_state.sh
date_utc=2026-06-06T23:21:09Z
git_head=a02832f
collected 28 items
28 passed

streamlit run app.py --server.headless true --server.port 8511
Uvicorn server started on 0.0.0.0:8511
Local URL: http://localhost:8511
```

Limitações, gaps e riscos:

- As exclusões em `Jogos` são deliberadamente conservadoras; entidades com vínculos operacionais são bloqueadas em vez de sofrer exclusão em cascata.
- Dashboard e Adversárias estão comprovados por renderização e dados sintéticos, mas ainda não por navegação humana fim a fim.

---

## Ciclo — Verificação visual e ensaio operacional com vídeo real

Fase atual declarada: `Fase 7 — Interface Streamlit` + ensaio operacional local.

Status: `PARCIAL COM EVIDÊNCIA`

Implementado / executado:

- Verificação visual com `agent-browser` nas páginas `Dashboard`, `Marcação`, `Relatórios` e `Adversárias`.
- Confirmação de carregamento sem overlay de erro e sem erros de console no fluxo visual observado.
- Ensaio operacional real em banco local com o vídeo `storage/videos/jogo_x6ppOlG0XlQ_2h19m44s_2h52m31s.mp4`.
- Criação local de adversária, atletas, jogo, `SetSegment`, `Possession` e `Event` usando o vídeo real.
- Geração local de relatório coletivo, individual e de adversária com arquivos HTML em `storage/reports/`.

Comandos executados:

```bash
streamlit run app.py --server.headless true --server.port 8512
agent-browser open http://localhost:8512
agent-browser snapshot -i
agent-browser screenshot /tmp/scoutpraia-dashboard-real.png --annotate
agent-browser screenshot /tmp/scoutpraia-tagging-real.png --annotate
agent-browser screenshot /tmp/scoutpraia-reports-real.png --annotate
python3 - <<'PY'
# cria cenário operacional real com vídeo local, evento e relatórios
PY
```

Resultado observado:

```text
Dashboard carregou com conteúdo e sem overlay.
Marcação carregou com vídeo real, seletor de jogo preenchido e histórico do evento real.
Relatórios carregou com prévia de KPIs e listagem dos arquivos HTML gerados.
Adversárias carregou com formulário e estado navegável sem erro de console.

Cenário real persistido:
match_id=1
event_id=1
collective_report=storage/reports/match-1_collective_...
individual_report=storage/reports/match-1_individual_atleta-real-e2e_...
opponent_report=storage/reports/match-1_opponent_adversaria-real-e2e_...
```

Limitações, gaps e riscos:

- A verificação visual automatizada confirmou carregamento e conteúdo, mas não substitui revisão humana do layout final.
- O botão de geração de relatório na página `Relatórios` ficou visível no navegador, porém a automação com `agent-browser` não confirmou disparo efetivo do clique; os relatórios do ensaio real foram gerados com sucesso via serviço Python local.
- O ensaio operacional real ainda foi curto: 1 jogo, 1 posse e 1 evento. Ainda falta um ensaio manual mais longo com marcação extensa em vídeo real.
- O Streamlit ainda emite warnings de depreciação de `use_container_width`; isso não bloqueou o fluxo, mas precisa ser removido.
- A prévia tabular de KPIs na página `Relatórios` ainda gera warning de serialização Arrow para colunas com estruturas aninhadas; a UI funciona, porém a apresentação desses campos ainda precisa ser normalizada.

---

## Ciclo — Correção de warnings Streamlit e prova da geração pela UI

Fase atual declarada: `Fase 7 — Interface Streamlit`.

Status: `PARCIAL COM EVIDÊNCIA`

Implementado / executado:

- Substituição de `use_container_width=True` por `width="stretch"` nas páginas `Dashboard`, `Jogos`, `Marcação`, `Relatórios` e `Adversárias`.
- Normalização da prévia de KPIs em `Relatórios` para evitar mistura de números, `None` e estruturas aninhadas na mesma coluna tabular.
- Separação explícita do KPI `set_performance` em tabela própria `Detalhe por set`.
- Normalização da tabela de tendências em `Adversárias` para texto exibível estável.
- Reforço do teste de UI da página `Relatórios` para gerar coletivo, individual e adversária via `AppTest`.
- Nova prova visual da página `Relatórios` com geração real de relatórios pela própria UI no navegador.

Comandos executados:

```bash
python3 -m pytest tests/test_streamlit_pages.py tests/test_report_service.py -W error::DeprecationWarning
streamlit run app.py --server.headless true --server.port 8515
agent-browser open http://localhost:8515
agent-browser snapshot
agent-browser click @e14
agent-browser snapshot
agent-browser eval "(() => { const btn = [...document.querySelectorAll('button')].find((button) => button.innerText.includes('Gerar coletivo')); if (!btn) return 'BUTTON_NOT_FOUND'; btn.click(); return btn.innerText; })()"
agent-browser eval "(() => { const btn = [...document.querySelectorAll('button')].find((button) => button.innerText.includes('Gerar individual')); if (!btn) return 'BUTTON_NOT_FOUND'; btn.click(); return btn.innerText; })()"
agent-browser eval "(() => { const btn = [...document.querySelectorAll('button')].find((button) => button.innerText.includes('Gerar adversária')); if (!btn) return 'BUTTON_NOT_FOUND'; btn.click(); return btn.innerText; })()"
find storage/reports -maxdepth 1 -type f | wc -l
```

Resultado observado:

```text
tests/test_streamlit_pages.py .....                                      [ 71%]
tests/test_report_service.py ..                                          [100%]
7 passed in 8.81s

Página Relatórios carregada sem novo warning de use_container_width.
Página Relatórios carregada sem novo warning Arrow no log do Streamlit após a normalização das tabelas.

Geração pela UI comprovada no navegador:
FILES_BEFORE=4
FILES_AFTER=5
status=Relatório coletivo gerado: /home/davis/SCOUT/storage/reports/match-1_collective_2026-06-07t02-31-14-956340utc.html

FILES_BEFORE=5
FILES_AFTER_INDIVIDUAL=6
FILES_AFTER=7
status=Relatório de adversária gerado: /home/davis/SCOUT/storage/reports/match-1_opponent_adversaria-real-e2e_2026-06-07t02-31-52-936160utc.html

Estado visual final da página:
6 relatório(s) gerado(s) para este jogo.
arquivo presente para collective, individual e opponent recém-gerados.
```

Limitações, gaps e riscos:

- O clique nativo `agent-browser click` no botão Streamlit `Gerar coletivo` não disparou o handler nesta sessão; a prova visual foi obtida com `agent-browser eval(...btn.click())`, que acionou o mesmo botão no DOM do navegador e atualizou a UI com sucesso.
- A prova de UI ficou forte para a página `Relatórios`, mas isso não substitui um ensaio humano longo de marcação com vídeo real.

---

## Ciclo — Ensaio manual mais longo com vídeo real e geração final pela interface

Fase atual declarada: `Fase 7 — Interface Streamlit`.

Status: `PARCIAL COM EVIDÊNCIA`

Implementado / executado:

- Execução de um ensaio mais longo na página `Marcação` com o vídeo real do jogo `Ensaio Operacional Real`.
- Inclusão de 6 eventos adicionais pela própria interface Streamlit, além do evento real inicial já existente.
- Geração final de relatório coletivo, individual e de adversária pela página `Relatórios`.
- Conferência do estado final por UI e por consulta direta ao banco local.

Comandos executados:

```bash
streamlit run app.py --server.headless true --server.port 8516
agent-browser open http://localhost:8516
agent-browser click @e22
agent-browser fill @e11 8450
agent-browser fill @e21 "ensaio-manual-1 technical_error"
agent-browser click @e60
agent-browser fill @e11 8465
agent-browser fill @e21 "ensaio-manual-2 team shot_attempt"
agent-browser click @e60
agent-browser fill @e11 8490
agent-browser fill @e21 "ensaio-manual-3 team shot_attempt"
agent-browser click @e60
agent-browser click @e73
agent-browser eval "(() => { const btn = [...document.querySelectorAll('button')].find((button) => button.innerText.includes('Gerar coletivo')); if (!btn) return 'BUTTON_NOT_FOUND'; btn.click(); return btn.innerText; })()"
agent-browser eval "(() => { const btn = [...document.querySelectorAll('button')].find((button) => button.innerText.includes('Gerar individual')); if (!btn) return 'BUTTON_NOT_FOUND'; btn.click(); return btn.innerText; })()"
agent-browser eval "(() => { const btn = [...document.querySelectorAll('button')].find((button) => button.innerText.includes('Gerar adversária')); if (!btn) return 'BUTTON_NOT_FOUND'; btn.click(); return btn.innerText; })()"
python3 - <<'PY'
# consulta final do banco: eventos e relatórios do jogo 1
PY
```

Resultado observado:

```text
Histórico recente na UI após o ensaio:
- evento 1: 8412.0 goal_scored team player_id=1
- eventos 2 a 7: novos registros salvos pela interface

Consulta final ao banco:
MATCH 1 Ensaio Operacional Real
EVENT_COUNT 7
REPORT_COUNT 9

Últimos relatórios gerados pela interface:
- collective: match-1_collective_2026-06-07t02-46-28-739133utc.html
- individual: match-1_individual_atleta-real-e2e_2026-06-07t02-46-30-267222utc.html
- opponent: match-1_opponent_adversaria-real-e2e_2026-06-07t02-46-31-769128utc.html

Prova visual da página Relatórios:
FILES_BEFORE=7
FILES_AFTER=10
9 relatório(s) gerado(s) para este jogo.
arquivo presente para os três relatórios recém-gerados.
```

Limitações, gaps e riscos:

- O ensaio ficou mais longo em quantidade de eventos, mas a automação do navegador não conseguiu variar corretamente todos os timestamps no `number_input`; os eventos 2 a 7 ficaram persistidos com `8450.0`.
- A tentativa de usar botões rápidos para alterar o tipo do evento não se refletiu no `selectbox` da UI nesta sessão; os novos eventos foram persistidos como `shot_attempt`, apesar das notas registrarem a intenção operacional.
- Isso prova que o fluxo principal de salvar eventos e gerar relatórios via UI funciona, mas também evidencia uma limitação real da automação usada sobre widgets Streamlit complexos.

---

## Ciclo — Protocolo operacional repetível para validação humana

Fase atual declarada: `Fase 9 — Validação operacional com vídeo real`.

Status: `FUNCIONANDO COMO DOCUMENTO DE PROCESSO`

Implementado / executado:

- Expansão de `docs/validation_protocol.md` com um protocolo humano repetível para ensaio operacional do MVP.
- Inclusão de:
  - pré-requisitos
  - preparação obrigatória
  - amostra operacional mínima
  - roteiro por etapa
  - evidência mínima obrigatória
  - critérios de aceite e reprovação
  - modelo textual de registro final

Comandos executados:

```bash
git diff --check
scripts/verify_current_state.sh
```

Resultado observado:

```text
`docs/validation_protocol.md` agora define um roteiro operacional humano repetível para:
- abrir a aplicação
- validar cadastro e vídeo real
- marcar uma amostra mínima
- editar evento
- gerar três relatórios pela interface
- registrar evidência final

Gate final:
28 passed
```

Limitações, gaps e riscos:

- O protocolo humano melhora repetibilidade, mas não substitui futura aprovação formal da taxonomia.
- O protocolo ainda depende de execução manual disciplinada; ele não é um teste automatizado.

---

## Ciclo — Script mínimo para subir o Scout e abrir a URL local

Fase atual declarada: `Fase 7 — Ergonomia operacional local`.

Status: `FUNCIONANDO COM EVIDÊNCIA`

Implementado / executado:

- Criação de `scripts/run_scout.sh` para:
  - subir `streamlit run app.py`
  - esperar a URL local responder
  - abrir o navegador automaticamente com `python3 -m webbrowser`
  - aceitar `--port` e `--no-browser`
- Atualização do `README.md` com o novo fluxo de execução rápida.
- Atualização de `docs/validation_protocol.md` para usar o script no protocolo humano.

Comandos executados:

```bash
bash -n scripts/run_scout.sh
scripts/run_scout.sh --no-browser --port 8520
git diff --check
scripts/verify_current_state.sh
```

Resultado observado:

```text
`scripts/run_scout.sh` passou na validação sintática.
O script subiu o Streamlit, aguardou `http://localhost:8520` responder e manteve o processo vivo.
O modo `--no-browser` funcionou sem depender de aplicação gráfica externa.

Gate final:
28 passed
```

Limitações, gaps e riscos:

- O script melhora muito o uso local, mas não substitui o protocolo humano de validação.
- A abertura automática do navegador depende do comportamento do `webbrowser` do Python no ambiente do operador.

---

## Ciclo — Dicionário central de rótulos e tradução da UI operacional

Fase atual declarada: `Fase 7 — Ergonomia operacional local`.

Status: `FUNCIONANDO COM EVIDÊNCIA`

Implementado / executado:

- Criação de `scoutpraia/ui_labels.py` como camada central de apresentação para traduzir:
  - tipos de evento
  - lados (`team` / `opponent`)
  - zonas
  - KPIs
  - tipos de relatório
  - cabeçalhos de tabela
- Atualização de `scoutpraia/pages/tagging.py` para exibir rótulos operacionais em português em:
  - botões rápidos
  - seleção de evento
  - seleção de lado
  - seleção de zona
  - seleção de posse
  - histórico recente
  - editor de qualquer evento salvo
- Atualização de `scoutpraia/pages/reports.py` para traduzir:
  - nomes de KPIs na prévia
  - métricas aninhadas por set
  - tipos de relatório na listagem de arquivos gerados
- Atualização de `scoutpraia/pages/opponents.py` para traduzir:
  - métricas de tendências
  - valor do lado preferencial
- Criação de `tests/test_ui_labels.py` para validar a camada central de rótulos.
- Ajuste de `tests/test_streamlit_pages.py` para cobrir o novo rótulo visível do botão rápido e o rótulo traduzido de posse.

Comandos executados:

```bash
python3 -m pytest tests/test_ui_labels.py tests/test_streamlit_pages.py -q
python3 -m pytest tests/test_report_service.py tests/test_ui_labels.py tests/test_streamlit_pages.py -q
scripts/verify_current_state.sh
```

Resultado observado:

```text
Os testes focados da UI e da camada de rótulos passaram:
- 8 passed
- 10 passed

Gate final:
31 passed
```

Limitações, gaps e riscos:

- A tradução foi aplicada na camada de apresentação; os identificadores internos continuam em inglês/snake_case por decisão técnica para preservar banco, serviços e testes.
- Campos livres como `event_subtype` e `outcome` continuam dependentes da disciplina de preenchimento do operador; a melhoria aqui foi de rótulo, não de padronização semântica.
- A taxonomia segue em `draft`; traduzir os nomes reduz ambiguidade operacional, mas não substitui validação observacional formal.

---

## Ciclo — Correção de duplicação da tabela `clips` no bootstrap do banco

Fase atual declarada: `Fase 7 — Ergonomia operacional local`.

Status: `FUNCIONANDO COM EVIDÊNCIA`

Implementado / executado:

- Correção em `scoutpraia/core/database.py` para tornar `import_models()` idempotente com guarda de processo (`_MODELS_IMPORTED`).
- A mudança evita novo registro do modelo `Clip` e, por consequência, evita o erro:
  - `sqlalchemy.exc.InvalidRequestError: Table 'clips' is already defined for this MetaData instance`
- Criação de regressão automatizada em `tests/test_smoke.py` cobrindo dupla chamada de `import_models()`.

Comandos executados:

```bash
python3 -m pytest tests/test_smoke.py -q
scripts/verify_current_state.sh
```

Resultado observado:

```text
Teste focal:
- 8 passed

Gate final:
32 passed
```

Limitações, gaps e riscos:

- A correção atua no registro duplicado de modelos no mesmo processo; ela não altera o schema nem faz migração estrutural.
- O problema foi tratado na causa operacional observada no bootstrap; se surgir novo caminho de importação fora de `import_models()`, ele deve ser auditado separadamente.

---

## Ciclo — Lançador gráfico `ScoutPraia.desktop` para 1 clique

Fase atual declarada: `Fase 7 — Ergonomia operacional local`.

Status: `FUNCIONANDO COM EVIDÊNCIA`

Implementado / executado:

- Criação de `ScoutPraia.desktop` na raiz do repositório como lançador gráfico para 1 clique.
- O lançador:
  - entra em `/home/davis/SCOUT`
  - executa `scripts/run_scout.sh`
  - mantém `Terminal=true` para permitir diagnóstico e encerramento manual da sessão
- Atualização do `README.md` com a orientação de uso do lançador.
- Permissão de execução aplicada em `ScoutPraia.desktop`.

Comandos executados:

```bash
chmod +x ScoutPraia.desktop
desktop-file-validate ScoutPraia.desktop
scripts/verify_current_state.sh
```

Resultado observado:

```text
`desktop-file-validate` não está disponível neste ambiente.

Gate final:
32 passed
```

Limitações, gaps e riscos:

- O lançador usa caminho absoluto `/home/davis/SCOUT`; se o repositório for movido de lugar, o `Exec` e o `Path` precisam ser ajustados.
- O uso de `Terminal=true` é intencional para manter o processo do Streamlit controlável; não é um lançamento totalmente silencioso.

---

## Ciclo — Guia de preenchimento da página `Marcação`

Fase atual declarada: `Fase 7 — Ergonomia operacional local`.

Status: `FUNCIONANDO COM EVIDÊNCIA`

Implementado / executado:

- Criação de `docs/guia_preenchimento_marcacao.md` com:
  - explicação de `set`
  - explicação de `posse`
  - preenchimento campo a campo da página `Marcação`
  - regra de uso do `Timestamp manual (s)` em segundos corridos
  - orientação sobre botões rápidos, histórico e edição
  - três exemplos operacionais de jogadas

Comandos executados:

```bash
scripts/verify_current_state.sh
```

Resultado observado:

```text
Gate final:
32 passed
```

Limitações, gaps e riscos:

- O guia é operacional e usa exemplos práticos de preenchimento; ele não substitui validação observacional formal da taxonomia.
- Os exemplos do guia ensinam o uso correto da tela, mas não devem ser tratados como regra oficial isolada sem confronto com `docs/taxonomy_dictionary.md`.

---

## Ciclo — Entrada de tempo em `MM:SS` na página `Marcação`

Fase atual declarada: `Fase 7 — Ergonomia operacional local`.

Status: `FUNCIONANDO COM EVIDÊNCIA`

Implementado / executado:

- Atualização de `scoutpraia/utils/timecode.py` para aceitar:
  - segundos simples
  - `MM:SS`
  - `HH:MM:SS`
  - frações com ponto ou vírgula
- Atualização de `scoutpraia/pages/tagging.py` para trocar os campos numéricos de tempo por entrada textual amigável em:
  - `Início do set`
  - `Fim do set`
  - `Início da posse`
  - `Fim da posse`
  - `Timestamp do vídeo`
  - `Timestamp do último evento`
- Inclusão de preview visual da conversão para segundos internos.
- Correção colateral: valor `0` segundo deixa de ser tratado como `None` em criação de set e posse.
- Atualização de `tests/test_smoke.py` e `tests/test_streamlit_pages.py`.
- Atualização de `docs/guia_preenchimento_marcacao.md` para refletir o novo fluxo sem conta manual.

Comandos executados:

```bash
python3 -m pytest tests/test_smoke.py tests/test_streamlit_pages.py -q
scripts/verify_current_state.sh
```

Resultado observado:

```text
Testes focados:
- 13 passed

Gate final:
32 passed
```

Limitações, gaps e riscos:

- O player continua sem captura automática do tempo atual; a melhoria remove a conta manual, mas o operador ainda precisa ler o tempo no vídeo e digitá-lo.
- A conversão aceita formatos de relógio e segundos, mas entradas totalmente livres continuam inválidas por desenho.

---

## Ciclo — Edição e exclusão de qualquer evento na página `Marcação`

Fase atual declarada: `Fase 7 — Ergonomia operacional local`.

Status: `FUNCIONANDO COM EVIDÊNCIA`

Implementado / executado:

- Substituição do editor de `último evento` por seleção explícita de qualquer evento salvo do jogo em `scoutpraia/pages/tagging.py`.
- Inclusão de seletor `Evento para editar ou excluir` com identificação por:
  - id do evento
  - tempo formatado
  - nome do evento
- Atualização do formulário para editar o evento selecionado, não apenas o mais recente.
- Atualização do botão de exclusão para remover o evento selecionado.
- Atualização de `tests/test_streamlit_pages.py` para provar:
  - criação de um evento novo
  - seleção do evento `1`
  - edição desse evento
  - exclusão desse evento
  - preservação do evento mais recente

Comandos executados:

```bash
python3 -m pytest tests/test_streamlit_pages.py -q
scripts/verify_current_state.sh
```

Resultado observado:

```text
Teste focal:
- 5 passed

Gate final:
32 passed
```

Limitações, gaps e riscos:

- A UI agora resolve a limitação de atuar só no último evento, mas sets e posses continuam sem edição/exclusão pela interface.
- O editor continua sem campos explícitos para editar `secondary_player_id` e `possession_id`; a mudança desta etapa focou seleção e ação sobre qualquer evento.

---

## Ciclo — Serviços e UI para edição/exclusão de `set`

Fase atual declarada: `Fase 7 — Ergonomia operacional local`.

Status: `FUNCIONANDO COM EVIDÊNCIA`

Implementado / executado:

- Inclusão de `update_set_segment()` e `delete_set_segment()` em `scoutpraia/services/match_service.py`.
- Regra de exclusão segura:
  - set não pode ser excluído se houver `possession` ou `event` vinculados.
- Inclusão de seletor `Set para editar ou excluir` na página `Marcação`.
- Inclusão de formulário `Editar set selecionado` na área `Sets e posses`.
- Inclusão de botão `Excluir set selecionado` na mesma área.
- Rótulo do seletor de set passou a mostrar:
  - número do set
  - id
  - início e fim formatados
- Atualização de `tests/test_match_service.py` para cobrir:
  - edição de set
  - exclusão de set sem dependência
  - bloqueio de exclusão com dependência
- Atualização de `tests/test_streamlit_pages.py` para cobrir:
  - seleção de set existente
  - atualização do set selecionado
  - exclusão de set selecionado sem dependências

Comandos executados:

```bash
python3 -m pytest tests/test_match_service.py tests/test_streamlit_pages.py -q
scripts/verify_current_state.sh
```

Resultado observado:

```text
Testes focados:
- 10 passed

Gate final:
34 passed
```

Limitações, gaps e riscos:

- A etapa atual resolve apenas `set`.
- `posse` ainda não possui edição/exclusão pela UI.
- O editor de evento ainda não expõe `secondary_player_id` e `possession_id`.

---

## Ciclo — Serviços e UI para edição/exclusão de `posse`

Fase atual declarada: `Fase 7 — Ergonomia operacional local`.

Status: `FUNCIONANDO COM EVIDÊNCIA`

Implementado / executado:

- Inclusão de `update_possession()` e `delete_possession()` em `scoutpraia/services/match_service.py`.
- Regra de exclusão segura:
  - posse não pode ser excluída se houver `event` vinculado via `possession_id`.
- Inclusão de seletor `Posse para editar ou excluir` na página `Marcação`.
- Inclusão de formulário `Editar posse selecionada` na área `Sets e posses`.
- Inclusão de botão `Excluir posse selecionada` na mesma área.
- Rótulo do seletor de posse passou a mostrar:
  - id
  - lado
  - set vinculado
  - início e fim formatados
- Atualização de `tests/test_match_service.py` para cobrir:
  - edição de posse
  - exclusão de posse sem dependência
  - bloqueio de exclusão com dependência
- Atualização de `tests/test_streamlit_pages.py` para cobrir:
  - seleção de posse existente
  - atualização da posse selecionada
  - exclusão da posse selecionada sem dependências

Comandos executados:

```bash
python3 -m pytest tests/test_match_service.py tests/test_streamlit_pages.py -q
scripts/verify_current_state.sh
```

Resultado observado:

```text
Testes focados:
- 12 passed in 5.00s

Gate final:
- 36 passed in 4.99s
```

Limitações, gaps e riscos:

- Esta etapa fecha apenas seleção, edição e exclusão de `posse`.
- O editor de evento continua sem campos explícitos para `secondary_player_id` e `possession_id`.
- A UI ainda não oferece edição/exclusão de sets e posses fora da página `Marcação`.

---

## Ciclo — Campos explícitos no editor de evento

Fase atual declarada: `Fase 7 — Ergonomia operacional local`.

Status: `FUNCIONANDO COM EVIDÊNCIA`

Implementado / executado:

- Inclusão de `Atleta secundária do evento` no editor da página `Marcação`.
- Inclusão de `Posse do evento` no editor da página `Marcação`.
- Atualização do `update_event()` via UI para persistir:
  - `secondary_player_id`
  - `possession_id`
- Atualização de `tests/test_streamlit_pages.py` para provar:
  - seleção de um evento existente
  - troca explícita da atleta secundária
  - troca explícita da posse vinculada
  - persistência da alteração antes da exclusão

Comandos executados:

```bash
python3 -m pytest tests/test_streamlit_pages.py tests/test_event_service.py -q
scripts/verify_current_state.sh
```

Resultado observado:

```text
Testes focados:
- 9 passed in 4.40s

Gate final:
- 36 passed in 3.80s
```

Limitações, gaps e riscos:

- O editor agora expõe `secondary_player_id` e `possession_id`, mas a UX ainda depende de seleção manual em listas.
- A cobertura atual é local e automatizada; a prova humana com vídeo real continua sendo responsabilidade do protocolo operacional.

---

## Ciclo — Filtros e navegação rápida no editor de eventos

Fase atual declarada: `Fase 7 — Ergonomia operacional local`.

Status: `FUNCIONANDO COM EVIDÊNCIA`

Implementado / executado:

- Inclusão de filtros explícitos no editor da página `Marcação`:
  - `Filtrar por set`
  - `Filtrar por lado`
  - `Filtrar por tipo de evento`
  - `Buscar evento`
- Inclusão de navegação rápida no editor:
  - `Evento anterior`
  - `Próximo evento`
  - contador `Evento filtrado X de Y`
- O rótulo do seletor `Evento para editar ou excluir` passou a mostrar também a atleta principal quando disponível.
- Atualização de `tests/test_streamlit_pages.py` para provar:
  - navegação entre eventos filtrados da equipe
  - edição do evento selecionado após navegação
  - filtro combinado por set, lado e busca textual
  - exclusão do evento filtrado correto
- Correção da causa raiz do gate documental:
  - `docs/MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md` foi consolidado como caminho documental do contrato MVP.

Comandos executados:

```bash
python3 -m pytest tests/test_streamlit_pages.py -q
scripts/verify_current_state.sh
```

Resultado observado:

```text
Testes focados:
- 8 passed in 3.30s

Gate final:
- 37 passed in 4.11s
```

Limitações, gaps e riscos:

- A navegação rápida atua sobre a lista filtrada atual; filtros muito amplos continuam exigindo uso manual da busca.
- Naquele ciclo, o contrato ainda estava em transição de caminho; essa observação deixa de valer após a migração canônica para `docs/`.

---

## Ciclo — Alinhamento documental da página `Marcação`

Fase atual declarada: `Fase 7 — Ergonomia operacional local`.

Status: `FUNCIONANDO COM EVIDÊNCIA`

Implementado / executado:

- Atualização de `docs/IMPLEMENTATION_STEPS_AI.md` para refletir:
  - edição/exclusão de qualquer evento salvo
  - edição/exclusão de `set` e `posse`
  - filtros e navegação rápida do editor
- Atualização de `docs/guia_preenchimento_marcacao.md` para refletir:
  - correção de qualquer evento salvo, não apenas do último
  - fluxo atual de correção com filtros e navegação
  - correção de `set` e `posse`
  - aceitação de `MM:SS` e `HH:MM:SS`
- Atualização de `docs/validation_protocol.md` para refletir:
  - validação humana do bloco `Localizar evento`
  - uso de filtros no editor
  - validação operacional de `set` e `posse` quando aplicável
- Atualização do resumo atual em `docs/IMPLEMENTATION_PROGRESS.md` para manter coerência com a UI implementada.

Comandos executados:

```bash
scripts/verify_current_state.sh
git diff --check
```

Resultado observado:

```text
Gate final:
- 37 passed in 5.35s
```

Limitações, gaps e riscos:

- O histórico de ciclos anteriores em `docs/IMPLEMENTATION_PROGRESS.md` permanece como registro temporal e ainda cita estados parciais de etapas antigas.
- O histórico desse ciclo registra um estado transitório anterior à migração canônica do contrato para `docs/`.

---

## Ciclo — Ergonomia fina da página `Marcação`

Fase atual declarada: `Fase 7 — Ergonomia operacional local`.

Status: `FUNCIONANDO COM EVIDÊNCIA`

Implementado / executado:

- Inclusão de ajuste rápido do tempo na criação de evento:
  - `-1s`
  - `-0.5s`
  - `+0.5s`
  - `+1s`
- O formulário de evento agora abre com defaults mais úteis:
  - `Set` mais recente disponível
  - `Posse` mais recente do set selecionado
  - `Número do set` em `Novo set` com próximo valor esperado
- O formulário preserva a seleção operacional corrente de:
  - `Set`
  - `Atleta`
  - `Atleta secundária`
  - `Zona`
  - `Posse`
  - `Pontos`
- Atualização de `tests/test_streamlit_pages.py` para provar:
  - ajuste rápido de timestamp
  - uso de defaults de `set` e `posse`
  - persistência útil do formulário após salvar evento
- Atualização de `docs/guia_preenchimento_marcacao.md` para refletir os atalhos de tempo e os defaults da tela.

Comandos executados:

```bash
python3 -m pytest tests/test_streamlit_pages.py -q
scripts/verify_current_state.sh
```

Resultado observado:

```text
Testes focados:
- 9 passed in 4.90s

Gate final:
- 38 passed in 7.77s
```

Limitações, gaps e riscos:

- O player continua sem captura automática do tempo real; a ergonomia melhora o ajuste manual, mas não substitui integração fina com o player HTML.
- A preservação de campos textuais (`Subtipo`, `Desfecho`, `Notas`) foi mantida para não apagar contexto digitado inadvertidamente.

---

## Ciclo — Robustez de importação dos modelos SQLModel

Fase atual declarada: `Fase 6 — Serviços internos iniciais`.

Status: `FUNCIONANDO COM EVIDÊNCIA`

Implementado / executado:

- Endurecimento de `scoutpraia/core/database.py` para importar apenas módulos de modelo cujas tabelas ainda não estão registradas em `SQLModel.metadata`.
- O plano de importação agora é explícito por módulo e por conjunto de tabelas.
- Isso evita redefinição de tabelas já carregadas parcialmente por outro caminho de importação no mesmo processo.
- Atualização de `tests/test_smoke.py` com prova específica:
  - metadado pré-carregado
  - reset controlado de `_MODELS_IMPORTED`
  - nova chamada de `import_models()` sem `InvalidRequestError`

Comandos executados:

```bash
python3 -m pytest tests/test_smoke.py -q
scripts/verify_current_state.sh
```

Resultado observado:

```text
Teste focal:
- 9 passed in 0.34s

Gate final:
- 39 passed in 5.83s
```

Limitações, gaps e riscos:

- Eu não reproduzi a exceção original no meu ambiente, então a correção foi feita na condição estrutural que permite o problema: importação redundante com `metadata` parcialmente populado.
- Se existir outro caminho de importação fora do pacote `scoutpraia.*`, ele continua sendo um risco de arquitetura e deve ser evitado.

---

## Ciclo — Correção de `session_state` tardio em `Novo set` e `Nova posse`

Fase atual declarada: `Fase 8 — UI Streamlit funcional do fluxo manual`.

Status: `FUNCIONANDO COM EVIDÊNCIA`

Implementado / executado:

- Regressões adicionadas em `tests/test_streamlit_pages.py` para provar criação de `set` e criação de `posse` sem `StreamlitAPIException`.
- Correção em `scoutpraia/pages/tagging.py` para remover a escrita tardia em chaves de widgets já instanciados:
  - `new_set_number`
  - `new_set_start`
  - `new_set_end`
  - `new_possession_set`
- Introdução de estado pendente não vinculado a widget:
  - `pending_new_set_state`
  - `pending_new_possession_state`
  - `management_success_message`
- O pós-submit agora aplica reset/default no rerun seguinte, antes da criação dos widgets.
- O formulário `Novo set` volta com:
  - próximo número sugerido
  - `Início do set = 00:00`
  - `Fim do set = 00:00`
- O formulário `Nova posse` volta com:
  - `Equipe da posse` preservada
  - `Set da posse` preservado
  - `Início da posse = 00:00`
  - `Fim da posse = 00:00`
  - `Resultado da posse` limpo
  - `Pontos feitos = 0`
  - `Pontos sofridos = 0`
- Remoção do uso redundante de `value=` em widgets de criação que já são controlados por `session_state`, para evitar warning de estado duplicado.

Comandos executados:

```bash
python3 -m pytest tests/test_streamlit_pages.py -q -k 'creates_set_without_session_state_exception or creates_possession_without_session_state_exception'
python3 -m pytest tests/test_streamlit_pages.py -q
```

Resultado observado:

```text
Testes de regressão:
- 2 passed, 9 deselected in 1.37s

Suíte da página:
- 11 passed in 3.68s

Gate final:
- 41 passed in 5.29s
```

Limitações, gaps e riscos:

- Esta correção fecha o defeito de `session_state` tardio nos formulários de criação de `set` e `posse`.
- A evidência final do repositório inteiro ainda depende do gate completo `scripts/verify_current_state.sh` deste ciclo.

---

## Ciclo — Formalização documental do protocolo humano para `Salvar set` e `Salvar posse`

Fase atual declarada: `Fase 8 — UI Streamlit funcional do fluxo manual`.

Status: `PARCIAL`

Implementado / executado:

- Atualização de `docs/validation_protocol.md` para incluir uma etapa específica de conferência de `Sets e posses` após mudanças de UI.
- O protocolo agora exige verificar no navegador real:
  - ausência de `StreamlitAPIException` ao salvar `set`
  - ausência de `StreamlitAPIException` ao salvar `posse`
  - reset e preservação corretos dos campos após submit
  - existência única do novo registro nos seletores de edição
- Atualização de `docs/guia_preenchimento_marcacao.md` com o comportamento esperado após:
  - `Salvar set`
  - `Salvar posse`
- O texto deixa explícito que a prova atualmente disponível neste ciclo é técnica/automatizada, não humana.

Comandos executados:

```bash
scripts/verify_current_state.sh
```

Resultado observado:

```text
Gate final:
- 41 passed in 5.69s
```

Limitações, gaps e riscos:

- Ainda não foi anexada prova humana real deste ciclo em forma de screenshots do navegador.
- Portanto, este ciclo está formalizado documentalmente, mas a validação humana específica continua pendente.

---

## Ciclo — Migração do contrato MVP para `docs/`

Fase atual declarada: `Fase 1 — Pré-implementação obrigatória`.

Status: `FUNCIONANDO COM EVIDÊNCIA`

Implementado / executado:

- `docs/MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md` deixou de ser symlink e passou a ser o arquivo real canônico do contrato MVP.
- `MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md` foi removido da raiz do repositório.
- `AGENTS.md` passou a instruir leitura do contrato em `docs/`.
- `scripts/verify_current_state.sh` passou a:
  - validar `docs/MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md`
  - falhar se o arquivo legado da raiz reaparecer
- `docs/IMPLEMENTATION_STEPS_AI.md`, `docs/AUDIT_MVP_AGENT_FLOW.md` e `docs/AUDIT_EVIDENCE_VALIDATION.md` foram alinhados ao novo caminho canônico.
- `docs/IMPLEMENTATION_PROGRESS.md` foi corrigido para remover a narrativa de alias transitório como estado atual.

Comandos executados:

```bash
scripts/verify_current_state.sh
```

Resultado observado:

```text
Gate final:
- 41 passed in 6.02s
```

Limitações, gaps e riscos:

- Scripts externos do usuário que apontem manualmente para o contrato na raiz precisarão ser atualizados para `docs/`.
- O histórico antigo em `docs/IMPLEMENTATION_PROGRESS.md` continua registrando estados transitórios de ciclos anteriores, mas o caminho canônico atual passa a ser `docs/`.

---

## Ciclo — Renomeação do estado padrão do filtro `Filtrar por set`

Fase atual declarada: `Fase 8 — UI Streamlit funcional do fluxo manual`.

Status: `FUNCIONANDO COM EVIDÊNCIA`

Implementado / executado:

- O estado padrão do filtro `Filtrar por set` na página `Marcação` foi renomeado de `Sem set` para `Todos`.
- A lógica de filtragem foi preservada: o valor padrão continua significando ausência de filtro por `set`.
- A lista do filtro agora mostra:
  - `Todos`
  - sets reais existentes no jogo
- `Sem set` continua reservado apenas para contextos de domínio onde o valor nulo representa ausência real de associação, como no editor de evento.
- Foi adicionado teste de regressão para garantir que o seletor `Filtrar por set` inicia com `Todos`.

Comandos executados:

```bash
python3 -m pytest tests/test_streamlit_pages.py -q
scripts/verify_current_state.sh
```

Resultado observado:

```text
python3 -m pytest tests/test_streamlit_pages.py -q
- 11 passed in 4.63s

scripts/verify_current_state.sh
- 41 passed in 5.00s
```

Limitações, gaps e riscos:

- Esta mudança é estritamente de nomenclatura/UX no filtro; não altera a regra de negócio dos `sets`.
- O filtro `Filtrar por set` continua sem suportar uma distinção entre “evento realmente sem set” e “sem filtro”, porque esse não é o fluxo operacional adotado neste MVP.

---

## Ciclo — Governança documental de status `draft`, `testing` e `approved`

Fase atual declarada: `Fase 1 — Pré-implementação obrigatória`.

Status: `FUNCIONANDO COM EVIDÊNCIA`

Implementado / executado:

- Inclusão de uma tabela objetiva de governança de status em `docs/evidence_matrix.md`, cobrindo:
  - o que cada status permite
  - o que bloqueia
  - impacto em UI, KPIs e relatórios
  - ações para transformar um item em estável
  - fontes verificáveis associadas
- Inclusão de uma régua de transição de status em `docs/validation_protocol.md`, explicitando:
  - `draft` → `testing`
  - `testing` → `approved`
  - `approved` → nova versão quando houver mudança semântica
- As fontes usadas na documentação foram ancoradas nos códigos já registrados em `docs/sources/README.md` e nos contratos internos do repositório.

Comandos executados:

```bash
scripts/verify_current_state.sh
```

Resultado observado:

```text
scripts/verify_current_state.sh
- 41 passed
```

Limitações, gaps e riscos:

- Esta entrega melhora a governança documental, mas não muda o status real dos itens da taxonomia.
- Itens hoje em `draft` ou `testing` continuam exigindo validação em vídeo antes de sustentarem KPI final estável.

---

## Ciclo — Correção estrutural do launcher `run_scout.sh`

Fase atual declarada: `Fase 8 — UI Streamlit funcional do fluxo manual`.

Status: `FUNCIONANDO COM EVIDÊNCIA`

Implementado / executado:

- Correção do falso positivo de readiness em `scripts/run_scout.sh`:
  - o script agora verifica se a porta já está em uso antes de lançar o Streamlit
  - o script não deve mais imprimir `server_ready=` quando a porta já estiver ocupada por outro processo
- Correção da abertura automática do navegador:
  - o script deixou de depender de `python3 -m webbrowser`, que retornava sucesso falso neste ambiente enquanto o `gio` falhava
  - o script agora tenta abrir a URL com opener explícito do sistema e, se falhar, imprime fallback claro para abertura manual
- O loop de readiness agora também considera a vida do processo recém-lançado, reduzindo risco de tratar processo morto como subida bem-sucedida.
- Foram adicionados testes de regressão em `tests/test_smoke.py` para cobrir:
  - falha rápida quando a porta já está ocupada
  - mensagem de fallback quando a abertura automática do navegador falha

Comandos executados:

```bash
bash -n scripts/run_scout.sh
python3 -m pytest tests/test_smoke.py -q
scripts/verify_current_state.sh
```

Resultado observado:

```text
bash -n scripts/run_scout.sh
- run_scout_syntax_ok

python3 -m pytest tests/test_smoke.py -q
- 11 passed in 5.70s

scripts/verify_current_state.sh
- 43 passed
```

Limitações, gaps e riscos:

- A abertura automática do navegador continua dependente das capacidades do ambiente gráfico local do usuário.
- A correção garante fallback claro; não garante que todo ambiente Linux/WSL conseguirá abrir o browser automaticamente.

---

## Execução 1 — Fechamento da operação local básica

Fase atual declarada: `Fase 10 — README e operação local`.

Status: `FUNCIONANDO COM EVIDÊNCIA`

Implementado / executado:

- Correção do comando de inicialização do banco no `README.md`:
  - de `python -m scoutpraia.core.database`
  - para `python3 -m scoutpraia.core.database`
- Validação do ambiente Python local com `python3 --version`.
- Validação da inicialização do banco com `python3 -m scoutpraia.core.database`.
- Validação do launcher `scripts/run_scout.sh` em porta livre usando `--no-browser`.
- Verificação visual do carregamento do `Dashboard` no navegador automatizado em `http://localhost:8521`.
- Execução do gate técnico completo do repositório após o ajuste documental.

Comandos executados:

```bash
python3 --version
python3 -m scoutpraia.core.database
scripts/run_scout.sh --no-browser --port 8521
scripts/verify_current_state.sh
```

Resultado observado:

```text
python3 --version
- Python 3.12.3

python3 -m scoutpraia.core.database
- Banco inicializado em data/scoutpraia.db

scripts/run_scout.sh --no-browser --port 8521
- server_ready=http://localhost:8521

verificação visual do Dashboard
- página carregada com navegação lateral visível em `Dashboard`

scripts/verify_current_state.sh
- 43 passed
```

Limitações, gaps e riscos:

- A porta padrão `8516` estava ocupada no momento desta execução; por isso a prova operacional do launcher foi feita em `8521`.
- O gate passou com arquivos não rastreados já existentes no workspace (`CALUDE.md` e arquivos em `docs/sources/`), que não fizeram parte desta execução.

---

## Execução 2 — Ensaio operacional final com vídeo real e geração dos 3 relatórios pela UI

Fase atual declarada: `Fase 9 — Validação operacional com vídeo real`.

Status: `FUNCIONANDO COM EVIDÊNCIA`

Premissas desta execução:

- O estado atual do jogo `CEPRAEA x CAMPINAS`, das atletas, dos eventos, das posses e dos sets foi tratado como dado real pré-existente criado/editado manualmente pelo usuário.
- O arquivo de contrato canônico do MVP usado nesta execução foi `docs/MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md`; o caminho legado na raiz permanece removido por migração estrutural anterior.

Implementado / executado:

- Validação do estado real persistido antes do ensaio:
  - `1` jogo cadastrado com vídeo real local.
  - `8` eventos persistidos.
  - `4` sets persistidos.
  - `9` posses persistidas.
  - `13` relatórios existentes antes da nova geração.
- Subida de uma instância dedicada da aplicação para ensaio em `http://localhost:8522`.
- Ensaio automatizado da UI real com navegador headless temporário via Playwright instalado por `npm` em `/tmp/scout-playwright`.
- Verificação da página `Marcação` com o jogo real:
  - cabeçalho `Marcação` carregado;
  - linha do jogo carregada como `Jogo 1 | Etapa do Circuito Brasileiro 2026 | Classificatória`;
  - screenshot salva em `/tmp/scout-playwright/exec2-tagging.png`.
- Geração dos 3 relatórios pela página `Relatórios`:
  - `Gerar coletivo`;
  - `Gerar individual`;
  - `Gerar adversária`.
- Verificação pós-ensaio:
  - contador de relatórios passou de `13` para `16`;
  - os 3 novos arquivos HTML existem fisicamente em `storage/reports/`;
  - screenshot salva em `/tmp/scout-playwright/exec2-reports.png`.

Comandos executados:

```bash
python3 - <<'PY'
from scoutpraia.core.database import create_db_and_tables, engine
from scoutpraia.models.match import Match, SetSegment, Possession
from scoutpraia.models.event import Event
from scoutpraia.models.report import Report
from sqlmodel import Session, select
create_db_and_tables()
with Session(engine) as s:
    print('matches', len(s.exec(select(Match)).all()))
    print('events', len(s.exec(select(Event)).all()))
    print('sets', len(s.exec(select(SetSegment)).all()))
    print('possessions', len(s.exec(select(Possession)).all()))
    print('reports', len(s.exec(select(Report)).all()))
PY

./scripts/run_scout.sh --no-browser --port 8522

mkdir -p /tmp/scout-playwright
cd /tmp/scout-playwright
npm init -y
npm install playwright@1.54.2
npx playwright install chromium
node /tmp/scout-playwright/exec2-ui.js

python3 - <<'PY'
from pathlib import Path
from scoutpraia.core.database import create_db_and_tables, engine
from scoutpraia.models.report import Report
from sqlmodel import Session, select
create_db_and_tables()
with Session(engine) as s:
    reports=s.exec(select(Report).order_by(Report.generated_at)).all()
    print('report_count', len(reports))
    for r in reports[-3:]:
        print(r.report_type, r.file_path, Path(r.file_path).exists())
PY
```

Resultado observado:

```text
estado pré-ensaio
- matches=1
- events=8
- sets=4
- possessions=9
- reports=13

launcher dedicado
- server_ready=http://localhost:8522

UI real — Marcação
- dashboard_loaded=yes
- tagging_heading=ok
- tagging_match_line=Jogo 1 | Etapa do Circuito Brasileiro 2026 | Classificatória
- tagging_screenshot=/tmp/scout-playwright/exec2-tagging.png

UI real — Relatórios
- reports_heading=ok
- reports_count_before=13
- collective_success=Relatório coletivo gerado: /home/davis/SCOUT/storage/reports/match-1_collective_2026-06-08t15-30-35-236624utc.html
- individual_success=Relatório individual gerado: /home/davis/SCOUT/storage/reports/match-1_individual_fernanda-campbell_2026-06-08t15-30-35-695231utc.html
- opponent_success=Relatório de adversária gerado: /home/davis/SCOUT/storage/reports/match-1_opponent_campinas-360_2026-06-08t15-30-35-964601utc.html
- reports_count_after=16
- reports_screenshot=/tmp/scout-playwright/exec2-reports.png

validação pós-ensaio
- report_count=16
- collective ... True
- individual ... True
- opponent ... True
```

Limitações, gaps e riscos:

- A taxonomia usada continua `draft`; esta execução prova operação real da UI e geração de relatórios, mas não converte KPI em evidência metodológica estável.
- A automação de navegador exigiu instalação temporária de Playwright via `npm` em `/tmp/scout-playwright` porque:
  - `python3 -m pip install --user playwright` falhou por `externally-managed-environment` (PEP 668);
  - `python3 -m venv /tmp/scoutpraia-playwright-venv` falhou por ausência de `ensurepip` / `python3-venv`.
- O ensaio gerou 3 novos relatórios reais no banco e em `storage/reports/`; isso faz parte da prova operacional, não de um teste sintético.

---

## Ciclo — Ajustes finais mínimos em `docs/SOURCES_ORGANIZATION_PLAN.md`

Fase atual declarada: `Fase documental de governança de fontes`.

Status: `AJUSTADO COM EVIDÊNCIA`

Implementado / executado:

- Ajuste de P1 para evitar prova instável:
  - removida a formulação que sugeria ausência total de referências por `grep` amplo em `docs/`;
  - substituída por critério operacional correto: o arquivo `Plano de Pesquisa para Scout Esportivo.md` não é referenciado por contratos, serviços, testes, scripts ou outros documentos operacionais fora do próprio plano.
- Ajuste do gate para separar explicitamente:
  - `execução parcial válida do plano`
  - `execução completa do plano`
- Ajuste de A4 e A5 para exigir registro de `DOI` como metadado preferencial junto da URL canônica, mesmo quando houver PDF local.

Comandos executados:

```bash
git diff --check
scripts/verify_current_state.sh
```

Resultado observado:

```text
git diff --check
- sem erros

scripts/verify_current_state.sh
- 43 passed
```

Limitações, gaps e riscos:

- O arquivo `docs/SOURCES_ORGANIZATION_PLAN.md` está agora coerente para execução, mas continua sendo um plano; ele não fecha por si só os gaps G1, G5 e G7.
- `README.md` permanece modificado pela Execução 1 e `docs/IMPLEMENTATION_PROGRESS.md` por registros desta sessão; isso faz parte do estado intencional atual do workspace.

---

## Execução — Ações A1–A7 de `docs/SOURCES_ORGANIZATION_PLAN.md`

Fase atual declarada: `Governança de fontes e rastreabilidade taxonômica`.

Status: `PARCIAL COM EVIDÊNCIA`

Implementado / executado:

- `A1` executada:
  - removido `docs/sources/Plano de Pesquisa para Scout Esportivo.md` do workspace.
- `A2` executada:
  - `docs/sources/README.md` agora documenta `regras.md` como artefato derivado, com limitações explícitas.
- `A3` executada:
  - `docs/sources/README.md` agora registra `SRC-SYNTHESIS-BH` com papel de curadoria secundária e proibição explícita de uso como fonte primária.
- `A4` executada:
  - adicionados arquivos locais para `SRC-NOTATIONAL-BH`:
    - `docs/sources/notational_analysis_bh_iannaccone_2022.pdf`
    - `docs/sources/womens_bh_statistics_kazan_2022.pdf`
- `A5` executada:
  - adicionados arquivos locais para `SRC-OBS-MEASUREMENT`:
    - `docs/sources/primer_observational_measurement_2017.html`
    - `docs/sources/validation_observational_instrument_handball_2023.html`
  - decisão técnica adotada:
    - as páginas oficiais da PMC foram salvas em HTML porque o download direto dos PDFs retornou challenge intermediário (`Preparing to download ...`) no ambiente atual.
    - isso mantém rastreabilidade local verificável sem declarar PDF inexistente como prova válida.
- `A6` executada:
  - `docs/sources/README.md` agora tem coluna `Arquivo local`, seção `Artefatos derivados`, `SRC-SYNTHESIS-BH` e `SRC-OPENAI-EVALS` com arquivo local.
- `A7` executada:
  - `docs/taxonomy_dictionary.md` agora tem coluna `Fonte` nas tabelas de eventos com distinção explícita entre `SRC-*` e `coach_decision`.

Impacto adicional analisado de `docs/sources/Working-with-evals.md`:

- O arquivo muda o diagnóstico do plano para `SRC-OPENAI-EVALS`:
  - deixa de ser "fonte sem arquivo local";
  - passa a ser fonte com snapshot local verificável.
- O conteúdo do arquivo registra um risco estrutural novo para Fase 2:
  - a plataforma Evals entra em `read-only` em `2026-10-31`;
  - o desligamento está previsto para `2026-11-30`.
- Consequência para o repo:
  - `SRC-OPENAI-EVALS` deve permanecer como referência conceitual para ciclo de avaliação;
  - não deve ser promovido a dependência estratégica futura do ScoutPraia.
- Esse impacto foi refletido em:
  - `docs/sources/README.md`
  - `docs/SOURCES_ORGANIZATION_PLAN.md`

Comandos executados:

```bash
cd docs/sources
rm -f "Plano de Pesquisa para Scout Esportivo.md"
curl -L 'https://hummov.awf.wroc.pl/pdf-130277-103963?filename=Notational-analysis-of-be.pdf' -o notational_analysis_bh_iannaccone_2022.pdf
curl -L 'https://hrcak.srce.hr/file/403495' -o womens_bh_statistics_kazan_2022.pdf
curl -L 'https://pmc.ncbi.nlm.nih.gov/articles/PMC5426358/' -o primer_observational_measurement_2017.html
curl -L 'https://pmc.ncbi.nlm.nih.gov/articles/PMC10422213/' -o validation_observational_instrument_handball_2023.html
file notational_analysis_bh_iannaccone_2022.pdf womens_bh_statistics_kazan_2022.pdf primer_observational_measurement_2017.html validation_observational_instrument_handball_2023.html

git diff --check
scripts/verify_current_state.sh

[ ! -f "docs/sources/Plano de Pesquisa para Scout Esportivo.md" ] && echo "OK A1"
grep -q "SRC-SYNTHESIS-BH" docs/sources/README.md && echo "OK A3"
grep -q "Artefatos derivados" docs/sources/README.md && echo "OK A2"
grep -q "Arquivo local" docs/sources/README.md && echo "OK A6"
grep -q "| Fonte |" docs/taxonomy_dictionary.md && echo "OK A7"
ls docs/sources/notational_analysis_bh_iannaccone_2022.pdf docs/sources/womens_bh_statistics_kazan_2022.pdf && echo "OK A4"
ls docs/sources/primer_observational_measurement_2017.html docs/sources/validation_observational_instrument_handball_2023.html && echo "OK A5"
```

Resultado observado:

```text
file
- notational_analysis_bh_iannaccone_2022.pdf: PDF document
- womens_bh_statistics_kazan_2022.pdf: PDF document
- primer_observational_measurement_2017.html: HTML document
- validation_observational_instrument_handball_2023.html: HTML document

git diff --check
- sem erros

scripts/verify_current_state.sh
- 43 passed

checks do plano
- OK A1
- OK A2
- OK A3
- OK A4
- OK A5
- OK A6
- OK A7
```

O que ainda não está pronto:

- `G1` continua aberto:
  - taxonomia segue `draft`;
  - não houve validação observacional humana suficiente para promover itens a `testing`/`approved`.
- `G4` continua aberto:
  - `docs/evidence_matrix.md` ainda não referencia `SRC-SYNTHESIS-BH` como fonte auxiliar.
- `G5` continua aberto:
  - validação observacional humana completa ainda depende de rodada dedicada.
- `G7` foi fechado neste ciclo posterior:
  - `docs/validation_protocol.md` agora registra os critérios numéricos explícitos de `κ > 0.81`, `ICC >= 0.90` e `α >= 0.90`;
  - o protocolo também registra a ressalva metodológica de que esses números são critério prático do ScoutPraia, não corte universal absoluto.

Limitações, gaps e riscos:

- Os arquivos locais de `SRC-OBS-MEASUREMENT` ficaram em HTML oficial, não PDF, por limitação prática do mecanismo de download direto da PMC neste ambiente atual.
- `Working-with-evals.md` melhora a auditabilidade local de `SRC-OPENAI-EVALS`, mas também formaliza que a plataforma Evals está em deprecação; isso enfraquece o valor dessa fonte como base futura de Fase 2.
- `CALUDE.md` foi tratado como duplicata byte a byte de `AGENTS.md` e removido do workspace, não versionado.
- As fontes em `docs/sources/` passam a ser tratadas como artefatos locais intencionais a serem versionados nesta leva de publicação.

---

## Ciclo — Fechamento de G7 e preparação da publicação das fontes locais

Fase atual declarada: `Governança de fontes e protocolo de validação`.

Status: `AJUSTADO COM EVIDÊNCIA`

Implementado / executado:

- `docs/validation_protocol.md` recebeu critérios numéricos explícitos para confiabilidade observacional:
  - `κ > 0.81`
  - `ICC >= 0.90`
  - `α >= 0.90`
- Os critérios foram documentados como regra prática do ScoutPraia, com ressalva explícita de que a literatura observacional não oferece corte universal único.
- `docs/SOURCES_ORGANIZATION_PLAN.md` foi alinhado ao novo estado:
  - `G7` passou a constar como resolvido;
  - `SRC-OPENAI-EVALS` passou a constar com arquivo local (`Working-with-evals.md`) e impacto de deprecação;
  - o inventário agora reflete os arquivos realmente presentes após A1–A7.
- Os não rastreados foram revisados:
  - `CALUDE.md` removido por ser duplicata de `AGENTS.md`;
  - arquivos de `docs/sources/` mantidos como artefatos intencionais para versionamento.

Comandos executados:

```bash
diff -q AGENTS.md CALUDE.md
rm -f CALUDE.md
git diff --check
scripts/verify_current_state.sh
```

Resultado observado:

```text
diff -q AGENTS.md CALUDE.md
- sem diferenças

git diff --check
- sem erros

scripts/verify_current_state.sh
- 43 passed
```

Limitações, gaps e riscos:

- `G1`, `G4` e `G5` continuam abertos.
- O fechamento de `G7` usa arquivos locais HTML da PMC; a base é verificável, mas não é cópia PDF binária do publisher.

---

## Ciclo — Fechamento de G4 em `docs/evidence_matrix.md`

Fase atual declarada: `Governança de evidência e taxonomia`.

Status: `AJUSTADO COM EVIDÊNCIA`

Implementado / executado:

- `docs/evidence_matrix.md` passou a referenciar `SRC-SYNTHESIS-BH` como fonte auxiliar explícita para:
  - `two_point_goal`
  - `spin_shot`
  - `inflight_goal`
  - `zone`
- A inclusão foi feita sem trocar a precedência das fontes primárias:
  - `SRC-IHF-RULES` continua a base normativa;
  - `SRC-NOTATIONAL-BH` continua a base científica específica;
  - `SRC-SYNTHESIS-BH` entra apenas como curadoria auxiliar que priorizou os papers.

Comandos executados:

```bash
git diff --check
scripts/verify_current_state.sh
```

Resultado observado:

```text
git diff --check
- sem erros

scripts/verify_current_state.sh
- 43 passed
```

O que ainda não está pronto:

- `G1` continua aberto: taxonomia segue `draft`.
- `G5` continua aberto: validação observacional humana completa ainda não foi concluída.

Limitações, gaps e riscos:

- `SRC-SYNTHESIS-BH` permanece fonte secundária; sua inclusão na matriz não autoriza tratá-la como substituto das fontes primárias.

---

## Ciclo — Correção segura de `scripts/setup_venv.sh`

Fase atual declarada: `Apoio operacional local do MVP`.

Status: `AJUSTADO COM EVIDÊNCIA`

Implementado / executado:

- Criação de proteção explícita em `scripts/setup_venv.sh` para impedir remoção automática da `.venv` existente.
- Inclusão de `--force` como único caminho para recriar a virtualenv já existente.
- Inclusão de `--help`.
- Inclusão de validação prévia do caminho de `requirements.txt`.
- Inclusão de variáveis opcionais:
  - `SCOUTPRAIA_VENV_DIR`
  - `SCOUTPRAIA_REQUIREMENTS`
- Ajuste das mensagens finais para refletir o caminho real da virtualenv criada.

Comandos executados:

```bash
bash -n scripts/setup_venv.sh
scripts/setup_venv.sh --help
scripts/setup_venv.sh
tmpdir=$(mktemp -d)
printf 'pytest==9.0.3\n' > "$tmpdir/requirements.txt"
SCOUTPRAIA_VENV_DIR="$tmpdir/venv" SCOUTPRAIA_REQUIREMENTS="$tmpdir/requirements.txt" scripts/setup_venv.sh
"$tmpdir/venv/bin/python" -m pytest --version
scripts/verify_current_state.sh
```

Resultado observado:

```text
bash -n scripts/setup_venv.sh
- ok

scripts/setup_venv.sh --help
- ajuda exibida com --force e variáveis opcionais

scripts/setup_venv.sh
- bloqueou recriação silenciosa:
  "ERRO: a virtualenv já existe em /home/davis/SCOUT/.venv"
  "Use --force para remover e recriar."

SCOUTPRAIA_VENV_DIR=... SCOUTPRAIA_REQUIREMENTS=... scripts/setup_venv.sh
- criou virtualenv temporária com virtualenv
- instalou pytest==9.0.3
- pytest --version retornou 9.0.3

scripts/verify_current_state.sh
- 43 passed
```

O que ainda não está pronto:

- `README.md` e `docs/IMPLEMENTATION_STEPS_AI.md` ainda descrevem o fluxo principal com `python3 -m venv` / `python -m venv`.
- Este ciclo corrigiu o script, mas ainda não consolidou o fallback documental para ambientes sem `ensurepip`.

Limitações, gaps e riscos:

- O script continua dependendo de `virtualenv` instalado no ambiente.
- A recriação real da `.venv` do repositório com `--force` não foi executada neste ciclo para evitar apagar o ambiente local ativo sem necessidade.

---

## Ciclo — Alinhamento documental do fallback de virtualenv

Fase atual declarada: `Apoio operacional local do MVP`.

Status: `AJUSTADO COM EVIDÊNCIA`

Implementado / executado:

- `README.md` passou a documentar explicitamente o fallback com `scripts/setup_venv.sh` quando `python3 -m venv .venv` falhar por ausência de `ensurepip` / `python3-venv`.
- `docs/IMPLEMENTATION_STEPS_AI.md` passou a registrar o mesmo fallback como caminho operacional secundário, sem substituir o fluxo padrão com `venv`.
- O texto documental agora está coerente com:
  - o comportamento implementado em `scripts/setup_venv.sh`;
  - a limitação real já observada neste ambiente para `python3 -m venv`.

Comandos executados:

```bash
git diff --check
scripts/verify_current_state.sh
```

Resultado observado:

```text
git diff --check
- sem erros

scripts/verify_current_state.sh
- 43 passed
```

O que ainda não está pronto:

- `requirements.txt` e `scripts/run_scout.sh` continuam com mudanças locais ainda não consolidadas neste ciclo.

Limitações, gaps e riscos:

- O fallback documental continua dependendo de `virtualenv` instalado no ambiente local.
- O fluxo padrão do projeto permanece sendo `python3 -m venv .venv`; o fallback existe para ambientes que não oferecem `ensurepip`.

---

## Ciclo — Consolidação da leva de `requirements.txt` e `scripts/run_scout.sh`

Fase atual declarada: `Apoio operacional local do MVP`.

Status: `AJUSTADO COM EVIDÊNCIA`

Implementado / executado:

- `requirements.txt` passou a fixar versões exatas do conjunto atualmente provado no ambiente local:
  - `streamlit==1.58.0`
  - `pandas==3.0.3`
  - `sqlmodel==0.0.38`
  - `plotly==6.8.0`
  - `jinja2==3.1.2`
  - `python-dotenv==1.2.2`
  - `pydantic==2.13.4`
  - `pytest==9.0.3`
- `scripts/run_scout.sh` passou a ativar automaticamente `ROOT_DIR/.venv` quando o ambiente existe, antes de resolver `streamlit`.
- `README.md` passou a explicar explicitamente esse comportamento do launcher.

Comandos executados:

```bash
python3 - <<'PY'
import importlib.metadata as m
for p in ['streamlit','pandas','sqlmodel','plotly','Jinja2','python-dotenv','pydantic','pytest']:
    print(f'{p}={m.version(p)}')
PY
bash -n scripts/run_scout.sh
tmpdir=$(mktemp -d)
virtualenv "$tmpdir/venv"
"$tmpdir/venv/bin/pip" install --dry-run -r requirements.txt
env -i HOME="$HOME" PATH=/usr/bin:/bin /bin/bash scripts/run_scout.sh --no-browser --port 8524
scripts/verify_current_state.sh
```

Resultado observado:

```text
python3 metadata
- streamlit=1.58.0
- pandas=3.0.3
- sqlmodel=0.0.38
- plotly=6.8.0
- Jinja2=3.1.2
- python-dotenv=1.2.2
- pydantic=2.13.4
- pytest=9.0.3

bash -n scripts/run_scout.sh
- ok

pip install --dry-run -r requirements.txt
- resolução das dependências passou em virtualenv temporária

env -i ... scripts/run_scout.sh --no-browser --port 8524
- launcher subiu mesmo com PATH mínimo
- `server_ready=http://localhost:8524`
- prova de que a ativação automática da `.venv` ocorreu antes da checagem de `streamlit`

scripts/verify_current_state.sh
- 43 passed
```

O que ainda não está pronto:

- Esta leva ainda não foi separada em commit próprio neste ciclo.

Limitações, gaps e riscos:

- Os pins de `requirements.txt` refletem o ambiente validado neste momento; futuras atualizações exigem nova prova reproduzível.
- `scripts/run_scout.sh` continua dependendo de uma `.venv` válida quando a intenção for isolar o ambiente do projeto do ambiente global.

---

## Ciclo — Checklist operacional editável para fechamento de `G1` e `G5`

Fase atual declarada: `Governança documental de validação humana e taxonomia`.

Status: `AJUSTADO COM EVIDÊNCIA`

Implementado / executado:

- `docs/validation_protocol.md` passou a conter um checklist operacional editável específico para:
  - congelamento da rodada;
  - evidência mínima para fechar `G5`;
  - revisão item a item para fechar `G1`;
  - gate de promoção de status;
  - critério formal de fechamento.
- `docs/SOURCES_ORGANIZATION_PLAN.md` passou a conter checklists explícitos dentro dos próprios gaps `G1` e `G5`.
- O objetivo foi eliminar lacuna operacional entre:
  - plano textual de fechamento;
  - execução humana real;
  - atualização documental após a rodada.

Comandos executados:

```bash
git diff --check
scripts/verify_current_state.sh
```

Resultado observado:

```text
git diff --check
- sem erros

scripts/verify_current_state.sh
- 43 passed
```

O que ainda não está pronto:

- `G1` continua aberto até a rodada humana promover ao menos parte da taxonomia para além de `draft`.
- `G5` continua aberto até a rodada humana ser executada e anexada com evidência real.

Limitações, gaps e riscos:

- O checklist reduz ambiguidade operacional, mas não substitui a execução humana com vídeo real.
- Nenhum status da taxonomia foi promovido neste ciclo; a mudança aqui é de governança e execução documental.
