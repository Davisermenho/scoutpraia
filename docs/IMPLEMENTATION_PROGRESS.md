# ScoutPraia — Progresso de Implementação e Evidência

Este arquivo acompanha o que foi implementado, o que foi verificado e o que ainda não está pronto. Ele deve ser atualizado a cada ciclo de implementação.

Regra: uma etapa só pode ser marcada como `FUNCIONANDO` quando houver evidência reproduzível por comando, teste ou arquivo verificável.

---

## Estado atual

Última atualização: `2026-06-06`

Status geral: `BASE TÉCNICA INICIAL FUNCIONANDO`

Importante: o MVP completo ainda **não** está pronto. A base de projeto, banco, modelos iniciais, seed de taxonomia e smoke tests estão funcionando. Marcação real, upload/cadastro de jogos completo, geração real de clipes, analytics completo e relatórios finais ainda não foram implementados.

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
date_utc=2026-06-06T07:41:37Z
cwd=/home/davis/SCOUT
git_branch=main
git_head=60e4267

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
tests/test_match_service.py . [ 10%]
tests/test_real_video_integration.py .. [ 30%]
tests/test_smoke.py ....... [100%]
10 passed

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
- `event_service.py`: criação de evento com validação contra taxonomia e zona
- `clip_service.py`: cálculo de janela e nome de clipe
- `validation_service.py`: cálculo simples de concordância
- `analytics_service.py`: KPIs coletivos mínimos
- `report_service.py`: renderização Jinja básica

Evidência:

- `clip_window` e `probe_video_metadata` testados em `tests/test_smoke.py`.

Pendências:

- `clip_service.py` ainda não executa `ffmpeg` nem cria registro `Clip`.
- `analytics_service.py` ainda não cobre todos os KPIs do MVP.
- `report_service.py` ainda não salva relatório nem cria registro `Report`.
- `validation_service.py` ainda não persiste `CodingAgreement`.

### Fase 7 — Interface Streamlit

Status: `PARCIAL`

Implementado:

- `app.py` com navegação local simples.
- página de Jogos com cadastro básico real; Dashboard, Marcação, Relatórios e Adversárias ainda são placeholders.

Evidência:

- importação do app e pacote passa indiretamente nos testes.

Pendências:

- Ainda não foi feita verificação visual com `streamlit run app.py`.
- Cadastro básico de jogos foi implementado na página Jogos; ainda falta associar elenco/roster ao jogo.
- Tela real de marcação ainda não implementada.
- Relatórios na UI ainda não implementados.

### Fase 8 — Testes

Status: `FUNCIONANDO COMO SMOKE TESTS`

Implementado:

- `tests/test_smoke.py`
- 7 testes passando

Evidência:

- `python3 -m pytest` retorna `10 passed`.

Limite atual:

- Os testes ainda são smoke tests. Faltam testes de fixture de jogo sintético, KPIs completos, clipes reais e relatórios completos.

---

## Pendências reais para MVP completo

O ScoutPraia ainda precisa de:

1. Testes completos de modelos e serviços.
2. Seed de dados de exemplo ou fixture sintética de jogo.
3. associar elenco disponível ao jogo com `match_roster`.
4. `clip_service.py` com `ffmpeg` real.
5. evoluir cadastro de atletas, adversárias e jogos com edição/exclusão.
6. Tela de marcação real com criação/edição/exclusão de eventos.
7. Analytics completo conforme o MVP.
8. Relatórios HTML completos e persistidos.
9. Validação operacional com vídeo real.
10. Verificação visual do Streamlit.
11. README operacional completo após a implementação funcional.
12. Commit das mudanças atuais quando o ciclo for aprovado.

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
