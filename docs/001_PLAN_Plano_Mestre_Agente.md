---
doc_id: PLAN_001
title: "Plano Mestre Determinístico do Agente"
status: canonical
version: "2.0.0"
authority_level: 5
category: PLAN
owner: Davi Sermenho
created_at: "2026-06-12"
last_updated: "2026-06-13"
repository: Davisermenho/scoutpraia
blocking_policy: "Nenhuma execução sem leitura prévia deste documento."
authority_scale: "1=informativo, 5=fonte obrigatória de execução para agentes"
parent_document: "https://docs.google.com/document/d/1bw-53YWvvTslmZA0XmZ-ySMGBc8BbudcNJ9WokPdcLY/edit?tab=t.0"
ux_ui_contract_document: "https://docs.google.com/document/d/1UQfD5H0g7PuA7nh_u_tv4yGzCoKpPtgLdX3pFYOkJus/edit?usp=drivesdk"
---

# ScoutPraia — Plano Mestre Determinístico do Agente

## Resumo executivo

Este documento é a versão consolidada e executável do plano de implementação do ScoutPraia por agente de IA. Ele foi criado para resolver os gaps identificados na auditoria do plano anterior: falta de ordem mestre, duplicação de blocos de UX/UI, ausência de backlog único, conflito semântico em módulos, diferença entre validação por leitura e validação por execução, e risco de a interface continuar sendo implementada por listas manuais em `tagging.py`.

O objetivo deste Plano Mestre é transformar o desenvolvimento do ScoutPraia em um fluxo determinístico, verificável e auditável. O agente não deve interpretar este documento como orientação genérica. Este documento define ordem de execução, bloqueios, dependências, artefatos esperados, testes obrigatórios, status efetivo de módulos e critérios de aceite.

O documento original `CRIANDO` permanece como base histórica, auditada e lexicalmente rica. Este Plano Mestre passa a ser a fonte curta de execução. O contrato específico de UX UI fica separado no documento vinculado, para preservar profundidade sem tornar este plano ilegível.

```yaml
master_plan_contract:
  purpose: "Definir a execução determinística do ScoutPraia por agente de IA."
  role: "Fonte principal de execução."
  parent_document_role: "Base histórica, auditoria e contexto expandido."
  ux_ui_document_role: "Contrato especializado de interface, experiência, validação humana e backlog de UI."
  may_skip_master_order: false
  may_use_old_plan_over_this_plan: false
  status_if_conflict: blocked
```

## Objetivo

Ser a fonte principal de execução determinística do ScoutPraia para agentes de IA, definindo ordem de execução, bloqueios, dependências, artefatos esperados, testes obrigatórios e critérios de aceite.

## 0. Gate obrigatório de execução por task

Este gate torna o Plano Mestre executável no padrão contract-driven. Nenhuma task pode entrar no plano, ser implementada, revisada, marcada como concluída ou usada como base para outra task se não cumprir todos os campos obrigatórios definidos abaixo.

```yaml
hard_task_gate:
  status: mandatory
  applies_to:
    - toda_task_do_Plano_Mestre
    - toda_task_do_Contrato_UX_UI
    - toda_task_de_codigo
    - toda_task_de_documentacao
    - toda_task_de_validacao
    - toda_task_de_build
    - toda_task_de_piloto
    - toda_task_de_uso_real
  hard_rule: "Nenhuma task pode entrar no plano se não tiver task_id, chunk associado, ação executável, justificativa técnica, fonte forte verificável, critério de aceite, prova esperada, objetivo, frontmatter completo e definição de DONE."
  block_if_missing_any:
    - task_id
    - chunk_id
    - executable_action
    - technical_justification
    - verifiable_strong_source
    - internal_contract_reference
    - acceptance_criteria
    - expected_proof
    - done_definition
    - validation_type
    - real_world_success_condition
```

### 0.1 Objetivo do Plano Mestre

Garantir que o agente implemente o ScoutPraia por ciclos pequenos, rastreáveis e verificáveis, sem improvisação, sem inferência semântica e sem avanço de fase sem prova. O Plano Mestre deve assegurar não apenas que arquivos sejam criados, mas que o que foi implementado funcione no mundo real: em revisão de vídeo, treino, piloto controlado e uso operacional por treinador ou analista.

```yaml
objective_contract:
  objective: "Conduzir a implementação real do ScoutPraia com ordem, gates, evidência e validação operacional."
  real_world_goal: "O sistema precisa funcionar para registrar, revisar, corrigir, persistir, recuperar e exportar dados reais de scout."
  failure_definition: "Código existente sem validação operacional não é DONE. Documento criado sem implementação testável não é DONE."
```

### 0.2 Justificativa técnica do Plano Mestre

O plano usa fluxo determinístico, contratos executáveis, registry de UI, validação por testes e evidência por ciclo porque agentes de IA precisam de trilhas explícitas e verificáveis para não tomar decisões implícitas. O padrão correto é restringir ações por schema, fonte, contrato, teste e prova. Structured Outputs exige aderência a schema, o que justifica um schema rígido para tasks e evidências. Workflows com caminhos predefinidos reduzem ambiguidade operacional. Testes automatizados e AppTest são necessários para verificar comportamento real da interface, e validação humana é necessária quando o resultado depende de uso sob contexto real.

```yaml
technical_justification_contract:
  source_based_rationale:
    - "schema_adherence_prevents_free_form_task_execution"
    - "predefined_workflows_reduce_agent_ambiguity"
    - "automated_tests_prove_regression_and_runtime_behavior"
    - "human_operator_validation_proves_real_world_use"
  implementation_rule: "Toda decisão arquitetural deve gerar artefato, teste, evidência e critério de rollback."
```

### 0.3 Bloco frontmatter obrigatório

Todo documento derivado, contrato de módulo, relatório de evidência, ADR ou plano de task deve começar com frontmatter completo. Documento sem frontmatter completo não pode ser usado como fonte de execução.

```yaml
required_frontmatter_schema:
  doc_id: required
  title: required
  status: "draft | canonical | deprecated | blocked | approved_by_human"
  version: required
  authority_level: required
  created_at: required
  updated_at: required
  owner: required
  repository: required
  scope: required
  objective: required
  source_policy: required
  evidence_policy: required
  validation_level: "reading | execution | human_operator | real_match"
  related_chunks: required
  related_tasks: required
  done_definition: required
  blocking_policy: required
```

### 0.4 Chunks operacionais

Os chunks operacionais são unidades de execução e leitura para agente. Cada task deve apontar para um chunk. O agente não pode executar task solta fora de chunk.

```yaml
operational_chunks:
  CHUNK_MASTER_00_GATES:
    objective: "Aplicar gates obrigatórios, frontmatter, fonte, contrato, evidência e bloqueios."
    owns:
      - hard_task_gate
      - required_frontmatter_schema
      - validation_status
      - evidence_path_policy

  CHUNK_MASTER_01_REPO_RECONCILIATION:
    objective: "Resolver conflitos entre documentação, código, testes e status efetivo de módulos."
    owns:
      - module_effective_status
      - finalization_v1_reconciliation
      - docs_conflict_report

  CHUNK_MASTER_02_SOURCE_REGISTER:
    objective: "Normalizar source IDs e registrar fontes especializadas no repositório."
    owns:
      - source_id_policy
      - canonical_source_ids
      - docs/sources/README.md

  CHUNK_MASTER_03_CONTRACT_DRIVEN_IMPLEMENTATION:
    objective: "Criar contratos executáveis, schemas, testes e implementação por TDD."
    owns:
      - events_v1_contracts
      - points_policy_v1
      - ui_contract_registry
      - pytest_validation

  CHUNK_MASTER_04_UI_UX_EXECUTION:
    objective: "Delegar execução de interface ao Contrato UX UI e garantir AppTest e validação humana."
    owns:
      - UX_UI_CONTRACT
      - tagging_py_refactor
      - AppTest
      - operator_walkthrough

  CHUNK_MASTER_05_REAL_WORLD_VALIDATION:
    objective: "Comprovar funcionamento em build, piloto, uso real, persistência, backup e exportação."
    owns:
      - build_local
      - pilot_report
      - real_match_report
      - post_match_backup
```

### 0.5 Schema obrigatório de task

```yaml
task_schema_required:
  task_id: required
  chunk_id: required
  objective: required
  executable_action: required
  technical_justification: required
  verifiable_strong_source:
    canonical_source_id: required
    source_url_or_repo_path: required
    validates: required
  internal_contract_reference: required
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

### 0.6 Matriz reforçada de tasks P0/P1

```yaml
contract_driven_tasks:
  - task_id: P0_001_CREATE_MASTER_EXECUTION_ORDER
    chunk_id: CHUNK_MASTER_00_GATES
    objective: "Definir ordem única de execução do agente."
    executable_action: "Manter master_execution_order como fonte primária de sequência."
    technical_justification: "Workflows com caminhos predefinidos reduzem ambiguidade de execução para agentes."
    verifiable_strong_source:
      canonical_source_id: SRC-AGENT-ANTHROPIC-WORKFLOWS
      validates: predefined_workflow_paths
    internal_contract_reference:
      - document_roles
      - master_execution_order
    commands_to_run:
      - git status --short
    acceptance_criteria:
      - master_execution_order_existe
      - nenhuma_fase_executa_fora_da_ordem
    expected_proof:
      - Plano_Mestre_contem_master_execution_order
    real_world_success_condition: "Agente sempre sabe a próxima ação antes de alterar arquivos."
    rollback_or_blocking_rule: "Bloquear task ambígua."
    done_definition: "Ordem mestre existe, está citada no prompt do agente e possui gates bloqueantes."

  - task_id: P0_002_CREATE_EFFECTIVE_MODULE_STATUS
    chunk_id: CHUNK_MASTER_01_REPO_RECONCILIATION
    objective: "Eliminar ambiguidade entre módulo ativo, bloqueado e pendente."
    executable_action: "Manter module_effective_status como tabela obrigatória de decisão."
    technical_justification: "Status divergente entre código e documentação cria risco de UI expor evento incorreto."
    verifiable_strong_source:
      canonical_source_id: SRC-OPENAI-STRUCTURED-OUTPUTS
      validates: schema_adherence_and_required_fields
    internal_contract_reference:
      - scoutpraia/contracts/events_v1.py
      - docs/005_CONT_Operacional_Eventos_v1.md
      - docs/012_ARCH_Agent_View_Design.md
    commands_to_run:
      - PYTHONPATH=. python3 scripts/audit_docs_contract_alignment.py
      - python3 -m pytest tests/test_events_v1_contract_registry.py -q
    acceptance_criteria:
      - finalization_v1_tem_status_unico
      - todo_modulo_tem_effective_status
    expected_proof:
      - docs_conflict_report.md
      - contract_registry_test.log
    real_world_success_condition: "Nenhum módulo conflitante aparece na UI de marcação."
    rollback_or_blocking_rule: "Se houver divergência, effective_status=blocked_pending_reconciliation."
    done_definition: "Tabela efetiva existe, conflitos estão bloqueados e testes de contrato passam."

  - task_id: P0_003_CREATE_GLOBAL_UX_UI_CONTRACT
    chunk_id: CHUNK_MASTER_04_UI_UX_EXECUTION
    objective: "Criar contrato global de interface antes de alterar tagging.py."
    executable_action: "Criar docs/011_UX_Contrato_Interface.md a partir do Contrato UX UI."
    technical_justification: "Design centrado no humano exige considerar usuários, tarefas e ambiente durante o ciclo de vida do sistema."
    verifiable_strong_source:
      canonical_source_id: SRC-UX-ISO-9241-210
      validates: human_centred_design_lifecycle
    internal_contract_reference:
      - ScoutPraia_Contrato_UX_UI
    commands_to_run:
      - git diff --check
    acceptance_criteria:
      - contrato_global_existe
      - fontes_UX_registradas
      - gate_UX_UI_definido
    expected_proof:
      - docs/011_UX_Contrato_Interface.md
      - ux_contract_review.md
    real_world_success_condition: "Operador entende a tela e consegue iniciar marcação sem depender do desenvolvedor."
    rollback_or_blocking_rule: "Sem contrato global, nenhuma UI nova pode ser implementada."
    done_definition: "Contrato existe no repositório, possui fontes, critérios e bloqueios."

  - task_id: P0_004_CREATE_ATTACK_NO_SHOT_UI_CONTRACT
    chunk_id: CHUNK_MASTER_04_UI_UX_EXECUTION
    objective: "Definir UI do primeiro módulo ativo sem ambiguidade."
    executable_action: "Criar docs/ux/modules/attack_no_shot_v1_ui.md."
    technical_justification: "Reconhecimento em vez de memorização exige labels humanos e botões claros para reduzir erro do operador."
    verifiable_strong_source:
      canonical_source_id: SRC-UX-NNG-HEURISTICS
      validates: recognition_rather_than_recall
    internal_contract_reference:
      - module_effective_status.attack_no_shot_v1
      - scoutpraia/contracts/events_v1.py
    commands_to_run:
      - python3 -m pytest tests/test_tagging_no_shot_attack_v1_ui.py -q
    acceptance_criteria:
      - labels_humanos_definidos
      - botoes_bloqueados_definidos
      - campos_obrigatorios_definidos
    expected_proof:
      - docs/ux/modules/attack_no_shot_v1_ui.md
      - pytest_report.txt
    real_world_success_condition: "Operador registra perda de posse sem arremesso em fluxo simples e sem código interno."
    rollback_or_blocking_rule: "Sem contrato de módulo, o módulo não pode renderizar botão."
    done_definition: "Contrato do módulo existe, é testado e não expõe eventos proibidos."

  - task_id: P0_005_CREATE_UI_REGISTRY_SCHEMA
    chunk_id: CHUNK_MASTER_03_CONTRACT_DRIVEN_IMPLEMENTATION
    objective: "Criar registry executável de UI para impedir botões e campos fora do contrato."
    executable_action: "Criar scoutpraia/ui/contracts.py com UIContract, UIButton, UIField, UIValidationRule e UIFeedback."
    technical_justification: "Modelos tipados e validação de schema impedem entrada livre e reduzem erro semântico."
    verifiable_strong_source:
      canonical_source_id: SRC-PYDANTIC-MODELS
      validates: typed_models_and_validation
    internal_contract_reference:
      - task_schema_required
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
    real_world_success_condition: "Evento bloqueado não aparece na tela, mesmo que exista em código legado."
    rollback_or_blocking_rule: "Se registry não bloqueia evento proibido, FASE_8 fica blocked."
    done_definition: "Registry existe, testes passam e tagging.py não decide sozinho o que renderizar."

  - task_id: P0_006_REFACTOR_QUICK_BUTTONS_TO_REGISTRY
    chunk_id: CHUNK_MASTER_04_UI_UX_EXECUTION
    objective: "Remover risco de botões rápidos manuais em tagging.py."
    executable_action: "Refatorar quick buttons para derivarem do registry de UI."
    technical_justification: "Testes de UI precisam simular entrada e inspecionar conteúdo renderizado para provar ausência de botões bloqueados."
    verifiable_strong_source:
      canonical_source_id: SRC-UI-STREAMLIT-APPTEST
      validates: simulated_user_input_and_rendered_output_inspection
    internal_contract_reference:
      - scoutpraia/pages/tagging.py
      - scoutpraia/ui/contracts.py
    commands_to_run:
      - python3 -m pytest tests/test_tagging_no_blocked_quick_buttons.py -q
      - python3 -m pytest tests/test_tagging_ux_contract.py -q
    acceptance_criteria:
      - QUICK_EVENT_TYPES_manual_removed_or_neutralized
      - blocked_events_do_not_render
      - labels_resolved_from_registry
    expected_proof:
      - streamlit_app_tests.log
      - tests/test_tagging_no_blocked_quick_buttons.py
    real_world_success_condition: "Tela real não oferece ao operador nenhuma ação proibida."
    rollback_or_blocking_rule: "Se botão proibido renderizar, build e piloto bloqueados."
    done_definition: "AppTest prova que botões bloqueados não aparecem."

  - task_id: P0_007_CREATE_OPERATOR_WALKTHROUGH
    chunk_id: CHUNK_MASTER_05_REAL_WORLD_VALIDATION
    objective: "Comprovar que a UI funciona com operador humano."
    executable_action: "Criar roteiro, executar walkthrough e registrar feedback/screenshot."
    technical_justification: "Interface só pode ser validada como produto quando o usuário real consegue cumprir a tarefa no contexto de uso."
    verifiable_strong_source:
      canonical_source_id: SRC-UX-ISO-9241-210
      validates: user_task_environment_fit_and_iterative_evaluation
    internal_contract_reference:
      - UX_UI_CONTRACT.operator_walkthrough_protocol
    commands_to_run:
      - python3 -m pytest -q
      - scripts/verify_current_state.sh
    acceptance_criteria:
      - operador_marca_evento_basico_sem_ajuda
      - operador_corrige_evento_salvo
      - operador_entende_erro_e_acao_corretiva
    expected_proof:
      - docs/ux/evidence/<cycle_id>/operator_walkthrough.md
      - docs/ux/evidence/<cycle_id>/operator_feedback.md
      - docs/ux/evidence/<cycle_id>/screenshots/
    real_world_success_condition: "Operador usa o sistema sem desenvolvedor e sem perda de dados."
    rollback_or_blocking_rule: "Sem validação humana, piloto permanece blocked."
    done_definition: "Walkthrough executado, evidências salvas e falhas críticas tratadas."

  - task_id: P1_001_RECONCILE_FINALIZATION_V1_STATUS
    status: completed
    completed_at: "2026-06-13"
    chunk_id: CHUNK_MASTER_01_REPO_RECONCILIATION
    objective: "Resolver conflito semântico de finalization_v1 antes de qualquer exposição na UI."
    executable_action: "Gerar relatório de conflito e aplicar decisão única nos documentos e contratos."
    technical_justification: "Conflito entre contrato executável e documentação quebra rastreabilidade e torna o comportamento não determinístico."
    verifiable_strong_source:
      canonical_source_id: SRC-OPENAI-STRUCTURED-OUTPUTS
      validates: required_schema_and_schema_adherence
    internal_contract_reference:
      - docs/005_CONT_Operacional_Eventos_v1.md
      - docs/012_ARCH_Agent_View_Design.md
      - scoutpraia/contracts/events_v1.py
    commands_to_run:
      - PYTHONPATH=. python3 scripts/audit_docs_contract_alignment.py
      - python3 -m pytest tests/test_events_v1_contract_registry.py -q
    acceptance_criteria:
      - decisao_unica_documentada
      - import_rule_v1_sem_conflito
      - UI_status_definido
    expected_proof:
      - docs_conflict_report.md
      - contract_delta.md
      - pytest_report.txt
    real_world_success_condition: "Finalização só aparece na UI quando regra, contrato, teste e documentação estiverem alinhados."
    rollback_or_blocking_rule: "Enquanto conflito existir, effective_status=blocked_pending_reconciliation."
    done_definition: "Sem conflito documental e com teste verde."
```

### 0.7 O que você não pediu, mas é vital para o sucesso total

```yaml
vital_unasked_requirements:
  - requirement_id: VITAL_001_TRACEABILITY_MATRIX
    explanation: "Cada task precisa ligar fonte, decisão, arquivo, teste, evidência e critério de DONE. Sem matriz de rastreabilidade, o agente pode alegar conclusão sem prova encadeada."
    add_to_plan: true
    expected_artifact: docs/evidence/<cycle_id>/traceability_matrix.md

  - requirement_id: VITAL_002_ROLLBACK_AND_BLOCK_POLICY
    explanation: "Toda task precisa definir rollback ou regra de bloqueio. Sem isso, uma alteração quebrada pode avançar até piloto."
    add_to_plan: true
    expected_artifact: rollback_or_blocking_rule por task

  - requirement_id: VITAL_003_SEED_DATA_AND_SMOKE_TEST
    explanation: "Para provar funcionamento real, o sistema precisa de dados mínimos de jogo, atletas, evento e vídeo de teste. Sem seed data, testes podem passar sem simular uso real."
    add_to_plan: true
    expected_artifact: tests/fixtures/ + smoke_test.log

  - requirement_id: VITAL_004_ADR_FOR_ARCHITECTURE_DECISIONS
    explanation: "Decisões como registry de UI, status efetivo dos módulos e build local precisam de ADR para não serem revertidas por inferência futura."
    add_to_plan: true
    expected_artifact: docs/adr/ADR_UI_REGISTRY.md

  - requirement_id: VITAL_005_REAL_WORLD_OBSERVABILITY
    explanation: "Uso real precisa registrar tempo, erro, recuperação, travamento, perda de dados e feedback do operador. Sem observabilidade, não há prova de funcionamento no mundo real."
    add_to_plan: true
    expected_artifact: docs/ux/evidence/<cycle_id>/ux_measurement_report.md
```


## 1. Papéis dos documentos

```yaml
document_roles:
  SCOUTPRAIA_AGENT_MASTER_PLAN:
    role: "plano de execução"
    authority: primary_for_agent_execution
    use_when:
      - escolher_proxima_tarefa
      - decidir_ordem_de_execucao
      - bloquear_por_conflito
      - validar_definition_of_done

  CRIANDO_ORIGINAL:
    role: "base histórica e auditoria ampliada"
    authority: context_only_unless_referenced_by_master
    use_when:
      - consultar_racional_completo
      - recuperar_contexto_lexical
      - verificar_auditoria_anterior
    must_not_use_for:
      - escolher_ordem_de_execucao_se_conflitar_com_master
      - liberar_modulo_bloqueado

  UX_UI_CONTRACT:
    role: "contrato especializado de interface"
    authority: primary_for_ui_ux
    use_when:
      - alterar_tagging_py
      - criar_botao_rapido
      - criar_formulario
      - criar_label_humano
      - validar_fluxo_de_marcacao
      - liberar_piloto

  EXECUTABLE_CONTRACTS:
    role: "comportamento executável do app"
    files:
      - scoutpraia/contracts/events_v1.py
      - scoutpraia/contracts/points_policy_v1.py
      - scoutpraia/ui/contracts.py
    authority: primary_for_runtime_behavior
```

## 2. Ordem mestre obrigatória

O agente deve seguir esta ordem antes de qualquer implementação. Nenhuma fase posterior pode ser executada enquanto a anterior estiver bloqueada.

```yaml
master_execution_order:
  - order: 0
    gate_id: PRE_GATE_CONTEXT
    purpose: "Identificar tarefa, módulo, arquivos afetados, branch, estado git e documentos aplicáveis."
    pass_if:
      - tarefa_identificada
      - modulo_identificado_ou_none
      - documentos_obrigatorios_listados
      - estado_git_verificado
    block_if:
      - tarefa_ambigua
      - estado_git_inesperado

  - order: 1
    gate_id: GATE_0_SOURCES_CONTRACTS_EVIDENCE
    purpose: "Garantir fonte forte, fonte interna, contrato, teste e evidência antes de agir."
    pass_if:
      - fonte_forte_externa_ou_excecao_justificada
      - fonte_interna_lida
      - contrato_compativel
      - teste_planejado_ou_existente
      - evidencia_planejada
    block_if:
      - fonte_ausente
      - contrato_ausente
      - teste_ausente
      - conflito_documental_nao_tratado

  - order: 2
    gate_id: GATE_UX_UI
    applies_when:
      - alteracao_em_interface
      - alteracao_em_tagging_py
      - criacao_de_modulo_visivel
      - build
      - piloto
      - uso_real
    pass_if:
      - UX_UI_CONTRACT_lido
      - contrato_de_modulo_lido_ou_criado
      - ui_registry_respeitado
      - AppTest_planejado
    block_if:
      - botao_manual_fora_do_registry
      - evento_bloqueado_renderizado
      - label_humano_ausente

  - order: 3
    gate_id: REPOSITORY_CONFLICT_RECONCILIATION
    purpose: "Resolver ou bloquear conflitos entre código, docs, Agent View, contrato operacional e testes."
    pass_if:
      - module_effective_status_definido
      - conflitos_documentados
      - decisao_de_bloqueio_ou_liberacao_explicita
    block_if:
      - finalization_v1_sem_decisao_unica
      - import_rule_v1_conflitante
      - MVP_ou_G5_declarado_sem_evidencia

  - order: 4
    gate_id: PHASE_0_TO_14
    purpose: "Executar a fase oficial correspondente, já com UX/UI integrado quando aplicável."
    pass_if:
      - fase_identificada
      - backlog_item_identificado
      - comandos_da_fase_planejados
      - evidencias_da_fase_planejadas

  - order: 5
    gate_id: UX_UI_BACKLOG
    applies_when:
      - tarefa_UI
      - tarefa_UX
      - tarefa_de_marcacao
    pass_if:
      - tarefa_UX_com_task_id
      - arquivos_UI_definidos
      - testes_UI_definidos
      - validacao_humana_definida_quando_aplicavel

  - order: 6
    gate_id: BUILD_PILOT_REAL_USE
    purpose: "Bloquear build, piloto e uso real se testes, UX, persistência ou evidência falharem."
    pass_if:
      - pytest_verde
      - verify_current_state_verde
      - ux_ui_gate_passed
      - dados_recuperaveis
      - operador_consegue_usar_sem_desenvolvedor
```

## 3. Tipos de validação

A validação precisa ser explicitamente classificada. O agente não pode declarar uma validação por leitura como se fosse validação por execução.

```yaml
validation_status:
  validation_by_reading:
    definition: "Validação por leitura de documentos, código, contratos e testes versionados."
    can_claim: "alinhamento documental observado"
    cannot_claim: "testes executados ou funcionamento real"

  validation_by_execution:
    definition: "Validação por comando executado no ambiente local ou CI."
    required_evidence:
      - pytest_report.txt
      - verify_current_state.log
      - command_output.log

  validation_by_human_operator:
    definition: "Validação por operador humano usando a interface."
    required_evidence:
      - operator_walkthrough.md
      - operator_feedback.md
      - screenshots_ui_marking_flow/

  validation_by_real_match:
    definition: "Validação durante jogo real ou análise de jogo real."
    required_evidence:
      - real_match_report.md
      - post_match_backup.zip
      - coach_feedback.md
```

## 4. Status efetivo dos módulos

Esta tabela resolve a ambiguidade entre documentos, código e UI. O agente deve obedecer ao `effective_status`.

```yaml
module_effective_status:
  attack_no_shot_v1:
    executable_status: "available_in_contract"
    docs_status: "importar_v1_confirmed_if_tests_green"
    agent_view_status: "importar_v1"
    ui_status: "allowed_after_ui_contract_and_registry"
    effective_status: "active_pending_ui_contract"
    required_resolution:
      - criar_docs_ux_modules_attack_no_shot_v1_ui_md
      - criar_ui_registry_entry
      - testar_AppTest

  finalization_v1:
    executable_status: "active_in_events_v1_and_tests"
    docs_status: "importar_v1"
    agent_view_status: "importar_v1"
    ui_status: "allowed_after_ui_contract_and_registry"
    effective_status: "active"
    activated_at: "2026-06-12"
    resolved_at: "2026-06-13"
    resolution: "Conflito documental resolvido — 005_CONT seções 2-bis, 3, 7 e 000_QUICK_REF atualizados."

  offensive_creation_v1:
    executable_status: "not_confirmed_for_ui"
    docs_status: "nao_importar_v1"
    ui_status: "blocked"
    effective_status: "blocked_pending_release"

  defensive_v1:
    executable_status: "not_confirmed_for_ui"
    docs_status: "nao_importar_v1"
    ui_status: "blocked"
    effective_status: "blocked_pending_release"

  shootout_v1:
    executable_status: "not_confirmed_for_ui"
    docs_status: "nao_importar_v1"
    ui_status: "blocked"
    effective_status: "blocked_pending_release"

  goalkeeper_v1:
    executable_status: "not_confirmed_for_ui"
    docs_status: "nao_importar_v1"
    ui_status: "blocked"
    effective_status: "blocked_pending_release"

  transition_v1:
    executable_status: "not_confirmed_for_ui"
    docs_status: "nao_importar_v1"
    ui_status: "blocked"
    effective_status: "blocked_pending_release"
```

## 5. Normalização de fontes

O agente deve registrar evidências usando o `canonical_source_id`. Aliases só podem aparecer como compatibilidade.

```yaml
source_id_policy:
  required_field: canonical_source_id
  aliases_allowed: true
  aliases_must_not_replace_canonical: true
  canonical_source_ids:
    SRC-IHF-RULES:
      aliases:
        - SRC_RULES_IHF_001
      use_for:
        - regra_esportiva
        - pontuacao
        - set
        - shootout
    SRC-NOTATIONAL-BH:
      aliases:
        - SRC_NOTATIONAL_BH_001
        - SRC_WOMENS_BH_STATS_001
      use_for:
        - indicadores
        - padroes_de_jogo
        - analise_notacional
    SRC-OBS-MEASUREMENT:
      aliases:
        - SRC_OBS_MEASUREMENT_001
        - SRC_HANDALL_AI_001
      use_for:
        - confiabilidade_observacional
        - protocolo_de_validacao
    SRC-UX-NNG-HEURISTICS:
      aliases:
        - SRC_UX_NNG_HEURISTICS_001
      use_for:
        - heuristicas_de_usabilidade
        - prevencao_de_erro
        - recuperacao_de_erro
    SRC-UX-ISO-9241-210:
      aliases:
        - SRC_UX_ISO_9241_210_001
      use_for:
        - design_centrado_no_humano
        - ciclo_de_vida_de_interacao
    SRC-A11Y-WCAG-22:
      aliases:
        - SRC_A11Y_WCAG_22_001
      use_for:
        - acessibilidade
        - foco_visivel
        - target_size
        - error_identification
    SRC-UI-STREAMLIT-APPTEST:
      aliases:
        - SRC_UI_STREAMLIT_001
        - SRC_UI_STREAMLIT_APP_TEST_001
      use_for:
        - testes_de_UI
        - AppTest
```

## 6. Backlog executável obrigatório

Este backlog substitui listas soltas de tarefas. O agente só pode executar uma tarefa se seu `depends_on` estiver resolvido.

```yaml
execution_backlog:
  - task_id: P0_001_CREATE_MASTER_EXECUTION_ORDER
    priority: P0
    status: done_in_this_document
    phase_id: PRE_GATE_CONTEXT
    depends_on: []
    files_to_create:
      - ScoutPraia — Plano Mestre Determinístico do Agente
    acceptance_criteria:
      - master_execution_order_existe
      - document_roles_existe
      - validation_status_existe

  - task_id: P0_002_CREATE_EFFECTIVE_MODULE_STATUS
    priority: P0
    status: done_in_this_document
    phase_id: REPOSITORY_CONFLICT_RECONCILIATION
    depends_on:
      - P0_001_CREATE_MASTER_EXECUTION_ORDER
    files_to_create:
      - module_effective_status_table
    acceptance_criteria:
      - finalization_v1_blocked_pending_reconciliation
      - blocked_modules_explicitados
      - active_module_requires_ui_contract

  - task_id: P0_003_CREATE_GLOBAL_UX_UI_CONTRACT
    priority: P0
    status: pending_repo_implementation
    phase_id: GATE_UX_UI
    depends_on:
      - P0_001_CREATE_MASTER_EXECUTION_ORDER
    files_to_create:
      - docs/011_UX_Contrato_Interface.md
    source_document:
      - ScoutPraia — Contrato UX UI e Backlog de Interface
    tests_to_add:
      - tests/test_ux_ui_contract_exists.py
    evidence_to_generate:
      - ux_contract_review.md
    block_if:
      - fontes_UX_nao_registradas
      - contrato_global_sem_criterios_de_aceite

  - task_id: P0_004_CREATE_ATTACK_NO_SHOT_UI_CONTRACT
    priority: P0
    status: pending_repo_implementation
    phase_id: FASE_5_ACTIVE_MODULE_SELECTION
    depends_on:
      - P0_003_CREATE_GLOBAL_UX_UI_CONTRACT
    files_to_create:
      - docs/ux/modules/attack_no_shot_v1_ui.md
    tests_to_add:
      - tests/test_attack_no_shot_v1_ui_contract.py
    acceptance_criteria:
      - quick_buttons_visiveis_definidos
      - campos_obrigatorios_definidos
      - mensagens_de_erro_definidas
      - labels_humanos_definidos

  - task_id: P0_005_CREATE_UI_REGISTRY_SCHEMA
    priority: P0
    status: pending_repo_implementation
    phase_id: FASE_6_TDD_IMPLEMENTATION
    depends_on:
      - P0_003_CREATE_GLOBAL_UX_UI_CONTRACT
      - P0_004_CREATE_ATTACK_NO_SHOT_UI_CONTRACT
    files_to_create:
      - scoutpraia/ui/contracts.py
      - tests/test_ui_contract_registry.py
    acceptance_criteria:
      - UIContract_schema_definido
      - UIButton_schema_definido
      - UIField_schema_definido
      - UIValidationRule_schema_definido
      - blocked_event_must_not_render_test_passes

  - task_id: P0_006_REFACTOR_QUICK_BUTTONS_TO_REGISTRY
    priority: P0
    status: pending_repo_implementation
    phase_id: FASE_8_UI_MARKING_INTERFACE
    depends_on:
      - P0_005_CREATE_UI_REGISTRY_SCHEMA
    files_to_modify:
      - scoutpraia/pages/tagging.py
    files_to_create:
      - scoutpraia/ui/quick_buttons.py
      - tests/test_tagging_no_blocked_quick_buttons.py
    acceptance_criteria:
      - QUICK_EVENT_TYPES_manual_removed_or_neutralized
      - blocked_events_do_not_render
      - labels_resolved_from_registry

  - task_id: P0_007_CREATE_OPERATOR_WALKTHROUGH
    priority: P0
    status: pending_repo_implementation
    phase_id: FASE_10_REAL_VIDEO_VALIDATION
    depends_on:
      - P0_006_REFACTOR_QUICK_BUTTONS_TO_REGISTRY
    files_to_create:
      - docs/ux/operator_walkthrough.md
      - docs/ux/operator_feedback.md
      - docs/ux/evidence/README.md
    acceptance_criteria:
      - tarefas_humanas_definidas
      - metricas_temporais_definidas
      - pass_fail_definido
      - screenshots_path_definido

  - task_id: P1_001_RECONCILE_FINALIZATION_V1_STATUS
    priority: P1
    status: blocked_pending_human_decision
    phase_id: REPOSITORY_CONFLICT_RECONCILIATION
    depends_on:
      - P0_002_CREATE_EFFECTIVE_MODULE_STATUS
    files_to_modify:
      - docs/005_CONT_Operacional_Eventos_v1.md
      - docs/012_ARCH_Agent_View_Design.md
      - scoutpraia/contracts/events_v1.py
      - tests/test_events_v1_contract_registry.py
    acceptance_criteria:
      - decisao_unica_documentada
      - UI_status_definido
      - import_rule_v1_sem_conflito
      - tests_green
    block_if:
      - decisao_humana_ausente
      - docs_e_codigo_divergem
```

## 7. Fases oficiais reescritas com UX UI integrado

As fases abaixo substituem os blocos antigos quando houver conflito.

```yaml
phase_overrides:
  FASE_5_ACTIVE_MODULE_SELECTION:
    phase_goal: "Selecionar módulo ativo somente quando contrato executável, documentação, UI contract e testes estiverem alinhados."
    required_inputs:
      - module_effective_status
      - docs/ux/modules/<module_id>_ui.md
      - scoutpraia/contracts/events_v1.py
      - docs/005_CONT_Operacional_Eventos_v1.md
      - docs/012_ARCH_Agent_View_Design.md
    pass_condition:
      - effective_status_not_blocked
      - ui_contract_exists_for_visible_module
      - import_rule_v1_explicit
      - no_conflict_between_docs_and_code
    block_if:
      - module_effective_status_blocked
      - ui_contract_missing
      - import_rule_v1_missing_or_conflicting
      - finalization_v1_pending_reconciliation

  FASE_6_TDD_IMPLEMENTATION:
    phase_goal: "Implementar por TDD, incluindo contrato de UI quando a alteração afetar interface."
    required_tests:
      - tests/test_events_v1_contract_registry.py
      - tests/test_points_policy_v1.py
      - tests/test_ui_contract_registry.py
      - tests/test_tagging_ux_contract.py_when_UI_changes
    block_if:
      - implementation_without_test
      - UI_change_without_AppTest
      - registry_change_without_unit_test
      - test_removed_to_pass_suite

  FASE_8_UI_MARKING_INTERFACE:
    phase_goal: "Implementar interface de marcação contract-driven, sem lista manual de eventos bloqueados."
    required_artifacts:
      - docs/011_UX_Contrato_Interface.md
      - docs/ux/modules/<module_id>_ui.md
      - scoutpraia/ui/contracts.py
      - scoutpraia/ui/quick_buttons.py
      - tests/test_tagging_no_blocked_quick_buttons.py
    pass_condition:
      - quick_buttons_registry_driven
      - blocked_events_not_rendered
      - labels_humanos_presentes
      - feedback_salvamento_visivel
      - historico_recente_visivel
      - pontos_derivados_ou_validados
    block_if:
      - QUICK_EVENT_TYPES_manual_expoe_evento_bloqueado
      - evento_sem_label_humano
      - botao_bloqueado_visivel
      - erro_sem_acao_corretiva

  FASE_10_REAL_VIDEO_VALIDATION:
    phase_goal: "Validar a marcação com vídeo real e operador humano, registrando clareza, tempo, erro e recuperação."
    required_artifacts:
      - docs/ux/operator_walkthrough.md
      - docs/ux/operator_feedback.md
      - docs/ux/evidence/<cycle_id>/screenshots/
    pass_condition:
      - operador_marca_evento_basico_sem_ajuda
      - operador_corrige_evento_salvo
      - operador_entende_pontos_calculados
      - tempos_medidos_registrados
    block_if:
      - validacao_humana_subjetiva_sem_roteiro
      - screenshots_ausentes
      - erro_sem_caminho_de_correcao

  FASE_11_BUILD_PACKAGE_LOCAL:
    phase_goal: "Gerar build local sem servidor externo, sem deploy web e sem dependência de internet para marcação."
    local_build_contract:
      no_external_server: true
      no_web_deploy_required: true
      no_auth_multiuser_scope: true
      offline_marking_required: true
    block_if:
      - ux_ui_gate_failed
      - tests_failed
      - build_requires_external_server
      - app_depends_on_internet_for_marking

  FASE_12_CONTROLLED_PILOT:
    phase_goal: "Executar piloto controlado somente se UI, persistência, exportação e recuperação forem utilizáveis por operador."
    pass_condition:
      - operador_usa_sem_desenvolvedor
      - eventos_salvos_recuperaveis
      - correcao_de_evento_funciona
      - exportacao_funciona
    block_if:
      - operador_nao_consegue_marcar_fluxo_basico
      - historico_nao_exibe_evento_salvo
      - dados_nao_persistem_apos_reabrir

  FASE_13_REAL_MATCH_USE:
    phase_goal: "Usar em jogo real somente como apoio confiável, sem atrapalhar a leitura da partida."
    pass_condition:
      - fluxo_rapido_validado
      - backup_pos_jogo_realizado
      - relatorio_exportado
      - coach_feedback_registrado
    block_if:
      - perda_critica_de_dados
      - operador_sem_backup
      - UI_atrapalha_marcacao
      - contrato_ativo_nao_confirmado
```

## 8. Política de evidências

```yaml
evidence_path_policy:
  text_evidence:
    path: docs/evidence/<cycle_id>/
    examples:
      - gate_failure_report.md
      - docs_conflict_report.md
      - pytest_report.txt
      - command_output.log

  ux_evidence:
    path: docs/ux/evidence/<cycle_id>/
    examples:
      - operator_walkthrough.md
      - operator_feedback.md
      - screenshots/
      - ux_measurement_report.md

  generated_runtime_data:
    path: storage/
    version_control: false
    examples:
      - local_database_files
      - videos
      - clips
      - generated_reports
      - binary_builds
```

## 9. Comandos mínimos por ciclo

```bash
scripts/verify_current_state.sh
python3 -m pytest -q
git diff --check
git status --short
PYTHONPATH=. python3 scripts/audit_docs_contract_alignment.py
```

Se a tarefa envolver UI, adicionar:

```bash
python3 -m pytest tests/test_ui_contract_registry.py -q
python3 -m pytest tests/test_tagging_ux_contract.py -q
python3 -m pytest tests/test_tagging_no_blocked_quick_buttons.py -q
```

Se a tarefa envolver planilha ou extração de matriz, adicionar:

```bash
PYTHONPATH=. python3 scripts/audit_scout_design_template.py docs/SCOUT_DESIGN_TEMPLATE.xlsx
PYTHONPATH=. python3 scripts/audit_scout_design_template_full_extraction.py \
  --chunks docs/SCOUT_DESIGN_TEMPLATE_FULL_EXTRACTION.json \
  --xlsx docs/SCOUT_DESIGN_TEMPLATE.xlsx \
  --full-extraction
```

## 10. Definition of Done do Plano Mestre

```yaml
master_definition_of_done:
  pass_if:
    - master_execution_order_existe
    - document_roles_definidos
    - validation_status_separado
    - module_effective_status_definido
    - source_id_policy_definida
    - execution_backlog_com_dependencias
    - fases_criticas_reescritas_com_UX_UI
    - evidence_path_policy_definida
  status: ready_for_repo_implementation
```

## 11. Prompt obrigatório para o agente

```markdown
Você é o agente de implementação do ScoutPraia.
Antes de agir, leia o Plano Mestre.
Não use o documento original como ordem de execução se ele conflitar com o Plano Mestre.
Classifique a validação como leitura, execução, operador humano ou jogo real.
Não implemente UI sem contrato UX UI.
Não renderize botão rápido fora do registry.
Não libere finalization_v1 enquanto o status efetivo estiver blocked_pending_reconciliation.
Não declare build, piloto ou uso real aprovado sem Gate UX UI e evidência.
Ao final, preencha o pacote de evidências do ciclo.
```

