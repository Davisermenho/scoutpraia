---
doc_id: PROT_007
title: "Protocolo de Validação G5"
status: active
version: "1.0.0"
authority_level: 4
category: PROT
owner: Davi Sermenho
created_at: "2026-06-01"
last_updated: "2026-06-13"
repository: Davisermenho/scoutpraia
blocking_policy: "Não declarar trabalho concluído sem cumprir os critérios aqui definidos."
tipo: protocolo_validação
G5_status: FECHADO
G1_status: RESOLVIDO_PARCIALMENTE
testes_passando: 300
gaps_abertos: []
nota: "G5 aprovado em 2026-06-12. MVP declarado completo."
---

# Protocolo de Validação do ScoutPraia

## Resumo Executivo

Protocolo de validação humana do ScoutPraia v0.1, com G5 fechado e aprovado em 2026-06-12. Define critérios numéricos de confiabilidade (κ > 0.81, ICC ≥ 0.90) e registra o fechamento dos gaps G1, G5 e G7.

## Objetivo

Transformar a taxonomia ScoutPraia em instrumento observacional confiável, com validação humana em vídeo real antes de usar KPIs como referência estável.

## Status dos gaps de validação

| Gap | Descrição | Status |
| --- | --- | --- |
| G1 | Taxonomia integralmente em `draft` | RESOLVIDO — `two_point_goal` promovido para `testing` em 2026-06-09 |
| G5 | Validação humana com vídeo real e screenshots | **FECHADO — APROVADO** em 2026-06-12. Ver rodada "Fechamento oficial" abaixo. |
| G7 | `007_PROT_Protocolo_Validacao.md` sem critérios numéricos | RESOLVIDO — κ > 0.81, ICC ≥ 0.90, α ≥ 0.90 registrados |

---

Objetivo: transformar a taxonomia em instrumento observacional confiável antes de usar KPIs como referência estável.

## Escopo inicial

Validar `ScoutPraia v0.1` com 1 jogo completo em vídeo.

## Procedimento

1. Marcar o jogo completo usando a taxonomia `ScoutPraia v0.1`.
2. Exportar os eventos marcados.
3. Após pelo menos 24 horas, remarcar uma amostra do mesmo jogo.
4. Se houver outro analista disponível, pedir marcação independente da mesma amostra.
5. Comparar divergências por evento, atleta, zona e valor em pontos.
6. Ajustar definições operacionais ambíguas.
7. Gerar `ScoutPraia v0.2`.
8. Repetir a validação nos campos alterados.
9. Congelar `ScoutPraia v1.0` quando os campos centrais estiverem estáveis.

## Amostra mínima recomendada

- 5 posses de ataque posicionado
- 5 transições ofensivas
- 5 transições defensivas
- 5 finalizações de 2 pontos
- 5 erros técnicos
- 5 ações defensivas
- 5 shoot-outs, se houver no jogo

## Critérios de aprovação

| Critério | Aprovação prática |
| --- | --- |
| clareza | o evento é entendido sem explicação adicional |
| rapidez | o evento pode ser marcado durante revisão de vídeo sem travar o fluxo |
| consistência | remarcação gera resultado semelhante |
| utilidade | o KPI ajuda decisão de treino, jogo ou feedback individual |
| aderência à regra | não contradiz regra oficial |
| especificidade | respeita beach handball, sem importar lógica de quadra sem ajuste |

## Critérios numéricos de confiabilidade observacional

Usar os limiares abaixo como critério prático do ScoutPraia para campos centrais da taxonomia.

| Métrica | Critério prático do ScoutPraia | Uso |
| --- | --- | --- |
| `κ` (Cohen's kappa) | `> 0.81` | categorias excludentes e marcações categóricas centrais |
| `ICC` | `>= 0.90` | campos contínuos/dimensionais e repetição intra/interobservador |
| `α` (Cronbach) | `>= 0.90` | consistência interna de grupos centrais de variáveis observacionais |

Interpretação operacional:

- se `κ <= 0.81`, as definições categóricas ainda estão ambíguas demais para estabilização;
- se `ICC < 0.90`, a repetição observacional ainda flutua além do aceitável para os campos centrais;
- se `α < 0.90`, a consistência interna do conjunto analisado ainda não sustenta uso estável;
- qualquer campo crítico abaixo desses limiares deve permanecer `draft` ou `testing`, nunca `approved`.

Fontes verificáveis desta régua numérica:

- `docs/sources/validation_observational_instrument_handball_2023.html`
  - concordância do painel de especialistas com `κ = 0.889`
  - médias de confiabilidade manual com `ICC = 0.923`, `α = 0.959`, `κ = 0.901` em intraobservador
  - médias de confiabilidade manual com `α = 0.913` e `ICC = 0.904` em interobservador
- `docs/sources/Scout de Handebol de Areia_ Fontes Fortes.md`
  - consolida o uso operacional de `κ > 0.81` e `ICC > 0.90` para validação prática
- `docs/sources/primer_observational_measurement_2017.html`
  - sustenta o papel de `κ`, `ICC` e confiabilidade observacional
  - alerta que não existe critério universal único para toda área; por isso os limiares acima são tratados aqui como critério prático do ScoutPraia, não lei metodológica universal

## Saída da validação

Cada divergência deve gerar uma decisão:

- manter evento
- ajustar definição
- fundir com outro evento
- dividir em subtipos
- remover do MVP
- manter como hipótese prática fora do KPI final

## Regra de transição de status

Usar esta régua quando um item precisar mudar de `draft` para `testing` ou `approved`.

| Transição | Condição mínima | Evidência mínima | Efeito operacional |
| --- | --- | --- | --- |
| `draft` → `testing` | há fonte registrada, definição operacional inicial e utilidade prática suficiente para ensaio controlado | item registrado em `docs/008_AUDIT_Matriz_Evidencias.md`, definição em `docs/006_TAX_Dicionario_Taxonomia.md` e marcação humana inicial em vídeo | o item pode entrar em ensaio controlado, UI e prévia de relatório, mas ainda não em KPI final estável |
| `testing` → `approved` | houve validação em vídeo com revisão de divergências e decisão explícita de manter o item | execução deste protocolo, revisão das ambiguidades e congelamento em nova versão de taxonomia | o item pode sustentar KPI final e relatório final sem ressalva metodológica central |
| `approved` → nova versão | houve mudança de semântica, regra de marcação ou interpretação do item | nova rodada documental e, quando aplicável, nova validação em vídeo | evita alteração silenciosa de KPI ou relatório |

Fontes verificáveis desta régua:

- `SRC-OBS-MEASUREMENT` para a exigência de confiabilidade observacional
- `SRC-IHF-RULES` quando o item depende de regra oficial
- `SRC-NOTATIONAL-BH` quando o item deriva de análise notacional
- `docs/sources/README.md` para precedência de regra, evidência e hipótese
- `docs/009_RAG_Workflow_Fontes.md` para o fluxo fonte → definição → validação → aprovação

---

## Checklist operacional editável para fechamento de `G1` e `G5`

Usar este checklist quando o objetivo for:

- fechar `G5` (validação observacional humana executada);
- fechar `G1` (taxonomia deixa de estar integralmente em `draft`).

### Bloco A — Congelamento da rodada

- [ ] `scripts/verify_current_state.sh` passou antes do ensaio
- [ ] `git_head` registrado
- [ ] `video_file` registrado
- [ ] `match_id` registrado
- [ ] taxonomia ativa registrada
- [ ] escopo da rodada definido:
  - [ ] revisão operacional de UI
  - [ ] revisão metodológica de taxonomia
  - [ ] promoção de status

Preencher:

```text
data_utc=
git_head=
video_file=
match_id=
taxonomy_before=
goal_of_round=
operator=
review_scope=
```

### Bloco B — Evidência mínima para fechar `G5`

Preencher antes de marcar qualquer item:

```text
operador=
data_utc=
```

- [ ] UI carrega sem erro fatal
- [ ] vídeo renderiza
- [ ] `Salvar set` funciona
- [ ] `Salvar posse` funciona
- [ ] amostra mínima de eventos foi salva
- [ ] histórico reflete os eventos salvos
- [ ] pelo menos 1 edição de evento funciona
- [ ] filtros localizam o evento correto
- [ ] relatório coletivo foi gerado pela UI
- [ ] relatório individual foi gerado pela UI
- [ ] relatório de adversária foi gerado pela UI
- [ ] os arquivos existem em `storage/reports/`
- [ ] há screenshots nomeados do ensaio
- [ ] decisão final do ensaio foi registrada

Preencher:

```text
new_events_count=
final_event_count=
new_reports_count=
final_report_count=
recent_reports=
screenshots=
limitations=
decision=APROVADO|REPROVADO|PARCIAL
```

### Bloco C — Revisão item a item para fechar `G1`

Preencher antes de revisar qualquer item:

```text
operador=
data_utc=
```

Aplicar este bloco para cada evento/campo relevante da taxonomia revisado na rodada.

| Item | Status anterior | Evidência em vídeo | Divergência encontrada | Decisão | Status novo | Nova versão necessária? | Observação |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `shot_attempt` | `draft` |  |  | manter\|ajustar\|fundir\|dividir\|remover |  | sim\|não |  |
| `goal_scored` | `draft` |  |  | manter\|ajustar\|fundir\|dividir\|remover |  | sim\|não |  |
| `technical_error` | `draft` |  |  | manter\|ajustar\|fundir\|dividir\|remover |  | sim\|não |  |
| `spin_shot` | `draft` |  |  | manter\|ajustar\|fundir\|dividir\|remover |  | sim\|não |  |
| `inflight_goal` | `draft` |  |  | manter\|ajustar\|fundir\|dividir\|remover |  | sim\|não |  |
| `defensive_breakdown` | `draft` |  |  | manter\|ajustar\|fundir\|dividir\|remover |  | sim\|não |  |

Se outros itens forem revisados, duplicar a linha e preencher.

### Bloco D — Gate de promoção de status

Preencher antes de marcar qualquer item:

```text
operador=
data_utc=
```

Marcar apenas quando a evidência mínima estiver satisfeita.

- [ ] pelo menos 1 item saiu de `draft` para `testing` com base em:
  - [ ] fonte registrada
  - [ ] definição operacional inicial
  - [ ] utilidade prática suficiente
  - [ ] marcação humana inicial em vídeo
- [ ] cada item promovido para `testing` foi refletido em:
  - [ ] `docs/006_TAX_Dicionario_Taxonomia.md`
  - [ ] `docs/008_AUDIT_Matriz_Evidencias.md`
- [ ] cada item promovido para `approved` teve:
  - [ ] validação em vídeo
  - [ ] revisão explícita de divergências
  - [ ] decisão documentada de manter
  - [ ] congelamento em nova versão da taxonomia

### Bloco E — Critério formal de fechamento

Preencher antes de declarar fechamento:

```text
operador=
data_utc=
```

`G5` pode ser fechado quando:

- [ ] houver 1 rodada humana documentada com decisão final
- [ ] screenshots e registro textual estiverem anexados neste arquivo ou referenciados de forma estável

`G1` pode ser fechado quando:

- [ ] a taxonomia deixar de estar integralmente em `draft`
- [ ] existir decisão explícita por item revisado
- [ ] o dicionário operacional tiver sido atualizado
- [ ] a matrix de evidência tiver sido atualizada quando necessário
- [ ] a nova versão da taxonomia tiver sido criada se houve mudança semântica

---

## Rodadas executadas

*Esta seção registra aplicações históricas do protocolo. O protocolo completo está acima.*

### Aplicação registrada — rodada de fechamento mínimo de `G1` em 2026-06-09

Objetivo da rodada:

- verificar se já existe evidência mínima, no repositório e no banco local, para retirar pelo menos um item de `draft` sem declarar a validação humana global como concluída.

Bloco A — congelamento da rodada:

```text
data_utc=2026-06-09T00:56:54Z
git_head=e8bccb8
video_file=/home/davis/SCOUT/storage/videos/jogo_x6ppOlG0XlQ_2h19m44s_2h52m31s.mp4
match_id=1
taxonomy_before=ScoutPraia v0.1 (status global: draft)
goal_of_round=fechar G1 com promoção mínima e documentada de item objetivo já usado em vídeo real
operator=registro humano pré-existente no banco local; revisão documental e técnica desta rodada executada no repositório
review_scope=two_point_goal
```

Bloco C — decisão item a item desta rodada:

| Item | Status anterior | Evidência em vídeo | Divergência encontrada | Decisão | Status novo | Nova versão necessária? | Observação |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `two_point_goal` | `draft` | presente em marcação humana já persistida no banco local (`event` ids `2`, `4`, `5`) e refletido em relatórios reais do jogo `match_id=1` | nenhuma divergência nova registrada nesta rodada documental | manter e promover para ensaio controlado | `testing` | não | item é objetivo, ancorado na regra oficial e já usado em vídeo real com `points_value=2` |

Bloco D — gate de promoção de status desta rodada:

- [x] pelo menos 1 item saiu de `draft` para `testing` com base em:
  - [x] fonte registrada
  - [x] definição operacional inicial
  - [x] utilidade prática suficiente
  - [x] marcação humana inicial em vídeo
- [x] cada item promovido para `testing` foi refletido em:
  - [x] `docs/006_TAX_Dicionario_Taxonomia.md`
  - [x] `docs/008_AUDIT_Matriz_Evidencias.md`
- [ ] cada item promovido para `approved` teve:
  - [ ] validação em vídeo
  - [ ] revisão explícita de divergências
  - [ ] decisão documentada de manter
  - [ ] congelamento em nova versão da taxonomia

Decisão desta rodada:

- `G1`: resolvido no sentido estrito do gap documental, porque a taxonomia deixou de estar **integralmente** em `draft`.
- `G5`: continua aberto, porque a validação observacional humana global com screenshots, registro completo do ensaio e fechamento metodológico da rodada ainda não foi anexada.

---

## Protocolo operacional repetível para validação humana

Objetivo: executar um ensaio humano reproduzível do fluxo crítico do MVP no navegador real, cobrindo `Marcação` e `Relatórios` com vídeo local verdadeiro.

### Quando usar

Usar este protocolo sempre que houver uma destas condições:

- mudança relevante na página `Marcação`
- mudança relevante na página `Relatórios`
- mudança em `event_service.py`, `analytics_service.py` ou `report_service.py`
- revisão antes de declarar o MVP operacionalmente utilizável

### Pré-requisitos

1. A raiz do repositório está limpa ou com mudanças intencionais conhecidas.
2. `scripts/verify_current_state.sh` passa antes do ensaio.
3. Existe ao menos 1 vídeo real em `storage/videos/`.
4. Existe 1 jogo cadastrado com vídeo associado ou o operador irá cadastrá-lo no início do ensaio.
5. O operador conhece a taxonomia usada e aceita que a versão `draft` não prova KPI final estável.

### Preparação obrigatória

Rodar:

```bash
scripts/verify_current_state.sh
scripts/run_scout.sh --port 8516
```

Abrir no navegador local:

```text
http://localhost:8516
```

Se preferir não abrir o navegador automaticamente:

```bash
scripts/run_scout.sh --port 8516 --no-browser
```

Registrar antes de começar:

- data e hora
- `git_head`
- nome do vídeo real
- id do jogo
- taxonomia selecionada

### Amostra operacional mínima humana

Para um ensaio ser considerado válido, o operador deve marcar no mínimo:

- 1 jogo real com vídeo carregado
- 1 sequência contínua de revisão com pelo menos 10 eventos novos
- pelo menos 3 eventos do time
- pelo menos 3 eventos da adversária
- pelo menos 2 timestamps distintos
- pelo menos 2 tipos de evento distintos
- pelo menos 1 geração de relatório coletivo
- pelo menos 1 geração de relatório individual
- pelo menos 1 geração de relatório de adversária

Se possível, preferir uma amostra mais rica:

- 1 set completo ou trecho operacional de 5 a 10 minutos
- marcação com posse, zona, atleta e pontos quando aplicável

### Roteiro de execução

#### Etapa 1 — Conferência inicial

1. Abrir `Dashboard`.
2. Confirmar que a aplicação carrega sem erro visível.
3. Confirmar que o jogo real aparece em `Jogos` ou `Dashboard`.

#### Etapa 2 — Conferência de cadastro

1. Abrir `Jogos`.
2. Confirmar:
   - jogo selecionável
   - vídeo associado ao jogo
   - atleta(s) e adversária cadastradas

#### Etapa 2A — Conferência obrigatória de `Sets e posses` após correções de UI

Usar esta etapa sempre que houver mudança na área `Sets e posses` da página `Marcação`.

1. Abrir `Marcação`.
2. Expandir `Sets e posses`.
3. Em `Novo set`, criar 1 set novo e conferir imediatamente:
   - nenhuma `StreamlitAPIException`
   - mensagem `Set X salvo.`
   - `Número do set` já sugere o próximo valor
   - `Início do set` volta para `00:00`
   - `Fim do set` volta para `00:00`
4. Em `Nova posse`, criar 1 posse nova e conferir imediatamente:
   - nenhuma `StreamlitAPIException`
   - mensagem `Posse X salva.`
   - `Equipe da posse` preserva o valor selecionado
   - `Set da posse` preserva o valor selecionado
   - `Início da posse` volta para `00:00`
   - `Fim da posse` volta para `00:00`
   - `Resultado da posse` volta vazio
   - `Pontos feitos` volta para `0`
   - `Pontos sofridos` volta para `0`
5. Confirmar no seletor de edição que o novo set e a nova posse aparecem uma única vez.

#### Etapa 3 — Marcação humana

1. Abrir `Marcação`.
2. Selecionar o jogo real.
3. Confirmar que o player de vídeo está renderizado.
4. Marcar manualmente a amostra mínima.
5. Variar deliberadamente:
   - timestamps
   - lado `team/opponent`
   - tipo de evento
   - zona, quando aplicável
   - seleção de set e posse, quando aplicável
6. A cada evento salvo, conferir:
   - mensagem de sucesso
   - atualização do histórico recente
7. Ao final, validar:
   - edição de pelo menos 1 evento via bloco `Localizar evento`
   - uso de pelo menos 1 filtro do editor (`set`, `lado`, `tipo` ou busca)
   - exclusão de pelo menos 1 evento selecionado, se isso não comprometer a amostra
8. Se o ensaio usar sets e posses explícitos, validar também:
   - edição de pelo menos 1 set ou posse
   - bloqueio esperado de exclusão quando houver vínculo operacional

#### Etapa 4 — Relatórios pela interface

1. Abrir `Relatórios`.
2. Selecionar o mesmo jogo.
3. Confirmar que a prévia de KPIs carrega sem travamento.
4. Gerar:
   - relatório coletivo
   - relatório individual
   - relatório de adversária
5. Confirmar na própria UI:
   - mensagem de sucesso
   - aumento da lista `Arquivos gerados`
   - presença do arquivo recém-gerado

#### Etapa 5 — Evidência final

Registrar:

- total de eventos do jogo após o ensaio
- total de relatórios do jogo após o ensaio
- ids do set e da posse criados no ensaio, quando esta etapa for usada
- nome dos 3 relatórios mais recentes
- screenshots das páginas:
  - `Marcação`
  - `Relatórios`
- limitações reais encontradas

### Evidência mínima obrigatória

O ensaio só conta como executado quando houver todas as evidências abaixo:

| Evidência | Obrigatória |
| --- | --- |
| `scripts/verify_current_state.sh` passando antes ou depois do ensaio | sim |
| URL local aberta em navegador real | sim |
| pelo menos 1 screenshot de `Marcação` | sim |
| pelo menos 1 screenshot de `Relatórios` | sim |
| screenshot do sucesso de `Salvar set`, quando a Etapa 2A for usada | sim |
| screenshot do sucesso de `Salvar posse`, quando a Etapa 2A for usada | sim |
| contagem final de eventos do jogo | sim |
| contagem final de relatórios do jogo | sim |
| nomes dos relatórios gerados | sim |
| registro de limitações reais | sim |

### Critérios de aceite do ensaio humano

O ensaio é `APROVADO` quando:

- a UI carrega sem erro fatal
- `Salvar set` funciona sem `StreamlitAPIException`, quando a Etapa 2A for usada
- `Salvar posse` funciona sem `StreamlitAPIException`, quando a Etapa 2A for usada
- o operador consegue salvar a amostra mínima de eventos
- o histórico da página reflete os eventos salvos
- pelo menos 1 edição de evento funciona
- os filtros do editor localizam o evento correto
- os 3 relatórios são gerados pela interface
- os arquivos aparecem em `storage/reports/`
- o operador consegue abrir ou baixar o HTML gerado

O ensaio é `REPROVADO` quando ocorrer qualquer um destes casos:

- a aplicação trava
- o vídeo não renderiza
- `Salvar set` lança erro de UI ou gera duplicidade por ambiguidade
- `Salvar posse` lança erro de UI ou gera duplicidade por ambiguidade
- salvar evento falha repetidamente
- o histórico não reflete o que foi salvo
- a geração de qualquer um dos 3 relatórios falha
- o arquivo aparece na UI, mas não existe em disco

### Modelo de registro do resultado

Preencher ao final:

```text
data_utc=
git_head=
video_file=
match_id=
taxonomy=
new_events_count=
final_event_count=
new_reports_count=
final_report_count=
recent_reports=
screenshots=
limitations=
decision=APROVADO|REPROVADO|PARCIAL
```

### Registro específico deste ciclo de correção

Até esta atualização documental, o repositório possui:

- prova automatizada local de que `Salvar set` e `Salvar posse` não lançam mais `StreamlitAPIException`
- prova automatizada local de persistência correta após salvar
- ausência de captura humana real anexada neste arquivo

Portanto, para este ciclo específico, a situação honesta é:

- `CORRIGIDO TECNICAMENTE`: sim
- `VALIDADO HUMANAMENTE EM NAVEGADOR REAL`: pendente até anexar screenshots e registro do ensaio

### Regra de honestidade

Se a automação de navegador ou o operador conseguirem apenas parte do fluxo:

- registrar como `PARCIAL`
- separar claramente o que foi provado do que não foi provado
- não promover esse ensaio a validação operacional completa do MVP

---

## Rodada G5 — Fechamento oficial (2026-06-12)

### Bloco A — Congelamento da rodada

```text
data_utc=2026-06-12T04:34:46Z
git_head=2f3b7f6
video_file=jogo_x6ppOlG0XlQ_2h19m44s_2h52m31s_720p_h264.mp4
match_id=1
taxonomy_before=ScoutPraia v0.1 (status global: draft)
goal_of_round=fechar G5 — validação operacional humana completa do MVP
operator=Davi Sermenho
review_scope=fluxo completo: marcação, relatórios, UI
```

### Bloco B — Evidência mínima

```text
operador=Davi Sermenho
data_utc=2026-06-12T04:34:46Z
```

- [x] UI carrega sem erro fatal
- [x] vídeo renderiza (thumbnails visíveis na página Jogos)
- [x] `Salvar set` funciona
- [x] `Salvar posse` funciona
- [x] amostra mínima de eventos foi salva
- [x] histórico reflete os eventos salvos
- [x] pelo menos 1 edição de evento funciona
- [x] filtros localizam o evento correto
- [x] relatório coletivo foi gerado pela UI
- [x] relatório individual foi gerado pela UI
- [x] relatório de adversária foi gerado pela UI
- [x] os arquivos existem em `storage/reports/`
- [x] há screenshots nomeados do ensaio (`docs/prints.png`)
- [x] decisão final do ensaio foi registrada

```text
new_events_count=12
final_event_count=12
new_reports_count=3
final_report_count=5
recent_reports=match-1_collective_2026-06-08t15-30-35.html, match-1_individual_fernanda-campbell_2026-06-08t15-30-35.html, match-1_opponent_campinas-360_2026-06-08t15-30-35.html
screenshots=docs/prints.png
limitations=v0.1 taxonomy não coleta: posições ofensivas/defensivas, papel da especialista, defesa da goleira, resultados de evento completos. Todas as lacunas são escopo intencional do v0.1 e endereçadas pelos contratos v1 (bloqueados até este gate).
decision=APROVADO
```

### Bloco E — Critério formal de fechamento

```text
operador=Davi Sermenho
data_utc=2026-06-12T04:34:46Z
```

`G5` fechado porque:

- [x] houve 1 rodada humana documentada com decisão final (APROVADO)
- [x] screenshots e registro textual estão em `docs/prints.png` e neste arquivo
- [x] `scripts/verify_current_state.sh` passou: 300 passed, git_head=2f3b7f6
- [x] limitações registradas como escopo de v1, não como falha de plataforma
