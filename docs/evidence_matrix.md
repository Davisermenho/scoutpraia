# Matriz de Evidência do ScoutPraia

Objetivo: registrar por que cada campo, evento ou KPI existe antes de entrar na versão aprovada da taxonomia.

## Regra de decisão

- `oficial`: vem de regra IHF ou regulamento aplicável
- `científica`: vem de artigo, análise notacional ou metodologia observacional
- `técnica`: decisão prática do treinador para utilidade de jogo/treino
- `hipótese`: ideia ainda não validada em vídeo

Itens `hipótese` não entram em KPI final até passarem por validação.

## Governança de status taxonômico

Objetivo: padronizar como cada status deve ser interpretado pelo agente, pela UI e pelos relatórios.

| Status | O que permite | O que bloqueia | Impacto na UI | Impacto em KPIs | Impacto em relatórios | Ações para transformar em estável | Fontes e evidências verificáveis |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `draft` | marcação manual inicial, ensaio operacional, teste de fluxo e revisão exploratória | KPI final estável, interpretação conclusiva e promoção silenciosa para versão aprovada | pode aparecer na UI de marcação e edição, desde que a taxonomia usada esteja explícita | não deve sustentar KPI final sozinho | pode aparecer em prévia, mas com cautela metodológica e versão visível da taxonomia | registrar fonte, escrever definição operacional, aplicar regra de inclusão/exclusão, testar em vídeo, ajustar ambiguidade e gerar nova versão da taxonomia | `SRC-OBS-MEASUREMENT`; `docs/taxonomy_dictionary.md`; `docs/validation_protocol.md`; `docs/rag_workflow.md` |
| `testing` | uso controlado em ensaios, comparação entre marcações, avaliação de utilidade prática e revisão por vídeo | congelamento como regra estável sem rodada de validação suficiente | pode aparecer na UI já em uso controlado, inclusive em ensaio humano com vídeo real | pode gerar indicador experimental, mas ainda não KPI final estável | pode entrar em prévia ou relatório com ressalva explícita | executar o protocolo de validação, comparar divergências, manter/ajustar/fundir/dividir/remover, repetir validação nos campos alterados | `SRC-IHF-RULES`; `SRC-NOTATIONAL-BH`; `SRC-OBS-MEASUREMENT`; `docs/validation_protocol.md` |
| `approved` | uso oficial na taxonomia ativa, apoio a decisão de treino/jogo, KPI estável e relatório final sem ressalva metodológica central | alteração silenciosa sem nova versão, sem nova evidência e sem revalidação quando a semântica mudar | deve aparecer como opção consolidada e clara na UI | pode sustentar KPI final | pode sustentar relatório final como item confiável | congelar a versão, manter vínculo com fonte/evidência, controlar mudança por nova versão e revalidação quando necessário | `SRC-IHF-RULES`; `docs/sources/README.md`; `docs/validation_protocol.md`; `docs/rag_workflow.md` |

### Notas operacionais sobre a tabela

- `draft` não significa “proibido usar”; significa “ainda não confiável como KPI final estável”.
- `testing` existe para itens que já têm base suficiente para ensaio controlado, mas ainda dependem de prova observacional ou revisão metodológica.
- `approved` só deve ser usado quando a definição estiver estável, a fonte estiver registrada e a validação em vídeo já tiver sido executada.
- Se um item mudar de significado, ele não deve permanecer na mesma versão da taxonomia; a mudança deve gerar nova versão.

## Matriz inicial

| Item | Tipo | Fonte | Evidência/justificativa | Uso no sistema | Status |
| --- | --- | --- | --- | --- | --- |
| `points_value` | oficial | `SRC-IHF-RULES` | beach handball tem ações com valores de pontuação distintos | cálculo de placar, eficiência e relatório | `testing` |
| `set_number` | oficial | `SRC-IHF-RULES` | jogo é organizado por sets | segmentação de scout e relatório por set | `testing` |
| `shootout_attempt` | oficial | `SRC-IHF-RULES` | shoot-out é situação especial do jogo | análise de eficiência em shoot-out | `testing` |
| `two_point_goal` | oficial | `SRC-IHF-RULES`, `SRC-SYNTHESIS-BH` | gols especiais valem mais que gol comum; `SRC-SYNTHESIS-BH` identifica os estudos de suporte para priorização do item | KPI de eficiência de 2 pontos | `testing` |
| `spin_shot` | oficial/científica | `SRC-IHF-RULES`, `SRC-NOTATIONAL-BH`, `SRC-SYNTHESIS-BH` | ação específica relevante no beach handball; `SRC-SYNTHESIS-BH` funciona como fonte auxiliar de curadoria dos papers notacionais | evento ofensivo e clipe técnico | `testing` |
| `inflight_goal` | oficial/científica | `SRC-IHF-RULES`, `SRC-NOTATIONAL-BH`, `SRC-SYNTHESIS-BH` | ação específica relevante no beach handball; `SRC-SYNTHESIS-BH` consolida a priorização dos estudos de arremesso | evento ofensivo e clipe técnico | `testing` |
| `zone` | científica/técnica | `SRC-NOTATIONAL-BH`, `SRC-SYNTHESIS-BH` | zonas permitem analisar tendência e eficiência; `SRC-SYNTHESIS-BH` aponta os estudos mais úteis para o recorte beach handball | mapa de finalização e vulnerabilidade defensiva | `testing` |
| `technical_error` | metodologia/técnica | `SRC-OBS-MEASUREMENT` | precisa de definição observável para reduzir ambiguidade | perda de posse e correção de treino | `draft` |
| `defensive_breakdown` | técnica | decisão do treinador | útil para feedback, mas interpretativo | relatório coletivo e clips de correção | `draft` |

## Próximo passo

Antes de `ScoutPraia v1.0`, cada item deve ter:

- definição operacional
- regra de inclusão
- regra de exclusão
- teste em vídeo
- decisão: manter, ajustar, dividir, fundir ou remover
