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

### Status `draft` — exploração e ensaio

- **Permite:** marcação manual, ensaio operacional, teste de fluxo, UI com taxonomia explícita
- **Bloqueia:** KPI final estável, relatório final sem ressalva, promoção silenciosa
- **Para avançar para `testing`:** registrar fonte + escrever definição operacional + marcação humana inicial em vídeo real
- **Fontes:** `SRC-OBS-MEASUREMENT`; `docs/taxonomy_dictionary.md`; `docs/validation_protocol.md`

### Status `testing` — uso controlado

- **Permite:** ensaio controlado, prévia de relatório com ressalva explícita, indicador experimental
- **Bloqueia:** congelamento como regra estável sem rodada de validação suficiente, KPI final sem ressalva
- **Para avançar para `approved`:** executar `docs/validation_protocol.md` → revisar divergências → congelar em nova versão da taxonomia
- **Fontes:** `SRC-IHF-RULES`; `SRC-NOTATIONAL-BH`; `SRC-OBS-MEASUREMENT`; `docs/validation_protocol.md`

### Status `approved` — uso oficial

- **Permite:** KPI final estável, relatório final sem ressalva, uso em decisão de treino/jogo
- **Bloqueia:** alteração silenciosa sem nova versão ou nova evidência
- **Para alterar:** mudança de semântica exige nova versão de taxonomia e revalidação
- **Fontes:** `SRC-IHF-RULES`; `docs/sources/README.md`; `docs/validation_protocol.md`

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
