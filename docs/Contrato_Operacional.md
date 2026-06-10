---
title: Contrato Operacional — Eventos v1
project: ScoutPraia
version: eventos_v1.0
owner: Davi Sermenho
last_updated: 2026-06-10
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
