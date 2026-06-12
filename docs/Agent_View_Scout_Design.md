---
doc_id: SCOUT_DESIGN_TEMPLATE_AGENT_VIEW
source_spreadsheet: SCOUT_DESIGN_TEMPLATE
source_spreadsheet_id: 1865ZgoC1t8H-acfeSxKirkgE5Ip8goE5ptFmRfi_QMs
status: agent_view_inicial
purpose: visão textual e legível por agentes da arquitetura definida na planilha
last_generated_from_drive: 2026-06-12
---

# SCOUT_DESIGN_TEMPLATE — visão textual para agentes

Este documento transforma as decisões críticas da planilha `SCOUT_DESIGN_TEMPLATE` em uma visão textual legível por agentes.

Ele existe porque a planilha é uma matriz humana de arquitetura. Agentes não devem depender do `.xlsx` binário como única fonte operacional. Agentes devem ler este documento em conjunto com os contratos executáveis e testes do repositório.

## Regra central

- `SCOUT_DESIGN_TEMPLATE.xlsx` é contrato humano de arquitetura e governança.
- Este documento é a visão textual derivada da planilha para agentes.
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

## Como agentes devem usar este documento

Agentes devem:

1. Ler este documento antes de alterar contratos, docs, UI, seed ou importação.
2. Confirmar o status do módulo na seção de módulos.
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

Esta é uma primeira visão textual consolidada das abas críticas. Ela não é exportação integral de todas as 60 abas. A próxima melhoria recomendada é criar um script para gerar/atualizar este documento automaticamente a partir da planilha e auditar drift entre ambos.

---

# Complemento obrigatório extraído da planilha

As seções abaixo completam a primeira versão do Agent View com informações críticas que estavam na planilha, mas ainda não estavam suficientemente explícitas para agentes.

## Mapa das abas críticas

O agente não precisa ler todas as 60 abas integralmente para cada tarefa, mas precisa entender o papel das abas críticas.

### Governança e navegação

- `ARCHITECTURE_README`: regra central da planilha, fonte humana de arquitetura e limites de uso.
- `MODULE_INDEX`: mapa mestre dos módulos, status, importação, UI, testes e política de uso pela IA.
- `SHEET_MAP`: mapa das abas, tipo de aba, escopo e dependências.
- `AI_USE_POLICY`: regras sobre o que a IA pode sugerir, importar, revisar ou bloquear.
- `VALIDATION_MATRIX`: relação entre módulo, teste, evidência, status e bloqueios.
- `SOURCE_REGISTER`: fontes fortes e escopo de uso.

### Contrato global

- `EVENTOS`: visão humana dos eventos, status, política de uso, campos e regras.
- `FIELD_DICTIONARY_GLOBAL`: dicionário global de campos reutilizáveis.
- `RESULT_DOMAIN_GLOBAL`: domínios de resultados por módulo/evento.
- `CROSS_MODULE_BOUNDARIES`: fronteiras entre módulos.
- `LEGACY_MIGRATION_RULES`: como tratar códigos antigos, futuros ou ambíguos.

### Normalização para auditoria

- `EVENT_REQUIRED_FIELDS`: campos obrigatórios normalizados por evento.
- `EVENT_OPTIONAL_FIELDS`: campos opcionais normalizados por evento.
- `EVENT_FORBIDDEN_FIELDS`: campos proibidos normalizados por evento.
- `EVENT_BLOCKING_RULES`: regras de bloqueio normalizadas por evento.

### Abas específicas por módulo

- `CAMPOS_AUXILIARES_*`: campos específicos do módulo.
- `RESULTADOS_*`: resultados permitidos do módulo.
- `TESTES_*`: casos de teste/aceitação do módulo.
- `VERSIONAMENTO_*`: histórico e versão do módulo.

Agentes devem priorizar abas globais antes de abas específicas. Quando houver conflito entre aba global e aba específica, o agente deve sinalizar conflito e exigir auditoria, não escolher sozinho.

## Dicionário global de campos críticos

Os campos abaixo devem ser reutilizados. Agentes não devem inventar nomes alternativos quando esses campos já existem.

| field_code | uso correto | módulo/escopo | risco se usado errado |
|---|---|---|---|
| `review_marker` | marca dúvida, incerteza, vídeo incompleto ou valor em revisão | global | não é evento técnico e não deve contar estatística |
| `athlete_id` | identifica atleta por ID | global | evitar nome livre em importação |
| `court_location` | zona da quadra | global | não usar texto livre quando houver zona padronizada |
| `goal_zone` | zona do gol | finalização, goleira, shoot-out | separar zona do arremesso e zona da defesa quando necessário |
| `position_code` | posição/função tática | global | não usar `specialist` como posição fixa |
| `system_code` | sistema tático | transição, defesa, criação | sistema de transição pode diferir do ataque posicionado |
| `result_possession` | resultado de ataque sem finalização | attack_no_shot_v1 | não usar em finalization_v1 |
| `result_shootout` | resultado do Shoot-out | shootout_v1 | não substituir por `goalkeeper_save` |
| `result_goalkeeper` | resultado da goleira | goalkeeper_v1 | não usar para Shoot-out |
| `result_transition` | resultado da transição | transition_v1 | não calcula pontos; exige evento ou estado terminal |
| `linked_finalization_id` | finalização vinculada | goalkeeper_v1; offensive_creation_v1 | evita defesa/criação sem evento terminal verificável |
| `linked_finalization_event_code` | código da finalização vinculada | goalkeeper_v1 | bloquear `shootout_attempt` como finalização vinculada da goleira |
| `terminal_event_id` | evento terminal da transição | transition_v1 | transição sem fechamento é inválida |
| `terminal_event_code` | código terminal da transição | transition_v1 | bloquear Shoot-out e eventos de goleira como terminal |
| `terminal_state` | estado terminal quando não há evento formal | transition_v1 | usar quando transição termina por estabilização/estado |
| `shootout_launcher_id` | passadora do Shoot-out | shootout_v1 | papel pode ser goleira ou jogadora de linha |
| `shootout_launcher_role` | papel da passadora | shootout_v1 | registrar papel, não posição fixa |
| `shootout_defender_id` | defensora do Shoot-out | shootout_v1 | não transformar automaticamente em `goalkeeper_id` |
| `shootout_defender_origin_role` | origem funcional da defensora | shootout_v1 | permite saber se era goleira dos sets sem misturar com goalkeeper_v1 |
| `goalkeeper_id` | goleira | goalkeeper_v1 | não usar para defensora de Shoot-out sem evento goalkeeper_v1 |
| `specialist_id` | especialista na troca goleira-especialista | goalkeeper_v1 | simultaneidade goleira-especialista pode gerar punição |
| `exchange_result` | resultado da troca goleira-especialista | goalkeeper_v1 | não converter automaticamente em `bad_substitution_attack` |
| `substitution_phase` | fase da substituição | transition_v1 | ofensiva e defensiva têm fases opostas |
| `substitution_timing` | tempo da troca | transition_v1 | antecipação é conceito central da transição |
| `transition_type` | tipo de transição | transition_v1 | precisa ser coerente com `result_transition` |
| `transition_system` | sistema na transição | transition_v1 | superioridade indireta deve explicitar 2x1, 3x2 ou 4x3 |
| `direct_lane_available` | caminho direto livre | transition_v1 | transição direta exige chance clara sem oposição relevante |
| `defensive_stabilization_status` | estabilização defensiva | transition_v1 | `defense_stabilized` encerra a transição |

## Papéis de pontuação (`scorer_role`)

`scorer_role` é obrigatório para derivar pontos corretamente em finalizações convertidas.

| scorer_role | significado | aplica-se a | regra |
|---|---|---|---|
| `field_player` | jogadora de linha comum no momento do arremesso | `simple_shot`; `spin_shot`; `inflight_shot`; `six_metre_throw` | `simple_shot+goal=1`; `spin/inflight/six_metre+goal=2`; sem gol = 0 |
| `specialist` | especialista/curinga no ataque no momento do arremesso | `simple_shot`; `spin_shot`; `inflight_shot`; `six_metre_throw` | `simple_shot+goal=2`; `spin/inflight/six_metre+goal=2`; sem gol = 0 |
| `goalkeeper` | goleira como finalizadora | `goalkeeper_shot` | `goalkeeper_shot+goal=2`; sem gol = 0 |

Regras obrigatórias:

- `specialist` é papel dinâmico, não posição fixa.
- `specialist` não pode ser `event_code`.
- `specialist` não pode ser `position_code`.
- `goalkeeper_shot` exige `scorer_role=goalkeeper`.

## Pontuação detalhada e combinações proibidas

Regras derivadas de `PONTUACAO_FINALIZACAO`:

| regra | decisão |
|---|---|
| `simple_shot + goal + field_player` | 1 ponto |
| `simple_shot + goal + specialist` | 2 pontos |
| `simple_shot + save/shot_wide/shot_blocked` | 0 pontos |
| `spin_shot + goal` | 2 pontos |
| `spin_shot + save/shot_wide/shot_blocked` | 0 pontos |
| `inflight_shot + goal` | 2 pontos |
| `inflight_shot + save/shot_wide/shot_blocked` | 0 pontos |
| `goalkeeper_shot + goal + goalkeeper` | 2 pontos |
| `goalkeeper_shot + save/shot_wide + goalkeeper` | 0 pontos |
| `goalkeeper_shot + shot_blocked` | combinação proibida/revisar na v1 |
| `six_metre_throw + goal` | 2 pontos |
| `six_metre_throw + save/shot_wide/rebound_live/execution_invalid_6m` | 0 pontos |
| `six_metre_throw + shot_blocked` | combinação proibida |

Regras de bloqueio:

- bloquear se `manual_points` divergir da regra derivada;
- bloquear `goalkeeper_shot` se `scorer_role != goalkeeper`;
- bloquear `six_metre_throw + shot_blocked`;
- bloquear `goalkeeper_shot + shot_blocked` na Finalização v1;
- se a goleira impede o gol no tiro de 6m, usar `save`; se rebate e o jogo segue vivo, usar `rebound_live`.

## Precedência de decisão em ataque sem finalização

Quando houver dúvida entre eventos de perda de posse sem finalização, aplicar esta ordem:

| prioridade | condição | evento preferido | excluir | revisão |
|---|---|---|---|---|
| 1 | decisão arbitral explícita de falta de ataque | `offensive_foul` | `technical_error_forced`; `technical_error_unforced` | marcar revisão se decisão arbitral não for visível/audível |
| 2 | entrada ilegal na área pela atacante | `goal_area_invasion_attack` | `technical_error_forced` | marcar revisão se houver dúvida entre área e outra perda |
| 3 | perda por jogo passivo | `passive_play_turnover` | `technical_error_unforced` | marcar revisão se sinalização/decisão não for clara |
| 4 | irregularidade de substituição durante posse ofensiva | `bad_substitution_attack` | `technical_error_unforced` | marcar revisão se subtipo for genérico |
| 5 | defesa causa erro sem controlar a bola | `technical_error_forced` | `technical_error_unforced` | marcar revisão se houver dúvida entre roubo/interceptação e erro forçado |
| 6 | falha técnica própria sem pressão defensiva clara | `technical_error_unforced` | `technical_error_forced` | sem revisão obrigatória |
| 7 | causa da perda não identificável | `turnover_unclassified` | todos os demais quando a causa é identificável | revisão obrigatória |

Regra de causa raiz: não usar `turnover_unclassified` por pressa. Ele é fallback de revisão.

## Campos obrigatórios/proibidos mínimos por módulo

Esta seção resume as abas normalizadas `EVENT_REQUIRED_FIELDS`, `EVENT_OPTIONAL_FIELDS`, `EVENT_FORBIDDEN_FIELDS` e `EVENT_BLOCKING_RULES`.

### finalization_v1

Obrigatórios típicos:

- `athlete_id`;
- `event_code`;
- `result_possession` ou campo de resultado equivalente da finalização;
- `scorer_role` quando houver possibilidade de pontuação diferenciada;
- `court_location` quando visível/exigido;
- `goal_zone` quando aplicável.

Proibidos/bloqueios críticos:

- `event_code=specialist_shot`;
- `position_code=specialist`;
- `manual_points` divergente de `points_policy_v1.py`;
- `goalkeeper_shot` sem `scorer_role=goalkeeper`;
- `six_metre_throw` sem decisão arbitral de 6m.

### attack_no_shot_v1

Obrigatórios típicos:

- `athlete_id` ou responsável pela ação quando identificável;
- `event_code`;
- `result_possession=lost_possession_no_shot`;
- `review_marker` quando a causa não for clara.

Proibidos/bloqueios críticos:

- não misturar com finalização;
- não atribuir pontos;
- não usar se houve arremesso com intenção clara de gol;
- `turnover_unclassified` exige revisão obrigatória.

### shootout_v1

Obrigatórios típicos:

- `shooter_id`;
- `shootout_launcher_id`;
- `shootout_launcher_role`;
- `shootout_defender_id`;
- `shootout_defender_role` ou origem funcional quando exigida;
- `result_shootout`;
- ordem/tentativa quando aplicável.

Proibidos/bloqueios críticos:

- não usar `goalkeeper_save` para defesa no Shoot-out;
- não criar `shootout_goal`, `shootout_miss`, `shootout_spin`, `shootout_inflight` como eventos separados;
- não usar `result_goalkeeper` no lugar de `result_shootout`;
- não usar Shoot-out como transição.

### goalkeeper_v1

Obrigatórios típicos:

- `goalkeeper_id`;
- `linked_finalization_id`;
- `linked_finalization_event_code`;
- `result_goalkeeper`;
- `goal_zone` quando aplicável.

Proibidos/bloqueios críticos:

- bloquear `goalkeeper_save` sem finalização vinculada;
- bloquear `goalkeeper_save` quando contexto for Shoot-out;
- bloquear `line_block_shot` para ação da goleira;
- não usar `goalkeeper_id` para defensora de Shoot-out sem evento de Goleira v1.

### transition_v1

Obrigatórios típicos:

- `transition_direction`;
- `substitution_phase`;
- `substitution_timing`;
- `transition_type`;
- `transition_trigger`;
- `result_transition`;
- `terminal_event_id` ou `terminal_state`.

Proibidos/bloqueios críticos:

- não calcular pontos em `transition_sequence`;
- bloquear `transition_goal` sem terminal de Finalização v1;
- bloquear `transition_turnover_no_shot` sem terminal de Ataque sem Finalização v1;
- bloquear `shootout_attempt` como terminal/gatilho de transição;
- bloquear eventos de Goleira v1 como terminal da transição.

## Fontes fortes e escopo de uso

O agente deve respeitar escopo de fonte:

| tipo de fonte | uso permitido | limite |
|---|---|---|
| IHF / regras oficiais | regras, pontuação, Shoot-out, 6m, substituição, critérios normativos | prevalece sobre interpretações práticas |
| CBHb/Federações | regulamento nacional/local, competição, documentos oficiais brasileiros | não substitui regra IHF quando a pergunta for regra internacional |
| EHF/IHF técnico | técnica, tática, treinamento, linguagem de jogo | não vira regra se conflitar com IHF |
| CEPRAEA / decisão operacional do treinador | nomenclatura interna, scout operacional, interpretação prática, transição por trocas | deve ser marcado como decisão prática, não regra oficial |
| NIST/OWASP/Data Carpentry | governança de IA, risco, planilha, auditoria, rastreabilidade | não define regra esportiva |
| `events_v1.py`, `points_policy_v1.py`, pytest e scripts | comportamento executável e validação | prevalecem para implementação do app |

Regra: fonte pode ser compartilhada entre ScoutPraia e RAG, mas função não pode ser confundida. RAG não decide lance automaticamente.

## Evidências e status de validação

Estados importantes para agentes:

| item | evidência/status | decisão |
|---|---|---|
| `shootout_v1` | EV-009 / teste conceitual | contrato validado, não importar |
| `goalkeeper_v1` | EV-010 / teste conceitual | contrato validado, não importar |
| `transition_v1` | EV-011 / teste conceitual | contrato validado, não importar |
| `points_policy_v1` | `tests/test_points_policy_v1.py` | contrato global de pontuação criado |
| `SCOUT_DESIGN_TEMPLATE` | auditor XLSX com `errors=0` | planilha auditável; warnings de proteção ainda podem existir |
| G5 | pendente | MVP completo não pode ser declarado |
| RAG/Chroma/embeddings | bloqueado | não implementar antes do gate |

Regras de aceitação:

- passar teste conceitual não libera UI;
- passar auditor da planilha não libera app;
- validar contrato não aprova G5;
- evento sem fonte, campo, teste e evidência não deve ser liberado;
- mudança que afeta coleta precisa de teste específico, pytest completo, `verify_current_state.sh`, `git diff --check` e registro de evidência.

## Requisitos mínimos de qualidade

Antes de implementar ou liberar qualquer regra/evento, verificar:

| atributo | critério |
|---|---|
| adequação funcional | o evento existe em contrato, planilha e/ou código conforme status |
| correção funcional | resultado e pontos são derivados, não digitados livremente |
| confiabilidade | campos obrigatórios vazios e campos proibidos preenchidos bloqueiam salvamento/importação |
| usabilidade | eventos principais são distinguíveis por nome e tipo de UI |
| manutenibilidade | listas controladas ficam em abas próprias ou contratos reutilizáveis |
| rastreabilidade | cada evento liga fonte, regra, campo, teste e evidência |
| testabilidade | toda regra crítica possui teste PASS/FAIL ou mínimo teste automatizado |

Regra final: evento sem rastreabilidade não pode ser liberado.

## O que não deve ser copiado integralmente para este documento

As seguintes abas devem continuar na planilha e serem consultadas apenas quando necessário:

- `POSIÇÕES`;
- `ZONAS_QUADRA`;
- `ZONAS_GOL`;
- `SISTEMAS`;
- `SUBTIPOS_*`;
- `TESTES_*` completos;
- `VERSIONAMENTO_*` completo;
- `CHECKLIST_AUDITORIA` completo.

Motivo: copiar tudo integralmente transformaria este documento em outra planilha gigante e aumentaria o risco de drift. Este Agent View deve conter decisões críticas para agentes, não todas as células da matriz humana.


