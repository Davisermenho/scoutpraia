---
doc_id: TAX_006
title: "Dicionário de Taxonomia v0.1"
status: draft
version: "0.1.0"
authority_level: 3
category: TAX
owner: Davi Sermenho
created_at: "2026-06-01"
last_updated: "2026-06-13"
repository: Davisermenho/scoutpraia
tipo: dicionário_taxonomia
status_global: draft
regra_crítica: "Evento sem status approved não sustenta KPI final"
leitura_obrigatória_para_agente: true
nota: "Status global draft não impede marcação ou uso em testes; impede apenas KPI final estável"
---

# Dicionário Operacional da Taxonomia

## Resumo Executivo

Dicionário de taxonomia v0.1 do ScoutPraia, em estado `draft`. Define os eventos observacionais, seus status de aprovação e as regras de uso por status (marcação, KPI, relatório).

## Objetivo

Registrar e governar cada evento da taxonomia ScoutPraia, especificando fonte, definição operacional e status de validação, até atingir o estado `approved` para uso em KPIs finais estáveis.

Versão inicial: `ScoutPraia v0.1`

Status: `draft`

Nota operacional:

- o status acima é da versão da taxonomia como um todo;
- itens individuais podem avançar para `testing` antes do fechamento completo da versão;
- a versão só deve deixar de estar `draft` quando a validação observacional humana global estiver concluída.

## Regra de uso por status

| Status | Marcação manual | UI de marcação | KPI | Relatório |
| --- | --- | --- | --- | --- |
| `draft` | permitida com cautela | pode aparecer | NÃO sustenta KPI final | somente prévia com ressalva |
| `testing` | permitida em ensaio controlado | aparece como opção em uso controlado | indicador experimental (não KPI final) | com ressalva metodológica explícita |
| `approved` | uso oficial na taxonomia ativa | opção consolidada | sustenta KPI final estável | relatório final sem ressalva |

Regra operacional: agente MUST NOT promover evento de `draft` diretamente para `approved` sem rodada de validação explícita registrada em `docs/007_PROT_Protocolo_Validacao.md`.

## Regra geral

Um evento só entra em KPI final quando tiver definição operacional e passar por revisão em vídeo.

## Eventos ofensivos

| Evento | Definição | Marcar quando | Não marcar quando | Regra de decisão | Fonte | Versão | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `shot_attempt` | tentativa de finalização contra o gol adversário | há arremesso ou ação clara de finalização | passe, finta sem arremesso ou posse interrompida antes da finalização | se a intenção principal é finalizar, marcar tentativa | `SRC-IHF-RULES`, `SRC-OBS-MEASUREMENT` | v0.1 | `draft` |
| `goal_scored` | finalização que resulta em gol válido | placar deve subir para a equipe | gol anulado ou erro de registro do placar | confirmar valor em `points_value` | `SRC-IHF-RULES` | v0.1 | `draft` |
| `shot_missed` | finalização sem gol e sem defesa da goleira | bola vai para fora, trave ou ação sem intervenção da goleira | defesa clara da goleira | se a goleira altera a trajetória, preferir `save` | `SRC-IHF-RULES`, `SRC-OBS-MEASUREMENT` | v0.1 | `draft` |
| `technical_error` | perda de posse sem arremesso causada por erro técnico ou tomada de decisão | posse acaba por passe errado, recepção falha, condução/violação ou erro não finalizador | arremesso defendido, bola fora em finalização ou roubo claro | se a posse acaba sem arremesso e sem ação defensiva clara, marcar erro técnico | `SRC-OBS-MEASUREMENT` | v0.1 | `draft` |
| `turnover` | qualquer perda de posse antes de uma nova posse da própria equipe | adversária passa a controlar a bola | fim de set, gol marcado ou bola parada sem mudança de posse | usar como categoria ampla; subtipo explica a causa | `SRC-OBS-MEASUREMENT` | v0.1 | `draft` |
| `assist` | passe imediatamente relacionado ao gol | passe cria finalização convertida | passe anterior sem relação direta com o gol | marcar atleta secundária como assistente | `SRC-OBS-MEASUREMENT`, `coach_decision` | v0.1 | `draft` |
| `two_point_attempt` | tentativa genérica de ação que pode valer 2 pontos | há arremesso de 2 pontos sem classificação específica já identificada na taxonomia ativa | spin, inflight, especialista ou shoot-out já classificados com evento próprio; arremesso comum | usar como fallback legado quando o mecanismo exato do lance de 2 pontos não foi marcado | `SRC-IHF-RULES` | v0.1 | `draft` |
| `two_point_goal` | gol genérico válido de 2 pontos | gol de 2 pontos sem classificação específica já identificada na taxonomia ativa | gol comum, gol anulado ou gol já classificado como inflight, especialista ou shoot-out | `points_value` deve ser `2`; preferir evento específico quando o mecanismo do lance estiver claro | `SRC-IHF-RULES` | v0.1 | `testing` |
| `specialist_attempt` | tentativa de finalização executada pela atleta atuando como especialista | atleta com colete/uniforme de especialista finaliza, convertendo ou não | arremesso comum de atleta de linha, inflight já classificado, shoot-out ou lance sem confirmação visual da especialista | usar somente quando a função de especialista estiver visível no vídeo ou operacionalmente confirmada | `SRC-IHF-RULES`, `SRC-SYNTHESIS-BH` | v0.1 | `draft` |
| `specialist_goal` | gol convertido pela atleta atuando como especialista | finalização da especialista resulta em gol válido de 2 pontos | gol comum, gol anulado, shoot-out ou gol já classificado por outra mecânica específica | `points_value` deve ser `2`; usar apenas com confirmação visual/operacional da especialista em quadra | `SRC-IHF-RULES`, `SRC-SYNTHESIS-BH` | v0.1 | `draft` |
| `spin_shot` | tentativa de finalização com giro característico | atleta executa giro antes da finalização | finta com giro sem arremesso | se houver dúvida, registrar como `two_point_attempt` e revisar em vídeo | `SRC-IHF-RULES`, `SRC-NOTATIONAL-BH` | v0.1 | `draft` |
| `inflight_attempt` | tentativa em que atleta recebe/controla no ar e finaliza antes de tocar o solo | finalização ocorre no ar após passe/recepção | passe alto sem finalização ou finalização após contato com o solo | contar apenas com tentativa de finalização | `SRC-IHF-RULES`, `SRC-NOTATIONAL-BH` | v0.1 | `draft` |
| `inflight_goal` | `inflight_attempt` convertido em gol válido | finalização aérea resulta em gol | gol comum ou gol anulado | `points_value` deve refletir a regra aplicável | `SRC-IHF-RULES`, `SRC-NOTATIONAL-BH` | v0.1 | `draft` |

## Eventos defensivos

| Evento | Definição | Marcar quando | Não marcar quando | Regra de decisão | Fonte | Versão | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `defensive_stop` | posse adversária encerrada sem gol por ação defensiva relevante | defesa força arremesso ruim, perda ou interrupção favorável | erro adversário sem pressão clara | marcar quando a defesa altera claramente a qualidade da posse | `SRC-OBS-MEASUREMENT`, `SRC-NOTATIONAL-BH` | v0.1 | `draft` |
| `steal` | recuperação direta de posse por ação defensiva | atleta intercepta ou toma a bola | bola perdida sem controle defensivo imediato | precisa haver ganho de posse claro | `SRC-OBS-MEASUREMENT`, `SRC-NOTATIONAL-BH` | v0.1 | `draft` |
| `block` | bloqueio de arremesso pela defesa de linha | defensor altera ou impede a trajetória do arremesso | defesa da goleira | se a goleira é responsável pela defesa, usar `save` | `SRC-OBS-MEASUREMENT`, `SRC-NOTATIONAL-BH` | v0.1 | `draft` |
| `forced_error` | erro adversário causado por pressão defensiva clara | pressão força passe ruim, violação ou perda | erro sem pressão identificável | se não houver evidência clara de pressão, não marcar | `SRC-OBS-MEASUREMENT`, `coach_decision` | v0.1 | `draft` |
| `goal_conceded` | gol sofrido pela equipe | adversária marca gol válido | gol anulado | registrar valor em pontos concedidos | `SRC-IHF-RULES` | v0.1 | `draft` |
| `defensive_breakdown` | falha coletiva ou individual que gera finalização clara adversária | há desorganização, troca perdida ou cobertura ausente | gol sofrido sem falha identificável | manter em `testing` por ser interpretativo | `coach_decision` | v0.1 | `draft` |

## Goleira, transição e situações especiais

| Evento | Definição | Marcar quando | Não marcar quando | Regra de decisão | Fonte | Versão | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `save` | defesa da goleira em finalização adversária | goleira altera ou impede gol em arremesso | defesa de linha sem participação da goleira | se a goleira altera a trajetória, preferir `save` em vez de `block` | `SRC-IHF-RULES`, `SRC-NOTATIONAL-BH` | v0.1 | `draft` |
| `save_shootout` | defesa da goleira em shoot-out | goleira defende em situação de shoot-out | defesa em jogo corrido | só usar com situação de shoot-out confirmada | `SRC-IHF-RULES` | v0.1 | `draft` |
| `goalkeeper_distribution` | reposição/passe da goleira que inicia ataque | goleira lança ou passa e gera posse organizada ou vantagem | simples tiro de meta sem sequência de ataque | marcar quando gerar posse organizada ou vantagem clara | `SRC-IHF-RULES`, `SRC-NOTATIONAL-BH` | v0.1 | `draft` |
| `fast_break_for` | transição ofensiva rápida favorável à equipe | equipe parte para ataque rápido com vantagem numérica ou posicional clara | ataque posicional regular | marcar quando posse rápida gera finalização ou vantagem clara | `SRC-NOTATIONAL-BH` | v0.1 | `draft` |
| `fast_break_against` | transição ofensiva rápida da adversária | adversária ataca em vantagem numérica ou posicional clara | ataque posicional adversário regular | marcar quando adversária finaliza ou cria vantagem clara em transição | `SRC-NOTATIONAL-BH` | v0.1 | `draft` |
| `transition_recovery_good` | recuperação defensiva eficiente na transição | equipe se reorganiza e impede vantagem clara da adversária | reorganização defensiva sem ação de transição clara | marcar quando equipe impede vantagem adversária por recomposição eficiente | `SRC-NOTATIONAL-BH`, `coach_decision` | v0.1 | `draft` |
| `transition_recovery_bad` | falha de recomposição na transição | adversária obtém finalização clara por atraso ou falha defensiva na transição | falha em ataque posicional sem contexto de transição | marcar quando adversária se aproveita diretamente de falha de recomposição | `SRC-NOTATIONAL-BH`, `coach_decision` | v0.1 | `draft` |
| `shootout_attempt` | tentativa em shoot-out | qualquer tentativa de shoot-out, convertida ou não | lances em jogo corrido | marcar todas as tentativas; usar `shootout_goal` ou `save_shootout` para desfecho | `SRC-IHF-RULES` | v0.1 | `draft` |
| `shootout_goal` | shoot-out convertido em gol | shoot-out resulta em gol válido | shoot-out não convertido | `points_value` deve refletir regra aplicável; não usar para gol em jogo corrido | `SRC-IHF-RULES` | v0.1 | `draft` |
| `shootout_miss` | shoot-out não convertido | shoot-out não resulta em gol (para fora, trave ou defesa) | gol marcado no shoot-out | separar defesa da goleira com `save_shootout` quando aplicável | `SRC-IHF-RULES` | v0.1 | `draft` |
| `timeout` | pedido de tempo registrado no vídeo | há interrupção oficial de tempo no vídeo | pausa sem confirmação oficial | marcar timestamp para contexto do relatório; não inferir timeout sem evidência clara | `SRC-IHF-RULES` | v0.1 | `draft` |
| `set_end` | fim do set | placar final do set é marcado | intervalo sem fim de set | marcar placar e timestamp final do set | `SRC-IHF-RULES` | v0.1 | `draft` |
