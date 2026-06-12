---
tipo: contrato_execução_agente
status: REFERÊNCIA_ESTÁVEL
fase_atual: 12
status_fase_atual: MVP_COMPLETO
leitura_obrigatória_para_agente: true
última_atualização: 2026-06-12
mvp_completo: true
g5_status: APROVADO
próxima_ação_imediata: "Ativar finalization_v1 — contrato validado, testes existem, botões já na UI (tagging.py linhas 69-77)"
---

# ScoutPraia — Plano de Implementação para IA

Este arquivo é o contrato de execução para uma IA implementar o ScoutPraia até o MVP completo. Ele deriva do `docs/MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md` e deve ser seguido na ordem.

A palavra "garantia" aqui significa garantia operacional por gates: a IA só pode avançar quando a fase anterior entrega arquivos, comportamento e validações definidos. Fontes e plano não garantem resultado por si mesmos; a completude vem de implementação, teste, revisão com vídeo e aceite final.

---

## Fase atual e próxima ação

**Fase atual: 9 — Validação operacional com vídeo real (PARCIAL)**

Estado das fases:

| Fase | Nome | Status |
|------|------|--------|
| 1 | Pré-implementação obrigatória | `[CONCLUÍDA]` |
| 2 | Estrutura base do projeto | `[CONCLUÍDA]` |
| 3 | Configuração, paths e banco | `[CONCLUÍDA]` |
| 4 | Modelos de dados | `[CONCLUÍDA COMO BASE]` |
| 5 | Taxonomia v0.1 | `[CONCLUÍDA]` |
| 6 | Serviços internos | `[CONCLUÍDA COM EVIDÊNCIA]` |
| 7 | Interface Streamlit | `[CONCLUÍDA COM EVIDÊNCIA]` |
| 8 | Testes e fixtures | `[FUNCIONANDO — 247 testes]` |
| 9 | Validação operacional com vídeo real | `[EM ANDAMENTO — G5 pendente]` |
| 10 | README e operação local | `[CONCLUÍDA]` |
| 11 | IA/RAG no ScoutPraia | `[BLOQUEADA — aguarda MVP completo]` |

**Verificar estado atual antes de qualquer ação:**

```bash
scripts/verify_current_state.sh
# resultado esperado: 247 passed
```

**Próxima ação:** executar o protocolo operacional de G5 em `docs/validation_protocol.md`.

---

---

## 0. Contrato de trabalho da IA

### 0.1 Restrições absolutas — ler antes de qualquer implementação

```
MUST NOT: criar frontend React
MUST NOT: criar backend FastAPI separado
MUST NOT: criar API pública
MUST NOT: criar banco PostgreSQL
MUST NOT: criar autenticação
MUST NOT: criar suporte multiusuário
MUST NOT: criar deploy ou infraestrutura em servidor
MUST NOT: versionar vídeos, banco local, clipes, relatórios gerados, .env, .venv, tmp/ ou binários locais
MUST NOT: avançar fase se o gate de aceite da fase anterior falhar
MUST NOT: declarar MVP completo sem evidência reproduzível
MUST NOT: iniciar RAG antes do MVP completo

MUST: implementar monólito local em Python
MUST: rodar scripts/verify_current_state.sh após cada mudança relevante
MUST: atualizar docs/IMPLEMENTATION_PROGRESS.md a cada ciclo
MUST: corrigir causa raiz, não apenas silenciar erro
MUST: manter MVP simples, local e utilizável por uma pessoa
```

### 0.2 Fontes validadoras

| Área | Fonte | Validação usada no plano |
| --- | --- | --- |
| Regras do esporte | IHF Rules of the Game — Beach Handball | pontuação, sets, shoot-out e ações especiais devem respeitar regra oficial |
| Metodologia observacional | A Primer on Observational Measurement | taxonomia precisa de definição operacional e confiabilidade de marcação |
| Análise notacional | Notational analysis of beach handball | zonas, finalizações e eficiência são indicadores adequados para análise de beach handball |
| Interface local | Streamlit docs | Streamlit suporta player de vídeo, multipage app, widgets e downloads locais |
| Estado da UI | Streamlit Session State docs | estado de navegação/marcação precisa ser controlado entre reruns |
| Banco local | Python `sqlite3` docs / SQLModel docs | SQLite local é suficiente para persistência simples do MVP |
| Vídeo | FFmpeg/ffprobe docs | `ffprobe` extrai metadados; `ffmpeg` corta clipes |
| Analytics | pandas docs | `groupby` e agregações sustentam KPIs coletivos e individuais |
| Relatórios | Jinja docs | templates HTML são caminho simples para relatórios locais |
| Gráficos | Plotly docs | gráficos interativos suportam dashboards e relatórios |
| Validação de dados | Pydantic docs | validação de campos reduz dados inválidos antes do banco |
| IA/RAG | Lewis et al.; NAACL 2024; OpenAI Evals | fontes externas, auditoria e evals ajudam a reduzir invenção e melhorar saída estruturada |

### 0.3 Links das fontes

- IHF Rules of the Game — Beach Handball: https://www.ihf.info/sites/default/files/2026-03/09B%20-%20Rules%20of%20the%20Game_Beach%20Handball_E.pdf
- A Primer on Observational Measurement: https://pmc.ncbi.nlm.nih.gov/articles/PMC5426358/
- Notational analysis of beach handball: https://hummov.awf.wroc.pl/Notational-analysis-of-beach-handball%2C130277%2C0%2C2.html
- Streamlit `st.video`: https://docs.streamlit.io/develop/api-reference/media/st.video
- Streamlit multipage apps: https://docs.streamlit.io/develop/concepts/multipage-apps
- Streamlit Session State: https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
- Streamlit `st.file_uploader`: https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader
- Streamlit `st.data_editor`: https://docs.streamlit.io/develop/api-reference/data/st.data_editor
- Streamlit `st.download_button`: https://docs.streamlit.io/develop/api-reference/widgets/st.download_button
- Python `sqlite3`: https://docs.python.org/3/library/sqlite3.html
- SQLModel create table and SQLite engine: https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/
- FFmpeg docs: https://www.ffmpeg.org/documentation.html
- FFmpeg CLI: https://www.ffmpeg.org/ffmpeg.html
- ffprobe: https://ffmpeg.org/ffprobe.html
- pandas `DataFrame.groupby`: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.groupby.html
- Plotly Python: https://plotly.com/python/
- Jinja docs: https://jinja.palletsprojects.com/
- Pydantic docs: https://pydantic.dev/docs/
- RAG original: https://arxiv.org/abs/2005.11401
- RAG em saída estruturada: https://aclanthology.org/2024.naacl-industry.19/
- OpenAI Evals: https://developers.openai.com/api/docs/guides/evals
- OpenAI Prompt Engineering: https://developers.openai.com/api/docs/guides/prompt-engineering

---

## 1. Pré-implementação obrigatória

### 1.1 Corrigir inconsistências do MVP documental

Antes de codar, revisar `docs/MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md` e corrigir:

- `match_roster` tem `player_id` duplicado; manter apenas um.
- `## 13.1 KPIs coletivos` aparece duplicado; manter apenas um.

Gate de aceite:

- `docs/MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md` não tem duplicações óbvias de campo/título.
- `git diff --check` não acusa espaços problemáticos, se o repo estiver em Git.

### 1.2 Confirmar arquivos de contrato

A IA deve ler estes arquivos antes de implementar:

- `docs/MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md`
- `docs/sources/README.md`
- `docs/evidence_matrix.md`
- `docs/taxonomy_dictionary.md`
- `docs/validation_protocol.md`
- `docs/rag_workflow.md`
- `docs/IMPLEMENTATION_STEPS_AI.md`

Gate de aceite:

- A IA consegue explicar em uma frase: ScoutPraia é monólito local em Python para marcar vídeo, gerar clipes, KPIs e relatórios.

---

## 2. Estrutura base do projeto

### 2.1 Criar árvore de diretórios

Criar exatamente esta base:

```text
app.py
requirements.txt
README.md
.env.example
data/.gitkeep
storage/videos/.gitkeep
storage/clips/.gitkeep
storage/reports/.gitkeep
storage/thumbnails/.gitkeep
scoutpraia/__init__.py
scoutpraia/core/__init__.py
scoutpraia/core/config.py
scoutpraia/core/paths.py
scoutpraia/core/database.py
scoutpraia/models/__init__.py
scoutpraia/models/team.py
scoutpraia/models/player.py
scoutpraia/models/opponent.py
scoutpraia/models/match.py
scoutpraia/models/event.py
scoutpraia/models/taxonomy.py
scoutpraia/models/validation.py
scoutpraia/models/clip.py
scoutpraia/models/report.py
scoutpraia/services/__init__.py
scoutpraia/services/video_service.py
scoutpraia/services/event_service.py
scoutpraia/services/clip_service.py
scoutpraia/services/validation_service.py
scoutpraia/services/analytics_service.py
scoutpraia/services/report_service.py
scoutpraia/pages/__init__.py
scoutpraia/pages/dashboard.py
scoutpraia/pages/matches.py
scoutpraia/pages/tagging.py
scoutpraia/pages/reports.py
scoutpraia/pages/opponents.py
scoutpraia/templates/report_collective.html
scoutpraia/templates/report_individual.html
scoutpraia/templates/report_opponent.html
scoutpraia/utils/__init__.py
scoutpraia/utils/timecode.py
scoutpraia/utils/zones.py
scoutpraia/utils/exports.py
tests/__init__.py
```

### 2.2 Criar dependências mínimas

`requirements.txt` deve conter inicialmente:

```text
streamlit
pandas
sqlmodel
plotly
jinja2
python-dotenv
pydantic
pytest
```

Não incluir `opencv-python` no MVP inicial. Ele fica para evolução.

### 2.3 Criar `.env.example`

```env
SCOUTPRAIA_DB_PATH=data/scoutpraia.db
SCOUTPRAIA_VIDEO_DIR=storage/videos
SCOUTPRAIA_CLIP_DIR=storage/clips
SCOUTPRAIA_REPORT_DIR=storage/reports
SCOUTPRAIA_THUMBNAIL_DIR=storage/thumbnails
FFMPEG_BINARY=ffmpeg
FFPROBE_BINARY=ffprobe
```

Gate de aceite:

- `python -m pytest` roda, mesmo sem testes relevantes ainda.
- `python -c "import scoutpraia"` não falha.
- `streamlit run app.py` inicia sem erro fatal quando `app.py` existir.

---

## 3. Configuração, paths e banco

### 3.1 `config.py`

Implementar carregamento de `.env` com valores padrão seguros.

Contrato:

- expor `Settings` com paths e binários.
- não exigir `.env`; `.env.example` é referência.
- validar que paths são relativos ao projeto ou absolutos válidos.

### 3.2 `paths.py`

Implementar helpers para:

- criar diretórios de storage se não existirem.
- normalizar nomes de arquivos.
- gerar paths de vídeo, clipe e relatório.
- impedir path traversal com `..`.

### 3.3 `database.py`

Implementar:

- engine SQLite local.
- `create_db_and_tables()`.
- helper `get_session()`.

Preferência: SQLModel. Se houver bloqueio real com SQLModel, usar `sqlite3`, mas registrar a decisão no README.

Gate de aceite:

- rodar um comando/script de init cria `data/scoutpraia.db`.
- tabelas são criadas sem erro.
- `data/*.db` permanece ignorado pelo Git.

---

## 4. Modelos de dados

### 4.1 Modelos obrigatórios

Implementar modelos SQLModel para:

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

### 4.2 Regras de modelagem

- Usar nomes Python claros e nomes de tabela estáveis.
- IDs inteiros autoincrementais são suficientes no MVP.
- Campos opcionais devem ser explicitamente opcionais.
- `Event.taxonomy_version_id` é obrigatório.
- `Event.timestamp_second` deve ser número inteiro ou decimal não negativo.
- `Event.points_value` deve permitir `0`, `1`, `2`.
- `TaxonomyVersion.status` deve aceitar `draft`, `testing`, `approved`, `archived`.
- `EventDefinition.evidence_type` deve aceitar `official_rule`, `scientific_literature`, `coach_decision`, `practical_hypothesis`.

Gate de aceite:

- teste cria e consulta um registro básico de atleta, adversária, jogo, taxonomia e evento.
- nenhum KPI pode ser calculado sem taxonomia associada ao evento.

---

## 5. Taxonomia v0.1 e matriz de evidência

### 5.1 Criar seed da taxonomia

Criar função ou script para inserir `ScoutPraia v0.1` com todos os eventos listados em `docs/taxonomy_dictionary.md`.

Eventos obrigatórios:

- ataque: `shot_attempt`, `goal_scored`, `shot_missed`, `turnover`, `technical_error`, `assist`, `two_point_attempt`, `two_point_goal`, `specialist_attempt`, `specialist_goal`, `spin_shot`, `inflight_attempt`, `inflight_goal`
- defesa: `defensive_stop`, `steal`, `block`, `forced_error`, `goal_conceded`, `defensive_breakdown`
- goleira: `save`, `save_shootout`, `goalkeeper_distribution`
- transição: `fast_break_for`, `fast_break_against`, `transition_recovery_good`, `transition_recovery_bad`
- especiais: `shootout_attempt`, `shootout_goal`, `shootout_miss`, `timeout`, `set_end`

### 5.2 Sincronizar com dicionário operacional

Cada evento deve ter:

- definição
- quando marcar
- quando não marcar
- regra de decisão
- tipo de evidência
- status inicial

Gate de aceite:

- não existe evento sem `EventDefinition`.
- eventos com `practical_hypothesis` não entram em KPI crítico sem aviso.
- seed pode rodar duas vezes sem duplicar dados.

---

## 6. Serviços internos

### 6.1 `video_service.py`

Implementar:

- validação de extensão `.mp4` e `.mov`.
- cópia ou registro seguro de vídeo local.
- extração de duração, resolução, fps e codec via `ffprobe`.
- tratamento de erro quando `ffprobe` não existir.

Gate:

- função retorna metadados reais para vídeo válido.
- função falha com mensagem clara para arquivo inexistente ou extensão inválida.

### 6.2 `event_service.py`

Implementar:

- criar evento.
- editar evento.
- excluir evento.
- listar eventos por jogo.
- validar `event_type` contra taxonomia ativa.
- validar `zone` contra zonas permitidas.
- validar `points_value` contra regra prática do evento.

Gate:

- tentativa de criar evento fora da taxonomia falha.
- evento válido é persistido e aparece no histórico.

### 6.3 `clip_service.py`

Implementar:

- calcular janela de corte por tipo de evento.
- proteger início menor que zero.
- gerar nome de clipe padronizado.
- executar `ffmpeg`.
- salvar registro `Clip`.

Janelas:

- padrão: 6 segundos antes, 4 depois.
- transição: 10 antes, 6 depois.
- shoot-out: 8 antes, 5 depois.
- sequência tática: 12 antes, 8 depois.

Gate:

- clipe gerado existe no filesystem.
- clipe tem nome previsível.
- erro de `ffmpeg` é capturado e exibido.

### 6.4 `validation_service.py`

Implementar:

- listar eventos sem definição operacional.
- validar se taxonomia está aprovada para relatório final.
- comparar duas sessões de marcação por `event_type`, atleta, zona e pontos.
- calcular concordância percentual simples.
- gerar `CodingAgreement` com divergências em JSON.

Gate:

- serviço identifica divergência artificial em fixture de teste.
- serviço aprova/reprova comparação com base em regra configurável.

### 6.5 `analytics_service.py`

Implementar KPIs coletivos:

- pontos por posse.
- gols por posse.
- taxa de conversão ofensiva.
- taxa de erro técnico.
- stops defensivos por posse.
- gols sofridos em transição.
- eficiência de 2 pontos.
- eficiência da especialista.
- eficiência em shoot-out.
- desempenho por set.

Implementar KPIs individuais:

- tentativas de finalização.
- conversão total.
- conversão por tipo.
- conversão por zona.
- turnovers.
- erros técnicos.
- roubos de bola.
- bloqueios.
- defesas.
- participação direta em gols.

Implementar KPIs por adversária:

- lado preferido de ataque.
- atleta que mais finaliza.
- atleta que mais converte 2 pontos.
- taxa de erro sob pressão.
- vulnerabilidade em transição.
- eficiência da especialista.
- desempenho em shoot-out.

Gate:

- todos os KPIs retornam `0`, `None` ou estrutura vazia quando não há dados, sem quebrar.
- fixture com eventos conhecidos gera números esperados.
- KPI crítico avisa quando usa evento de taxonomia não aprovada.

### 6.6 `report_service.py`

Implementar:

- payload coletivo.
- payload individual.
- payload de adversária.
- renderização HTML com Jinja.
- exportação do HTML para `storage/reports/`.
- registro `Report` com `payload_json`.

PDF é opcional. Se não for implementado, deixar claro no README.

Gate:

- relatório HTML é gerado e abre como arquivo local.
- relatório informa versão da taxonomia.
- relatório contém links relativos para clipes existentes quando houver.

---

## 7. Interface Streamlit

### 7.1 `app.py`

Implementar app local com navegação para:

- Dashboard
- Jogos
- Marcação
- Relatórios
- Adversárias

Usar `st.Page`/`st.navigation` ou padrão de multipage equivalente. Manter simples.

Gate:

- `streamlit run app.py` abre app sem erro.
- cada página renderiza mesmo com banco vazio.

### 7.2 Página Dashboard

Exibir:

- jogos recentes.
- resumo de KPIs recentes.
- atalhos operacionais.

Gate:

- dashboard vazio exibe estado vazio, não erro.

### 7.3 Página Jogos

Implementar:

- cadastro de adversária se necessário.
- cadastro de jogo.
- cadastro/seleção de atletas disponíveis.
- associação de vídeo local.
- leitura de metadados.

Gate:

- é possível criar jogo com adversária e vídeo.
- vídeo aparece vinculado ao jogo.

### 7.4 Página Marcação

Implementar tela crítica:

- player de vídeo com `st.video`.
- timestamp manual visível/editável.
- botões grandes para eventos.
- seleção rápida de atleta.
- seleção de atleta secundária quando aplicável.
- seleção de zona.
- seleção de set.
- seleção de posse quando necessário.
- feed lateral de eventos salvos.
- editar/excluir qualquer evento salvo.
- editar/excluir set.
- editar/excluir posse.
- filtros para localizar evento por set, lado, tipo e busca textual.
- navegação rápida entre eventos filtrados.

Limitação reconhecida:

- Streamlit não garante controle fino do tempo real do player HTML nativo. Para MVP, aceitar timestamp manual e botões rápidos. Hotkeys podem ficar para evolução se exigirem componente customizado.

Gate:

- usuário consegue marcar pelo menos 20 eventos sem recarregar o app manualmente.
- eventos salvos aparecem no histórico.
- edição e exclusão de evento funcionam sobre qualquer item selecionado.
- edição e exclusão de `set` e `posse` funcionam.
- filtros e navegação do editor permitem localizar o evento correto sem excluir registros intermediários.

### 7.5 Página Relatórios

Implementar:

- seleção de jogo.
- prévia de KPIs.
- gerar relatório coletivo.
- gerar relatório individual por atleta.
- gerar relatório de adversária.
- botão de download/abrir HTML.

Gate:

- relatório coletivo é gerado para jogo com eventos.
- relatório individual é gerado para atleta com eventos.
- app não quebra quando não há eventos.

### 7.6 Página Adversárias

Implementar:

- cadastro/listagem de adversárias.
- histórico de jogos contra adversária.
- tendências calculadas.
- plano de jogo manual/editável.

Gate:

- adversária pode ser criada, editada e consultada.
- página exibe tendências quando há dados.

---

## 8. Testes e fixtures

### 8.1 Testes mínimos

Criar testes para:

- criação de banco.
- criação de taxonomia seed.
- criação e validação de evento.
- cálculo de cada KPI principal.
- cálculo de janela de clipe.
- geração de nome de clipe.
- geração de relatório HTML.
- comparação de marcações no `validation_service`.

### 8.2 Fixture de jogo sintético

Criar dados sintéticos suficientes para cobrir:

- gol comum.
- gol de 2 pontos.
- erro técnico.
- defesa da goleira.
- roubo de bola.
- bloqueio.
- transição.
- shoot-out.
- relatório coletivo.
- relatório individual.

Gate:

- `pytest` passa.
- fixture sintética gera KPIs previsíveis.

---

## 9. Validação operacional com vídeo real

### 9.1 Primeiro jogo completo

Executar fluxo real:

1. cadastrar adversária.
2. cadastrar jogo.
3. associar vídeo local.
4. cadastrar elenco disponível.
5. marcar jogo completo ou amostra operacional mínima.
6. gerar clipes principais.
7. gerar relatório coletivo.
8. gerar relatório individual de pelo menos 1 atleta.
9. gerar relatório de adversária.

### 9.2 Validação da taxonomia

Seguir `docs/validation_protocol.md`:

1. marcar jogo com `ScoutPraia v0.1`.
2. remarcar amostra após 24 horas.
3. comparar divergências.
4. ajustar definições.
5. criar `ScoutPraia v0.2`.
6. congelar `ScoutPraia v1.0` apenas quando campos centrais estiverem estáveis.

Gate:

- divergências são registradas.
- relatório final informa taxonomia usada.
- KPIs críticos não dependem de eventos sem definição operacional.

---

## 10. README e operação local

### 10.1 README obrigatório

Documentar:

- objetivo do ScoutPraia.
- premissas do MVP.
- como instalar dependências.
- como configurar `.env`.
- como iniciar o app.
- como inicializar banco.
- como cadastrar jogo.
- como marcar eventos.
- como gerar clipes.
- como gerar relatórios.
- limitações conhecidas.

### 10.2 Comandos esperados

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m scoutpraia.core.database
streamlit run app.py
pytest
```

Fallback operacional quando `python -m venv .venv` falhar por ausência de `ensurepip` / pacote `python3-venv`:

```bash
scripts/setup_venv.sh
source .venv/bin/activate
cp .env.example .env
python -m scoutpraia.core.database
streamlit run app.py
pytest
```

Regras desse fallback:

- usar apenas quando o fluxo padrão com `venv` falhar no ambiente local;
- `scripts/setup_venv.sh` depende de `virtualenv`;
- o script não remove `.venv` existente sem `--force`.

Gate:

- uma pessoa consegue rodar o projeto localmente seguindo só o README.

---

## 11. IA/RAG no ScoutPraia

### 11.1 Não implementar RAG antes do MVP funcional

O MVP completo não depende de RAG. RAG entra depois que:

- taxonomia v0.1 existe.
- marcação funciona.
- clipes funcionam.
- relatórios funcionam.
- validação operacional foi executada.

### 11.2 Usos permitidos de IA/RAG após MVP

- auditar matriz de evidência.
- apontar evento sem fonte.
- apontar conflito com regra oficial.
- sugerir alteração após divergência de marcação.
- revisar relatório para evitar afirmações sem dado.

Gate:

- IA/RAG nunca altera taxonomia aprovada sem criar nova versão.
- toda sugestão de IA entra como hipótese até ser validada.

---

## 12. Definição de MVP completo

O ScoutPraia só está completo quando todos os itens forem verdadeiros:

- app inicia localmente com `streamlit run app.py`.
- banco SQLite é criado automaticamente ou por comando documentado.
- atletas podem ser cadastradas.
- adversárias podem ser cadastradas.
- jogos podem ser cadastrados.
- vídeo local pode ser associado ao jogo.
- metadados do vídeo são extraídos com `ffprobe`.
- eventos podem ser criados, editados, excluídos e listados.
- cada evento aponta para versão de taxonomia.
- taxonomia v0.1 existe com dicionário operacional.
- zonas são padronizadas.
- clipes são gerados com `ffmpeg`.
- KPIs coletivos são calculados.
- KPIs individuais são calculados.
- KPIs por adversária são calculados.
- relatório coletivo HTML é gerado.
- relatório individual HTML é gerado.
- relatório de adversária HTML é gerado.
- relatório informa versão da taxonomia.
- validação de marcação consegue registrar divergências.
- README permite rodar tudo do zero.
- testes mínimos passam.
- vídeos, clipes, banco e outputs gerados não entram no Git.

Se qualquer item falhar, o MVP não está completo.

---

## 13. Ordem final de execução resumida

1. Corrigir duplicações no MVP documental.
2. Criar estrutura de diretórios.
3. Criar `requirements.txt` e `.env.example`.
4. Implementar config, paths e banco.
5. Implementar modelos.
6. Implementar seed da taxonomia v0.1.
7. Implementar `video_service.py`.
8. Implementar `event_service.py`.
9. Implementar `clip_service.py`.
10. Implementar `validation_service.py`.
11. Implementar `analytics_service.py`.
12. Implementar `report_service.py`.
13. Implementar `app.py` e navegação.
14. Implementar páginas Streamlit.
15. Criar templates HTML.
16. Criar testes e fixture sintética.
17. Rodar `pytest`.
18. Rodar `streamlit run app.py`.
19. Fazer teste operacional com vídeo local.
20. Rodar validação de taxonomia.
21. Atualizar README.
22. Revisar critérios de MVP completo.
23. Só então considerar RAG/auditoria avançada.
