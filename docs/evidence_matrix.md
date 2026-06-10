---
tipo: matriz_evidência
cobertura_atual: "11/31 eventos documentados (20 faltantes)"
última_atualização: 2026-06-10
gap_ativo: "G4 resolvido; G5 aberto (validação humana)"
regra_crítica: "Evento não presente nesta matriz não pode entrar em KPI crítico"
---

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
| `two_point_goal` | oficial | `SRC-IHF-RULES`, `SRC-SYNTHESIS-BH` | gols especiais valem mais que gol comum; após a separação da especialista, permanece como fallback genérico/legado quando a mecânica específica não foi marcada | KPI de eficiência de 2 pontos (agregado/fallback) | `testing` |
| `specialist_attempt` | oficial/técnica | `SRC-IHF-RULES`, `SRC-SYNTHESIS-BH` | a especialista constitui mecanismo tático próprio de 2 pontos e precisa de denominador separado para análise operacional | eficiência da especialista e leitura tática de uso do recurso | `draft` |
| `specialist_goal` | oficial/técnica | `SRC-IHF-RULES`, `SRC-SYNTHESIS-BH` | o gol da especialista responde a pergunta tática diferente de spin, inflight e shoot-out | eficiência da especialista e separação de KPIs de 2 pontos | `draft` |
| `spin_shot` | oficial/científica | `SRC-IHF-RULES`, `SRC-NOTATIONAL-BH`, `SRC-SYNTHESIS-BH` | ação específica relevante no beach handball; `SRC-SYNTHESIS-BH` funciona como fonte auxiliar de curadoria dos papers notacionais | evento ofensivo e clipe técnico | `testing` |
| `inflight_goal` | oficial/científica | `SRC-IHF-RULES`, `SRC-NOTATIONAL-BH`, `SRC-SYNTHESIS-BH` | ação específica relevante no beach handball; `SRC-SYNTHESIS-BH` consolida a priorização dos estudos de arremesso | evento ofensivo e clipe técnico | `testing` |
| `zone` | científica/técnica | `SRC-NOTATIONAL-BH`, `SRC-SYNTHESIS-BH` | zonas permitem analisar tendência e eficiência; `SRC-SYNTHESIS-BH` aponta os estudos mais úteis para o recorte beach handball | mapa de finalização e vulnerabilidade defensiva | `testing` |
| `technical_error` | metodologia/técnica | `SRC-OBS-MEASUREMENT` | precisa de definição observável para reduzir ambiguidade | perda de posse e correção de treino | `draft` |
| `defensive_breakdown` | técnica | decisão do treinador | útil para feedback, mas interpretativo | relatório coletivo e clips de correção | `draft` |

## Eventos pendentes de documentação na matriz

Os eventos abaixo existem na taxonomia mas ainda não têm registro explícito nesta matriz.
Nenhum deles pode entrar em KPI final até ser documentado aqui.

| Evento | Categoria | Fonte esperada | Status atual |
| --- | --- | --- | --- |
| `shot_attempt` | ofensivo | `SRC-IHF-RULES`, `SRC-OBS-MEASUREMENT` | `draft` |
| `goal_scored` | ofensivo | `SRC-IHF-RULES` | `draft` |
| `shot_missed` | ofensivo | `SRC-IHF-RULES`, `SRC-OBS-MEASUREMENT` | `draft` |
| `turnover` | ofensivo | `SRC-OBS-MEASUREMENT` | `draft` |
| `assist` | ofensivo | `SRC-OBS-MEASUREMENT`, `coach_decision` | `draft` |
| `two_point_attempt` | ofensivo | `SRC-IHF-RULES` | `draft` |
| `inflight_attempt` | ofensivo | `SRC-IHF-RULES`, `SRC-NOTATIONAL-BH` | `draft` |
| `defensive_stop` | defensivo | `SRC-OBS-MEASUREMENT`, `SRC-NOTATIONAL-BH` | `draft` |
| `steal` | defensivo | `SRC-OBS-MEASUREMENT`, `SRC-NOTATIONAL-BH` | `draft` |
| `block` | defensivo | `SRC-OBS-MEASUREMENT`, `SRC-NOTATIONAL-BH` | `draft` |
| `forced_error` | defensivo | `SRC-OBS-MEASUREMENT`, `coach_decision` | `draft` |
| `goal_conceded` | defensivo | `SRC-IHF-RULES` | `draft` |
| `save` | goleira | `SRC-IHF-RULES`, `SRC-NOTATIONAL-BH` | `draft` |
| `save_shootout` | goleira | `SRC-IHF-RULES` | `draft` |
| `goalkeeper_distribution` | goleira | `SRC-IHF-RULES`, `SRC-NOTATIONAL-BH` | `draft` |
| `fast_break_for` | transição | `SRC-NOTATIONAL-BH` | `draft` |
| `fast_break_against` | transição | `SRC-NOTATIONAL-BH` | `draft` |
| `transition_recovery_good` | transição | `SRC-NOTATIONAL-BH`, `coach_decision` | `draft` |
| `transition_recovery_bad` | transição | `SRC-NOTATIONAL-BH`, `coach_decision` | `draft` |
| `shootout_goal` | especial | `SRC-IHF-RULES` | `draft` |
| `shootout_miss` | especial | `SRC-IHF-RULES` | `draft` |
| `timeout` | especial | `SRC-IHF-RULES` | `draft` |
| `set_end` | especial | `SRC-IHF-RULES` | `draft` |

## Próximo passo

Antes de `ScoutPraia v1.0`, cada item deve ter:

- definição operacional
- regra de inclusão
- regra de exclusão
- teste em vídeo
- decisão: manter, ajustar, dividir, fundir ou remover

**Critério de conclusão desta matriz:**

```
[ ] todos os 31 eventos têm linha na tabela principal
[ ] todos os itens têm fonte registrada
[ ] status de cada item está sincronizado com docs/taxonomy_dictionary.md
```
