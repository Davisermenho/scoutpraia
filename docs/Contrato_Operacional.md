---
title: Contrato Operacional — Eventos v1
project: ScoutPraia
version: eventos_v1.0
owner: Davi Sermenho
last_updated: 2026-06-11
status: todos_contratos_validados
semantic_source: Contrato_Operacional.md
implementation_source: SCOUT_DESIGN_TEMPLATE
repository: Davisermenho/scoutpraia
---


# Contrato Operacional — Eventos v1


## 1. Objetivo


Este documento define as regras semânticas, taxonômicas e operacionais para os módulos v1 do ScoutPraia. Ele deve ser usado como referência controlada por humanos e agentes de IA.


Regra principal:


```yaml
global_rule:
  source_priority:
    1: "SCOUT_DESIGN_TEMPLATE"
    2: "Contrato_Operacional.md"
    3: "Davisermenho/scoutpraia"
  blocking_rule: "Divergência entre fontes bloqueia implementação até correção."
```


## 2. Fontes de verdade


```yaml
sources:
  semantic_rules: "Contrato_Operacional.md"
  implementation_structure: "SCOUT_DESIGN_TEMPLATE"
  code_and_tests: "Davisermenho/scoutpraia"
  evidence: "ACCEPTANCE_EVIDENCE"
  blocking_rule: "Divergência entre fontes bloqueia implementação até correção."
```


## 2-bis. Estado consolidado


Referência rápida para agentes. Para regras detalhadas, consultar as seções 6 a 9.


```yaml
consolidated_state:
  last_reviewed_at: "2026-06-11"
  git_head: "aa8934c"
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
  conceptual_contracts:
    shootout_v1:
      status: "arquitetura_em_definicao_validada_por_teste_conceitual"
      import_rule_v1: "nao_importar_v1"
      ui: "nao_liberada"
      importacao: "nao_liberada"
      seed_operacional: "inalterado"
      evidence_status: "passed"
    goalkeeper_v1:
      status: "arquitetura_em_definicao_validada_por_teste_conceitual"
      import_rule_v1: "nao_importar_v1"
      ui: "nao_liberada"
      importacao: "nao_liberada"
      seed_operacional: "inalterado"
      evidence: ["EV-010"]
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
    blocking_rule: "Mesmo validado por contrato, não importar no app antes de implementação controlada e testes de integração."


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

  EV-010:
    module: "goalkeeper_v1"
    status: "passed"
    git_head: "aa8934c"
    local_validation:
      goalkeeper_contract: "13 passed in 0.02s"
      registry_contract: "14 passed in 0.02s"
      full_pytest: "226 passed in 14.19s"
      verify_current_state: "verde; 226 passed in 13.81s"
      git_diff_check: "sem saída"
      git_status_short: "limpo"
    seed:
      taxonomy: "ScoutPraia v0.1"
      taxonomy_status: "draft"
      event_definitions: 31
    import_rule_v1: "nao_importar_v1"

  global_validation_after_goalkeeper:
    command: "python3 -m pytest -q"
    actual_result: "226 passed in 14.19s"
    verify_current_state: "verde; 226 passed in 13.81s"
    git_diff_check: "sem saída"
    git_status_short: "limpo"
    git_head: "aa8934c"
```


## 11. Regras de liberação


```yaml
release_rules:
  current_state: "todos_contratos_validados"
  last_reviewed_at: "2026-06-11"
  git_head: "aa8934c"
  app_import_ready:
    attack_no_shot_v1: "importar_v1"
    finalization_v1: "aguarda_ativacao_app"
    offensive_creation_v1: "aguarda_ativacao_app"
    defensive_v1: "aguarda_ativacao_app"
    shootout_v1: "nao_liberado"
    goalkeeper_v1: "nao_liberado"
  blockers_before_full_app_activation:
    - "Validar que nenhum módulo v1 é importado apenas por category."
    - "Executar testes de integração de app antes de ativar finalization_v1, offensive_creation_v1 e defensive_v1."
    - "Confirmar fluxo de app com attack_no_shot_v1 ativo antes de ativar módulos dependentes."
    - "Não liberar UI/importação de shootout_v1 enquanto permanecer apenas como contrato conceitual validado por teste."
    - "Não liberar UI/importação de goalkeeper_v1 enquanto permanecer apenas como contrato conceitual validado por teste."
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
  status: "arquitetura_em_definicao_validada_por_teste_conceitual"
  import_rule_v1: "nao_importar_v1"
  app_ui_status: "nao_liberado"
  import_status: "nao_liberado"
  seed_status: "inalterado"
  git_head: "aa8934c"
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
  local_validation:
    goalkeeper_contract: "13 passed in 0.02s"
    registry_contract: "14 passed in 0.02s"
    full_pytest: "226 passed in 14.19s"
    verify_current_state: "verde; 226 passed in 13.81s"
    git_diff_check: "sem saída"
    git_status_short: "limpo"
  evidence_status: "passed"
```

### G1-GOALKEEPER-EV-010 — Evidência local do contrato conceitual (2026-06-11)

```yaml
g1_goalkeeper_ev010:
  date: "2026-06-11"
  git_head: "aa8934c"
  executed_by: "Davi Sermenho"
  status_after_evidence: "arquitetura_em_definicao_validada_por_teste_conceitual"
  import_rule_v1: "nao_importar_v1"
  ui: "nao_liberada"
  importacao: "nao_liberada"
  seed_operacional: "inalterado"
  evidence:
    EV-010:
      command: "python3 -m pytest tests/test_goalkeeper_contract.py -q"
      result: "13 passed in 0.02s"
      status: "passed"
    registry_contract:
      command: "python3 -m pytest tests/test_events_v1_contract_registry.py -q"
      result: "14 passed in 0.02s"
      status: "passed"
    global_validation_after_goalkeeper:
      command: "python3 -m pytest -q"
      result: "226 passed in 14.19s"
      verify_current_state: "verde; 226 passed in 13.81s"
      git_diff_check: "sem saída"
      git_status_short: "limpo"
  seed_note: "Taxonomia operacional padrão permanece ScoutPraia v0.1 draft com 31 eventos; a evidência do goalkeeper_v1 não altera seed, UI ou importação."
```
