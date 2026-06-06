# Matriz de Evidência do ScoutPraia

Objetivo: registrar por que cada campo, evento ou KPI existe antes de entrar na versão aprovada da taxonomia.

## Regra de decisão

- `oficial`: vem de regra IHF ou regulamento aplicável
- `científica`: vem de artigo, análise notacional ou metodologia observacional
- `técnica`: decisão prática do treinador para utilidade de jogo/treino
- `hipótese`: ideia ainda não validada em vídeo

Itens `hipótese` não entram em KPI final até passarem por validação.

## Matriz inicial

| Item | Tipo | Fonte | Evidência/justificativa | Uso no sistema | Status |
| --- | --- | --- | --- | --- | --- |
| `points_value` | oficial | `SRC-IHF-RULES` | beach handball tem ações com valores de pontuação distintos | cálculo de placar, eficiência e relatório | `testing` |
| `set_number` | oficial | `SRC-IHF-RULES` | jogo é organizado por sets | segmentação de scout e relatório por set | `testing` |
| `shootout_attempt` | oficial | `SRC-IHF-RULES` | shoot-out é situação especial do jogo | análise de eficiência em shoot-out | `testing` |
| `two_point_goal` | oficial | `SRC-IHF-RULES` | gols especiais valem mais que gol comum | KPI de eficiência de 2 pontos | `testing` |
| `spin_shot` | oficial/científica | `SRC-IHF-RULES`, `SRC-NOTATIONAL-BH` | ação específica relevante no beach handball | evento ofensivo e clipe técnico | `testing` |
| `inflight_goal` | oficial/científica | `SRC-IHF-RULES`, `SRC-NOTATIONAL-BH` | ação específica relevante no beach handball | evento ofensivo e clipe técnico | `testing` |
| `zone` | científica/técnica | `SRC-NOTATIONAL-BH` | zonas permitem analisar tendência e eficiência | mapa de finalização e vulnerabilidade defensiva | `testing` |
| `technical_error` | metodologia/técnica | `SRC-OBS-MEASUREMENT` | precisa de definição observável para reduzir ambiguidade | perda de posse e correção de treino | `draft` |
| `defensive_breakdown` | técnica | decisão do treinador | útil para feedback, mas interpretativo | relatório coletivo e clips de correção | `draft` |

## Próximo passo

Antes de `ScoutPraia v1.0`, cada item deve ter:

- definição operacional
- regra de inclusão
- regra de exclusão
- teste em vídeo
- decisão: manter, ajustar, dividir, fundir ou remover
