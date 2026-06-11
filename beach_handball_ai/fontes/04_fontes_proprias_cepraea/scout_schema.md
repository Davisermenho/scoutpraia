---
status: base_interna_elaborada_v0
tipo: fonte_propria_cepraea
uso_previsto: schema_de_scout
escopo: "modelo operacional do dado de marcacao e dos KPIs atuais"
fonte_base:
  - scoutpraia/models/event.py
  - scoutpraia/services/analytics_service.py
  - scoutpraia/ui_labels.py
  - scoutpraia/templates/report_collective.html
  - docs/taxonomy_dictionary.md
observacao: "Schema funcional do ScoutPraia v0.1. Descreve o que o app persiste e o que os relatorios usam hoje."
---

# Scout Schema CEPRAEA

## Finalidade

Este schema resume o dado operacional que o ScoutPraia v0.1 consegue registrar hoje. Ele deve ser usado para:

- alinhar marcacao manual
- evitar campo inventado fora do app
- orientar leitura de relatórios

## Entidades operacionais principais

### Match

Representa o jogo e guarda contexto geral, inclusive relacao com video e adversaria.

### Set

Segmenta o jogo por set para permitir leitura parcial e consolidada.

### Possession

Representa a posse como unidade de leitura coletiva para eficiencia e perda sem finalizacao.

### Event

E a menor unidade de observacao registrada manualmente.

### Clip

Relaciona evento e video para revisao e feedback.

### Report

Materializa leitura coletiva, individual ou de adversaria.

## Estrutura atual do evento

Campos persistidos em `scoutpraia/models/event.py`:

```text
id
match_id
set_id
possession_id
taxonomy_version_id
event_type
event_subtype
player_id
secondary_player_id
team_side
timestamp_second
outcome
zone
points_value
result_possession
scorer_role
court_lane
shot_origin_depth
goal_zone
trajectory_visible
derived_points
review_marker
notes
```

## Campos que devem ser tratados como centrais

- `event_type`
- `team_side`
- `timestamp_second`
- `points_value`
- `zone`
- `player_id`

Sem eles, a leitura técnica e os KPIs ficam comprometidos.

## Vocabulário operacional atual

### Eventos ofensivos

- `shot_attempt`
- `goal_scored`
- `shot_missed`
- `technical_error`
- `turnover`
- `assist`
- `two_point_attempt`
- `two_point_goal`
- `specialist_attempt`
- `specialist_goal`
- `simple_shot`
- `spin_shot`
- `inflight_shot`
- `goalkeeper_shot`
- `six_metre_throw`
- `inflight_attempt`
- `inflight_goal`

### Eventos de perda sem finalizacao v1

- `ball_control_turnover`
- `offensive_foul_turnover`
- `passive_play_turnover`
- `substitution_error_turnover`

### Eventos defensivos

- `defensive_stop`
- `steal`
- `block`
- `forced_error`
- `goal_conceded`
- `defensive_breakdown`

### Goleira, transicao e situacoes especiais

- `save`
- `save_shootout`
- `goalkeeper_distribution`
- `fast_break_for`
- `fast_break_against`
- `transition_recovery_good`
- `transition_recovery_bad`
- `shootout_attempt`
- `shootout_goal`
- `shootout_miss`
- `timeout`
- `set_end`

## Domínios auxiliares

### Lado da equipe

- `team`
- `opponent`

### Zonas principais

- `left_wing`
- `left_half`
- `center`
- `right_half`
- `right_wing`
- `6m_left`
- `6m_center`
- `6m_right`
- `shootout_lane`

## Agrupamentos analíticos já usados pelo app

### Tentativas ofensivas

O analytics atual trata como tentativas:

- `shot_attempt`
- `two_point_attempt`
- `specialist_attempt`
- `inflight_attempt`
- `shootout_attempt`
- `spin_shot`
- `simple_shot`
- `inflight_shot`
- `goalkeeper_shot`
- `six_metre_throw`

### Gols

- `goal_scored`
- `two_point_goal`
- `specialist_goal`
- `inflight_goal`
- `shootout_goal`

### Eventos críticos

- `technical_error`
- `forced_error`
- `defensive_breakdown`
- `fast_break_against`
- `transition_recovery_bad`
- `goal_conceded`

## KPIs coletivos atuais

O relatorio coletivo ja expõe hoje:

- `points_total`
- `goals_total`
- `points_per_possession`
- `offensive_conversion_rate`
- `technical_error_rate`
- `no_shot_attack_total`
- `finalization_attempts_total`
- `two_point_efficiency`
- `specialist_efficiency`
- `shootout_efficiency`
- `specialist_shots_total`

## KPIs individuais atuais

O app ja consegue consolidar por atleta:

- volume de arremessos
- gols totais
- conversao total
- conversao por tipo
- conversao por zona
- turnovers
- erros tecnicos
- roubos
- bloqueios
- defesas
- participacao direta em gol

## KPIs de adversaria atuais

O app ja consegue expor:

- `preferred_attack_side`
- `most_frequent_shooter_player_id`
- `top_two_point_scorer_player_id`
- `pressure_error_rate`
- `transition_vulnerability`
- `specialist_efficiency`
- `shootout_efficiency`

## Exemplo minimo de leitura de evento

```json
{
  "event_type": "specialist_goal",
  "team_side": "team",
  "timestamp_second": 214.4,
  "player_id": 9,
  "zone": "right_half",
  "points_value": 2,
  "notes": "entrada da especialista apos troca"
}
```

## Regras de schema

- nao criar campo conceitual fora do modelo sem necessidade comprovada
- nao trocar evento observavel por interpretacao livre em `notes`
- sempre preferir codigo de evento consistente a descricao longa solta
- qualquer extensao futura deve preservar compatibilidade com analytics e relatórios atuais
