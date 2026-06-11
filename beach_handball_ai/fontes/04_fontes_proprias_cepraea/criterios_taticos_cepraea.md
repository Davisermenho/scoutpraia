---
status: base_interna_elaborada_v0
tipo: fonte_propria_cepraea
uso_previsto: criterios_taticos
escopo: "criterios internos para transformar scout em leitura de treino e jogo"
fonte_base:
  - docs/evidence_matrix.md
  - docs/taxonomy_dictionary.md
  - docs/validation_protocol.md
  - scoutpraia/services/analytics_service.py
  - scoutpraia/templates/report_collective.html
  - scoutpraia/templates/report_individual.html
  - scoutpraia/templates/report_opponent.html
observacao: "Criterios internos de interpretacao. Nao substituir fonte normativa nem KPI validado. Usar junto com clips e contexto do jogo."
---

# Criterios Taticos CEPRAEA

## Regra de ouro

Decisao tática interna deve nascer de:

- evento observavel
- agregado coerente
- revisao em clipe quando o contexto for decisivo

Nao usar:

- impressao subjetiva sem evento
- termo interno sem definicao
- KPI de item `draft` como verdade final estabilizada

## Escala de confianca interna

### Nivel 1 — fato observavel

Baseado diretamente em evento, posse, set ou clipe.

### Nivel 2 — padrão observado

Recorrencia identificada em mais de uma posse ou mais de um clipe.

### Nivel 3 — hipótese de treino

Leitura útil, mas ainda dependente de nova revisão ou validação humana mais forte.

## Critérios por bloco de jogo

### 1. Ataque

Perguntas:

- a equipe consegue chegar na finalizacao?
- converte o suficiente quando finaliza?

Olhar primeiro:

- `offensive_conversion_rate`
- `finalization_attempts_total`
- `no_shot_attack_total`
- `no_shot_attack_causes`

Interpretação interna:

- pouca finalizacao com muita perda sem finalizacao indica ruptura de construção
- muita finalizacao com baixa conversao indica problema de escolha, execucao ou leitura da goleira

### 2. Especialista e 2 pontos

Perguntas:

- a especialista gera vantagem real?
- o time depende demais de fallback generico de 2 pontos?

Olhar primeiro:

- `two_point_efficiency`
- `specialist_efficiency`
- `specialist_shots_total`
- `points_by_technical_type`
- `points_by_scorer_role`

Interpretação interna:

- especialista eficiente sugere recurso tático rentavel
- muitos 2 pontos sem mecanismo especifico podem indicar marcacao imprecisa ou leitura tática pobre

### 3. Erro técnico e posse

Perguntas:

- qual erro derruba mais a posse?
- o problema e execução, decisão ou troca?

Olhar primeiro:

- `technical_error_rate`
- `technical_error`
- `ball_control_turnover`
- `offensive_foul_turnover`
- `passive_play_turnover`
- `substitution_error_turnover`

Interpretação interna:

- erro de controle recorrente aponta necessidade de limpeza tecnica
- perda por jogo passivo aponta atraso de leitura apos pre-aviso
- erro de troca aponta problema operacional, nao necessariamente tecnico de arremesso

### 4. Defesa de linha

Perguntas:

- a defesa gera parada real ou apenas contato sem efeito?
- o time esta produzindo roubo, bloqueio ou erro forçado?

Olhar primeiro:

- `defensive_stops_per_possession`
- `steal`
- `block`
- `forced_error`
- `defensive_breakdown`

Interpretação interna:

- parada defensiva com baixo bloqueio pode indicar defesa posicional eficiente sem contestacao final
- falha defensiva recorrente deve ser revista com clipe antes de virar regra de treino

### 5. Goleira

Perguntas:

- a goleira esta interrompendo finalizacoes reais?
- a reposicao gera continuidade qualificada?

Olhar primeiro:

- `save`
- `save_shootout`
- `goalkeeper_distribution`
- eventos de gol sofrido e 6 metros no contexto do relatorio

Interpretação interna:

- nao misturar defesa da goleira com bloqueio de linha
- avaliar goleira por ciclo completo, nao so por highlight de defesa

### 6. Transicao

Perguntas:

- a equipe sofre contra-ataque?
- recompõe em tempo util?

Olhar primeiro:

- `transition_vulnerability`
- `fast_break_against`
- `transition_recovery_good`
- `transition_recovery_bad`

Interpretação interna:

- vulnerabilidade em transicao e problema coletivo de retorno, cobertura ou decisao de risco
- boa recomposicao recorrente tambem deve entrar como padrao positivo

### 7. Shoot-out

Perguntas:

- quem sustenta execucao sob pressao?
- a resposta emocional parece interferir na acao?

Olhar primeiro:

- `shootout_efficiency`
- `shootout_attempt`
- `shootout_goal`
- `shootout_miss`
- `save_shootout`

Interpretação interna:

- shoot-out ruim nao deve ser lido so como problema tecnico; pode ser tema de rotina mental
- combinar leitura do dado com a publicacao EHF de pressao psicologica em shoot-out

### 8. Adversaria

Perguntas:

- qual corredor/ lado ela prefere?
- quem mais finaliza e quem mais pontua 2 pontos?

Olhar primeiro:

- `preferred_attack_side`
- `most_frequent_shooter_player_id`
- `top_two_point_scorer_player_id`
- `specialist_efficiency`
- `transition_vulnerability`

Interpretação interna:

- lado preferencial ajuda a montar plano defensivo
- especialista eficiente da adversaria pede resposta tática especifica, nao so ajuste generico

## Como transformar dado em recomendacao

Estrutura recomendada de saida:

1. `evidencia`
2. `leitura`
3. `acao de treino ou jogo`

Exemplo:

- evidencia: `specialist_efficiency` alta e `specialist_shots_total` recorrente
- leitura: a entrada da especialista esta sendo convertida com boa relacao risco-retorno
- acao: manter o gatilho e treinar variacao de corredor para nao ficar previsivel

## Diretrizes internas condicionais do CEPRAEA adulto feminino

As diretrizes abaixo servem para treino e tomada de decisao da comissao.
Elas nao substituem evidencia observavel, nao congelam KPI final e nao valem como regra oficial.

### 1. Prioridade ofensiva

- priorizar a finalizacao de maior valor quando houver contexto tecnico claro para isso
- usar aerea, giro ou acao da especialista conforme corredor, tempo e qualidade real da posse
- se a melhor opcao for o passe extra, preferir a continuidade da jogada a uma finalizacao forcada

### 2. Alternancia de estrutura ofensiva

- queda recorrente da eficiencia de 2 pontos pode justificar troca de estrutura ofensiva
- quando o `4:0` deixar de gerar vantagem real, considerar uma variacao com mais infiltracao e referencia perto de 6 metros
- qualquer troca deve ser sustentada por mais de uma posse ou clipe, nao por impulso isolado

### 3. Criterios defensivos de sistema

- no `3:0`, a prioridade e manter bloco compacto e flutuacao lateral disciplinada
- no `2:1`, a prioridade e atrasar a armação adversaria sem quebrar a cobertura da base
- em ambos os casos, a leitura final depende de `block`, `forced_error`, `save`, `defensive_breakdown` e revisao de clipe

### 4. Criterio de transicao

- buscar aceleracao ofensiva quando a troca adversaria abrir janela real
- se a vantagem imediata nao aparecer, reorganizar a posse em vez de forcar erro
- na perda da bola, a prioridade e recomposicao util e troca disciplinada, nao observacao passiva do desfecho da jogada

### 5. Criterio de substituicao funcional

- a troca especialista-goleira deve ser lida como parte da decisao tática, nao so como gesto mecanico
- quando a troca mal executada expuser o gol vazio, registrar isso como problema operacional com impacto coletivo
- o nome interno `slide` pode orientar treino e comunicacao, mas a prova analitica continua em eventos e clipes

### 6. Jogo passivo e clutch time

- apos pre-aviso arbitral, evitar posse lateral vazia e acionar a solucao vertical mais segura do contexto
- nos ultimos 15 segundos, a regra oficial governa a acao; o criterio interno serve apenas para organizar risco, posse e pressao
- faltas, empurroes ou contatos de desespero nesse recorte devem ser tratados como erro de decisao de alta gravidade

### 7. Shoot-out

- leitura ruim de shoot-out nao deve ser reduzida a erro tecnico isolado
- combinar eficiencia, perfil de escolha, resposta emocional observavel e material EHF de pressao psicologica
- qualquer protocolo interno de ataque ou defesa no shoot-out precisa ser revisado em clipes, nao apenas assumido por reputacao

### 8. Arbitragem e adaptacao

- mapear cedo o criterio da dupla de arbitros para giro, contato e conducoes de fim de set
- adaptar a leitura tecnica a condicao de areia e ao contexto competitivo sem transformar ajuste situacional em regra permanente
- qualquer observacao desse tipo entra como `padrao observado` ou `hipotese de treino`, nunca como KPI estabilizado

## O que nao concluir automaticamente

- que um evento `draft` ja sustenta KPI final
- que uma atleta esta "bem" ou "mal" so por uma posse
- que uma vulnerabilidade e estrutural sem revisar clipes
- que uma convencao interna ja virou ontologia estavel
