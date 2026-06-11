---
status: base_interna_elaborada_v0
tipo: fonte_propria_cepraea
uso_previsto: playbook_tatico
escopo: "regras internas de leitura e uso do scout no ciclo treinador-video-relatorio"
fonte_base:
  - docs/MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md
  - docs/taxonomy_dictionary.md
  - docs/evidence_matrix.md
  - docs/validation_protocol.md
  - scoutpraia/services/analytics_service.py
  - scoutpraia/templates/report_collective.html
observacao: "Playbook interno base. Prioriza o que o app ja mede hoje e separa regra oficial, leitura observavel e decisao tecnica."
---

# Playbook CEPRAEA

## Finalidade

Este playbook organiza como o CEPRAEA deve usar o ScoutPraia atual para transformar video em:

- marcação observavel
- leitura tecnica disciplinada
- feedback para treino
- relatorio coletivo, individual e de adversaria

Ele nao substitui regra oficial nem protocolo de validacao. Sua funcao e operacionalizar o uso interno do que o app ja mede.

## Hierarquia de decisao

Sempre decidir nesta ordem:

1. regra oficial IHF/CBHb aplicavel
2. `docs/taxonomy_dictionary.md`
3. `docs/evidence_matrix.md`
4. `docs/validation_protocol.md`
5. convencao interna CEPRAEA

Regra:

- linguagem interna nunca pode ser apresentada como regra oficial
- interpretacao tática nunca pode apagar o evento observavel que a sustenta

## Regra central do playbook

Separar sempre tres camadas:

- `fato observavel`: o que aconteceu no video e pode ser marcado no app
- `leitura tecnica`: o que isso sugere para o jogo
- `decisao de treino`: o que a comissao vai corrigir, repetir ou explorar

Exemplo:

- fato observavel: `specialist_goal`
- leitura tecnica: a equipe converteu bem a entrada da especialista
- decisao de treino: repetir gatilho de uso da especialista contra defesa baixa

## Blocos de leitura priorizados no ScoutPraia atual

### 1. Finalizacao

Perguntas principais:

- estamos finalizando o suficiente?
- com que eficiencia?
- qual mecanismo de finalizacao entrega mais pontos?

Indicadores atuais:

- `offensive_conversion_rate`
- `finalization_attempts_total`
- `finalization_efficiency_by_type`
- `points_by_technical_type`

Leitura interna:

- baixa conversao sem erro técnico elevado sugere problema de qualidade da finalizacao
- baixa conversao com alta perda sem finalizacao sugere quebra antes do arremesso

### 2. Jogo de 2 pontos

Perguntas principais:

- quais mecanismos de 2 pontos usamos de fato?
- a especialista esta entregando ganho real?

Indicadores atuais:

- `two_point_efficiency`
- `specialist_efficiency`
- `specialist_shots_total`
- `points_by_scorer_role`

Leitura interna:

- separar 2 pontos genericos de 2 pontos da especialista
- nao usar `two_point_goal` como leitura tática fina quando o mecanismo especifico estiver claro

### 3. Posses sem finalizacao

Perguntas principais:

- onde a posse quebra antes do arremesso?
- qual a principal causa recorrente?

Indicadores atuais:

- `no_shot_attack_total`
- `no_shot_attack_causes`
- `technical_error_rate`

Leitura interna:

- erro de controle, falta de ataque, jogo passivo e erro de troca nao devem ser agregados como uma massa unica
- o primeiro uso do playbook aqui e descobrir o gargalo dominante da posse

### 4. Defesa e goleira

Perguntas principais:

- a defesa de linha esta gerando parada real?
- estamos confundindo bloqueio com defesa da goleira?

Indicadores atuais:

- `defensive_stops_per_possession`
- contagem de `block`
- contagem de `save` e `save_shootout`

Leitura interna:

- bloqueio, roubo, erro forçado e defesa da goleira sao mecanismos diferentes
- nao elogiar "boa defesa" sem saber qual mecanismo realmente produziu a parada

### 5. Transicao

Perguntas principais:

- estamos sofrendo vulnerabilidade em transicao?
- a recomposicao esta chegando em tempo?

Indicadores atuais:

- `transition_vulnerability`
- `fast_break_against`
- `transition_recovery_good`
- `transition_recovery_bad`

Leitura interna:

- transicao ruim recorrente vira tema de treino coletivo
- uma boa leitura de transicao exige revisar o contexto do clipe, nao so a contagem

### 6. Shoot-out

Perguntas principais:

- quem converte sob pressao?
- como a goleira responde ao shoot-out?

Indicadores atuais:

- `shootout_efficiency`
- `shootout_attempt`
- `shootout_goal`
- `shootout_miss`
- `save_shootout`

Leitura interna:

- shoot-out e bloco proprio de decisao
- nao misturar seu desempenho com finalizacao comum ou 6 metros

## Convencoes internas de sistema e protocolo

Estas convencoes organizam o playbook do CEPRAEA adulto feminino.
Elas nao substituem regra oficial e nao autorizam inferencia automatica sem evento observavel.

### 1. Ataque em Carrossel (`4:0`)

Uso interno:

- atacar sem pivô fixa, com circulacao, largura e troca de corredor
- desgastar defesa pesada e abrir linha para especialista, giro ou aerea

Leitura de apoio:

- combina melhor com revisao de `points_by_technical_type`, `specialist_efficiency` e perdas sem finalizacao

### 2. Estrutura com infiltracao (`3:1`)

Uso interno:

- manter uma referencia mais agressiva perto da linha de 6 metros adversaria
- buscar fixacao de defensora central para abrir aerea, passe de profundidade ou segunda acao curta

Leitura de apoio:

- usar como linguagem de treino e revisao em clipe; o ScoutPraia atual nao classifica `3:1` como sistema autonomo

### 3. Defesa base `3:0`

Uso interno:

- proteger o centro e compactar o bloco proximo a 6 metros
- coordenar o pacto entre bloqueio de linha e leitura da goleira

Leitura de apoio:

- revisar `block`, `save`, `forced_error` e `defensive_breakdown` antes de concluir que o sistema foi bem executado

### 4. Defesa pressao `2:1`

Uso interno:

- adiantar uma defensora para atrasar a circulacao central e pressionar a especialista adversaria
- induzir passe previsivel, jogo passivo ou erro de decisao

Leitura de apoio:

- confirmar em clipe se a pressao gerou atraso real da posse e nao apenas exposicao do bloco

### 5. Protocolo de saida em `slide`

Uso interno:

- nomear a troca rapida especialista-goleira para reduzir risco de gol em quadra vazia
- orientar timing de saida, entrada e recomposicao

Leitura de apoio:

- observar `substitution_error_turnover`, vulnerabilidade de transicao e contexto do clipe

### 6. Contra-ataque direto da goleira

Uso interno:

- autorizar leitura agressiva quando a goleira adversaria demora na recomposicao
- explorar gol direto apenas quando a janela estiver clara

Leitura de apoio:

- nao transformar tentativa ocasional em identidade automatica sem revisar taxa de acerto e risco associado

### 7. Protocolo de jogo passivo

Uso interno:

- ao pre-aviso arbitral, encurtar a posse e priorizar acao vertical
- ativar isolamento, passe de profundidade ou mecanismo de 2 pontos de maior seguranca disponivel

Leitura de apoio:

- distinguir protocolo bem executado de simples aceleracao ansiosa; revisar `passive_play_turnover` e o clipe

### 8. Protocolo de ultimos 15 segundos

Uso interno:

- em vantagem, proteger posse e evitar contato defensivo de alto risco
- em desvantagem, subir a pressao dentro do limite regulamentar e operacional do set

Leitura de apoio:

- quando a pergunta for sobre regra, citar primeiro a IHF 2026; aqui o termo vale apenas como organizador do playbook interno

### 9. Estrategia de shoot-out

Uso interno:

- separar rotina de ataque e rotina defensiva para o shoot-out
- combinar execucao tecnica com rotina mental e leitura previa da goleira/atacante adversaria

Leitura de apoio:

- sustentar a decisao com `shootout_efficiency`, `save_shootout` e revisao de clipes; nao reduzir o bloco a intuicao

## Fluxo operacional recomendado

### Antes do jogo

- definir 2 a 4 perguntas de observacao prioritarias
- confirmar se ha interesse especial em transicao, especialista, goleira ou shoot-out

### Durante a marcacao

- registrar primeiro o evento observavel
- usar notas so quando o evento sozinho nao preserva o contexto
- evitar interpretar taticamente no meio da marcacao se isso atrasar o fluxo

### Depois da marcacao

- revisar alertas criticos
- revisar perdas sem finalizacao
- revisar mecanicas de 2 pontos
- revisar clips das posses mais relevantes

### Na devolutiva para treino

- transformar o scout em 3 blocos:
  - manter
  - corrigir
  - explorar

## Regras internas de linguagem

- usar "regra" apenas para o que vier de fonte normativa
- usar "padrão observado" para recorrencia de video
- usar "hipótese de treino" para leitura ainda nao validada

## O que este playbook nao autoriza

- criar KPI final a partir de termo interno sem evidência
- promover evento `draft` para verdade tática estabilizada
- misturar convenção CEPRAEA com arbitragem/regra oficial
- usar um relatorio experimental como conclusao definitiva de desempenho
