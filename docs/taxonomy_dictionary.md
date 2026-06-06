# Dicionário Operacional da Taxonomia

Versão inicial: `ScoutPraia v0.1`

Status: `draft`

## Regra geral

Um evento só entra em KPI final quando tiver definição operacional e passar por revisão em vídeo.

## Eventos ofensivos

| Evento | Definição | Marcar quando | Não marcar quando | Regra de decisão | Status |
| --- | --- | --- | --- | --- | --- |
| `shot_attempt` | tentativa de finalização contra o gol adversário | há arremesso ou ação clara de finalização | passe, finta sem arremesso ou posse interrompida antes da finalização | se a intenção principal é finalizar, marcar tentativa | `draft` |
| `goal_scored` | finalização que resulta em gol válido | placar deve subir para a equipe | gol anulado ou erro de registro do placar | confirmar valor em `points_value` | `draft` |
| `shot_missed` | finalização sem gol e sem defesa da goleira | bola vai para fora, trave ou ação sem intervenção da goleira | defesa clara da goleira | se a goleira altera a trajetória, preferir `save` | `draft` |
| `technical_error` | perda de posse sem arremesso causada por erro técnico ou tomada de decisão | posse acaba por passe errado, recepção falha, condução/violação ou erro não finalizador | arremesso defendido, bola fora em finalização ou roubo claro | se a posse acaba sem arremesso e sem ação defensiva clara, marcar erro técnico | `draft` |
| `turnover` | qualquer perda de posse antes de uma nova posse da própria equipe | adversária passa a controlar a bola | fim de set, gol marcado ou bola parada sem mudança de posse | usar como categoria ampla; subtipo explica a causa | `draft` |
| `assist` | passe imediatamente relacionado ao gol | passe cria finalização convertida | passe anterior sem relação direta com o gol | marcar atleta secundária como assistente | `draft` |
| `two_point_attempt` | tentativa de ação que pode valer 2 pontos | spin, inflight, especialista/goleira ou shoot-out conforme regra aplicável | arremesso comum | separar tentativa de conversão | `draft` |
| `two_point_goal` | gol válido de 2 pontos | ação especial resulta em gol confirmado | gol comum, gol anulado ou erro de pontuação | `points_value` deve ser `2` | `draft` |
| `spin_shot` | tentativa de finalização com giro característico | atleta executa giro antes da finalização | finta com giro sem arremesso | se houver dúvida, registrar como `two_point_attempt` e revisar em vídeo | `draft` |
| `inflight_attempt` | tentativa em que atleta recebe/controla no ar e finaliza antes de tocar o solo | finalização ocorre no ar após passe/recepção | passe alto sem finalização ou finalização após contato com o solo | contar apenas com tentativa de finalização | `draft` |
| `inflight_goal` | `inflight_attempt` convertido em gol válido | finalização aérea resulta em gol | gol comum ou gol anulado | `points_value` deve refletir a regra aplicável | `draft` |

## Eventos defensivos

| Evento | Definição | Marcar quando | Não marcar quando | Regra de decisão | Status |
| --- | --- | --- | --- | --- | --- |
| `defensive_stop` | posse adversária encerrada sem gol por ação defensiva relevante | defesa força arremesso ruim, perda ou interrupção favorável | erro adversário sem pressão clara | marcar quando a defesa altera claramente a qualidade da posse | `draft` |
| `steal` | recuperação direta de posse por ação defensiva | atleta intercepta ou toma a bola | bola perdida sem controle defensivo imediato | precisa haver ganho de posse claro | `draft` |
| `block` | bloqueio de arremesso pela defesa de linha | defensor altera ou impede a trajetória do arremesso | defesa da goleira | se a goleira é responsável pela defesa, usar `save` | `draft` |
| `forced_error` | erro adversário causado por pressão defensiva clara | pressão força passe ruim, violação ou perda | erro sem pressão identificável | se não houver evidência clara de pressão, não marcar | `draft` |
| `goal_conceded` | gol sofrido pela equipe | adversária marca gol válido | gol anulado | registrar valor em pontos concedidos | `draft` |
| `defensive_breakdown` | falha coletiva ou individual que gera finalização clara adversária | há desorganização, troca perdida ou cobertura ausente | gol sofrido sem falha identificável | manter em `testing` por ser interpretativo | `draft` |

## Goleira, transição e situações especiais

| Evento | Definição | Regra de decisão | Status |
| --- | --- | --- | --- |
| `save` | defesa da goleira em finalização adversária | marcar quando a goleira altera ou impede gol em arremesso | `draft` |
| `save_shootout` | defesa da goleira em shoot-out | só usar em situação de shoot-out | `draft` |
| `goalkeeper_distribution` | reposição/passe da goleira que inicia ataque | marcar quando gerar posse organizada ou vantagem clara | `draft` |
| `fast_break_for` | transição ofensiva rápida favorável | marcar quando posse rápida gera finalização ou vantagem clara | `draft` |
| `fast_break_against` | transição ofensiva rápida da adversária | marcar quando adversária finaliza ou cria vantagem clara em transição | `draft` |
| `transition_recovery_good` | recuperação defensiva eficiente na transição | marcar quando equipe impede vantagem clara da adversária | `draft` |
| `transition_recovery_bad` | falha de recomposição na transição | marcar quando adversária obtém finalização clara por atraso defensivo | `draft` |
| `shootout_attempt` | tentativa em shoot-out | marcar todas as tentativas, convertidas ou não | `draft` |
| `shootout_goal` | shoot-out convertido | `points_value` deve refletir regra aplicável | `draft` |
| `shootout_miss` | shoot-out não convertido | separar defesa da goleira com `save_shootout` quando aplicável | `draft` |
| `timeout` | pedido de tempo registrado no vídeo | marcar timestamp para contexto do relatório | `draft` |
| `set_end` | fim do set | marcar placar e timestamp final do set | `draft` |
