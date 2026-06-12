---
doc_id: SCOUT_DESIGN_TEMPLATE_AGENT_VIEW
source_spreadsheet: SCOUT_DESIGN_TEMPLATE
source_spreadsheet_id: 1865ZgoC1t8H-acfeSxKirkgE5Ip8goE5ptFmRfi_QMs
status: agente_view_inicial
purpose: visão textual e legível por agentes da arquitetura definida na planilha
last_generated_from_drive: 2026-06-12
must_not_replace:
  - scoutpraia/contracts/events_v1.py
  - scoutpraia/contracts/points_policy_v1.py
  - tests
  - scripts/audit_*.py
---

# SCOUT_DESIGN_TEMPLATE — visão textual para agentes

Este arquivo transforma as decisões críticas da planilha `SCOUT_DESIGN_TEMPLATE` em uma visão textual legível por agentes.

Ele existe porque a planilha `.xlsx` é uma matriz humana de arquitetura, mas não deve ser usada isoladamente como fonte operacional por agentes. Agentes devem ler este arquivo em conjunto com os contratos executáveis e testes.

## Regra central

- `SCOUT_DESIGN_TEMPLATE.xlsx` é contrato humano de arquitetura e governança.
- Este arquivo é a visão textual derivada da planilha para agentes.
- `events_v1.py` e `points_policy_v1.py` são fontes executáveis para comportamento do sistema.
- `Contrato_Operacional.md` registra histórico, evidências e decisões.
- `pytest`, `verify_current_state.sh` e scripts de auditoria são evidência executável.
- Nenhum módulo com `import_rule_v1=nao_importar_v1` pode ser liberado em UI/importação sem teste, evidência local, contrato atualizado e liberação explícita.

## Gate atual para agentes

Enquanto G5 não estiver aprovado:

- não migrar seed v0.1 para v1;
- não liberar UI de módulos v1 bloqueados;
- não importar módulos `nao_importar_v1`;
- não tratar a planilha como banco oficial de lances;
- não transformar contexto, campo auxiliar ou legado em botão principal;
- usar contratos v1 para raciocínio, auditoria e criação de testes, não como autorização automática de app.

## Vocabulário operacional v0.1 x contratos v1

### v0.1 operacional

- Usado pelo seed atual, banco atual, UI atual e MVP atual.
- Status global da taxonomia atual: `draft`.
- Não deve ser substituído automaticamente por v1 sem plano de migração, testes e alteração explícita no contrato.

### v1 contratos

- Usado por `events_v1.py`, `points_policy_v1.py`, planilha, testes conceituais e auditores.
- Pode orientar arquitetura, validação e correção de docs.
- Só entra em seed/UI/importação quando `import_rule_v1=importar_v1` e houver evidência executável.

## Prioridade de decisão para agentes

Quando houver conflito:

1. Contrato executável e testes vencem para comportamento do app.
2. Este Agent View vence para leitura textual da planilha por agentes.
3. `Contrato_Operacional.md` vence para histórico e evidência de decisão.
4. `SCOUT_DESIGN_TEMPLATE.xlsx` vence para edição humana da matriz, mas precisa ser refletido aqui para agentes.
5. Docs antigos como `taxonomy_dictionary.md` e `evidence_matrix.md` não devem reativar códigos legados quando divergirem dos contratos v1.

## Módulos

| module_id | eventos principais | status contrato | import_rule_v1 | UI | política para agente |
|---|---|---|---|---|---|
| finalization_v1 | simple_shot; spin_shot; inflight_shot; goalkeeper_shot; six_metre_throw | contrato_validado | nao_importar_v1 | nao_liberada | usar como contrato; não importar |
| attack_no_shot_v1 | technical_error_unforced; technical_error_forced; offensive_foul; goal_area_invasion_attack; passive_play_turnover; bad_substitution_attack; turnover_unclassified | contrato_validado | importar_v1 | liberada conforme app | pode usar e importar respeitando campos/regras |
| offensive_creation_v1 | assist_to_finalization | contrato_validado | nao_importar_v1 | nao_liberada | usar como contrato; não importar |
| defensive_v1 | line_block_shot | contrato_validado | nao_importar_v1 | nao_liberada | usar como contrato; não importar |
| shootout_v1 | shootout_attempt | arquitetura_em_definicao_validada_por_teste_conceitual | nao_importar_v1 | nao_liberada | usar como contrato; não importar |
| goalkeeper_v1 | goalkeeper_save; goalkeeper_goal_allowed; goalkeeper_specialist_exchange | arquitetura_em_definicao_validada_por_teste_conceitual | nao_importar_v1 | nao_liberada | usar como contrato; não importar |
| transition_v1 | transition_sequence | arquitetura_em_definicao_validada_por_teste_conceitual | nao_importar_v1 | nao_liberada | usar como contrato; não importar |

## Regra global de pontuação

A pontuação não deve ser digitada livremente nem inferida por rótulo visual. A pontuação deve ser derivada por `points_policy_v1.py`.

Regras críticas:

- `specialist` não é `event_code` nem `position_code`; é `scorer_role`.
- `specialist_shot` é código proibido.
- `simple_shot + goal + scorer_role=field_player` deriva 1 ponto.
- `simple_shot + goal + scorer_role=specialist` deriva 2 pontos.
- `spin_shot + goal` deriva 2 pontos.
- `inflight_shot + goal` deriva 2 pontos.
- `goalkeeper_shot + goal + scorer_role=goalkeeper` deriva 2 pontos.
- `six_metre_throw + goal` deriva 2 pontos.
- `shootout_attempt + goal` deriva 2 pontos.
- resultados sem gol ou perda sem finalização derivam 0 quando permitidos.
- `manual_points` divergente da pontuação derivada deve ser bloqueado.

## Eventos principais e decisões críticas

### finalization_v1

#### simple_shot

- Arremesso comum com intenção clara de gol.
- Pode valer 1 ou 2 conforme `scorer_role`.
- Se `scorer_role=field_player` e resultado `goal`, pontos = 1.
- Se `scorer_role=specialist` e resultado `goal`, pontos = 2.
- Proibido criar `specialist_shot`.
- Proibido usar `position_code=specialist`.

#### spin_shot

- Finalização com giro completo e intenção clara de gol.
- Gol vale 2 pontos.
- Sem gol vale 0.
- Não usar para finta com giro sem arremesso.

#### inflight_shot

- Finalização de aérea: recebe e arremessa no ar antes de tocar o solo.
- Gol vale 2 pontos.
- Assistência é campo auxiliar ou vínculo, não evento duplicado.

#### specialist_finish_role

- Campo auxiliar, não botão principal.
- Indica que a finalizadora atuava como especialista.
- Deve ser registrado como `scorer_role=specialist` junto do tipo técnico real: `simple_shot`, `spin_shot` ou `inflight_shot`.
- Não usar `specialist_shot` como evento.
- Não usar `specialist` como posição fixa.

#### goalkeeper_shot

- Finalização da goleira em jogo normal/transição.
- Exige `scorer_role=goalkeeper`.
- Gol vale 2 pontos.
- Não confundir passe longo da goleira com finalização da goleira.

#### six_metre_throw

- Tiro de 6m marcado pela arbitragem.
- Gol vale 2 pontos.
- Não confundir arremesso perto da área com tiro de 6m se não houver decisão arbitral.

### shootout_v1

#### shootout_attempt

- Tentativa completa de Shoot-out.
- Shoot-out é módulo próprio, não Finalização v1 e não Goleira v1.
- Registrar uma tentativa completa com campos auxiliares.
- Não criar `shootout_goal`, `shootout_miss`, `shootout_spin`, `shootout_inflight` ou `shootout_interception` como eventos separados.
- Defesa no Shoot-out deve ser `shootout_attempt + result_shootout=save`, não `goalkeeper_save`.
- Se houver falta defensiva impeditiva, `result_shootout=defender_foul_6m_awarded` e o próximo evento deve ser `six_metre_throw`.

### goalkeeper_v1

#### goalkeeper_save

- Defesa da goleira no set/jogo normal ou tiro de 6m.
- Exige `linked_finalization_id` e `linked_finalization_event_code`.
- Não usar para Shoot-out.
- Não usar para bloqueio de jogadora de linha.
- Defesa que sai pela linha de fundo mantém posse da equipe da goleira.
- Defesa que sai pela lateral mantém posse da equipe adversária.

#### goalkeeper_goal_allowed

- Gol sofrido pela goleira vinculado a finalização adversária válida.
- Usado para eficiência real da goleira.
- Não usar para gol no Shoot-out.

#### goalkeeper_specialist_exchange

- Ciclo de troca goleira-especialista.
- Ações da goleira começam quando especialista sai para ela entrar e terminam quando goleira sai para especialista entrar.
- Goleira e especialista juntas em quadra configuram risco/violação e exigem revisão/punição quando aplicável.

### transition_v1

#### transition_sequence

- Transição no beach handball é baseada principalmente em trocas pela zona de substituição.
- Transição ofensiva: defensoras saem e atacantes entram para criar transição direta ou superioridade indireta.
- Transição defensiva: atacantes saem e defensoras entram para neutralizar transição adversária.
- Antecipação ocorre quando jogadora que não participa do lance sai antes da conclusão para permitir entrada com vantagem.
- Transição não calcula pontos; pontos vêm do evento terminal de finalização.
- `transition_goal` exige terminal de Finalização v1.
- `transition_turnover_no_shot` exige terminal de Ataque sem Finalização v1.
- Shoot-out não é transição.

## Fronteiras entre módulos

- Shoot-out não é Goleira v1: defesa no Shoot-out fica em `shootout_attempt + result_shootout=save`, não em `goalkeeper_save`.
- Goleira v1 deve vincular finalização válida: `goalkeeper_save` e `goalkeeper_goal_allowed` exigem `linked_finalization_id`.
- Defensivo v1 não é Goleira v1: `line_block_shot` é ação de linha; `goalkeeper_save` é ação da goleira.
- Transição v1 não substitui Finalização v1: gol em transição precisa de terminal de finalização.
- Transição v1 não substitui Ataque sem Finalização: perda em transição precisa de terminal de perda sem finalização quando a causa for identificável.
- Goleira pode ser gatilho de transição, mas não terminal de `transition_sequence`.
- Shoot-out fica fora de `transition_sequence`.
- Criação ofensiva cria finalização, mas não calcula pontos.
- Finalização v1 e Ataque sem Finalização v1 são mutuamente exclusivos na posse: arremesso x perda sem arremesso.

## Política de uso pela IA

- `usar_e_importar`: pode usar na coleta/importação respeitando campos e regras.
- `usar_e_importar_com_revisao`: pode usar com revisão obrigatória.
- `usar_como_contrato_nao_importar`: pode usar para raciocinar, auditar e criar testes; não importar nem expor no app.
- `usar_como_auxiliar_nao_importar`: usar como campo/atributo; nunca como evento principal.
- `usar_somente_revisao_nao_importar`: usar apenas em análise/auditoria; exigir `review_marker`.
- `nao_usar_legado_futuro`: não usar em nova coleta; mapear para evento atual ou revisão.
- Se houver conflito entre `EVENTOS` e aba específica, o agente não deve decidir sozinho; deve sinalizar conflito e exigir auditoria.

## Migração e bloqueio de legados

| legado | regra atual |
|---|---|
| save | migrar para `goalkeeper_save` somente com finalização vinculada; bloquear se contexto for Shoot-out |
| save_shootout | migrar para `shootout_attempt + result_shootout=save`; nunca `goalkeeper_save` |
| goal_conceded | migrar para `goalkeeper_goal_allowed` quando houver goleira e finalização vinculada |
| empty_goal_conceded | contexto/revisão de Goleira ou Transição; não virar botão primário |
| fast_break_against | contexto/direção de `transition_sequence`, não evento primário |
| transition_recovery_good | resultado de neutralização defensiva em `transition_sequence` |
| transition_recovery_bad | falha da transição ou terminal vinculado em `transition_sequence` |
| specialist_shot | migrar para tipo técnico real de finalização + `scorer_role=specialist` |
| timeout; set_end; match_end | contexto de partida; não evento técnico v1 |
| golden_goal | contexto; o gol continua sendo finalização terminal |

## Domínios de resultado críticos

### finalization_v1

- `goal`: terminal de gol; pontos derivados pela política de pontuação.
- `save`: defesa adversária; pode vincular Goleira v1 quando aplicável.
- `shot_wide`: arremesso para fora.
- `shot_blocked`: permitido para `simple_shot`, `spin_shot`, `inflight_shot`; pode vincular `line_block_shot`; não usar para `goalkeeper_shot` nem `six_metre_throw` na v1.

### attack_no_shot_v1

- `lost_possession_no_shot`: perda sem finalização; terminal de ataque sem arremesso; não misturar com finalização.

### goalkeeper_v1

- `save_controlled`: defesa controlada.
- `save_out_endline`: defesa sai pela linha de fundo; posse da equipe da goleira.
- `save_out_sideline`: defesa sai pela lateral; posse da adversária.
- `goal_allowed`: gol sofrido vinculado a finalização.
- `exchange_successful`: troca goleira-especialista correta.
- `overlap_violation`: sobreposição goleira-especialista; exige revisão/punição quando aplicável.

### transition_v1

- `transition_goal`: exige evento terminal de Finalização v1.
- `direct_transition_chance`: chance direta criada.
- `indirect_superiority_created`: superioridade indireta criada.
- `direct_transition_neutralized`: transição direta neutralizada.
- `indirect_transition_neutralized`: transição indireta neutralizada.
- `transition_slowed_to_set`: transição desacelera para ataque posicionado e defesa estabiliza.

### shootout_v1

- `goal`: gol no Shoot-out.
- `save`: defesa no Shoot-out; não contaminar `goalkeeper_save`.

## Regras de bloqueio prioritárias

- Bloquear `event_code=specialist_shot`.
- Bloquear `position_code=specialist`.
- Bloquear pontos manuais divergentes de `points_policy_v1.py`.
- Bloquear `goalkeeper_save` sem finalização vinculada.
- Bloquear `goalkeeper_save` quando o contexto for Shoot-out.
- Bloquear `line_block_shot` para ações da goleira.
- Bloquear `transition_goal` sem terminal de Finalização v1.
- Bloquear `transition_sequence` terminal com `goalkeeper_save`, `goalkeeper_goal_allowed` ou `goalkeeper_specialist_exchange`.
- Bloquear `shootout_attempt` como terminal ou gatilho de transição.
- Bloquear qualquer evento legado/futuro com `usable_by_ai=nao_usar_legado_futuro` em nova coleta.

## Como agentes devem usar este arquivo

Agentes devem:

1. Ler este arquivo antes de alterar contratos, docs, UI, seed ou importação.
2. Confirmar o status do módulo no `MODULE_INDEX`/seção de módulos acima.
3. Verificar se o módulo está `importar_v1` ou `nao_importar_v1`.
4. Usar `points_policy_v1.py` para pontuação.
5. Usar `events_v1.py` para registry executável.
6. Usar scripts de auditoria para validar mudanças.
7. Nunca implementar decisão baseada apenas em docs antigos quando houver conflito com este Agent View ou contratos executáveis.

## Comandos de validação relacionados

```bash
python3 -m pytest tests/test_points_policy_v1.py -q
python3 -m pytest tests/test_docs_contract_alignment_audit.py -q
PYTHONPATH=. python3 scripts/audit_docs_contract_alignment.py
PYTHONPATH=. python3 scripts/audit_scout_design_template.py docs/SCOUT_DESIGN_TEMPLATE.xlsx
python3 -m pytest -q
scripts/verify_current_state.sh
git diff --check
git status -sb
```

## Limite desta versão

Esta é uma primeira visão textual consolidada das abas críticas. Ela não é exportação integral de todas as 60 abas. A próxima melhoria recomendada é criar um script para gerar/atualizar este arquivo automaticamente a partir do XLSX e auditar drift entre ambos.
