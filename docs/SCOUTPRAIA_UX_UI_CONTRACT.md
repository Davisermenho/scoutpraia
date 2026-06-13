---
doc_id: SCOUTPRAIA_UX_UI_CONTRACT
status: canonical_ux_ui_contract
version: "1.0.0"
authority_level: 5
created_at: "2026-06-12"
repository: "Davisermenho/scoutpraia"
master_plan: "https://docs.google.com/document/d/1gy0j8QDDAlh7Qp9ehsYy4P9o1BpaFpKq8eHS7zx56Ds/edit?usp=drivesdk"
parent_document: "https://docs.google.com/document/d/1bw-53YWvvTslmZA0XmZ-ySMGBc8BbudcNJ9WokPdcLY/edit?tab=t.0"
blocking_policy: "Nenhuma UI, build, piloto ou uso real pode ser aprovado sem passar por este contrato."
---

# ScoutPraia — Contrato UX UI e Backlog de Interface

## Resumo executivo

Este documento separa a camada de UX UI do Plano Mestre para preservar profundidade técnica, riqueza lexical e precisão operacional. A interface do ScoutPraia não é acabamento visual. Ela é o ponto de captura dos dados. Uma decisão ruim de interface pode gerar erro de marcação, perda de tempo, dupla contagem, ausência de feedback, dificuldade de recuperação e baixa confiança nos relatórios.

A tela de marcação deve ser tratada como instrumento técnico de análise, não como formulário genérico. O operador precisa enxergar o jogo ativo, a taxonomia, o timestamp, o evento selecionado, a atleta, o resultado, a pontuação derivada, o último evento salvo e o histórico recente. O sistema deve prevenir erro antes de salvar e facilitar correção depois de salvar.

```yaml
ux_ui_contract_summary:
  purpose: "Garantir que a interface gere dados corretos, rápidos, recuperáveis e auditáveis."
  primary_user: "treinador ou analista de handebol de areia"
  primary_screen: "Marcação"
  principle: "UI ruim vira dado ruim; dado ruim vira relatório ruim."
  may_render_blocked_event: false
  may_use_raw_event_code_as_primary_label: false
  may_release_pilot_without_human_validation: false
```
## 0. Gate obrigatório de UX UI por task

Nenhuma task de UX UI pode entrar no backlog, alterar interface, criar botão, criar campo, criar label, alterar `tagging.py`, liberar build, liberar piloto ou liberar uso real se não estiver ligada a fonte forte, chunk, ação executável, critério de aceite e prova esperada.

```yaml
ux_ui_hard_task_gate:
  status: mandatory
  hard_rule: "Nenhuma task de UX UI pode entrar no plano se não tiver task_id, chunk associado, ação executável, justificativa técnica, fonte verificável, critério de aceite, prova esperada e definição de DONE."
  block_if_missing_any:
    - task_id
    - chunk_id
    - executable_action
    - technical_justification
    - verifiable_strong_source
    - UI_or_UX_contract_reference
    - acceptance_criteria
    - expected_proof
    - done_definition
    - real_world_success_condition
```

### 0.1 Objetivo do Contrato UX UI

Garantir que a interface do ScoutPraia funcione no mundo real como instrumento técnico de marcação: rápida, compreensível, rastreável, recuperável, testável, auditável e segura contra eventos bloqueados. O contrato deve impedir que a UI vire um formulário genérico ou uma coleção de botões manuais desconectados do contrato de eventos.

```yaml
ux_ui_objective_contract:
  objective: "Garantir captura correta de dados por meio de interface contract-driven."
  real_world_goal: "Operador consegue marcar, revisar, corrigir e confiar no dado sem ajuda do desenvolvedor."
  failure_definition: "Tela bonita, mas lenta, ambígua, sem feedback ou sem prova de uso real, não é DONE."
```

### 0.2 Justificativa técnica do Contrato UX UI

A UX UI precisa ser tratada como contrato porque a interface é o ponto de entrada dos dados do scout. Se a interface expõe evento errado, usa label ambíguo, omite status, não previne erro ou não permite recuperação, o banco recebe dado errado e o relatório final perde confiabilidade.

```yaml
ux_ui_technical_justification_contract:
  principles:
    - UI_e_ponto_de_captura_de_dados
    - erro_de_UI_vira_erro_de_scout
    - label_humano_reduz_memorizacao
    - status_visivel_aumenta_confianca
    - teste_AppTest_prova_renderizacao
    - operador_humano_prova_uso_real
```

### 0.3 Frontmatter obrigatório para documentos UX UI

```yaml
ux_ui_required_frontmatter_schema:
  doc_id: required
  title: required
  status: "draft | canonical | blocked | approved_by_human"
  version: required
  authority_level: required
  created_at: required
  updated_at: required
  owner: required
  repository: required
  module_id: optional
  scope: required
  objective: required
  primary_user: required
  primary_screen: required
  source_policy: required
  accessibility_policy: required
  evidence_policy: required
  validation_level: "reading | execution | human_operator | real_match"
  related_chunks: required
  related_tasks: required
  done_definition: required
  blocking_policy: required
```

### 0.4 Chunks operacionais UX UI

```yaml
ux_ui_operational_chunks:
  CHUNK_UX_00_SOURCES_AND_GATES:
    objective: "Registrar fontes fortes de UX UI e bloquear task sem evidência."
    owns:
      - ux_ui_canonical_sources
      - ux_ui_hard_task_gate
      - frontmatter_schema

  CHUNK_UX_01_INFORMATION_ARCHITECTURE:
    objective: "Definir páginas, entradas, saídas e bloqueios da experiência completa."
    owns:
      - app_information_architecture
      - navigation_contract
      - product_flow

  CHUNK_UX_02_MARKING_SCREEN_CONTRACT:
    objective: "Definir a tela de marcação como instrumento técnico de captura."
    owns:
      - visibility_of_system_status
      - event_marking_flow
      - recent_history
      - feedback

  CHUNK_UX_03_LABELS_AND_SEMANTICS:
    objective: "Garantir linguagem humana e impedir conflito entre código interno e termo de treinador."
    owns:
      - ui_label_glossary
      - forbidden_labels
      - semantic_rules

  CHUNK_UX_04_EXECUTABLE_UI_REGISTRY:
    objective: "Converter contratos em objetos executáveis que controlam botões, campos, validações e feedback."
    owns:
      - UIContract
      - UIButton
      - UIField
      - UIValidationRule
      - UIFeedback

  CHUNK_UX_05_AUTOMATED_AND_HUMAN_VALIDATION:
    objective: "Provar funcionamento com AppTest e operador humano."
    owns:
      - AppTest
      - operator_walkthrough
      - ux_measurement_protocol
      - screenshots
```

### 0.5 Schema obrigatório de task UX UI

```yaml
ux_ui_task_schema_required:
  task_id: required
  chunk_id: required
  objective: required
  executable_action: required
  technical_justification: required
  verifiable_strong_source: required
  UI_or_UX_contract_reference: required
  files_to_create: optional
  files_to_modify: optional
  tests_to_add: optional
  commands_to_run: required
  acceptance_criteria: required
  expected_proof: required
  real_world_success_condition: required
  rollback_or_blocking_rule: required
  done_definition: required
```


### 0.6 Tasks UX UI reforçadas — parte 1

```yaml
ux_ui_contract_driven_tasks_part_1:
  - task_id: UX_001_CREATE_GLOBAL_CONTRACT
    chunk_id: CHUNK_UX_00_SOURCES_AND_GATES
    objective: "Criar contrato global de UX UI no repositório."
    executable_action: "Criar docs/UX_UI_CONTRACT.md."
    technical_justification: "Design centrado no humano precisa ser planejado no ciclo de vida do sistema interativo."
    verifiable_strong_source: SRC-UX-ISO-9241-210
    UI_or_UX_contract_reference:
      - global_ux_ui_contract
      - accessibility_baseline
    commands_to_run:
      - git diff --check
    acceptance_criteria:
      - contrato_global_existe
      - fontes_UX_registradas
      - baseline_acessibilidade_definido
    expected_proof:
      - docs/UX_UI_CONTRACT.md
      - ux_contract_review.md
    real_world_success_condition: "Interface passa a ter regra antes de código."
    rollback_or_blocking_rule: "Sem contrato global, bloquear alteração em tagging.py."
    done_definition: "Contrato criado, fonte registrada e aceites objetivos definidos."

  - task_id: UX_002_CREATE_ATTACK_NO_SHOT_UI_CONTRACT
    chunk_id: CHUNK_UX_02_MARKING_SCREEN_CONTRACT
    objective: "Criar contrato do módulo attack_no_shot_v1."
    executable_action: "Criar docs/ux/modules/attack_no_shot_v1_ui.md."
    technical_justification: "Usuário deve reconhecer ações visíveis em vez de memorizar códigos internos."
    verifiable_strong_source: SRC-UX-NNG-HEURISTICS
    UI_or_UX_contract_reference:
      - attack_no_shot_v1_ui_contract_draft
      - ui_label_glossary
    commands_to_run:
      - python3 -m pytest tests/test_tagging_no_shot_attack_v1_ui.py -q
    acceptance_criteria:
      - labels_humanos_definidos
      - campos_obrigatorios_definidos
      - eventos_proibidos_listados
      - feedback_definido
    expected_proof:
      - docs/ux/modules/attack_no_shot_v1_ui.md
      - pytest_report.txt
    real_world_success_condition: "Operador registra perda de posse sem arremesso sem ver código interno."
    rollback_or_blocking_rule: "Sem contrato de módulo, não renderizar módulo."
    done_definition: "Contrato do módulo existe e passa teste de UI."

  - task_id: UX_003_CREATE_UI_REGISTRY_SCHEMA
    chunk_id: CHUNK_UX_04_EXECUTABLE_UI_REGISTRY
    objective: "Criar schema executável para impedir UI fora do contrato."
    executable_action: "Implementar UIContract, UIButton, UIField, UIValidationRule e UIFeedback."
    technical_justification: "Modelos tipados permitem validar estruturas e impedir campos ou botões inválidos."
    verifiable_strong_source: SRC-PYDANTIC-MODELS
    UI_or_UX_contract_reference:
      - ui_registry_schema
    commands_to_run:
      - python3 -m pytest tests/test_ui_contract_registry.py -q
    acceptance_criteria:
      - blocked_module_has_no_visible_buttons
      - visible_button_requires_human_label
      - derived_field_is_read_only
    expected_proof:
      - scoutpraia/ui/contracts.py
      - tests/test_ui_contract_registry.py
      - pytest_report.txt
    real_world_success_condition: "UI não consegue renderizar ação proibida por erro humano de programação."
    rollback_or_blocking_rule: "Se schema não bloquear evento proibido, FASE_8 fica blocked."
    done_definition: "Registry executável criado e validado por teste."
```

### 0.7 Continuação das tasks UX UI

As tasks UX_004, UX_005 e UX_006 também devem obedecer ao schema obrigatório acima: task_id, chunk_id, ação executável, justificativa técnica, fonte verificável, critério de aceite, prova esperada, condição de sucesso real e definição de DONE.

### 0.9 Reforços críticos agora obrigatórios

```yaml
ux_ui_required_reinforcements:
  operational_persona:
    status: mandatory
    artifact: docs/ux/operator_persona.md
    acceptance: "perfil do treinador ou analista, contexto de uso, pressão operacional e limitações descritas"
    proof: "operator_persona.md versionado e citado no walkthrough"

  visual_screenshot_baseline:
    status: mandatory
    artifact: docs/ux/evidence/<cycle_id>/screenshots/baseline/
    acceptance: "capturas da tela de marcação, erro, histórico, correção e salvamento"
    proof: "baseline visual salvo antes de piloto e comparado após mudanças"

  error_message_catalog:
    status: mandatory
    artifact: docs/ux/error_message_catalog.md
    acceptance: "todo erro tem campo afetado, motivo e ação corretiva"
    proof: "catálogo versionado e teste de erro validando mensagem contextual"

  real_world_observability:
    status: mandatory
    artifact: docs/ux/evidence/<cycle_id>/real_world_observability.md
    acceptance: "tempo, erro, recuperação, travamento, perda de estado e feedback registrados"
    proof: "relatório de observabilidade anexado ao pacote de evidências"
```

## 1. Fontes especializadas obrigatórias

As fontes abaixo devem ser registradas no `docs/sources/README.md` do repositório antes de qualquer implementação de UX UI ser considerada fechada.

```yaml
ux_ui_canonical_sources:
  SRC-UX-NNG-HEURISTICS:
    title: "Nielsen Norman Group — 10 Usability Heuristics for User Interface Design"
    url: "https://www.nngroup.com/articles/ten-usability-heuristics/"
    validates:
      - visibility_of_system_status
      - match_between_system_and_real_world
      - user_control_and_freedom
      - consistency_and_standards
      - error_prevention
      - recognition_rather_than_recall
      - flexibility_and_efficiency_of_use
      - minimalist_design
      - error_recovery
      - help_and_documentation

  SRC-UX-ISO-9241-210:
    title: "ISO 9241-210:2019 — Human-centred design for interactive systems"
    url: "https://www.iso.org/standard/77520.html"
    validates:
      - human_centred_design
      - user_task_environment_fit
      - iterative_evaluation
      - design_lifecycle

  SRC-A11Y-WCAG-22:
    title: "W3C WCAG 2.2 Quick Reference"
    url: "https://www.w3.org/WAI/WCAG22/quickref/"
    validates:
      - target_size_minimum
      - focus_visible
      - error_identification
      - labels_or_instructions
      - predictable_interaction

  SRC-UI-STREAMLIT-APPTEST:
    title: "Streamlit — Native App Testing Framework"
    url: "https://docs.streamlit.io/develop/concepts/app-testing"
    validates:
      - AppTest
      - simulated_user_input
      - rendered_output_inspection
      - pytest_integration
```

## 2. Arquitetura de informação do produto

A UI completa não pode ser pensada apenas como uma tela. O ScoutPraia precisa de arquitetura de navegação previsível.

```yaml
app_information_architecture:
  Jogos:
    purpose: "Cadastrar, selecionar e revisar jogos."
    primary_data:
      - competition_name
      - opponent
      - phase
      - video_path
    blocks_if:
      - jogo_sem_id
      - video_path_invalido_quando_video_for_obrigatorio

  Atletas:
    purpose: "Cadastrar elenco, número, função e vínculo com jogo."
    primary_data:
      - player_name
      - jersey_number
      - role
      - active_status
    blocks_if:
      - atleta_sem_nome
      - numero_duplicado_no_mesmo_elenco_sem_justificativa

  Marcação:
    purpose: "Registrar eventos de jogo com velocidade, contrato e rastreabilidade."
    primary_data:
      - match_id
      - timestamp
      - event_code
      - player_id
      - result
      - derived_points
      - contract_version
    blocks_if:
      - evento_bloqueado_visivel
      - pontos_divergentes_salvos
      - historico_recente_ausente

  Relatórios:
    purpose: "Gerar leitura objetiva e interpretação técnica sem misturar hipótese com KPI final."
    primary_data:
      - eventos_rastreaveis
      - KPIs_aprovados
      - filtros
      - exportacoes
    blocks_if:
      - kpi_sem_evidence_matrix
      - estatistica_sem_evento_origem

  Auditoria:
    purpose: "Revisar evidências, conflitos, testes e decisões humanas."
    primary_data:
      - cycle_evidence_package
      - docs_conflict_report
      - ux_operator_feedback
      - pytest_logs
    blocks_if:
      - claim_sem_evidencia

  Configuração:
    purpose: "Configurar fontes, taxonomia ativa, paths locais e preferências de operação."
    primary_data:
      - active_taxonomy
      - storage_path
      - export_path
      - source_register
    blocks_if:
      - taxonomia_ativa_ausente
```

## 3. Contrato global de UX UI

```yaml
global_ux_ui_contract:
  visibility_of_system_status:
    must_show:
      - jogo_ativo
      - adversario
      - competicao
      - taxonomia_ativa
      - set_ativo
      - posse_ativa_quando_existir
      - timestamp_atual
      - evento_selecionado
      - pontos_calculados
      - ultimo_evento_salvo
      - status_de_salvamento
    block_if_missing: true

  match_between_system_and_real_world:
    must_use:
      - portugues_claro
      - terminologia_do_beach_handball
      - linguagem_de_treinador
      - labels_humanos
    forbidden_as_primary_label:
      - event_code_cru
      - module_id_cru
      - enum_tecnico_sem_label
    block_if_missing: true

  user_control_and_freedom:
    must_support:
      - editar_evento_salvo
      - excluir_evento_com_confirmacao
      - corrigir_timestamp
      - corrigir_atleta
      - corrigir_resultado
      - revisar_historico
      - recuperar_estado_sem_perda
    block_if_missing: true

  error_prevention:
    must_prevent:
      - evento_bloqueado_na_UI
      - botao_rapido_de_modulo_nao_importar_v1
      - specialist_como_event_code
      - specialist_como_position_code
      - shootout_misturado_com_goalkeeper_save
      - transicao_calculando_pontos
      - manual_points_divergente
      - resultado_incompativel_com_evento
    block_if_missing: true

  recognition_rather_than_recall:
    must_provide:
      - botoes_visiveis_para_eventos_liberados
      - labels_humanos_para_todos_os_eventos_visiveis
      - ajuda_contextual_curta
      - preview_de_timestamp
      - historico_recente
      - feedback_de_salvamento
    block_if_missing: true

  flexibility_and_efficiency:
    must_support:
      - botoes_rapidos_contract_driven
      - fluxo_principal_em_uma_tela
      - repeticao_de_acoes_frequentes
      - defaults_seguros
      - minimo_atrito_para_evento_simples
    block_if_missing: true

  error_recovery:
    every_error_must_show:
      - campo_afetado
      - motivo
      - acao_corretiva
    forbidden_error_output:
      - traceback_para_usuario_final
      - codigo_sem_explicacao
      - erro_generico_sem_campo
    block_if_missing: true
```

## 4. Baseline de acessibilidade

```yaml
accessibility_baseline:
  labels_or_instructions:
    required: true
    evidence: accessibility_checklist.md

  focus_visible:
    required: true
    evidence: keyboard_navigation_check.md

  target_size_minimum:
    recommended_minimum: "24x24 CSS px quando controlável pelo layout"
    note: "Em Streamlit, quando o controle fino não for possível, registrar limitação e compensação por espaçamento, labels claros e ordem visual."
    evidence: accessibility_checklist.md

  error_identification:
    required: true
    rule: "Erro deve ser identificado em texto e associado ao campo afetado."
    evidence: error_recovery_test.log

  predictable_interaction:
    required: true
    rule: "A mesma ação deve ter o mesmo efeito em todas as telas."
    evidence: ux_heuristic_audit.md
```

## 5. Glossário canônico de labels da UI

```yaml
ui_label_glossary:
  spin_shot:
    label: "Giro"
    forbidden_labels:
      - spin
      - rotação
  inflight_shot:
    label: "Aérea"
    forbidden_labels:
      - fly
      - in-flight sem explicação
  shootout_attempt:
    label: "Shoot-out"
    forbidden_labels:
      - penalti
      - tiro de 6m
  specialist:
    label: "Especialista"
    semantic_rule: "Papel da arremessadora, não evento e não posição."
  goalkeeper:
    label: "Goleira"
  defender:
    label: "Defensora"
  return_pass:
    label: "Devolução"
  block:
    label: "Bloqueio"
  transition_sequence:
    label: "Transição"
    semantic_rule: "Transição não calcula pontos; pontos vêm do evento terminal."
  goalkeeper_save:
    label: "Defesa da goleira"
    semantic_rule: "Não usar em shoot-out; defesa no shoot-out pertence ao módulo de shoot-out."
  lost_possession_no_shot:
    label: "Perda de posse sem arremesso"
```

## 6. Schema mínimo do registry executável de UI

O arquivo `scoutpraia/ui/contracts.py` deve implementar, no mínimo, estas estruturas. O objetivo é impedir que `tagging.py` seja fonte de verdade da UI.

```yaml
ui_registry_schema:
  UIContract:
    fields:
      - module_id: str
      - import_rule_v1: str
      - ui_status: "hidden | visible | testing | blocked"
      - quick_buttons: list[UIButton]
      - fields: list[UIField]
      - validation_rules: list[UIValidationRule]
      - feedback: UIFeedback
      - source_contracts: list[str]
    invariants:
      - blocked_module_has_no_visible_buttons
      - visible_button_requires_human_label
      - visible_field_requires_human_label
      - derived_field_is_read_only

  UIButton:
    fields:
      - event_code: str
      - label: str
      - visible: bool
      - order: int
      - module_id: str
      - default_values: dict
    block_if:
      - event_code_forbidden
      - label_empty
      - module_blocked

  UIField:
    fields:
      - field_name: str
      - label: str
      - required: bool
      - read_only: bool
      - order: int
      - helper_text: str
    block_if:
      - required_field_without_label
      - derived_field_editable

  UIValidationRule:
    fields:
      - rule_id: str
      - applies_to: list[str]
      - block_if: list[str]
      - message: str
      - corrective_action: str
    block_if:
      - message_empty
      - corrective_action_empty

  UIFeedback:
    fields:
      - success_message: str
      - error_messages: dict
      - warning_messages: dict
    block_if:
      - success_message_empty
      - error_without_action
```

## 7. Template de contrato de UI por módulo

```yaml
module_ui_contract_template:
  module_id: ""
  import_rule_v1: ""
  ui_status: "hidden | visible | testing | blocked"
  primary_user_task: ""
  quick_buttons:
    visible: []
    hidden: []
    forbidden: []
  form_fields:
    required: []
    optional: []
    derived_read_only: []
    forbidden: []
  field_order: []
  labels:
    event_labels: {}
    field_labels: {}
    result_labels: {}
    helper_texts: {}
  validation_rules:
    block_if: []
    warn_if: []
    derive: []
  feedback:
    success_message: ""
    error_messages: {}
  accessibility:
    required_labels: true
    keyboard_flow_required: true
    visible_error_text_required: true
  tests:
    unit_tests: []
    streamlit_app_tests: []
    human_validation_script: ""
  evidence:
    screenshots: []
    pytest_logs: []
    operator_feedback: ""
```

## 8. Primeiro contrato de módulo recomendado: attack_no_shot_v1

```yaml
attack_no_shot_v1_ui_contract_draft:
  module_id: attack_no_shot_v1
  effective_status: active_pending_ui_contract
  ui_status: testing
  primary_user_task: "Registrar perda de posse sem arremesso com causa clara."
  quick_buttons:
    visible:
      - event_code: ball_control_turnover
        label: "Perda por erro de controle"
      - event_code: offensive_foul_turnover
        label: "Falta de ataque"
      - event_code: passive_play_turnover
        label: "Passivo"
      - event_code: substitution_error_turnover
        label: "Erro de substituição"
    forbidden:
      - specialist_goal
      - specialist_attempt
      - goal_conceded
      - shootout_goal
  form_fields:
    required:
      - timestamp
      - atleta
      - resultado_da_posse
      - causa_da_perda
    derived_read_only:
      - pontos_calculados
    forbidden:
      - manual_points_divergente
      - scorer_role_specialist
      - shot_origin_depth
  feedback:
    success_message: "Evento de ataque sem arremesso salvo."
    error_messages:
      missing_cause: "Informe a causa da perda de posse."
      invalid_result: "Ataque sem arremesso deve terminar como perda de posse sem arremesso."
  tests:
    streamlit_app_tests:
      - tests/test_tagging_no_shot_attack_v1_ui.py
      - tests/test_tagging_no_blocked_quick_buttons.py
```

## 9. Protocolo de medição UX

```yaml
ux_measurement_protocol:
  target_basic_event_marking_time:
    target: "<= 10 segundos"
    start_event: "operador identifica o lance no vídeo"
    stop_event: "evento salvo e visível no histórico"
    repetitions: 5
    evidence_file: docs/ux/evidence/<cycle_id>/ux_measurement_report.md

  target_error_recovery_time:
    target: "<= 20 segundos"
    start_event: "operador identifica erro no último evento salvo"
    stop_event: "evento corrigido e histórico atualizado"
    repetitions: 3
    evidence_file: docs/ux/evidence/<cycle_id>/ux_measurement_report.md

  target_blocked_event_buttons_visible:
    target: 0
    method: "AppTest + inspeção visual"
    evidence_file: docs/ux/evidence/<cycle_id>/blocked_buttons_report.md

  target_manual_points_mismatch_saved:
    target: 0
    method: "teste automatizado contra points_policy_v1"
    evidence_file: docs/ux/evidence/<cycle_id>/points_validation_report.md
```

## 10. Roteiro de validação humana

```yaml
operator_walkthrough_protocol:
  operator_profile: "treinador ou analista que entende handebol de areia"
  required_setup:
    - jogo_de_teste_cadastrado
    - atletas_cadastradas
    - taxonomia_ativa
    - video_de_teste_vinculado

  tasks:
    - task_id: UXH_001
      name: "Marcar perda de posse sem arremesso"
      expected_result: "evento salvo, pontos 0, histórico atualizado"
      pass_if:
        - operador_entende_botao
        - operador_nao_precisa_codigo_interno
        - evento_aparece_no_historico

    - task_id: UXH_002
      name: "Corrigir timestamp do último evento"
      expected_result: "timestamp atualizado sem perda de dados"
      pass_if:
        - operador_encontra_evento
        - operador_edita_sem_ajuda
        - historico_reflete_correcao

    - task_id: UXH_003
      name: "Interpretar erro de campo obrigatório"
      expected_result: "erro indica campo, motivo e ação corretiva"
      pass_if:
        - erro_e_claro
        - acao_corretiva_e_visivel
        - operador_corrige_sem_desenvolvedor

  required_evidence:
    - docs/ux/evidence/<cycle_id>/operator_walkthrough.md
    - docs/ux/evidence/<cycle_id>/operator_feedback.md
    - docs/ux/evidence/<cycle_id>/screenshots/
```

## 11. Backlog UX UI

```yaml
ux_ui_backlog:
  - task_id: UX_001_CREATE_GLOBAL_CONTRACT
    priority: P0
    output:
      - docs/UX_UI_CONTRACT.md
    acceptance:
      - contrato_global_existe
      - fontes_UX_registradas
      - layout_global_definido
      - baseline_acessibilidade_definido

  - task_id: UX_002_CREATE_ATTACK_NO_SHOT_UI_CONTRACT
    priority: P0
    depends_on:
      - UX_001_CREATE_GLOBAL_CONTRACT
    output:
      - docs/ux/modules/attack_no_shot_v1_ui.md
    acceptance:
      - botoes_permitidos_definidos
      - botoes_bloqueados_definidos
      - campos_obrigatorios_definidos
      - mensagens_de_erro_definidas

  - task_id: UX_003_CREATE_UI_REGISTRY_SCHEMA
    priority: P0
    depends_on:
      - UX_002_CREATE_ATTACK_NO_SHOT_UI_CONTRACT
    output:
      - scoutpraia/ui/contracts.py
      - tests/test_ui_contract_registry.py
    acceptance:
      - blocked_module_has_no_visible_buttons
      - visible_button_requires_human_label
      - derived_field_is_read_only

  - task_id: UX_004_TEST_BLOCKED_QUICK_BUTTONS
    priority: P0
    depends_on:
      - UX_003_CREATE_UI_REGISTRY_SCHEMA
    output:
      - tests/test_tagging_no_blocked_quick_buttons.py
    acceptance:
      - specialist_goal_nao_renderiza
      - specialist_attempt_nao_renderiza
      - goal_conceded_nao_renderiza
      - shootout_goal_nao_renderiza

  - task_id: UX_005_REFACTOR_QUICK_BUTTONS
    priority: P0
    depends_on:
      - UX_004_TEST_BLOCKED_QUICK_BUTTONS
    output:
      - scoutpraia/ui/quick_buttons.py
      - scoutpraia/pages/tagging.py
    acceptance:
      - quick_buttons_vem_do_registry
      - lista_manual_nao_expoe_evento_bloqueado

  - task_id: UX_006_CREATE_OPERATOR_WALKTHROUGH
    priority: P1
    depends_on:
      - UX_005_REFACTOR_QUICK_BUTTONS
    output:
      - docs/ux/operator_walkthrough.md
      - docs/ux/operator_feedback.md
      - docs/ux/evidence/README.md
    acceptance:
      - roteiro_humano_existe
      - metricas_temporais_definidas
      - criterios_pass_fail_definidos
```

## 12. Definition of Done UX UI

```yaml
ux_ui_definition_of_done:
  required_documents:
    - docs/UX_UI_CONTRACT.md
    - docs/ux/modules/<module_id>_ui.md
  required_code:
    - scoutpraia/ui/contracts.py
    - scoutpraia/ui/quick_buttons.py
  required_tests:
    - tests/test_ui_contract_registry.py
    - tests/test_tagging_no_blocked_quick_buttons.py
    - tests/test_tagging_ux_contract.py
  required_human_evidence_before_pilot:
    - docs/ux/evidence/<cycle_id>/operator_walkthrough.md
    - docs/ux/evidence/<cycle_id>/operator_feedback.md
    - docs/ux/evidence/<cycle_id>/screenshots/
  must_pass:
    - nenhum_botao_bloqueado_visivel
    - todo_evento_visivel_tem_label_humano
    - todo_erro_tem_acao_corretiva
    - evento_salvo_aparece_no_historico
    - operador_consegue_usar_sem_desenvolvedor
  final_status_allowed_only_if_all_pass: approved_by_human
```

