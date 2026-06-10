---
tipo: plano_implementação_eventos_v1
status_geral: IMPLEMENTADO_COM_EVIDÊNCIA
import_rule_v1: nao_importar_v1
lote_1_contrato: CONCLUÍDO
lote_2_finalização: CONCLUÍDO
lote_3_ataque_sem_finalização: CONCLUÍDO
lote_4_modelo_banco: CONCLUÍDO
lote_5_ui_marcação: CONCLUÍDO
lote_6_relatórios_kpis: CONCLUÍDO
próxima_ação: "Aguardar G5; não alterar import_rule_v1 antes de G5 aprovado"
última_atualização: 2026-06-10
---

# Plano de implementação — Eventos v1

## RESTRIÇÕES CRÍTICAS (MUST NOT para agentes)

```
MUST NOT: alterar import_rule_v1 para importar_eventos_v1 sem todos os testes passando
MUST NOT: misturar eventos de Ataque sem finalização com Finalização
MUST NOT: misturar transição ofensiva com Ataque sem finalização
MUST NOT: criar specialist_shot como evento separado
MUST NOT: criar position_code=specialist
MUST NOT: permitir pontos manuais para Finalização v1.0
MUST NOT: liberar six_metre_throw + shot_blocked
MUST NOT: liberar goalkeeper_shot + shot_blocked na v1.0
MUST NOT: mover shootout_attempt para Finalização v1.0
MUST: rodar python3 -m pytest antes de cada mudança de status
MUST: rodar scripts/verify_current_state.sh após cada mudança relevante
```

## Status de implementação atual

Todos os lotes foram concluídos. `import_rule_v1` permanece `nao_importar_v1` até G5 aprovado.

| Lote | Descrição | Status |
| --- | --- | --- |
| Lote 1 | Contrato no código (`events_v1.py`) | CONCLUÍDO |
| Lote 2 | Serviço de Finalização | CONCLUÍDO |
| Lote 3 | Serviço de Ataque sem finalização | CONCLUÍDO |
| Lote 4 | Modelo/banco (campos v1 em `event.py`) | CONCLUÍDO |
| Lote 5 | UI de marcação (blocos v1 em `tagging.py`) | CONCLUÍDO |
| Lote 6 | Relatórios/KPIs (analytics + templates) | CONCLUÍDO |

---

Este plano orienta a implementação conjunta dos módulos já contratados para o ScoutPraia:

- Ataque sem finalização v1.0
- Finalização v1.0

O objetivo é levar os contratos validados da planilha/Contrato_Operacional para o app real sem misturar conceitos, sem ativar importação antes dos testes e sem quebrar o scout incompleto já existente.

## Estado atual

### Contratos prontos

- Ataque sem finalização v1.0: módulo de eventos em que o ataque termina sem arremesso e gera perda/troca de posse.
- Finalização v1.0: módulo de eventos em que há arremesso com intenção clara de gol.

### Finalização v1.0

Status na planilha:

```text
module_contract_status = contrato_validado
import_rule_v1 = nao_importar_v1
EV-006 = passed
```

Eventos principais:

- `simple_shot`
- `spin_shot`
- `inflight_shot`
- `goalkeeper_shot`
- `six_metre_throw`

Evento auxiliar preservado:

- `specialist_finish_role` — campo/função auxiliar, não botão principal.

### Regra crítica da Finalização

A pontuação deve ser derivada. O app não deve permitir escolha manual de pontos para Finalização v1.0.

Exemplos:

```text
simple_shot + goal + scorer_role=field_player = 1
simple_shot + goal + scorer_role=specialist = 2
spin_shot + goal = 2
inflight_shot + goal = 2
goalkeeper_shot + goal = 2
six_metre_throw + goal = 2
não gol = 0
```

## Diagnóstico do app atual

### 1. O modelo Event ainda é genérico

Atualmente o modelo `Event` tem campos como:

- `event_type`
- `event_subtype`
- `outcome`
- `zone`
- `points_value`
- `notes`

Ele ainda não possui campos explícitos para:

- `scorer_role`
- `result_possession`
- `shot_origin_depth`
- `court_lane`
- `goal_zone`
- `trajectory_visible`
- `derived_points`
- `manual_points`
- `review_marker`

Decisão: não adicionar todos os campos de uma vez sem plano de migração. Primeiro criar uma camada de contrato/serviço capaz de validar e derivar os dados, depois decidir migração de banco.

### 2. A tela de marcação ainda usa pontos manuais

A tela de marcação atual exibe `Pontos` como selectbox com valores `[0, 1, 2]`.

Para Finalização v1.0, isso conflita com o contrato, pois `points_value` deve ser derivado pela combinação:

```text
event_code + result_possession + scorer_role
```

Decisão: na implementação da Finalização, remover ou bloquear escolha manual de pontos para eventos do contrato v1 e exibir apenas o valor calculado.

### 3. O serviço de evento ainda valida pontuação pela taxonomia antiga

O serviço atual usa listas como `SCORING_EVENTS` e `TWO_POINT_ONLY_EVENTS`. Isso não cobre a modelagem nova, porque `simple_shot` pode valer 1 ou 2 dependendo de `scorer_role`.

Decisão: criar serviço específico de contrato para os módulos v1 antes de alterar o comportamento global de `event_service.py`.

### 4. A taxonomia seed ainda tem eventos antigos

A taxonomia atual tem eventos como:

- `shot_attempt`
- `goal_scored`
- `shot_missed`
- `two_point_goal`
- `spin_shot`
- `inflight_attempt`
- `inflight_goal`

Decisão: não substituir a taxonomia antiga diretamente. Criar camada `event_contracts_v1` e importar eventos v1 somente quando `import_rule_v1` for liberado.

## Arquitetura recomendada de implementação

### Fase 1 — Criar camada de contrato no código

Criar arquivo:

```text
scoutpraia/contracts/events_v1.py
```

Responsabilidade:

- declarar eventos validados de Ataque sem finalização v1.0;
- declarar eventos validados de Finalização v1.0;
- declarar quais eventos continuam bloqueados por `import_rule_v1 = nao_importar_v1`;
- declarar botões principais e campos auxiliares;
- impedir `specialist_finish_role` como botão;
- impedir `shootout_attempt` dentro da Finalização v1.0.

Não deve alterar o app ainda.

Testes da fase 1:

```text
tests/test_events_v1_contract_registry.py
```

Validações:

- eventos principais existem;
- auxiliares não aparecem como botão;
- `import_rule_v1` continua bloqueado;
- Ataque sem finalização e Finalização não compartilham resultados proibidos.

### Fase 2 — Criar serviço de pontuação e resultado da Finalização

Criar arquivo:

```text
scoutpraia/services/finalization_contract_service.py
```

Responsabilidade:

- validar `event_code + result_possession` pela matriz de resultados;
- derivar `points_value` pela tabela de pontuação;
- bloquear `manual_points` divergente;
- bloquear `specialist_shot`;
- bloquear `position_code=specialist`;
- bloquear `lost_possession_no_shot` em Finalização;
- bloquear `six_metre_throw + shot_blocked`;
- bloquear `goalkeeper_shot + shot_blocked`.

Testes da fase 2:

```text
tests/test_finalization_contract_service.py
```

Casos obrigatórios:

- `simple_shot + goal + field_player = 1`;
- `simple_shot + goal + specialist = 2`;
- `simple_shot + save + specialist = 0`;
- `six_metre_throw + rebound_live = 0`;
- `six_metre_throw + shot_blocked` bloqueia;
- `goalkeeper_shot + shot_blocked` bloqueia;
- `manual_points` divergente bloqueia.

### Fase 3 — Criar serviço de Ataque sem finalização

Criar arquivo:

```text
scoutpraia/services/no_shot_attack_contract_service.py
```

Responsabilidade:

- aceitar somente eventos em que a posse termina sem arremesso;
- exigir troca/perda de posse quando aplicável;
- impedir finalizações dentro do módulo;
- impedir transição ofensiva como evento de Ataque sem finalização;
- validar jogo passivo apenas nos subtipos aprovados;
- validar erro de troca somente quando ocorre com a equipe em posse de bola e gera perda da posse.

Testes da fase 3:

```text
tests/test_no_shot_attack_contract_service.py
```

Casos obrigatórios:

- invasão de área não é erro forçado;
- especialista atrasada não é causa direta de turnover;
- erro de troca só entra se a equipe está com posse e perde a posse;
- jogo passivo apenas nos subtipos aprovados;
- finalização não entra em Ataque sem finalização.

### Fase 4 — Adaptar o banco de dados de forma controlada

A modelagem nova precisa de campos que o modelo `Event` ainda não tem.

Opções:

#### Opção A — Campo JSON auxiliar

Adicionar um campo `metadata_json` ou `context_json` ao evento.

Vantagem: menos migração inicial.

Risco: validação fica menos rígida no banco.

#### Opção B — Campos explícitos

Adicionar campos formais ao modelo `Event`, como:

- `result_possession`
- `scorer_role`
- `court_lane`
- `shot_origin_depth`
- `goal_zone`
- `trajectory_visible`
- `derived_points`
- `review_marker`

Vantagem: banco mais claro e relatórios mais fáceis.

Risco: migração maior.

Decisão recomendada: usar campos explícitos para os campos estáveis de v1 e reservar `notes`/campo auxiliar apenas para observações humanas.

Teste obrigatório:

```text
tests/test_event_model_v1_fields.py
```

### Fase 5 — Adaptar a tela de marcação

Arquivo principal:

```text
scoutpraia/pages/tagging.py
```

Mudanças necessárias:

- separar grupos de botões por módulo;
- mostrar Ataque sem finalização e Finalização como blocos distintos;
- não mostrar `specialist_finish_role` como botão;
- não mostrar `shootout_attempt` dentro de Finalização v1.0;
- substituir pontos manuais por pontos calculados nos eventos de Finalização;
- exibir `scorer_role` como campo auxiliar;
- exibir `result_possession` com opções filtradas por evento;
- exibir `shot_origin_depth` e `court_lane` em finalizações de jogo corrido;
- permitir `six_metre_throw` com resultados específicos: `goal`, `save`, `shot_wide`, `rebound_live`, `execution_invalid_6m`.

Testes obrigatórios:

```text
tests/test_tagging_finalization_v1_ui.py
tests/test_tagging_no_shot_attack_v1_ui.py
```

### Fase 6 — Integrar com relatórios e KPIs

Após a marcação salvar corretamente, ajustar relatórios.

Relatórios mínimos:

- total de posses sem finalização;
- causas de perda de posse sem finalização;
- total de finalizações;
- aproveitamento por tipo de finalização;
- pontos por tipo técnico;
- pontos por `scorer_role`;
- arremessos de especialista;
- tiros de 6m: gol, defesa, fora, rebote vivo, execução inválida.

Testes obrigatórios:

```text
tests/test_reports_events_v1.py
```

## Ordem de implementação recomendada

Não implementar tudo de uma vez.

### Lote 1 — Registro de contrato no código

Arquivos:

- `scoutpraia/contracts/events_v1.py`
- `tests/test_events_v1_contract_registry.py`

Objetivo:

- reproduzir o contrato validado no código sem mexer na UI.

Critério de aceite:

```bash
python3 -m pytest tests/test_finalization_contract.py tests/test_events_v1_contract_registry.py -q
```

### Lote 2 — Serviço de Finalização

Arquivos:

- `scoutpraia/services/finalization_contract_service.py`
- `tests/test_finalization_contract_service.py`

Objetivo:

- tirar a lógica do teste autocontido e colocá-la em serviço real.

Critério de aceite:

```bash
python3 -m pytest tests/test_finalization_contract.py tests/test_finalization_contract_service.py -q
```

### Lote 3 — Serviço de Ataque sem finalização

Arquivos:

- `scoutpraia/services/no_shot_attack_contract_service.py`
- `tests/test_no_shot_attack_contract_service.py`

Objetivo:

- validar perdas de posse sem finalização e impedir mistura com finalizações/transição.

### Lote 4 — Modelo/banco

Arquivos:

- `scoutpraia/models/event.py`
- migração ou adaptação de criação de tabelas
- testes de modelo

Objetivo:

- persistir os campos necessários ao contrato.

### Lote 5 — UI de marcação

Arquivos:

- `scoutpraia/pages/tagging.py`
- testes Streamlit específicos

Objetivo:

- usuário consegue marcar os eventos v1 respeitando os bloqueios.

### Lote 6 — Relatórios/KPIs

Arquivos:

- serviços de relatório
- testes de relatório

Objetivo:

- transformar eventos marcados em análise útil.

## Regras de segurança

1. Não alterar `import_rule_v1` para importável antes de teste de implementação passar.
2. Não misturar Ataque sem finalização com Finalização.
3. Não misturar transição ofensiva com Ataque sem finalização.
4. Não recriar `specialist_shot` como evento.
5. Não criar `position_code=specialist`.
6. Não permitir pontos manuais para Finalização v1.0.
7. Não liberar `six_metre_throw + shot_blocked`.
8. Não liberar `goalkeeper_shot + shot_blocked` na v1.0.
9. Não mover `shootout_attempt` para Finalização v1.0.
10. Rodar testes antes de cada mudança de status.

## Critério para liberar no app

A liberação só deve acontecer quando os seguintes comandos passarem:

```bash
python3 -m pytest
scripts/verify_current_state.sh
```

E quando houver evidência registrada para:

- contrato v1 carregado no código;
- serviço de Finalização aprovado;
- serviço de Ataque sem finalização aprovado;
- UI de marcação aprovada;
- modelo/banco aprovado;
- relatórios mínimos aprovados.

Somente depois disso os eventos podem mudar de:

```text
import_rule_v1 = nao_importar_v1
```

para uma regra explícita de importação, como:

```text
import_rule_v1 = importar_eventos_v1
```