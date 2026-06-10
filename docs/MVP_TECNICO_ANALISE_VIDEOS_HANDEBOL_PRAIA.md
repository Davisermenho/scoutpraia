---
tipo: contrato_produto
status: REFERÊNCIA_ESTÁVEL
não_alterar_sem: nova versão explícita do MVP
lido_antes_de_implementar: obrigatório
última_atualização: 2026-06-10
escopo_proibido: "React, FastAPI, PostgreSQL, autenticação, multiusuário, deploy, API pública"
documentos_de_execução:
  - docs/IMPLEMENTATION_STEPS_AI.md  # ordem de execução para agentes
  - docs/IMPLEMENTATION_PROGRESS.md  # estado atual
  - docs/taxonomy_dictionary.md      # taxonomia operacional
---

# ScoutPraia — MVP Técnico Completo (Arquitetura Python-Only)

## ESCOPO PROIBIDO — ler antes de qualquer implementação

```
MUST NOT: frontend React
MUST NOT: backend FastAPI separado
MUST NOT: API REST completa ou API pública
MUST NOT: banco PostgreSQL
MUST NOT: autenticação ou multiusuário
MUST NOT: deploy em servidor
MUST NOT: versionar vídeos, banco, clipes, relatórios, .env, .venv, tmp/ ou binários locais
```

Para a ordem de implementação, seguir `docs/IMPLEMENTATION_STEPS_AI.md`.

---

## 1. Objetivo

Construir o `ScoutPraia` como um sistema local, de uso individual por `Davi Sermenho`, para analisar vídeos exatos de jogos de handebol de praia e entregar:

- scout individual por atleta
- scout coletivo por jogo
- feedback com clipes cortados
- análise de adversárias
- plano objetivo para o próximo jogo

O foco do MVP é `resultado operacional rápido`, não arquitetura corporativa.

---

## 2. Premissas do projeto

- o sistema será usado apenas por `Davi Sermenho`
- o sistema rodará localmente
- os jogos serão analisados a partir de `vídeos já baixados`
- não há necessidade inicial de backend separado
- não há necessidade inicial de frontend web separado
- não há necessidade inicial de API pública

Conclusão prática:

O `ScoutPraia` deve ser um `monólito local em Python`.

---

## 3. Decisão de arquitetura

### 3.1 O que NÃO será feito no MVP

- frontend React
- backend FastAPI separado
- API REST completa
- banco PostgreSQL
- autenticação
- multiusuário
- deploy em servidor

### 3.2 O que será feito

- interface local com `Streamlit`
- banco local com `SQLite`
- processamento com `Python`
- métricas com `Pandas`
- cortes de vídeo com `FFmpeg`
- geração de relatórios em `HTML` e opcionalmente `PDF`

Essa é a arquitetura correta porque reduz custo, tempo de implementação e complexidade.

---

## 4. Resultado esperado do MVP

Ao final de cada jogo, o sistema deve permitir:

- cadastrar o jogo e associar o vídeo
- assistir o vídeo dentro da ferramenta
- marcar eventos rapidamente
- gerar clipes automáticos por evento
- consolidar scout individual e coletivo
- gerar relatório acionável para comissão e atletas

Meta operacional:

- `até 30 min`: scout bruto + clipes principais
- `até 2 h`: relatório coletivo
- `até 24 h`: relatórios individuais e plano da próxima adversária

---

## 5. Stack técnica

## 5.1 Stack principal

- `Python 3.11+`
- `Streamlit`
- `SQLite`
- `Pandas`
- `FFmpeg`
- `Plotly`
- `SQLModel` ou `sqlite3`
- `Jinja2`

## 5.2 Bibliotecas recomendadas

- `streamlit` — interface local
- `pandas` — agregações e KPIs
- `sqlmodel` — modelagem simples com SQLite
- `alembic` — opcional, se quiser versionar schema
- `plotly` — gráficos
- `jinja2` — geração de relatórios HTML
- `python-dotenv` — configurações locais
- `pydantic` — validação de dados
- `opencv-python` — opcional para evolução futura

---

## 6. Arquitetura do sistema

## 6.1 Visão geral

```text
[Streamlit UI]
      |
      v
[Serviços Python]
  |      |      |
  |      |      +--> [FFmpeg]
  |      |
  |      +---------> [SQLite]
  |
  +---------------> [Arquivos locais: vídeos, clipes, relatórios]
```

## 6.2 Estrutura lógica

- interface única local
- persistência local em arquivo `.db`
- armazenamento em pastas locais
- processamento síncrono no MVP

Não há necessidade de fila, workers ou microsserviços nesta fase.

---

## 7. Estrutura de diretórios recomendada

```text
scoutpraia/
  app.py
  requirements.txt
  README.md
  .env
  data/
    scoutpraia.db
  storage/
    videos/
    clips/
    reports/
    thumbnails/
  scoutpraia/
    core/
      config.py
      paths.py
      database.py
    models/
      team.py
      player.py
      opponent.py
      match.py
      event.py
      taxonomy.py
      validation.py
      clip.py
      report.py
    services/
      video_service.py
      event_service.py
      clip_service.py
      validation_service.py
      analytics_service.py
      report_service.py
    pages/
      dashboard.py
      matches.py
      tagging.py
      reports.py
      opponents.py
    templates/
      report_collective.html
      report_individual.html
      report_opponent.html
    utils/
      timecode.py
      zones.py
      exports.py
```

---

## 8. Fluxo operacional do ScoutPraia

## 8.1 Fluxo principal

1. abrir o `ScoutPraia`
2. cadastrar jogo
3. associar vídeo local
4. cadastrar elenco disponível
5. assistir e marcar eventos
6. gerar clipes automáticos
7. revisar métricas
8. gerar relatório coletivo
9. gerar relatório individual
10. gerar análise da próxima adversária

## 8.2 Fluxo realista por jogo

### Antes do jogo

- cadastrar adversária
- registrar contexto da partida
- preparar categorias de observação

### Pós-jogo imediato

- subir vídeo
- marcar eventos prioritários
- gerar clipes de correção rápida

### Pós-jogo completo

- revisar eventos
- consolidar KPIs
- gerar relatórios

---

## 9. Modelo de dados

## 9.1 Entidades principais

### `players`

- `id`
- `name`
- `shirt_number`
- `primary_role`
- `secondary_role`
- `active`

### `opponents`

- `id`
- `name`
- `category`
- `notes`

### `matches`

- `id`
- `match_date`
- `competition_name`
- `phase`
- `opponent_id`
- `video_path`
- `duration_seconds`
- `video_width`
- `video_height`
- `video_fps`
- `video_codec`
- `final_score_team`
- `final_score_opponent`
- `notes`

### `match_roster`

- `id`
- `match_id`
- `player_id`
- `available`
- `starter`

### `sets`

- `id`
- `match_id`
- `set_number`
- `start_second`
- `end_second`
- `score_team`
- `score_opponent`

### `possessions`

- `id`
- `match_id`
- `set_id`
- `team_side`
- `start_second`
- `end_second`
- `result`
- `points_scored`
- `points_conceded`

### `events`

- `id`
- `match_id`
- `set_id`
- `possession_id`
- `taxonomy_version_id`
- `event_type`
- `event_subtype`
- `player_id`
- `secondary_player_id`
- `team_side`
- `timestamp_second`
- `outcome`
- `zone`
- `points_value`
- `notes`

### `taxonomy_versions`

- `id`
- `name`
- `status`
- `created_at`
- `approved_at`
- `notes`

Status sugeridos:

- `draft`
- `testing`
- `approved`
- `archived`

### `event_definitions`

- `id`
- `taxonomy_version_id`
- `event_type`
- `definition`
- `include_when`
- `exclude_when`
- `decision_rule`
- `evidence_type`
- `active`

Tipos de evidência sugeridos:

- `official_rule`
- `scientific_literature`
- `coach_decision`
- `practical_hypothesis`

### `coding_sessions`

- `id`
- `match_id`
- `taxonomy_version_id`
- `coder_name`
- `session_type`
- `started_at`
- `finished_at`
- `notes`

Tipos de sessão:

- `primary`
- `intraobserver_retest`
- `interobserver_review`

### `coding_agreements`

- `id`
- `match_id`
- `taxonomy_version_id`
- `comparison_type`
- `agreement_percent`
- `total_events_compared`
- `total_disagreements`
- `disagreements_json`
- `approved`
- `notes`

### `clips`

- `id`
- `match_id`
- `event_id`
- `player_id`
- `clip_path`
- `start_second`
- `end_second`
- `label`

### `reports`

- `id`
- `match_id`
- `report_type`
- `generated_at`
- `file_path`
- `payload_json`

---

## 10. Taxonomia de eventos

## 10.1 Eventos obrigatórios do MVP

### Ataque

- `shot_attempt`
- `goal_scored`
- `shot_missed`
- `turnover`
- `technical_error`
- `assist`
- `two_point_attempt`
- `two_point_goal`
- `specialist_attempt`
- `specialist_goal`
- `spin_shot`
- `inflight_attempt`
- `inflight_goal`

### Defesa

- `defensive_stop`
- `steal`
- `block`
- `forced_error`
- `goal_conceded`
- `defensive_breakdown`

### Goleira

- `save`
- `save_shootout`
- `goalkeeper_distribution`

### Transição

- `fast_break_for`
- `fast_break_against`
- `transition_recovery_good`
- `transition_recovery_bad`

### Situações especiais

- `shootout_attempt`
- `shootout_goal`
- `shootout_miss`
- `timeout`
- `set_end`

---

## 10.2 Campos mínimos por evento

Cada evento deve registrar:

- jogo
- set
- versão da taxonomia
- tempo do vídeo
- atleta principal
- atleta secundária, quando houver
- tipo do evento
- resultado
- zona
- valor em pontos
- observação curta opcional

---

## 10.3 Dicionário operacional obrigatório

Cada evento da taxonomia deve ter uma definição operacional antes de ser usado em relatório.

Formato mínimo:

| Campo | Descrição |
| --- | --- |
| `event_type` | nome técnico do evento |
| `definition` | o que conta como esse evento |
| `include_when` | situações em que deve ser marcado |
| `exclude_when` | situações parecidas que não devem ser marcadas |
| `decision_rule` | regra objetiva para resolver dúvida |
| `evidence_type` | regra oficial, literatura, decisão técnica ou hipótese prática |

Regra do MVP:

- evento sem definição operacional pode existir em `draft`, mas não deve entrar em KPI final
- evento com baixa concordância deve ser renomeado, fundido, dividido ou removido
- decisão prática do treinador deve ser marcada como decisão prática, não como regra oficial

Exemplo:

| `event_type` | Definição | Não marcar quando | Regra de decisão |
| --- | --- | --- | --- |
| `technical_error` | perda de posse por erro não causado diretamente por finalização ou defesa da goleira | arremesso defendido, bola fora após finalização, gol sofrido | se a posse acaba sem arremesso e sem ação defensiva clara, marcar como erro técnico |
| `specialist_goal` | gol convertido pela atleta atuando como especialista | gol comum, gol anulado, shoot-out ou gol já classificado por outra mecânica específica | marcar apenas com confirmação visual/operacional da especialista em quadra; `points_value=2` |
| `inflight_goal` | gol em que a atleta recebe/controla no ar e finaliza antes de tocar o solo | passe alto sem finalização, toque sem controle, gol comum | contar apenas se houver finalização válida antes do contato com o solo |
| `defensive_stop` | posse adversária encerrada sem gol por ação defensiva da equipe | erro adversário sem pressão clara, arremesso livre errado | marcar quando a defesa altera claramente a qualidade ou continuidade da posse |

## 10.4 Versionamento da taxonomia

A taxonomia deve ser versionada para evitar comparar jogos marcados com critérios diferentes.

Versões mínimas:

- `ScoutPraia v0.1` — primeira taxonomia testável
- `ScoutPraia v0.2` — ajustes após 1 jogo completo
- `ScoutPraia v1.0` — primeira versão aprovada para relatórios consistentes

Regra:

- todo evento salvo deve apontar para uma `taxonomy_version`
- relatórios devem informar a versão usada
- ao mudar definição de evento, criar nova versão em vez de alterar silenciosamente a anterior

## 10.5 Validação mínima da taxonomia

Antes de congelar `ScoutPraia v1.0`, executar uma validação simples com vídeo.

Procedimento mínimo:

1. marcar 1 jogo completo com `ScoutPraia v0.1`
2. remarcar uma amostra do mesmo jogo depois de pelo menos 24 horas
3. se houver outro analista disponível, comparar marcações independentes
4. listar divergências por `event_type`, atleta, zona e valor em pontos
5. corrigir definições operacionais ambíguas
6. aprovar apenas campos úteis, rápidos e consistentes

Critério prático inicial:

- campos centrais de pontuação, finalização e shoot-out devem ter concordância alta
- campos interpretativos, como `defensive_breakdown` e `forced_error`, podem ficar em `testing` até estabilizarem
- nenhum KPI crítico deve depender de evento ainda marcado como hipótese prática não validada

---

## 11. Zonas de quadra

Para o MVP, usar zonas discretas:

- `left_wing`
- `left_half`
- `center`
- `right_half`
- `right_wing`
- `6m_left`
- `6m_center`
- `6m_right`
- `shootout_lane`

Isso já suporta:

- mapa de finalização
- análise de vulnerabilidade defensiva
- tendência lateral de ataque

---

## 12. Interface do sistema

## 12.1 Telas do Streamlit

### Tela 1 — Dashboard

- jogos recentes
- resumo dos últimos KPIs
- atalhos para análise

### Tela 2 — Jogos

- cadastrar jogo
- carregar vídeo
- ver metadados do arquivo

### Tela 3 — Marcação

- player de vídeo
- relógio/timestamp
- painel de eventos
- escolha da atleta
- escolha da zona
- histórico de eventos recentes

### Tela 4 — Relatórios

- relatório coletivo
- relatório individual
- links para clipes

### Tela 5 — Adversárias

- histórico de jogos contra adversária
- tendências observadas
- plano de jogo

---

## 12.2 Requisitos da tela de marcação

Essa é a tela crítica do sistema.

Deve conter:

- vídeo em reprodução
- botão de pausa
- botão de retroceder alguns segundos
- timestamp visível
- botões grandes de eventos
- seleção rápida de atleta
- seleção de zona
- feed lateral de eventos salvos

---

## 12.3 Hotkeys recomendadas

- `G` = gol
- `S` = arremesso
- `E` = erro técnico
- `T` = turnover
- `R` = roubo
- `B` = bloqueio
- `D` = defesa da goleira
- `Q` = shoot-out

Se o Streamlit limitar atalhos globais, manter botões rápidos como fallback.

---

## 13. KPIs do MVP

## 13.1 KPIs coletivos

- pontos por posse
- gols por posse
- taxa de conversão ofensiva
- taxa de erro técnico
- stops defensivos por posse
- gols sofridos em transição
- eficiência de 2 pontos
- eficiência em shoot-out
- desempenho por set

## 13.2 KPIs individuais

- tentativas de finalização
- conversão total
- conversão por tipo
- conversão por zona
- turnovers
- erros técnicos
- roubos de bola
- bloqueios
- defesas
- participação direta em gols

## 13.3 KPIs por adversária

- lado preferido de ataque
- atleta que mais finaliza
- atleta que mais converte 2 pontos
- taxa de erro sob pressão
- vulnerabilidade em transição
- desempenho em shoot-out

---

## 14. Regras de corte de clipes

## 14.1 Regra padrão

Para cada evento:

- cortar `6 segundos antes`
- cortar `4 segundos depois`

## 14.2 Regras especiais

### Transição

- cortar `10 segundos antes`
- cortar `6 segundos depois`

### Shoot-out

- cortar `8 segundos antes`
- cortar `5 segundos depois`

### Sequência tática

- cortar `12 segundos antes`
- cortar `8 segundos depois`

## 14.3 Padrão de nome do clipe

```text
{data}_{adversaria}_{set}_{tempo}_{evento}_{atleta}.mp4
```

Exemplo:

```text
2026-06-06_argentina_set1_00-06-21_two_point_goal_maria-9.mp4
```

---

## 15. Processamento de vídeo

## 15.1 Entrada

- arquivo local `.mp4`
- arquivo local `.mov`, se necessário

## 15.2 Metadados extraídos

- duração
- resolução
- fps
- codec

## 15.3 Ferramenta

Usar `ffprobe` para leitura e `ffmpeg` para corte.

## 15.4 Exemplo de corte

```bash
ffmpeg -ss 00:06:15 -to 00:06:25 -i jogo.mp4 -c:v libx264 -c:a aac clip_saida.mp4
```

---

## 16. Relatórios

## 16.1 Relatório coletivo

Deve conter:

- placar
- resumo por set
- eficiência ofensiva
- eficiência defensiva
- transição
- shoot-out
- 3 pontos fortes
- 3 correções prioritárias
- links para clipes

## 16.2 Relatório individual

Deve conter:

- ações ofensivas
- ações defensivas
- erros recorrentes
- melhores lances
- mapa de finalização
- clipes positivos
- clipes de correção
- plano individual

## 16.3 Relatório de adversária

Deve conter:

- padrão ofensivo principal
- padrão defensivo principal
- atleta mais perigosa
- zonas preferenciais
- vulnerabilidades
- plano de ataque
- plano defensivo

---

## 17. Serviços internos do sistema

## 17.1 `video_service.py`

Responsável por:

- validar arquivo
- extrair metadados
- organizar paths

## 17.2 `event_service.py`

Responsável por:

- criar, editar e excluir eventos
- validar consistência
- relacionar eventos com posse e set

## 17.3 `clip_service.py`

Responsável por:

- calcular janela de corte
- executar `ffmpeg`
- salvar clipes

## 17.4 `validation_service.py`

Responsável por:

- carregar definições operacionais da taxonomia
- validar se eventos usados em KPIs pertencem a uma versão aprovada
- comparar duas sessões de marcação
- gerar lista de divergências por evento, atleta, zona e pontuação
- calcular concordância simples para calibração do MVP

No MVP, a concordância pode começar como percentual simples por categoria. Métricas mais formais, como kappa, podem entrar depois se houver necessidade.

## 17.5 `analytics_service.py`

Responsável por:

- calcular KPIs
- agrupar métricas por atleta, jogo, set e adversária

## 17.6 `report_service.py`

Responsável por:

- montar payload do relatório
- renderizar HTML
- exportar PDF, se necessário

---

## 18. Banco local

## 18.1 Escolha

Usar `SQLite`.

## 18.2 Justificativa

- simples
- local
- zero administração
- suficiente para uso individual
- bom desempenho para volume inicial

## 18.3 Local do arquivo

```text
data/scoutpraia.db
```

---

## 19. Configuração local

## 19.1 Variáveis mínimas

Arquivo `.env`:

```env
SCOUTPRAIA_DB_PATH=data/scoutpraia.db
SCOUTPRAIA_VIDEO_DIR=storage/videos
SCOUTPRAIA_CLIP_DIR=storage/clips
SCOUTPRAIA_REPORT_DIR=storage/reports
FFMPEG_BINARY=ffmpeg
FFPROBE_BINARY=ffprobe
```

---

## 20. Roadmap de implementação

## Fase 1 — Base local

- criar estrutura do projeto
- configurar SQLite
- cadastrar atletas
- cadastrar adversárias
- cadastrar jogos

## Fase 2 — Vídeo

- anexar vídeo local
- extrair metadados
- organizar storage

## Fase 3 — Marcação

- tela Streamlit de tagging
- criação de eventos
- edição e exclusão

## Fase 4 — Validação da taxonomia

- criar `ScoutPraia v0.1`
- cadastrar definições operacionais dos eventos
- marcar 1 jogo completo
- remarcar amostra do jogo para teste intraobservador
- comparar marcações, registrar divergências e ajustar definições
- congelar `ScoutPraia v1.0` antes de usar KPIs como referência estável

## Fase 5 — Clipes

- integração com `ffmpeg`
- geração automática por evento
- organização por atleta

## Fase 6 — Analytics

- cálculos de KPIs
- resumos coletivos
- resumos individuais

## Fase 7 — Relatórios

- HTML coletivo
- HTML individual
- HTML de adversária

---

## 21. Critérios de sucesso do MVP

O MVP está aprovado se:

- um jogo inteiro puder ser analisado sem travar a operação
- a marcação for rápida o bastante para uso real
- os eventos principais tiverem definição operacional clara
- a taxonomia aprovada estiver versionada
- a validação de 1 jogo completo gerar divergências revisáveis
- os clipes forem gerados corretamente na maioria dos eventos
- o scout individual for útil para feedback
- o scout coletivo apoiar decisão de treino e jogo

---

## 22. Riscos reais

- excesso de campos na marcação
- taxonomia confusa
- KPI baseado em evento ainda não validado
- mudança silenciosa de definição entre jogos
- clipes com tempo errado
- vídeo mal nomeado
- querer automação visual cedo demais

Mitigação:

- reduzir fricção da tela de marcação
- manter categorias simples
- versionar a taxonomia
- validar 1 jogo completo antes de congelar KPIs
- padronizar nomes
- revisar 1 jogo completo antes de ampliar

---

## 23. Evolução depois do MVP

Depois que o fluxo local estiver estável:

1. OCR de placar e tempo
2. sugestão automática de timestamps
3. classificação semiautomática de jogadas
4. reconhecimento assistido de atletas
5. refatoração para API, se um dia deixar de ser single-user

---

## 24. Conclusão

Para o cenário real do `ScoutPraia`, a melhor decisão técnica é:

- sistema local
- monólito em Python
- interface em `Streamlit`
- dados em `SQLite`
- cortes com `FFmpeg`
- relatórios gerados localmente

Essa abordagem entrega o que importa com o menor custo de implementação e manutenção.

É a arquitetura correta para um sistema que será usado apenas por `Davi Sermenho`.
