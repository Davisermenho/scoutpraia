---
doc_id: CONT_005
title: "Contrato Operacional — Eventos v1"
status: canonical
version: "1.0.0"
authority_level: 5
category: CONT
owner: Davi Sermenho
created_at: "2026-06-01"
last_updated: "2026-06-13"
repository: Davisermenho/scoutpraia
blocking_policy: "Nenhuma execução sem leitura prévia deste documento."
project: ScoutPraia
semantic_source: 005_CONT_Operacional_Eventos_v1.md
implementation_source: SCOUT_DESIGN_TEMPLATE
---

# Contrato Operacional — Eventos v1

## Resumo Executivo

Contrato canônico que define as regras semânticas, taxonômicas e operacionais dos módulos v1 do ScoutPraia. Governa quais eventos podem ser importados, exibidos na UI e usados em KPIs, com referência cruzada ao `SCOUT_DESIGN_TEMPLATE`.

## 1. Objetivo

Este documento define as regras semânticas, taxonômicas e operacionais para os módulos v1 do ScoutPraia. Ele deve ser usado como referência controlada por humanos e agentes de IA.

Regra principal:

```yaml
global_rule:
  source_priority:
    1: "SCOUT_DESIGN_TEMPLATE"
    2: "005_CONT_Operacional_Eventos_v1.md"
    3: "Davisermenho/scoutpraia"
  blocking_rule: "Divergência entre fontes bloqueia implementação até correção."
```

## 2. Fontes de verdade

```yaml
sources:
  semantic_rules: "005_CONT_Operacional_Eventos_v1.md"
  implementation_structure: "SCOUT_DESIGN_TEMPLATE"
  code_and_tests: "Davisermenho/scoutpraia"
  evidence: "ACCEPTANCE_EVIDENCE"
  blocking_rule: "Divergência entre fontes bloqueia implementação até correção."
```

## 2-bis. Estado consolidado

Referência rápida para agentes. Para regras detalhadas, consultar as seções 6 a 9.

```yaml
consolidated_state:
  last_reviewed_at: "2026-06-10"
  git_head: "7352846"
  modules:
    attack_no_shot_v1:
      status: "contrato_validado"
      import_rule_v1: "importar_v1"
      evidence: ["EV-001", "EV-002", "EV-003", "EV-004", "EV-005"]
      evidence_status: "passed"
    finalization_v1:
      status: "contrato_validado"
      import_rule_v1: "nao_importar_v1"
      evidence: ["EV-006"]
      evidence_status: "passed"
    offensive_creation_v1:
      status: "contrato_validado"
      import_rule_v1: "nao_importar_v1"
      evidence: ["EV-007"]
      evidence_status: "passed"
    defensive_v1:
      status: "contrato_validado"
      import_rule_v1: "nao_importar_v1"
      evidence: ["EV-008"]
      evidence_status: "passed"
```

## 3. Status dos módulos

```yaml
module_status:
  attack_no_shot_v1:
    name: "Ataque sem finalização v1.0"
    status: "contrato_validado"
    import_rule_v1: "importar_v1"
    evidence: ["EV-001", "EV-002", "EV-003", "EV-004", "EV-005"]
    evidence_status: "passed"
    validated_core_events:
      - "technical_error_unforced"
      - "technical_error_forced"
      - "offensive_foul"
      - "goal_area_invasion_attack"
      - "passive_play_turnover"
      - "bad_substitution_attack"
      - "turnover_unclassified"

  finalization_v1:
    name: "Finalização v1.0"
    status: "contrato_validado"
    import_rule_v1: "nao_importar_v1"
    evidence: ["EV-006"]
    evidence_status: "passed"
    validated_core_events:
      - "simple_shot"
      - "spin_shot"
      - "inflight_shot"
      - "goalkeeper_shot"
      - "six_metre_throw"
    auxiliary_only:
      - "specialist_finish_role"

  offensive_creation_v1:
    name: "Criação ofensiva v1.0"
    status: "contrato_validado"
    import_rule_v1: "nao_importar_v1"
    evidence: ["EV-007"]
    evidence_status: "passed"
    validated_core_event: "assist_to_finalization"
    reclassified_auxiliary_events:
      - "assist_to_inflight_shot"
      - "pivot_feed_to_shot"
    review_only_events:
      - "advantage_pass_to_free_player"
      - "collective_action_creates_shot"
    blocking_rule: "Mesmo validado por contrato, não importar no app antes de implementação controlada e testes de integração."

  defensive_v1:
    name: "Defensivo v1.0"
    status: "contrato_validado"
    import_rule_v1: "nao_importar_v1"
    evidence: ["EV-008"]
    evidence_status: "passed"
    validated_core_event: "line_block_shot"
    review_only_events:
      - "defensive_pressure_forced_error"
      - "steal_or_interception"
    future_events:
      - "defensive_rebound_recovery"
    blocking_rule: "Mesmo validado por contrato, não importar no app antes de implementação controlada e testes de integração."
```

## 4. Governança global

```yaml
global_constraints:
  forbidden_actions:
    - "importar_via_category_apenas"
    - "misturar_ataque_sem_finalizacao_com_finalizacao"
    - "misturar_transicao_com_ataque_sem_finalizacao"
    - "misturar_criacao_ofensiva_com_finalizacao"
    - "misturar_defensivo_com_goleira"
    - "misturar_defensivo_com_transicao"
    - "criar_specialist_shot"
    - "criar_position_code_specialist"
    - "allow_manual_points_in_finalization"
    - "allow_goal_zone_outside_finalization"
  activation_rules:
    - "require_implementation_test_evidence"
    - "require_import_rule_v1_explicit"
    - "require_module_contract_status_explicit"
    - "require_contract_scope_explicit"
```

## 5. Taxonomias globais

```yaml
taxonomies:
  systems:
    valid_codes: ["AT_3X1", "AT_4X0", "DEF_3X0", "DEF_2X1", "man_to_man"]
    context_only: ["fast_break_attack", "specialist_on_court", "empty_goal_attack", "high_press"]
    note: "Especialista é papel dinâmico, não sistema ou posição."

  court_zones:
    lanes: ["lane_1_outer_left", "lane_2_inner_left", "lane_3_central_axis", "lane_4_inner_right", "lane_5_outer_right"]
    depth: ["depth_0_backcourt", "depth_1_far", "depth_2_mid", "depth_3_near_area"]
    note: "Zona da quadra descreve localização espacial, não função tática."

  goal_zones:
    note: "Aplicável apenas à Finalização quando a trajetória ao gol for visível ou inferível com segurança."

  possession_results:
    global: ["goal", "save", "shot_wide", "shot_blocked", "lost_possession_no_shot", "rebound_live", "execution_invalid_6m"]
```

## 6. Módulo attack_no_shot_v1

```yaml
module_attack_no_shot:
  module_id: "attack_no_shot_v1"
  name: "Ataque sem finalização v1.0"
  definition: "Toda posse ofensiva sem arremesso intencional ao gol."
  status: "contrato_validado"
  import_rule_v1: "importar_v1"
  last_reviewed_at: "2026-06-10"
  git_head: "7352846"
  mandatory_result: "lost_possession_no_shot"
  source_tabs:
    events: "EVENTOS"
    fields: "CAMPOS_AUXILIARES_ATAQUE_SEM_FINALIZACAO"
    tests: "TESTES_ATAQUE_SEM_FINALIZACAO"
  official_events:
    - "technical_error_unforced"
    - "technical_error_forced"
    - "offensive_foul"
    - "goal_area_invasion_attack"
    - "passive_play_turnover"
    - "bad_substitution_attack"
    - "turnover_unclassified"
  deprecated_codes:
    - "ball_control_turnover"
    - "offensive_foul_turnover"
    - "substitution_error_turnover"
    - "turnover_cause_detail"
```

## 7. Módulo finalization_v1

```yaml
module_finalization:
  module_id: "finalization_v1"
  name: "Finalização v1.0"
  definition: "Ação com arremesso intencional ao gol."
  status: "contrato_validado"
  import_rule_v1: "nao_importar_v1"
  last_reviewed_at: "2026-06-10"
  git_head: "7352846"
  evidence: "EV-006"
  source_tabs:
    events: "EVENTOS"
    fields: "CAMPOS_AUXILIARES_FINALIZACAO"
    results_by_event: "RESULTADOS_POR_EVENTO_FINALIZACAO"
    scoring: "PONTUACAO_FINALIZACAO"
    tests: "TESTES_FINALIZACAO"
  core_events:
    simple_shot:
      ui_type: "botao_principal"
      points_rule: "1 se goal + field_player; 2 se goal + specialist; 0 se não gol"
    spin_shot:
      ui_type: "botao_principal"
      points_rule: "2 se goal; 0 se não gol"
    inflight_shot:
      ui_type: "botao_principal"
      points_rule: "2 se goal; 0 se não gol"
    goalkeeper_shot:
      ui_type: "botao_principal"
      points_rule: "2 se goal; 0 se não gol"
    six_metre_throw:
      ui_type: "botao_principal"
      points_rule: "2 se goal; 0 se não gol"
  auxiliary_only:
    specialist_finish_role:
      rule: "Especialista é função dinâmica via scorer_role/offensive_role; não é botão nem position_code."
  forbidden_logic:
    - "Não criar specialist_shot."
    - "Não criar position_code=specialist."
    - "Não permitir pontos manuais divergentes da pontuação derivada."
    - "Não permitir lost_possession_no_shot em Finalização."
    - "Não permitir six_metre_throw + shot_blocked."
    - "Não permitir goalkeeper_shot + shot_blocked na v1.0."
```

## 8. Módulo offensive_creation_v1

```yaml
module_offensive_creation:
  module_id: "offensive_creation_v1"
  name: "Criação ofensiva v1.0"
  definition: "Ações ofensivas que criam, melhoram ou organizam condição de finalização, sem serem a finalização em si e sem serem perda de posse sem arremesso."
  status: "contrato_validado"
  import_rule_v1: "nao_importar_v1"
  last_reviewed_at: "2026-06-10"
  git_head: "7352846"
  evidence: "EV-007"
  source_tabs:
    events: "EVENTOS"
    fields: "CAMPOS_AUXILIARES_CRIACAO_OFENSIVA"
    results: "RESULTADOS_CRIACAO_OFENSIVA"
    tests: "TESTES_CRIACAO_OFENSIVA"
    versioning: "VERSIONAMENTO_CRIACAO_OFENSIVA"
  active_core_event:
    assist_to_finalization:
      ui_type: "botao_principal"
      rule: "Último passe que gera finalização imediata."
      required_result_creation: "shot_created"
      allowed_creation_types: ["direct_assist", "inflight_setup", "pivot_feed"]
      required_fields:
        - "passer_id"
        - "receiver_id"
        - "system_code"
        - "pass_origin_position"
        - "receiver_position"
        - "pass_origin_zone"
        - "receiver_zone"
        - "creation_type"
        - "created_finalization_type"
        - "result_creation"
  reclassified_auxiliary_events:
    assist_to_inflight_shot:
      maps_to: "assist_to_finalization + creation_type=inflight_setup + created_finalization_type=inflight_shot"
      ui_type: "campo_auxiliar"
      import_rule_v1: "nao_importar_v1"
    pivot_feed_to_shot:
      maps_to: "assist_to_finalization + creation_type=pivot_feed"
      ui_type: "campo_auxiliar"
      import_rule_v1: "nao_importar_v1"
  review_only_events:
    advantage_pass_to_free_player:
      ui_type: "botao_secundario_revisao"
      required: ["created_advantage", "result_creation=clear_chance_created", "review_marker=Sim"]
      reason: "Subjetivo sem exemplos reais suficientes; não liberar como botão ativo."
    collective_action_creates_shot:
      ui_type: "fallback_revisao"
      required: ["system_code", "creation_type", "result_creation", "review_marker=Sim"]
      reason: "Amplo demais para botão v1.0; usar apenas quando passe criador não for isolável."
  location_rules:
    pass_origin_position: "POSIÇÕES"
    receiver_position: "POSIÇÕES"
    pass_origin_zone: "ZONAS_QUADRA"
    receiver_zone: "ZONAS_QUADRA"
    note: "Posição tática não substitui zona espacial; zona espacial não substitui posição tática."
  forbidden_logic:
    - "Criação ofensiva não calcula pontos."
    - "Não usar goal_zone em Criação ofensiva."
    - "Não usar shot_origin_depth em Criação ofensiva."
    - "Não usar result_possession sem linked_finalization_id."
    - "Não usar turnover_after_creation_error como resultado ativo; perda sem arremesso pertence ao attack_no_shot_v1."
    - "Não criar botões novos a partir de creation_type."
```

## 9. Módulo defensive_v1

```yaml
module_defensive:
  module_id: "defensive_v1"
  name: "Defensivo v1.0"
  definition: "Ações observáveis de jogadoras de linha defensiva que bloqueiam finalização, forçam erro ou recuperam/interceptam posse, sem misturar com Goleira, Transição ou Finalização."
  status: "contrato_validado"
  import_rule_v1: "nao_importar_v1"
  last_reviewed_at: "2026-06-10"
  git_head: "7352846"
  evidence: "EV-008"
  source_tabs:
    events: "EVENTOS"
    fields: "CAMPOS_AUXILIARES_DEFENSIVO"
    results: "RESULTADOS_DEFENSIVO"
    tests: "TESTES_DEFENSIVO"
    versioning: "VERSIONAMENTO_DEFENSIVO"
  active_core_event:
    line_block_shot:
      ui_type: "botao_principal"
      rule: "Bloqueio/interferência legal de jogadora de linha em finalização bloqueável."
      required_result_defense: "shot_blocked_linked"
      required_link: "linked_finalization_id"
      allowed_linked_finalization_event_code: ["simple_shot", "spin_shot", "inflight_shot"]
      forbidden_linked_finalization_event_code: ["six_metre_throw", "goalkeeper_shot"]
      required_fields:
        - "defender_id"
        - "defensive_system_code"
        - "defensive_position_code"
        - "linked_finalization_id"
        - "linked_finalization_event_code"
        - "court_lane"
        - "court_depth"
        - "result_defense"
  review_only_events:
    defensive_pressure_forced_error:
      ui_type: "botao_secundario_revisao"
      required: ["linked_attack_no_shot_id", "review_marker=Sim"]
      reason: "Não duplicar technical_error_forced sem vínculo com attack_no_shot_v1."
    steal_or_interception:
      ui_type: "botao_secundario_revisao"
      required: ["defensive_control_clear", "review_marker=Sim"]
      reason: "Conecta com troca de posse e Transição; manter em revisão/futuro."
  future_events:
    defensive_rebound_recovery:
      ui_type: "future_module"
      reason: "Depende de modelagem de Rebote/Transição."
  defensive_positions_by_system:
    DEF_3X0: ["def_3x0_cobertura", "def_3x0_base", "def_3x0_solta"]
    DEF_2X1: ["def_2x1_cobertura", "def_2x1_avancada", "def_2x1_solta"]
  forbidden_logic:
    - "Não usar Base no DEF_2X1."
    - "Não usar Avançada no DEF_3X0."
    - "Não usar name_ui como defensive_position_code; usar position_code."
    - "Não registrar defesa da goleira como Defensivo v1.0."
    - "Não registrar line_block_shot sem linked_finalization_id."
    - "Não permitir line_block_shot vinculado a six_metre_throw ou goalkeeper_shot na v1.0."
    - "Não duplicar technical_error_forced sem linked_attack_no_shot_id."
    - "Não calcular pontos em Defensivo."
    - "Não usar goal_zone, scorer_role ou shot_origin_depth em Defensivo."
```

## 10. Evidências de aceitação

```yaml
acceptance_tests:
  EV-001:
    command: "python3 -m pytest tests/test_attack_no_shot_contract.py -q"
    expected_result: "all tests passed"
    actual_result: "25 passed in 0.05s"
    status: "passed"
    executed_by: "Davi Sermenho"
    executed_at: "2026-06-10"
    git_head: "5cf588c"
    module: "attack_no_shot_v1"

  EV-002:
    command: "python3 -m pytest -q"
    expected_result: "all tests passed"
    actual_result: "196 passed in 12.77s"
    status: "passed"
    executed_by: "Davi Sermenho"
    executed_at: "2026-06-10"
    git_head: "5cf588c"
    module: "global"

  EV-003:
    command: "scripts/verify_current_state.sh"
    expected_result: "all checks passed"
    actual_result: "verde; 199 passed in 12.93s; hygiene/import/seed/git whitespace ok"
    status: "passed"
    executed_by: "Davi Sermenho"
    executed_at: "2026-06-10"
    git_head: "7352846"
    module: "global"

  EV-004:
    command: "python3 -m pytest tests/test_attack_no_shot_import_scope.py -q"
    expected_result: "all tests passed"
    actual_result: "4 passed in 0.03s"
    status: "passed"
    executed_by: "Davi Sermenho"
    executed_at: "2026-06-10"
    git_head: "5cf588c"
    module: "attack_no_shot_v1"

  EV-005:
    command: "python3 -m pytest tests/test_eventos_sheet_scope.py -q"
    expected_result: "all tests passed"
    actual_result: "7 passed in 0.01s"
    status: "passed"
    executed_by: "Davi Sermenho"
    executed_at: "2026-06-10"
    git_head: "5cf588c"
    module: "sheet_scope"

  EV-006:
    command: "python3 -m pytest tests/test_finalization_contract.py"
    expected_result: "29 passed"
    actual_result: "29 passed in 0.04s"
    status: "passed"
    executed_by: "Davi Sermenho"
    executed_at: "2026-06-10"
    commit: "614626e907d2d25bbbd46d473d241055aa33eacf"
    module: "finalization_v1"

  EV-007:
    command: "python3 -m pytest tests/test_offensive_creation_contract.py"
    expected_result: "20 passed"
    actual_result: "20 passed in 0.04s"
    status: "passed"
    executed_by: "Davi Sermenho"
    executed_at: "2026-06-10"
    commit: "11da639bbdb5b90973972059424690cc28d66145"
    module: "offensive_creation_v1"

  EV-008:
    command: "python3 -m pytest tests/test_defensive_contract.py -q"
    expected_result: "28 passed"
    actual_result: "28 passed in 0.05s"
    status: "passed"
    executed_by: "Davi Sermenho"
    executed_at: "2026-06-10"
    commit: "7a93d7728c966f229cf253d8fc5ca3ead154138d"
    module: "defensive_v1"
```

## 11. Regras de liberação

```yaml
release_rules:
  current_state: "todos_contratos_validados"
  last_reviewed_at: "2026-06-10"
  git_head: "7352846"
  app_import_ready:
    attack_no_shot_v1: "importar_v1"
    finalization_v1: "aguarda_ativacao_app"
    offensive_creation_v1: "aguarda_ativacao_app"
    defensive_v1: "aguarda_ativacao_app"
  blockers_before_full_app_activation:
    - "Validar que nenhum módulo v1 é importado apenas por category."
    - "Executar testes de integração de app antes de ativar finalization_v1, offensive_creation_v1 e defensive_v1."
    - "Confirmar fluxo de app com attack_no_shot_v1 ativo antes de ativar módulos dependentes."
```

## 12. Histórico de alterações

As entradas abaixo são registros históricos. O estado atual e autoritativo está nas seções 3, 6, 10 e 11.

### G0 — Alinhamento Ataque sem finalização v1.0 (2026-06-10)

```yaml
g0_attack_no_shot_alignment:
  date: "2026-06-10"
  module_id: "attack_no_shot_v1"
  status: "contrato_validado"
  import_rule_v1: "importar_v1"
  official_events: ["technical_error_unforced", "technical_error_forced", "offensive_foul", "goal_area_invasion_attack", "passive_play_turnover", "bad_substitution_attack", "turnover_unclassified"]
  deprecated_codes: ["ball_control_turnover", "offensive_foul_turnover", "substitution_error_turnover", "turnover_cause_detail"]
  repo_commits: ["904868a", "ac033d6", "2df3044", "3ee9553", "e5c080a", "01cced7"]
  evidence_completed: ["EV-001", "EV-002", "EV-003", "EV-004", "EV-005"]
```

### G0 — Evidência aprovada (Ataque sem finalização v1.0)

```yaml
g0_attack_no_shot_acceptance:
  date: "2026-06-10"
  git_head: "5cf588c"
  executed_by: "Davi Sermenho"
  module_id: "attack_no_shot_v1"
  status_after_evidence: "contrato_validado"
  import_rule_v1: "importar_v1"
  evidence:
    EV-001:
      command: "python3 -m pytest tests/test_attack_no_shot_contract.py -q"
      result: "25 passed in 0.05s"
      status: "passed"
    EV-002:
      command: "python3 -m pytest -q"
      result: "196 passed in 14.89s"
      status: "passed"
    EV-003:
      command: "scripts/verify_current_state.sh"
      result: "verde; 196 passed in 11.96s; hygiene/import/seed/git whitespace ok"
      status: "passed"
    EV-004:
      command: "python3 -m pytest tests/test_attack_no_shot_import_scope.py -q"
      result: "4 passed in 0.03s"
      status: "passed"
    EV-005:
      command: "python3 -m pytest tests/test_eventos_sheet_scope.py -q"
      result: "7 passed in 0.02s"
      status: "passed"
  compatibility_note: "Códigos legados de UI foram mantidos como aliases temporários; os nomes oficiais continuam sendo os definidos no SCOUT_DESIGN_TEMPLATE."
  seed_note: "Taxonomia operacional padrão permanece ScoutPraia v0.1 draft com 31 eventos; G0 valida contrato/código, não troca automática do seed."
```

### G1-FIX — Correção do contrato operacional (2026-06-10)

```yaml
g1_fix_summary:
  date: "2026-06-10"
  git_head: "7352846"
  executed_by: "Davi Sermenho"
  changes:
    - "Seção 3: attack_no_shot_v1 atualizado de bloqueado_por_auditoria para contrato_validado."
    - "Seção 6: status e import_rule_v1 corrigidos; current_blockers e blocking_rule removidos."
    - "Seção 10: EV-001 a EV-005 atualizados de pending para passed com resultados reais e git_head."
    - "Seção 10: EV-006 recebeu commit hash da planilha ACCEPTANCE_EVIDENCE."
    - "Seção 11: release_rules atualizado; blockers resolvidos removidos; app_import_ready adicionado."
    - "Campo import_rule padronizado para import_rule_v1 em todas as seções (alinhado com código e planilha)."
    - "Escapes de markdown removidos dos blocos YAML e cabeçalhos."
    - "Seção 2-bis (Estado consolidado) adicionada como referência rápida para agentes."
    - "last_reviewed_at e git_head adicionados às seções de módulos 6 a 9."
    - "Seções 12-13 convertidas para Histórico de alterações com marcação explícita."
```



## 14. Abertura de módulo — shootout_v1
```yaml
module_shootout:
  module_id: "shootout_v1"
  name: "Shoot-out v1.0"
  status: "arquitetura_em_definicao"
  import_rule_v1: "nao_importar_v1"
  source_tabs:
    events: "EVENTOS"
    fields: "CAMPOS_AUXILIARES_SHOOTOUT"
    results: "RESULTADOS_SHOOTOUT"
    tests: "TESTES_SHOOTOUT"
    versioning: "VERSIONAMENTO_SHOOTOUT"
  active_core_candidate:
    shootout_attempt:
      ui_type: "botao_principal"
      rule: "Tentativa individual de shoot-out em fluxo regulamentar próprio."
      required_fields: ["shooter_id", "goalkeeper_id", "result_shootout", "shootout_phase", "attempt_order"]
      optional_fields: ["court_lane", "goal_zone", "trajectory_visible", "execution_validity", "review_marker"]
      scoring_rule: "2 pontos se result_shootout=goal; 0 nos demais resultados."
  result_candidates: ["goal", "save", "shot_wide", "execution_invalid", "goalkeeper_violation_retry"]
  forbidden_logic:
    - "Não criar shootout_goal ou shootout_miss como eventos separados."
    - "Não misturar shoot-out com six_metre_throw."
    - "Não usar result_possession no módulo Shoot-out v1.0."
    - "Não usar shot_origin_depth ou scorer_role em Shoot-out v1.0."
    - "Não importar no app até evidência de contrato e testes."
  current_status: "Módulo aberto, ainda não validado. Não pertence aos quatro módulos fechados anteriormente."
```


## 15. Refinamento tático — shootout_v1
```yaml
shootout_tactical_refinement:
  date: "2026-06-10"
  decision: "Shoot-out v1.0 deve registrar a tentativa completa, não apenas o arremesso final."
  core_event: "shootout_attempt"
  model: "single_event_with_tactical_phases"
  tactical_phases:
    - "decisão da goleira lançadora"
    - "comportamento pré-lançamento da defensora-goleira"
    - "tipo e resultado do lançamento"
    - "qualidade da recepção da atacante"
    - "pressão e armadilha defensiva"
    - "resposta técnica da atacante"
    - "resultado final e pontuação derivada"
  required_new_fields:
    - "launcher_goalkeeper_id"
    - "defender_goalkeeper_id"
    - "defender_goalkeeper_role"
    - "pre_launch_defensive_behavior"
    - "launch_type"
    - "launch_result"
    - "defensive_trap_type"
  conditional_fields:
    reception_quality: "obrigatório quando launch_result in [pass_completed, pass_pressured]"
    shooter_pressure_level: "obrigatório quando reception_quality preenchido"
    defender_recovery_behavior: "obrigatório quando defender_goalkeeper_role != traditional_goalkeeper"
  action_type_rule: "shootout_action_type é campo auxiliar; não criar eventos shootout_spin, shootout_double_spin, shootout_inflight ou shootout_lob."
  status: "arquitetura_em_definicao"
  import_rule_v1: "nao_importar_v1"
```


## 16. Correção conceitual — papéis funcionais no shootout_v1
```yaml
shootout_role_modeling:
  date: "2026-06-10"
  decision: "No shoot-out, lançadora e defensora são papéis funcionais, não posições fixas."
  implication: "Qualquer athlete_id pode exercer o papel de lançadora ou defensora do shoot-out quando estiver regulamentarmente naquela função."
  deprecated_fields:
    - "launcher_goalkeeper_id"
    - "defender_goalkeeper_id"
    - "defender_goalkeeper_role"
  required_fields_replacing_them:
    - "shootout_launcher_id"
    - "shootout_launcher_role"
    - "shootout_defender_id"
    - "shootout_defender_role"
  launcher_role_values:
    - "designated_goalkeeper_launcher"
    - "line_player_launcher"
    - "specialist_launcher"
    - "emergency_launcher"
    - "unknown_review"
  defender_role_values:
    - "traditional_goalkeeper_defender"
    - "advanced_line_defender"
    - "hybrid_goalkeeper_defender"
    - "pass_interceptor_defender"
    - "goal_line_recovery_defender"
    - "unknown_review"
  blocking_rules:
    - "block_if shootout_launcher_id empty"
    - "block_if shootout_launcher_role empty"
    - "block_if shootout_defender_id empty"
    - "block_if shootout_defender_role empty"
    - "block_if shootout_launcher_role=unknown_review and review_marker != Sim"
    - "block_if shootout_defender_role=unknown_review and review_marker != Sim"
    - "block_if legacy goalkeeper field exists"
  status: "aplicado_na_planilha"
```


## 17. Auditoria cruzada — shootout_v1
```yaml
shootout_cross_audit:
  date: "2026-06-10"
  checked_sources:
    - "EVENTOS"
    - "CAMPOS_AUXILIARES_SHOOTOUT"
    - "RESULTADOS_SHOOTOUT"
    - "TESTES_SHOOTOUT"
    - "VERSIONAMENTO_SHOOTOUT"
  corrections_applied:
    - "goalkeeper_id foi rebaixado para legacy_goalkeeper_id bloqueado."
    - "launcher_goalkeeper_id, defender_goalkeeper_id e defender_goalkeeper_role permanecem como campos legados proibidos."
    - "goalkeeper_violation_retry foi substituído por defender_infraction_retry."
    - "execution_validity passou a usar defender_infraction em vez de goalkeeper_violation."
    - "Textos do evento foram migrados para atleta lançadora e atleta defensora, sem presumir posição fixa."
  current_core_event: "shootout_attempt"
  module_status: "arquitetura_em_definicao"
  import_rule_v1: "nao_importar_v1"
  result_under_review: "defender_infraction_retry"
  next_step: "criar tests/test_shootout_contract.py somente após revisão final dos campos condicionais."
```


## 18. Correção operacional — sem repetição normal no shootout_v1
```yaml
shootout_no_retry_rule_correction:
  date: "2026-06-10"
  decision: "No shoot-out v1.0 não há repetição normal da tentativa por paralisação comum."
  removed_logic:
    - "defender_infraction_retry"
    - "retry_linked_attempt_id"
    - "retry_ordered"
  corrected_rules:
    ball_ground_contact:
      rule: "Se a bola toca a areia em passe obrigatório, a tentativa é perdida."
      result_shootout: "launch_ground_contact"
      points: 0
    legal_pass_interception:
      rule: "Se a atleta defensora intercepta legalmente o passe, a tentativa é perdida."
      result_shootout: "pass_intercepted"
      points: 0
    defensive_contact_generates_6m:
      rule: "Se a ação defensiva impede clara chance de gol de forma irregular, a consequência operacional é tiro de 6m."
      result_shootout: "defender_foul_6m_awarded"
      points: 0
      next_event_required: "six_metre_throw"
  current_result_shootout_values:
    - "goal"
    - "save"
    - "shot_wide"
    - "attacker_execution_error"
    - "launch_ground_contact"
    - "pass_intercepted"
    - "defender_foul_6m_awarded"
  status: "aplicado_na_planilha"
  import_rule_v1: "nao_importar_v1"
```


## 19. Registro de repositório — shootout_v1 pronto para teste conceitual
```yaml
shootout_repo_registration:
  date: "2026-06-10"
  module_id: "shootout_v1"
  status: "arquitetura_em_definicao_pronta_para_teste_conceitual"
  import_rule_v1: "nao_importar_v1"
  app_ui_status: "nao_liberado"
  import_status: "nao_liberado"
  core_event:
    event_code: "shootout_attempt"
    ui_type: "botao_principal"
    allowed_results:
      - "goal"
      - "save"
      - "shot_wide"
      - "attacker_execution_error"
      - "launch_ground_contact"
      - "pass_intercepted"
      - "defender_foul_6m_awarded"
  key_rules:
    - "shootout_attempt é o único evento principal do módulo."
    - "Pontuação é derivada: 2 se result_shootout=goal; 0 nos demais resultados."
    - "Bola toca a areia em passe obrigatório: result_shootout=launch_ground_contact."
    - "Passe interceptado legalmente: result_shootout=pass_intercepted."
    - "Ação defensiva irregular que gera 6m: result_shootout=defender_foul_6m_awarded e next_event_required=six_metre_throw."
    - "six_metre_throw não substitui shootout_attempt como evento principal."
    - "Não existe repetição normal da tentativa no contrato v1."
    - "Lançadora e defensora são papéis funcionais, não posições fixas."
  functional_role_fields:
    launcher:
      - "shootout_launcher_id"
      - "shootout_launcher_role"
    defender:
      - "shootout_defender_id"
      - "shootout_defender_role"
  deprecated_or_blocked:
    event_codes:
      - "shootout_goal"
      - "shootout_miss"
      - "shootout_spin"
      - "shootout_double_spin"
      - "shootout_inflight"
      - "shootout_interception"
    fields:
      - "goalkeeper_id"
      - "launcher_goalkeeper_id"
      - "defender_goalkeeper_id"
      - "defender_goalkeeper_role"
      - "retry_linked_attempt_id"
      - "legacy_retry_linked_attempt_id"
    results:
      - "defender_infraction_retry"
      - "goalkeeper_violation_retry"
      - "retry_ordered"
  repository_changes:
    commits:
      - "d15400b Registra shootout v1 como contrato pronto para teste"
      - "2d96a73 Inclui shootout v1 no teste de registry"
      - "0bbaca6 Adiciona testes conceituais do contrato de shootout"
      - "3d7f76a Exporta contrato shootout v1"
    files:
      - "scoutpraia/contracts/events_v1.py"
      - "tests/test_events_v1_contract_registry.py"
      - "tests/test_shootout_contract.py"
      - "scoutpraia/contracts/__init__.py"
  required_local_validation:
    - "git pull"
    - "python3 -m pytest tests/test_shootout_contract.py -q"
    - "python3 -m pytest tests/test_events_v1_contract_registry.py -q"
    - "python3 -m pytest -q"
    - "scripts/verify_current_state.sh"
    - "git diff --check"
    - "git status --short"
  evidence_status: "pending_local_validation"
```


## 20. Abertura de módulo — goalkeeper_v1
```yaml
goalkeeper_module_opening:
  date: "2026-06-10"
  module_id: "goalkeeper_v1"
  name: "Goleira v1.0"
  status: "arquitetura_em_definicao"
  import_rule_v1: "nao_importar_v1"
  app_ui_status: "nao_liberado"
  import_status: "nao_liberado"
  seed_status: "inalterado"
  source_tabs:
    events: "EVENTOS"
    fields: "CAMPOS_AUXILIARES_GOLEIRA"
    results: "RESULTADOS_GOLEIRA"
    tests: "TESTES_GOLEIRA"
    versioning: "VERSIONAMENTO_GOLEIRA"
  core_candidate:
    goalkeeper_save:
      ui_type: "botao_principal"
      rule: "Ação observável da atleta que exerce função de goleira no jogo normal/set, impedindo finalização adversária válida de resultar em gol."
      required_fields:
        - "goalkeeper_id"
        - "linked_finalization_id"
        - "linked_finalization_event_code"
        - "result_goalkeeper"
        - "save_type"
      allowed_linked_finalization_event_code:
        - "simple_shot"
        - "spin_shot"
        - "inflight_shot"
        - "goalkeeper_shot"
      blocked_linked_event_code:
        - "shootout_attempt"
        - "six_metre_throw"
  current_result_candidates:
    - "save_controlled"
    - "save_rebound_live"
    - "save_rebound_out"
    - "save_restart"
    - "goal_allowed_review"
    - "uncertain_review"
  forbidden_logic:
    - "Não registrar defesa da atleta defensora no Shoot-out como goalkeeper_save."
    - "Não registrar bloqueio de jogadora de linha como goalkeeper_save."
    - "Não registrar goalkeeper_save sem linked_finalization_id."
    - "Não calcular pontos em goalkeeper_v1."
    - "Não substituir módulo futuro de Transição por transition_after_save."
  current_status: "Módulo aberto na planilha; ainda não validado por teste no repositório."
```


## 21. Auditoria inicial — goalkeeper_v1
```yaml
goalkeeper_initial_audit:
  date: "2026-06-10"
  module_id: "goalkeeper_v1"
  status: "arquitetura_em_definicao"
  import_rule_v1: "nao_importar_v1"
  decisions:
    six_metre_throw:
      decision: "fora da Goleira v1.0"
      rule: "goalkeeper_save não pode vincular linked_finalization_event_code=six_metre_throw nesta fase."
      reason: "Defesa em tiro de 6m exige revisão específica futura."
    goal_allowed_review:
      decision: "fora do resultado permitido de goalkeeper_save"
      rule: "goal_allowed_review fica como análise futura/revisão, não como result_goalkeeper válido do núcleo goalkeeper_save."
      reason: "Gol sofrido não é defesa positiva da goleira."
    rebound_result:
      decision: "campo condicional"
      rule: "Obrigatório apenas quando result_goalkeeper=save_rebound_live."
      reason: "Defesa controlada ou bola para fora não exigem classificação de rebote vivo."
    transition_after_save:
      decision: "campo marcador opcional"
      rule: "Pode indicar fast_outlet ou controlled_outlet, mas não substitui futuro módulo de Transição."
    goalkeeper_shot:
      decision: "finalização vinculável"
      rule: "goalkeeper_save pode vincular linked_finalization_event_code=goalkeeper_shot quando a goleira adversária finaliza em jogo normal."
  allowed_linked_finalization_event_code:
    - "simple_shot"
    - "spin_shot"
    - "inflight_shot"
    - "goalkeeper_shot"
  blocked_linked_finalization_event_code:
    - "shootout_attempt"
    - "six_metre_throw"
  allowed_result_goalkeeper:
    - "save_controlled"
    - "save_rebound_live"
    - "save_rebound_out"
    - "save_restart"
    - "uncertain_review"
  blocked_result_goalkeeper:
    - "goal_allowed_review"
  current_status: "Arquitetura auditada na planilha; ainda sem teste no repositório."
```


## 22. Auditoria cruzada — goalkeeper_v1
```yaml
goalkeeper_cross_audit:
  date: "2026-06-10"
  module_id: "goalkeeper_v1"
  status: "arquitetura_em_definicao_auditada"
  import_rule_v1: "nao_importar_v1"
  checked_sources:
    - "EVENTOS"
    - "CAMPOS_AUXILIARES_GOLEIRA"
    - "RESULTADOS_GOLEIRA"
    - "TESTES_GOLEIRA"
    - "VERSIONAMENTO_GOLEIRA"
  corrections_applied:
    - "shot_goal_zone, trajectory_visible e review_marker foram adicionados aos campos auxiliares porque já apareciam como opcionais em EVENTOS."
    - "save_body_part teve regra de qualidade visual corrigida para bloquear save_type específico quando a parte do corpo não está visível."
    - "goal_allowed_review permanece bloqueado como result_goalkeeper do núcleo goalkeeper_save."
    - "six_metre_throw permanece bloqueado como linked_finalization_event_code nesta v1.0."
    - "shootout_attempt permanece bloqueado para evitar mistura com shootout_v1."
    - "line_block_shot/defensive_position_code permanecem bloqueados para evitar mistura com defensive_v1."
  current_core_event: "goalkeeper_save"
  required_fields:
    - "goalkeeper_id"
    - "linked_finalization_id"
    - "linked_finalization_event_code"
    - "result_goalkeeper"
    - "save_type"
  allowed_result_goalkeeper:
    - "save_controlled"
    - "save_rebound_live"
    - "save_rebound_out"
    - "save_restart"
    - "uncertain_review"
  blocked_result_goalkeeper:
    - "goal_allowed_review"
  allowed_linked_finalization_event_code:
    - "simple_shot"
    - "spin_shot"
    - "inflight_shot"
    - "goalkeeper_shot"
  blocked_linked_finalization_event_code:
    - "shootout_attempt"
    - "six_metre_throw"
  next_step: "criar tests/test_goalkeeper_contract.py somente após revisão final ou aprovação do usuário."
```


## 23. Correção de arquitetura — goalkeeper_v1 ampliado
```yaml
goalkeeper_architecture_correction:
  date: "2026-06-10"
  module_id: "goalkeeper_v1"
  status: "arquitetura_em_definicao_corrigida"
  import_rule_v1: "nao_importar_v1"
  reason: "A goleira no beach handball não é responsável apenas por defesas; também precisa ser avaliada contra 6m, gols sofridos e ciclo de troca com a especialista."
  core_events:
    goalkeeper_save:
      purpose: "Registrar defesas da goleira vinculadas a finalizações adversárias."
      linked_finalization_event_code_allowed:
        - "simple_shot"
        - "spin_shot"
        - "inflight_shot"
        - "goalkeeper_shot"
        - "six_metre_throw"
      allowed_results:
        - "save_controlled"
        - "save_rebound_live"
        - "save_out_endline"
        - "save_out_sideline"
        - "uncertain_review"
      possession_rules:
        save_controlled: "possession_after_save=goalkeeper_team"
        save_rebound_live: "possession_after_save=live_ball"
        save_out_endline: "possession_after_save=goalkeeper_team; restart_after_save=goalkeeper_throw"
        save_out_sideline: "possession_after_save=opponent_team; restart_after_save=opponent_throw_in"
    goalkeeper_goal_allowed:
      purpose: "Registrar gols sofridos pela goleira vinculados a finalizações adversárias."
      linked_finalization_event_code_allowed:
        - "simple_shot"
        - "spin_shot"
        - "inflight_shot"
        - "goalkeeper_shot"
        - "six_metre_throw"
      required_result: "goal_allowed"
      reason: "Sem gols sofridos, não há como calcular eficiência real da goleira contra 6m ou por tipo de arremesso."
    goalkeeper_specialist_exchange:
      purpose: "Registrar o ciclo operacional entre goleira e especialista."
      required_fields:
        - "goalkeeper_id"
        - "specialist_id"
        - "exchange_phase"
        - "exchange_result"
        - "court_overlap_detected"
      result_values:
        - "exchange_successful"
        - "goalkeeper_late_exit"
        - "specialist_late_entry"
        - "overlap_violation"
        - "empty_goal_risk"
        - "exchange_turnover"
        - "unknown_review"
      rule: "A ação funcional da goleira começa quando a especialista sai para a goleira entrar e termina quando a goleira sai para a especialista entrar."
      punishment_rule: "Se exchange_result=overlap_violation, punishment_applied deve ser preenchido."
  shootout_boundary:
    rule: "Defesa no Shoot-out continua em shootout_attempt, não em goalkeeper_save."
    added_field: "shootout_defender_origin_role"
    allowed_values:
      - "set_goalkeeper"
      - "line_player"
      - "specialist"
      - "unknown_review"
    purpose: "Permitir saber quando a defensora do Shoot-out era goleira dos sets sem misturar shootout_v1 com goalkeeper_v1."
  current_status: "Planilha corrigida; ainda sem teste no repositório."
```


## 24. Auditoria cruzada final — goalkeeper_v1 ampliado
```yaml
goalkeeper_final_cross_audit:
  date: "2026-06-10"
  module_id: "goalkeeper_v1"
  status: "arquitetura_em_definicao_pronta_para_teste_conceitual"
  import_rule_v1: "nao_importar_v1"
  checked_sources:
    - "EVENTOS"
    - "CAMPOS_AUXILIARES_GOLEIRA"
    - "RESULTADOS_GOLEIRA"
    - "TESTES_GOLEIRA"
    - "VERSIONAMENTO_GOLEIRA"
    - "CAMPOS_AUXILIARES_SHOOTOUT"
    - "TESTES_SHOOTOUT"
  core_events:
    - "goalkeeper_save"
    - "goalkeeper_goal_allowed"
    - "goalkeeper_specialist_exchange"
  corrections_applied:
    - "goalkeeper_id passou a ser obrigatório nos três núcleos do módulo."
    - "linked_finalization_id ficou obrigatório apenas em goalkeeper_save e goalkeeper_goal_allowed; fica bloqueado em goalkeeper_specialist_exchange."
    - "goal_allowed_review permanece como legado/futuro bloqueado; gol sofrido válido usa goalkeeper_goal_allowed + result_goalkeeper=goal_allowed."
    - "uncertain_review exige review_marker=Sim."
    - "shootout_defender_origin_role foi mantido em shootout_v1 para identificar goleira dos sets no Shoot-out sem criar goalkeeper_save."
  validated_boundaries:
    shootout_v1: "Defesa/gol no Shoot-out permanece em shootout_attempt."
    finalization_v1: "six_metre_throw é finalização vinculável para medir eficiência da goleira contra 6m."
    defensive_v1: "Bloqueio de linha permanece fora de goalkeeper_v1."
    transition_future: "transition_after_save e empty_goal_risk são marcadores, não transição completa."
  possession_rules_after_save:
    save_controlled: "possession_after_save=goalkeeper_team"
    save_rebound_live: "possession_after_save=live_ball; restart_after_save=live_play"
    save_out_endline: "possession_after_save=goalkeeper_team; restart_after_save=goalkeeper_throw"
    save_out_sideline: "possession_after_save=opponent_team; restart_after_save=opponent_throw_in"
  next_step: "criar tests/test_goalkeeper_contract.py no repositório, sem liberar UI/importação."
```


## 25. Registro de repositório — goalkeeper_v1 pronto para teste conceitual
```yaml
goalkeeper_repo_registration:
  date: "2026-06-10"
  module_id: "goalkeeper_v1"
  status: "arquitetura_em_definicao_pronta_para_teste_conceitual"
  import_rule_v1: "nao_importar_v1"
  app_ui_status: "nao_liberado"
  import_status: "nao_liberado"
  seed_status: "inalterado"
  core_events:
    - "goalkeeper_save"
    - "goalkeeper_goal_allowed"
    - "goalkeeper_specialist_exchange"
  registry_scope:
    file: "scoutpraia/contracts/events_v1.py"
    exported_file: "scoutpraia/contracts/__init__.py"
    registry_test: "tests/test_events_v1_contract_registry.py"
    contract_test: "tests/test_goalkeeper_contract.py"
  repository_changes:
    commits:
      - "967fa1e Registra goalkeeper v1 como contrato pronto para teste"
      - "573c185 Inclui goalkeeper v1 no teste de registry"
      - "4fd8ed6 Adiciona testes conceituais do contrato goalkeeper v1"
      - "285246c Exporta contrato goalkeeper v1"
    files:
      - "scoutpraia/contracts/events_v1.py"
      - "tests/test_events_v1_contract_registry.py"
      - "tests/test_goalkeeper_contract.py"
      - "scoutpraia/contracts/__init__.py"
  validated_design_rules:
    - "goalkeeper_save registra defesa da goleira em jogo normal/set ou tiro de 6m, vinculada à finalização adversária."
    - "goalkeeper_goal_allowed registra gol sofrido pela goleira para permitir eficiência real."
    - "goalkeeper_specialist_exchange registra ciclo operacional entre goleira e especialista."
    - "six_metre_throw é finalização vinculável para medir eficiência contra 6m."
    - "Shoot-out permanece em shootout_attempt; usar shootout_defender_origin_role para saber se a defensora era goleira dos sets."
    - "Bloqueio de linha permanece em defensive_v1."
    - "Fundo/lateral têm consequências de posse diferentes."
  required_local_validation:
    - "git pull"
    - "python3 -m pytest tests/test_goalkeeper_contract.py -q"
    - "python3 -m pytest tests/test_events_v1_contract_registry.py -q"
    - "python3 -m pytest -q"
    - "scripts/verify_current_state.sh"
    - "git diff --check"
    - "git status --short"
  evidence_status: "pending_local_validation"
```


## 26. Abertura de módulo — transition_v1
```yaml
transition_module_opening:
  date: "2026-06-11"
  module_id: "transition_v1"
  name: "Transição v1.0"
  status: "arquitetura_em_definicao"
  import_rule_v1: "nao_importar_v1"
  app_ui_status: "nao_liberado"
  import_status: "nao_liberado"
  seed_status: "inalterado"
  source_tabs:
    events: "EVENTOS"
    fields: "CAMPOS_AUXILIARES_TRANSICAO"
    results: "RESULTADOS_TRANSICAO"
    tests: "TESTES_TRANSICAO"
    versioning: "VERSIONAMENTO_TRANSICAO"
  core_candidate:
    transition_sequence:
      ui_type: "botao_principal"
      rule: "Sequência observável que conecta mudança de posse, defesa, rebote, reposição ou erro adversário a uma ação ofensiva/defensiva antes do jogo estabilizar."
      required_fields:
        - "transition_direction"
        - "transition_trigger"
        - "trigger_event_id"
        - "transition_start_zone"
        - "transition_speed"
        - "numerical_context"
        - "result_transition"
      optional_link_fields:
        - "terminal_event_id"
        - "terminal_event_code"
        - "terminal_state"
      key_rule: "Toda transição precisa de gatilho e fechamento: terminal_event_id ou terminal_state."
  result_candidates:
    - "transition_goal"
    - "transition_shot_created"
    - "transition_saved"
    - "transition_turnover_no_shot"
    - "transition_slowed_to_set"
    - "defensive_recovery_success"
    - "defensive_recovery_fail"
    - "interrupted_review"
    - "uncertain_review"
  boundaries:
    finalization_v1: "Gol/finalização em transição deve existir como evento terminal de Finalização."
    attack_no_shot_v1: "Perda sem arremesso em transição deve vincular evento terminal de ataque sem finalização."
    goalkeeper_v1: "Defesa da goleira pode ser gatilho, mas não terminal de transition_v1."
    shootout_v1: "shootout_attempt fica bloqueado como gatilho ou terminal de transition_v1."
    defensive_v1: "Retorno defensivo pode terminar em recuperação/bloqueio, vinculado quando houver evento terminal próprio."
  forbidden_logic:
    - "Não calcular pontos em transition_v1."
    - "Não registrar gol de transição sem finalização terminal vinculada."
    - "Não registrar transição sem trigger_event_id ou terminal_state/terminal_event_id."
    - "Não usar transition_sequence para Shoot-out."
  current_status: "Módulo aberto na planilha; ainda não validado por teste no repositório."
```


## 27. Auditoria inicial — transition_v1
```yaml
transition_initial_audit:
  date: "2026-06-11"
  module_id: "transition_v1"
  status: "arquitetura_em_definicao_auditada"
  import_rule_v1: "nao_importar_v1"
  decisions:
    core_event:
      decision: "transition_sequence mantido como único núcleo inicial"
      reason: "Transição é cadeia vinculada; não criar eventos separados para fast break, contra-ataque ou retorno defensivo nesta fase."
    direction:
      decision: "transição ofensiva e defensiva no mesmo evento"
      rule: "transition_direction diferencia offensive_transition e defensive_transition."
    trigger_event_id:
      decision: "campo condicional"
      rule: "Obrigatório quando o gatilho vier de evento registrado; não obrigatório para referee_restart, substitution_context ou unknown_review."
    transition_slowed_to_set:
      decision: "resultado válido com fechamento obrigatório"
      rule: "result_transition=transition_slowed_to_set exige terminal_state=slowed_to_set_attack."
    goalkeeper_boundary:
      decision: "goalkeeper_v1 pode ser gatilho, não terminal"
      rule: "goalkeeper_save pode iniciar transição; goalkeeper_save, goalkeeper_goal_allowed e goalkeeper_specialist_exchange não podem ser terminal_event_code."
    transition_goal:
      decision: "gol de transição exige finalização terminal"
      rule: "result_transition=transition_goal exige terminal_event_code em [simple_shot, spin_shot, inflight_shot, goalkeeper_shot, six_metre_throw]."
  current_results:
    - "transition_goal"
    - "transition_shot_created"
    - "transition_saved"
    - "transition_turnover_no_shot"
    - "transition_slowed_to_set"
    - "defensive_recovery_success"
    - "defensive_recovery_fail"
    - "interrupted_review"
    - "uncertain_review"
  current_status: "Arquitetura auditada na planilha; ainda sem teste no repositório."
```


## 28. Correção conceitual — transition_v1 baseado em substituições
```yaml
transition_concept_correction:
  date: "2026-06-11"
  module_id: "transition_v1"
  status: "arquitetura_em_definicao_corrigida"
  import_rule_v1: "nao_importar_v1"
  reason: "No beach handball, o jogo de transição acontece principalmente pela troca funcional na zona de substituição, não por corrida longa de uma área à outra."
  corrected_core_definition:
    transition_sequence: "Cadeia de troca funcional pela linha lateral/zona de substituição que cria ou neutraliza vantagem antes da defesa adversária estabilizar."
  offensive_transition:
    rule: "Defensoras saem pela zona de substituição e atacantes entram próximas à área adversária."
    objective: "Chegar rápido, antecipar trocas e impedir que a defesa adversária monte estrutura."
    types:
      direct_transition:
        definition: "Goleira lança para atacante sem defensora ou goleira adversária em oposição relevante, gerando clara chance de gol."
        required_field: "direct_lane_available"
      indirect_superiority:
        definition: "Atacantes entram criando superioridade 2x1, 3x2 ou 4x3 antes da defesa estabilizar."
        tactical_system_examples:
          - "2x1"
          - "3x2"
          - "4x3"
  defensive_transition:
    rule: "Atacantes saem pela zona de substituição e defensoras entram próximas à área da própria goleira."
    objective: "Antecipar a troca para neutralizar transição direta e, em sequência, transição indireta adversária."
    types:
      defensive_neutralization_direct: "Entrada defensiva neutraliza lançamento direto/atacante livre adversária."
      defensive_neutralization_indirect: "Entrada defensiva organiza 2x1, 3x0 ou ajuste equivalente contra superioridade adversária."
  anticipation:
    definition: "Atleta que não participa diretamente do lance sai antes da conclusão para permitir entrada antecipada de atleta do papel oposto."
    attack_to_defense: "Atacante sai antes do fim do lance para defensora entrar e neutralizar transição adversária."
    defense_to_attack: "Defensora sai antes do fim do lance para atacante entrar com vantagem ofensiva."
  required_new_fields:
    - "substitution_phase"
    - "substitution_timing"
    - "transition_type"
    - "transition_target_zone"
    - "defensive_stabilization_status"
  optional_new_fields:
    - "exiting_player_id"
    - "entering_player_id"
    - "exiting_role"
    - "entering_role"
    - "substitution_zone"
    - "anticipation_side"
    - "transition_system"
    - "transition_positions"
    - "direct_lane_available"
  end_condition:
    rule: "A transição termina quando ocorre evento terminal ou quando a defesa adversária estabiliza."
    stabilized_defense: "Ação posterior deve ser tratada como ataque posicionado, não transição."
  tactical_note: "Posições e sistemas da transição podem ser diferentes do ataque/defesa posicionados; exemplo: transição em 4:0 e ataque posicionado em 3:1."
  current_status: "Planilha corrigida com conceito real de transição; ainda sem teste no repositório."
```


## 29. Auditoria cruzada final — transition_v1 corrigido
```yaml
transition_final_cross_audit:
  date: "2026-06-11"
  module_id: "transition_v1"
  status: "arquitetura_em_definicao_pronta_para_teste_conceitual"
  import_rule_v1: "nao_importar_v1"
  checked_sources:
    - "EVENTOS"
    - "CAMPOS_AUXILIARES_TRANSICAO"
    - "RESULTADOS_TRANSICAO"
    - "TESTES_TRANSICAO"
    - "VERSIONAMENTO_TRANSICAO"
  core_event: "transition_sequence"
  corrected_concept: "Transição no beach handball é cadeia de substituição funcional pela zona de substituição, com antecipação, criação ou neutralização de vantagem antes da estabilização defensiva."
  required_fields:
    - "transition_direction"
    - "substitution_phase"
    - "substitution_timing"
    - "transition_type"
    - "transition_trigger"
    - "transition_start_zone"
    - "transition_target_zone"
    - "transition_speed"
    - "numerical_context"
    - "defensive_stabilization_status"
    - "result_transition"
    - "terminal_event_id ou terminal_state"
  final_result_domain:
    - "transition_goal"
    - "transition_shot_created"
    - "transition_saved"
    - "transition_turnover_no_shot"
    - "transition_slowed_to_set"
    - "defensive_recovery_success"
    - "defensive_recovery_fail"
    - "interrupted_review"
    - "uncertain_review"
    - "direct_transition_chance"
    - "indirect_superiority_created"
    - "direct_transition_neutralized"
    - "indirect_transition_neutralized"
  coherence_rules:
    substitution_phase:
      offensive_transition: "defenders_exit_attackers_enter"
      defensive_transition: "attackers_exit_defenders_enter"
    transition_type:
      direct_transition_chance: "transition_type=direct_transition"
      indirect_superiority_created: "transition_type=indirect_superiority"
      direct_transition_neutralized: "transition_type=defensive_neutralization_direct"
      indirect_transition_neutralized: "transition_type=defensive_neutralization_indirect"
    indirect_superiority:
      allowed_systems:
        - "2x1"
        - "3x2"
        - "4x3"
    anticipation:
      rule: "substitution_timing=anticipation_before_lance_ends exige anticipation_side."
    direct_transition:
      rule: "transition_type=direct_transition exige direct_lane_available."
    end_condition:
      rule: "defensive_stabilization_status=defense_stabilized encerra a transição; ação posterior é ataque posicionado."
    terminal_event:
      transition_goal: "exige terminal_event_code em Finalização v1."
      transition_turnover_no_shot: "exige terminal_event_code em Attack No Shot v1."
      blocked_terminal_codes:
        - "shootout_attempt"
        - "goalkeeper_save"
        - "goalkeeper_goal_allowed"
        - "goalkeeper_specialist_exchange"
  current_status: "Arquitetura corrigida e auditada na planilha; pronta para teste conceitual no repositório."
  next_step: "criar tests/test_transition_contract.py no repositório, sem liberar UI/importação."
```


## 30. Registro de repositório — transition_v1 pronto para teste conceitual
```yaml
transition_repo_registration:
  date: "2026-06-11"
  module_id: "transition_v1"
  status: "arquitetura_em_definicao_pronta_para_teste_conceitual"
  import_rule_v1: "nao_importar_v1"
  app_ui_status: "nao_liberado"
  import_status: "nao_liberado"
  seed_status: "inalterado"
  core_events:
    - "transition_sequence"
  registry_scope:
    file: "scoutpraia/contracts/events_v1.py"
    exported_file: "scoutpraia/contracts/__init__.py"
    registry_test: "tests/test_events_v1_contract_registry.py"
    contract_test: "tests/test_transition_contract.py"
  repository_changes:
    commits:
      - "4c4ef79 Registra transition v1 como contrato pronto para teste"
      - "60ddf51 Inclui transition v1 no teste de registry"
      - "7e39fc7 Adiciona testes conceituais do contrato transition v1"
      - "d86d7b6 Exporta contrato transition v1"
    files:
      - "scoutpraia/contracts/events_v1.py"
      - "tests/test_events_v1_contract_registry.py"
      - "tests/test_transition_contract.py"
      - "scoutpraia/contracts/__init__.py"
  validated_design_rules:
    - "transition_sequence é o único núcleo inicial do transition_v1."
    - "Transição no beach handball é cadeia de substituição funcional pela zona de substituição, com antecipação, criação ou neutralização de vantagem antes da estabilização defensiva."
    - "transition_direction diferencia offensive_transition e defensive_transition sem criar dois módulos separados."
    - "substitution_phase distingue defensoras saindo/atacantes entrando e atacantes saindo/defensoras entrando."
    - "substitution_timing=anticipation_before_lance_ends exige anticipation_side."
    - "direct_transition_chance exige transition_type=direct_transition e direct_lane_available."
    - "indirect_superiority_created exige transition_type=indirect_superiority e transition_system em 2x1, 3x2 ou 4x3."
    - "Neutralizações defensivas exigem transition_type defensivo correspondente."
    - "defensive_stabilization_status=defense_stabilized encerra a transição."
    - "transition_goal exige evento terminal de Finalização v1."
    - "transition_turnover_no_shot exige evento terminal de Attack No Shot v1."
    - "Shoot-out, eventos da Goleira como terminal, ataque posicionado isolado e pontos diretos ficam bloqueados em transition_v1."
  required_local_validation:
    - "git pull"
    - "python3 -m pytest tests/test_transition_contract.py -q"
    - "python3 -m pytest tests/test_events_v1_contract_registry.py -q"
    - "python3 -m pytest -q"
    - "scripts/verify_current_state.sh"
    - "git diff --check"
    - "git status --short"
  evidence_status: "pending_local_validation"
```


## 31. Melhoria de governança da planilha — MODULE_INDEX e SHEET_MAP
```yaml
spreadsheet_governance_update:
  date: "2026-06-11"
  target: "SCOUT_DESIGN_TEMPLATE"
  status: "indice_arquitetural_criado"
  reason: "Reduzir risco de ambiguidade gerado pela quantidade de abas e tornar explícita a relação entre módulos, eventos, abas de suporte, status, importação e política de uso pela IA."
  created_sheets:
    MODULE_INDEX:
      purpose: "Mapa mestre dos módulos v1."
      columns:
        - "module_id"
        - "module_name"
        - "primary_events"
        - "support_tabs"
        - "module_contract_status"
        - "import_rule_v1"
        - "repo_status"
        - "evidence_id"
        - "ui_status"
        - "ai_use_policy"
        - "notes"
      covered_modules:
        - "finalization_v1"
        - "attack_no_shot_v1"
        - "offensive_creation_v1"
        - "defensive_v1"
        - "shootout_v1"
        - "goalkeeper_v1"
        - "transition_v1"
    SHEET_MAP:
      purpose: "Mapa das abas da planilha e suas dependências."
      columns:
        - "sheet_name"
        - "sheet_type"
        - "module_id"
        - "owner_scope"
        - "is_contract_source"
        - "is_generated"
        - "can_be_deleted"
        - "depends_on"
        - "notes"
  validation_basis:
    - "Data Carpentry: metadados claros reduzem ambiguidade em planilhas com múltiplas abas."
    - "NIST AI RMF: governança e documentação reduzem risco no ciclo de design/desenvolvimento/uso de IA."
    - "OWASP LLM Top 10: políticas explícitas de uso reduzem risco de saída incorreta/misinformation."
  current_effect:
    - "Nenhum módulo foi liberado para importação."
    - "Nenhuma UI foi liberada."
    - "Nenhum evento foi movido ou removido."
    - "A mudança apenas adiciona camada de navegação, governança e redução de risco."
  next_recommended_step: "Adicionar em EVENTOS as colunas active_contract, usable_by_ai e legacy_status para reduzir o risco de uso de eventos legados/futuros pela IA."
```



## 32. Melhoria de governança da aba EVENTOS — política explícita de uso pela IA
```yaml
eventos_ai_use_policy_update:
  date: "2026-06-11"
  target: "SCOUT_DESIGN_TEMPLATE!EVENTOS"
  status: "colunas_de_controle_adicionadas"
  reason: "Reduzir risco de a IA usar eventos legados, futuros ou bloqueados como se fossem eventos contratuais atuais."
  added_columns:
    active_contract:
      purpose: "Indica se a linha pertence ao contrato atual/candidato v1 ou se é legado/futuro bloqueado."
      values:
        - "Sim"
        - "Não"
        - "Sim_com_restricao"
    usable_by_ai:
      purpose: "Define política explícita de uso pela IA."
      values_examples:
        - "usar_e_importar"
        - "usar_e_importar_com_revisao"
        - "usar_como_contrato_nao_importar"
        - "usar_como_auxiliar_nao_importar"
        - "usar_somente_revisao_nao_importar"
        - "nao_usar_legado_futuro"
        - "usar_apenas_como_marcador_de_qualidade"
    legacy_status:
      purpose: "Classifica se a linha é núcleo v1, auxiliar, revisão, futuro bloqueado, legado substituído ou marcador operacional."
  applied_policy:
    importable_current_module:
      import_rule_v1: "importar_v1"
      usable_by_ai: "usar_e_importar"
      example: "attack_no_shot_v1"
    non_importable_contract:
      import_rule_v1: "nao_importar_v1"
      usable_by_ai: "usar_como_contrato_nao_importar"
      example: "finalization_v1, defensive_v1, shootout_v1, goalkeeper_v1, transition_v1"
    auxiliary_contract:
      ui_type: "campo_auxiliar"
      usable_by_ai: "usar_como_auxiliar_nao_importar"
    review_contract:
      ui_type: "botao_secundario_revisao ou fallback_revisao"
      usable_by_ai: "usar_somente_revisao_nao_importar"
    legacy_future_events:
      module_contract_status: "rascunho_modulo_futuro"
      usable_by_ai: "nao_usar_legado_futuro"
      examples:
        - "save"
        - "save_shootout"
        - "goal_conceded"
        - "fast_break_against"
        - "transition_recovery_good"
        - "transition_recovery_bad"
    global_quality_marker:
      code: "review_marker"
      usable_by_ai: "usar_apenas_como_marcador_de_qualidade"
  validation_basis:
    - "Data Carpentry: significado deve ser codificado em campos explícitos, não apenas em posição/formatação visual."
    - "OWASP LLM Top 10: políticas explícitas reduzem risco de misinformation e improper output handling."
    - "NIST AI RMF: governança e documentação são controles de risco no ciclo de IA."
  current_effect:
    - "Nenhum evento foi movido ou removido."
    - "Nenhum módulo foi liberado para importação."
    - "A aba EVENTOS passou de 31 para 34 colunas."
    - "Eventos legados/futuros agora estão explicitamente marcados como nao_usar_legado_futuro."
  next_recommended_step: "Criar CROSS_MODULE_BOUNDARIES e AI_USE_POLICY para formalizar fronteiras entre módulos e regras globais de uso pela IA."
```


## 33. Melhoria de governança — CROSS_MODULE_BOUNDARIES e AI_USE_POLICY
```yaml
spreadsheet_cross_module_governance_update:
  date: "2026-06-11"
  target: "SCOUT_DESIGN_TEMPLATE"
  status: "fronteiras_e_politica_ia_criadas"
  reason: "Formalizar fronteiras entre módulos e impedir que a IA misture eventos, resultados, campos e regras de módulos diferentes."
  created_sheets:
    CROSS_MODULE_BOUNDARIES:
      purpose: "Fronteiras explícitas entre módulos."
      columns:
        - "boundary_id"
        - "source_module"
        - "target_module"
        - "allowed_relation"
        - "blocked_misuse"
        - "required_link_or_field"
        - "validation_rule"
        - "ai_action"
        - "evidence_source"
        - "notes"
      initial_boundaries:
        - "shootout_v1 != goalkeeper_v1"
        - "goalkeeper_v1 precisa vincular finalization_v1"
        - "defensive_v1 != goalkeeper_v1"
        - "transition_v1 -> finalization_v1 quando result_transition=transition_goal"
        - "transition_v1 -> attack_no_shot_v1 quando result_transition=transition_turnover_no_shot"
        - "goalkeeper_v1 pode ser gatilho de transition_v1, mas não terminal"
        - "shootout_v1 fica fora de transition_v1"
        - "offensive_creation_v1 cria finalization_v1, mas não substitui finalização"
        - "finalization_v1 e attack_no_shot_v1 são mutuamente exclusivos na posse"
        - "goalkeeper_specialist_exchange não substitui automaticamente bad_substitution_attack"
    AI_USE_POLICY:
      purpose: "Política explícita do que a IA pode sugerir, importar, revisar ou bloquear."
      columns:
        - "policy_id"
        - "scope"
        - "condition"
        - "allowed_to_suggest"
        - "allowed_to_import"
        - "requires_human_review"
        - "blocked_reason"
        - "source_of_truth"
        - "expected_ai_behavior"
      key_rules:
        - "usable_by_ai=usar_e_importar pode ser usado e importado respeitando required_fields/blocking_rules."
        - "usable_by_ai=usar_como_contrato_nao_importar pode ser usado para arquitetura/teste, mas não para UI/importação."
        - "usable_by_ai=nao_usar_legado_futuro deve ser bloqueado em nova coleta."
        - "Módulo com import_rule_v1=nao_importar_v1 não pode gerar UI/importação sem evidência explícita."
        - "Conflito entre EVENTOS e aba específica exige auditoria humana."
        - "Incerteza/vídeo incompleto/regra ausente exige review_marker."
  updated_sheets:
    SHEET_MAP:
      added:
        - "CROSS_MODULE_BOUNDARIES"
        - "AI_USE_POLICY"
  current_effect:
    - "Nenhum módulo foi liberado para importação."
    - "Nenhuma UI foi liberada."
    - "Nenhum evento foi movido ou removido."
    - "SCOUT_DESIGN_TEMPLATE agora possui 49 abas."
    - "A governança passa a ter índice, mapa de abas, política de uso por evento, fronteiras entre módulos e política global da IA."
  next_recommended_step: "Criar FIELD_DICTIONARY_GLOBAL e RESULT_DOMAIN_GLOBAL para consolidar campos/resultados e preparar auditoria automática planilha x repositório."
```


## 34. Melhoria de normalização — FIELD_DICTIONARY_GLOBAL e RESULT_DOMAIN_GLOBAL
```yaml
spreadsheet_normalization_update:
  date: "2026-06-11"
  target: "SCOUT_DESIGN_TEMPLATE"
  status: "dicionarios_globais_criados"
  reason: "Consolidar campos auxiliares e resultados críticos de todos os módulos para reduzir duplicidade, ambiguidade e risco de divergência entre abas específicas, EVENTOS e repositório."
  created_sheets:
    FIELD_DICTIONARY_GLOBAL:
      purpose: "Dicionário global de campos auxiliares e campos críticos usados por módulos."
      columns:
        - "field_code"
        - "field_name_ui"
        - "module_id"
        - "field_type"
        - "allowed_values_or_ref"
        - "required_when"
        - "source_sheet"
        - "used_by_events"
        - "ai_policy"
        - "repo_symbol"
        - "risk_note"
        - "normalization_status"
      initial_scope:
        - "campos globais: athlete_id, court_location, goal_zone, position_code, system_code, review_marker"
        - "campos de resultado: result_possession, result_shootout, result_goalkeeper, result_transition"
        - "campos de vínculo: linked_finalization_id, linked_finalization_event_code, terminal_event_id, terminal_event_code, terminal_state"
        - "campos de Shoot-out: shootout_launcher_id, shootout_launcher_role, shootout_defender_id, shootout_defender_origin_role"
        - "campos de Goleira: goalkeeper_id, specialist_id, exchange_result"
        - "campos de Transição: substitution_phase, substitution_timing, transition_type, transition_system, direct_lane_available, defensive_stabilization_status"
    RESULT_DOMAIN_GLOBAL:
      purpose: "Domínio global de resultados por módulo/evento."
      columns:
        - "result_code"
        - "result_name_ui"
        - "module_id"
        - "allowed_event_code"
        - "result_field"
        - "points_policy"
        - "possession_effect"
        - "terminal_policy"
        - "forbidden_with"
        - "source_sheet"
        - "repo_symbol"
        - "normalization_status"
      initial_scope:
        - "Finalização: goal, save, shot_wide, shot_blocked"
        - "Ataque sem finalização: lost_possession_no_shot"
        - "Criação ofensiva: shot_created, clear_chance_created"
        - "Defensivo: shot_blocked_linked, possession_won"
        - "Goleira: save_controlled, save_out_endline, save_out_sideline, goal_allowed, exchange_successful, overlap_violation"
        - "Transição: transition_goal, direct_transition_chance, indirect_superiority_created, direct_transition_neutralized, indirect_transition_neutralized, transition_slowed_to_set"
        - "Shoot-out: goal, save como result_shootout"
  updated_sheets:
    SHEET_MAP:
      added:
        - "FIELD_DICTIONARY_GLOBAL"
        - "RESULT_DOMAIN_GLOBAL"
  current_effect:
    - "Nenhum módulo foi liberado para importação."
    - "Nenhuma UI foi liberada."
    - "Nenhum evento foi movido ou removido."
    - "SCOUT_DESIGN_TEMPLATE agora possui 51 abas."
    - "A planilha passa a ter dicionário global de campos e domínio global de resultados para apoiar auditoria automática."
  next_recommended_step: "Criar VALIDATION_MATRIX consolidando testes por módulo, evidências EV e arquivos de teste do repositório."
```


## 35. Melhoria de validação — VALIDATION_MATRIX
```yaml
spreadsheet_validation_matrix_update:
  date: "2026-06-11"
  target: "SCOUT_DESIGN_TEMPLATE"
  status: "matriz_de_validacao_criada"
  reason: "Consolidar em uma única aba a relação entre módulos, abas de teste da planilha, testes do repositório, evidências EV, git_head, regras de importação, status de UI, seed e próximas ações."
  created_sheet:
    VALIDATION_MATRIX:
      purpose: "Matriz consolidada de validação, evidências, testes e bloqueios."
      columns:
        - "validation_id"
        - "module_id"
        - "scope"
        - "sheet_test_source"
        - "repo_test_file"
        - "repo_test_status"
        - "evidence_id"
        - "git_head"
        - "import_rule_v1"
        - "ui_status"
        - "seed_status"
        - "blocking_condition"
        - "next_action"
        - "notes"
      initial_scope:
        - "attack_no_shot_v1 -> EV-001 a EV-005, importar_v1"
        - "finalization_v1 -> contrato validado bloqueado"
        - "offensive_creation_v1 -> contrato validado bloqueado"
        - "defensive_v1 -> contrato validado bloqueado"
        - "shootout_v1 -> EV-009, nao_importar_v1"
        - "goalkeeper_v1 -> EV-010, nao_importar_v1"
        - "transition_v1 -> pendente_EV-011, validacao_local_pendente"
        - "governança global -> MODULE_INDEX, SHEET_MAP, EVENTOS policy, CROSS_MODULE_BOUNDARIES, AI_USE_POLICY, FIELD_DICTIONARY_GLOBAL, RESULT_DOMAIN_GLOBAL"
        - "repositório global -> pytest completo e verify_current_state.sh"
  updated_sheets:
    SHEET_MAP:
      added:
        - "VALIDATION_MATRIX"
  current_effect:
    - "Nenhum módulo foi liberado para importação."
    - "Nenhuma UI foi liberada."
    - "Nenhum evento foi movido ou removido."
    - "SCOUT_DESIGN_TEMPLATE agora possui 52 abas."
    - "A validação fica rastreável por módulo, teste, evidência e bloqueio."
  next_recommended_step: "Executar validação local do transition_v1 no repositório e, se passar, registrar EV-011."
```


## 36. Evidência EV-011 — transition_v1 validado por teste conceitual
```yaml
ev_011_transition_v1:
  date: "2026-06-11"
  module_id: "transition_v1"
  status: "passed"
  module_contract_status: "arquitetura_em_definicao_validada_por_teste_conceitual"
  git_head: "a7b8f97"
  local_validation:
    transition_contract:
      command: "python3 -m pytest tests/test_transition_contract.py -q"
      result: "15 passed in 0.04s"
    registry_contract:
      command: "python3 -m pytest tests/test_events_v1_contract_registry.py -q"
      result: "16 passed in 0.03s"
    full_pytest:
      command: "python3 -m pytest -q"
      result: "247 passed in 17.70s"
    verify_current_state:
      command: "scripts/verify_current_state.sh"
      result: "verde; 247 passed in 11.98s"
    git_diff_check:
      command: "git diff --check"
      result: "sem saída"
    git_status_short:
      command: "git status --short"
      result: "limpo"
  seed:
    taxonomy: "ScoutPraia v0.1"
    taxonomy_status: "draft"
    event_definitions: 31
    expected_event_definitions: 31
    seed_status: "inalterado"
  import_rule_v1: "nao_importar_v1"
  app_ui_status: "nao_liberado"
  import_status: "nao_liberado"
  validated_design_rules:
    - "transition_sequence é o único núcleo inicial de transition_v1."
    - "Transição é cadeia de substituição funcional pela zona de substituição, com antecipação e estabilização defensiva."
    - "transition_direction diferencia transição ofensiva e defensiva no mesmo evento."
    - "substitution_phase e substitution_timing controlam troca funcional e antecipação."
    - "direct_transition_chance exige transition_type=direct_transition."
    - "indirect_superiority_created exige transition_type=indirect_superiority e sistema de superioridade."
    - "Neutralizações defensivas exigem transition_type defensivo correspondente."
    - "defensive_stabilization_status=defense_stabilized encerra transição."
    - "transition_goal exige evento terminal de Finalização v1."
    - "transition_turnover_no_shot exige evento terminal de Attack No Shot v1."
    - "Shoot-out, eventos da Goleira como terminal, ataque posicionado isolado e points ficam bloqueados em transition_v1."
  conclusion: "transition_v1 fechado como contrato conceitual validado; permanece bloqueado para UI/importação."
```


## 37. Correção semântica da aba EVENTOS — required_result_field
```yaml
eventos_required_result_field_update:
  date: "2026-06-11"
  target: "SCOUT_DESIGN_TEMPLATE!EVENTOS"
  status: "required_result_field_criado"
  reason: "A coluna antiga result_possession_auto deixou de representar apenas posse e passou a carregar resultados obrigatórios de Shoot-out, Goleira e Transição. Para reduzir ambiguidade, foi criada required_result_field ao lado da coluna antiga, preservando compatibilidade."
  structural_change:
    old_column_preserved: "result_possession_auto"
    new_column: "required_result_field"
    position: "ao lado de result_possession_auto"
  mapping_policy:
    finalization_v1: "required_result_field=result_possession"
    attack_no_shot_v1: "required_result_field=result_possession"
    shootout_v1: "required_result_field=result_shootout"
    goalkeeper_save: "required_result_field=result_goalkeeper"
    goalkeeper_goal_allowed: "required_result_field=result_goalkeeper"
    goalkeeper_specialist_exchange: "required_result_field=exchange_result"
    transition_v1: "required_result_field=result_transition"
    auxiliary_or_future_rows: "required_result_field=NA quando não houver resultado técnico exigido"
    review_marker: "required_result_field=review_marker"
  validation:
    checked_range: "EVENTOS!Q1:T40"
    result: "Cabeçalho e primeiras linhas conferidos; required_result_field aparece entre result_possession_auto e positive_example."
  current_effect:
    - "Nenhum evento foi movido ou removido."
    - "Nenhum módulo foi liberado para importação."
    - "Nenhuma UI foi liberada."
    - "result_possession_auto permanece para compatibilidade."
    - "required_result_field passa a ser a coluna semanticamente correta para novos usos e auditorias."
  next_recommended_step: "Criar EVENTOS_LEGADOS_FUTUROS ou LEGACY_MIGRATION_RULES para mapear explicitamente eventos antigos para códigos atuais ou bloqueio."
```


## 38. Melhoria de migração — LEGACY_MIGRATION_RULES
```yaml
legacy_migration_rules_update:
  date: "2026-06-11"
  target: "SCOUT_DESIGN_TEMPLATE"
  status: "legacy_migration_rules_criada"
  reason: "Mapear explicitamente eventos legados/futuros para códigos atuais, contexto ou bloqueio, reduzindo risco de a IA usar eventos antigos como eventos técnicos válidos."
  created_sheet:
    LEGACY_MIGRATION_RULES:
      purpose: "Regras de migração, bloqueio e revisão para códigos legados/futuros."
      columns:
        - "legacy_code"
        - "legacy_name"
        - "legacy_scope"
        - "legacy_status"
        - "new_module_id"
        - "new_event_code"
        - "new_result_or_field"
        - "migration_action"
        - "ai_policy"
        - "requires_human_review"
        - "blocking_rule"
        - "evidence_source"
        - "notes"
      initial_rules:
        - "save -> goalkeeper_v1.goalkeeper_save quando houver finalização vinculada; bloquear em Shoot-out."
        - "save_shootout -> shootout_v1.shootout_attempt + result_shootout=save; bloquear goalkeeper_save."
        - "goal_conceded -> goalkeeper_v1.goalkeeper_goal_allowed quando houver goleira e finalização vinculada."
        - "empty_goal_conceded -> contexto/revisão de goalkeeper_v1 ou transition_v1; não virar botão primário."
        - "fast_break_against -> contexto de transition_v1 com transition_direction=defensive_transition."
        - "transition_recovery_good -> transition_v1 com resultado de neutralização defensiva quando houver evidência."
        - "transition_recovery_bad -> transition_v1 como falha defensiva/terminal vinculado quando houver evidência."
        - "suspension_committed, timeout, set_end, golden_goal, match_end -> bloquear como eventos técnicos v1; manter como contexto futuro."
        - "specialist_shot -> finalization_v1 com tipo técnico real + scorer_role=specialist."
  updated_sheets:
    SHEET_MAP:
      added:
        - "LEGACY_MIGRATION_RULES"
    VALIDATION_MATRIX:
      added:
        - "VAL-013 global_governance migração de legados e futuros"
  validation:
    checked_range: "LEGACY_MIGRATION_RULES!A1:M20"
    result: "Cabeçalho e 13 regras iniciais conferidos."
  current_effect:
    - "Nenhum evento foi movido ou removido."
    - "Nenhum módulo foi liberado para importação."
    - "Nenhuma UI foi liberada."
    - "Códigos legados/futuros agora têm política explícita de migração, contexto ou bloqueio."
  next_recommended_step: "Criar SOURCE_REGISTER para vincular fontes fortes às regras e módulos."
```


## 39. Melhoria de fontes — SOURCE_REGISTER
```yaml
source_register_update:
  date: "2026-06-11"
  target: "SCOUT_DESIGN_TEMPLATE"
  status: "source_register_criado"
  reason: "Vincular fontes fortes, internas e executáveis às regras, módulos, governança e validação da planilha, reduzindo risco de decisões sem rastreabilidade."
  created_sheet:
    SOURCE_REGISTER:
      purpose: "Registro de fontes fortes, fontes internas e evidências executáveis usadas para sustentar regras, arquitetura, governança e validação."
      columns:
        - "source_id"
        - "title"
        - "organization"
        - "source_type"
        - "version_or_date"
        - "link_or_location"
        - "module_id"
        - "rule_supported"
        - "evidence_level"
        - "usage_allowed"
        - "validation_scope"
        - "risk_if_missing"
        - "related_sheets"
        - "notes"
      initial_sources:
        SRC-001: "IHF Rules of the Game — Beach Handball"
        SRC-002: "NIST AI Risk Management Framework"
        SRC-003: "OWASP Top 10 for LLM/GenAI Applications"
        SRC-004: "Data Carpentry Spreadsheet Ecology / Good Practices"
        SRC-005: "VERSA / Verified Event Data Format for Reliable Sports Analytics"
        SRC-006: "005_CONT_Operacional_Eventos_v1.md"
        SRC-007: "scoutpraia/contracts/events_v1.py"
        SRC-008: "pytest + verify_current_state.sh"
        SRC-009: "SCOUT_DESIGN_TEMPLATE"
  updated_sheets:
    SHEET_MAP:
      added:
        - "SOURCE_REGISTER"
    VALIDATION_MATRIX:
      added:
        - "VAL-014 global_governance registro de fontes fortes e internas"
  validation:
    checked_range: "SOURCE_REGISTER!A1:N20"
    result: "Cabeçalho e 9 fontes iniciais conferidos."
  current_effect:
    - "Nenhum evento foi movido ou removido."
    - "Nenhum módulo foi liberado para importação."
    - "Nenhuma UI foi liberada."
    - "Fontes fortes e internas passam a ter source_id para futuras auditorias e regras críticas."
  next_recommended_step: "Criar abas normalizadas EVENT_REQUIRED_FIELDS, EVENT_OPTIONAL_FIELDS, EVENT_FORBIDDEN_FIELDS e EVENT_BLOCKING_RULES, ou iniciar script de auditoria planilha x repositório."
```


## 40. Melhoria de normalização — regras por evento em abas auditáveis
```yaml
event_rules_normalization_update:
  date: "2026-06-11"
  target: "SCOUT_DESIGN_TEMPLATE"
  status: "normalizacao_inicial_de_regras_criada"
  reason: "Reduzir dependência de células com múltiplas regras separadas por ponto-e-vírgula e preparar auditoria automática planilha x repositório."
  created_sheets:
    EVENT_REQUIRED_FIELDS:
      purpose: "Normalizar campos obrigatórios em uma regra por linha."
      columns:
        - "rule_id"
        - "module_id"
        - "event_code"
        - "field_code"
        - "required_when"
        - "source_column"
        - "source_sheet"
        - "repo_symbol"
        - "validation_status"
        - "notes"
      initial_rules_count: 19
    EVENT_OPTIONAL_FIELDS:
      purpose: "Normalizar campos opcionais/condicionais em uma regra por linha."
      initial_rules_count: 11
    EVENT_FORBIDDEN_FIELDS:
      purpose: "Normalizar campos/códigos proibidos em uma regra por linha."
      initial_rules_count: 12
    EVENT_BLOCKING_RULES:
      purpose: "Normalizar regras de bloqueio em uma regra por linha."
      initial_rules_count: 13
  updated_sheets:
    SHEET_MAP:
      added:
        - "EVENT_REQUIRED_FIELDS"
        - "EVENT_OPTIONAL_FIELDS"
        - "EVENT_FORBIDDEN_FIELDS"
        - "EVENT_BLOCKING_RULES"
    VALIDATION_MATRIX:
      added:
        - "VAL-015 global_governance normalização de regras por evento"
  validation:
    checked_range: "EVENT_REQUIRED_FIELDS!A1:J25"
    result: "Cabeçalho e 19 regras obrigatórias iniciais conferidos."
  current_effect:
    - "Nenhum evento foi movido ou removido."
    - "Nenhum módulo foi liberado para importação."
    - "Nenhuma UI foi liberada."
    - "As regras originais da aba EVENTOS foram preservadas."
    - "As novas abas são fonte auxiliar de auditoria e ainda não substituem 100% das regras originais."
  next_recommended_step: "Expandir a normalização até cobrir 100% das regras críticas ou criar script de auditoria planilha x repositório usando essas abas."
```

## 41. Governança de leitura da planilha — frontmatter comum e SHEET_CONTRACTS
```yaml
spreadsheet_frontmatter_and_contracts_update:
  date: "2026-06-12"
  target: "SCOUT_DESIGN_TEMPLATE"
  status: "frontmatter_comum_e_sheet_contracts_criados"
  decision: "Manter a estrutura A1:C6 como frontmatter comum, linha 7 como cabeçalho real da aba e linha 8 como início dos dados. Não deslocar cabeçalhos para linha 15 sem nova decisão explícita."
  common_frontmatter:
    range: "A1:C6"
    rows:
      - "frontmatter_key | frontmatter_value | agent_instruction"
      - "artifact_id | SCOUT_DESIGN_TEMPLATE | identificar_artefato"
      - "schema_version | frontmatter_v1 | usar_esta_versao_de_metadados"
      - "sheet_name | CURRENT_TAB | usar_nome_da_aba_lida_no_contexto"
      - "canonical_registry_sheet | SOURCE_REGISTER | consultar_fontes_e_permissoes"
      - "data_region | header_row=7; data_start_row=8 | linha_7_eh_cabecalho_e_linha_8_inicia_dados"
  created_sheet:
    SHEET_CONTRACTS:
      purpose: "Centralizar o contrato específico de cada aba, incluindo função, chave primária, chaves estrangeiras, dependências, política de UI, política SQLite, validação e uso pelo agente."
      header_row: 7
      data_start_row: 8
      key_columns:
        - "sheet_name"
        - "sheet_role"
        - "primary_key"
        - "foreign_keys"
        - "depends_on"
        - "referenced_by"
        - "ui_generation_policy"
        - "sqlite_generation_policy"
        - "validation_policy"
        - "agent_usage"
        - "notes"
  agent_rules:
    - "Ler A1:C6 antes de interpretar qualquer aba."
    - "Usar linha 7 como cabeçalho real da tabela."
    - "Usar linha 8 em diante como dados."
    - "Consultar SHEET_CONTRACTS antes de gerar UI, SQLModel/sqlite3, validações ou testes."
    - "Consultar SOURCE_REGISTER antes de usar fonte, evidência, regra ou permissão."
    - "Consultar MODULE_INDEX antes de filtrar ou implementar module_id."
    - "Consultar SHEET_MAP antes de navegar entre abas."
    - "Tratar TESTES_* como especificações BDD/TDD e não como few-shot prompts."
    - "Gerar selectbox/enum quando foreign_keys ou allowed_values apontarem para domínio/tabela; não gerar text_input livre."
    - "Usar CROSS_MODULE_BOUNDARIES para state machine, session_state, sequência temporal e bloqueios entre módulos."
  contracts_initial_scope:
    central_sheets:
      - "SOURCE_REGISTER"
      - "MODULE_INDEX"
      - "SHEET_MAP"
      - "EVENTOS"
      - "FIELD_DICTIONARY_GLOBAL"
      - "RESULT_DOMAIN_GLOBAL"
      - "CROSS_MODULE_BOUNDARIES"
      - "EVENT_BLOCKING_RULES"
    pilot_module_sheets:
      - "CAMPOS_AUXILIARES_GOLEIRA"
      - "RESULTADOS_GOLEIRA"
      - "TESTES_GOLEIRA"
      - "CAMPOS_AUXILIARES_FINALIZACAO"
      - "CAMPOS_AUXILIARES_TRANSICAO"
      - "TESTES_FINALIZACAO"
      - "TESTES_TRANSICAO"
  updated_sheet:
    INSTRUCOES:
      status: "atualizada"
      added_section: "Governança atual da planilha"
      content_summary: "Documenta frontmatter comum, SHEET_CONTRACTS, SOURCE_REGISTER, MODULE_INDEX, SHEET_MAP, TESTES como BDD/TDD, campos fechados, state machine e preservação da linha 7 como cabeçalho."
  current_effect:
    - "Nenhum módulo foi liberado para UI ou importação."
    - "Nenhum evento foi movido ou removido."
    - "A mudança adiciona governança de leitura, contratos específicos por aba e relacionamentos explícitos para reduzir inferência do agente."
    - "A planilha passa a orientar o futuro compilador de contratos por module_id, evitando envio de todas as abas ao LLM."
  next_recommended_step: "Expandir SHEET_CONTRACTS para todas as abas restantes e depois criar o script extrator/compilador de contratos por module_id."
```


