# Plano de Implementação Técnica — Ataque sem Finalização v1.0

Status: `aprovado_para_implementacao`

Este plano implementa somente o módulo **Ataque sem Finalização v1.0**, conforme `Contrato_Operacional.md` e `SCOUT_DESIGN_TEMPLATE`.

## Escopo

Implementar os sete eventos aprovados do módulo:

- `technical_error_unforced`
- `technical_error_forced`
- `offensive_foul`
- `goal_area_invasion_attack`
- `passive_play_turnover`
- `bad_substitution_attack`
- `turnover_unclassified`

## Fora de escopo

Não implementar nesta fase:

- finalizações;
- goleira;
- defesa;
- transição;
- shoot-out;
- golden goal;
- relatórios gerais;
- dashboard completo;
- RAG;
- API pública;
- multiusuário.

## Entrega técnica

- Criar contrato operacional de domínio em Python.
- Criar validação PASS/FAIL dos campos obrigatórios.
- Derivar `result_possession_auto = lost_possession_no_shot`.
- Garantir `points = 0`.
- Bloquear campos proibidos do módulo.
- Implementar `review_marker` obrigatório nas condições aprovadas.
- Implementar cálculo de consistência intraobservador para `TESTE-OBS-01`.

## Critérios PASS/FAIL

- Todos os eventos derivam `result_possession_auto = lost_possession_no_shot`.
- Todos os eventos têm `points = 0`.
- `technical_error_unforced` e `technical_error_forced` exigem `technical_error_subtype`.
- `passive_play_turnover` exige `passive_play_subtype` e `system_code`.
- `bad_substitution_attack` exige `substitution_error_subtype` e `system_code`.
- `substitution_violation_other` exige `review_marker`.
- `turnover_unclassified` exige `review_marker`.
- Evento fora do módulo é bloqueado.
- `finish_type_code`, `goal_zone` e pontos diferentes de zero são bloqueados.
- `TESTE-OBS-01` aprova consistência intraobservador maior ou igual a 85%.
- `TESTE-OBS-01` reprova consistência abaixo de 85%.

## Comandos de validação esperados

```bash
python3 -m pytest tests/test_attack_no_shot_contract.py -q
python3 -m pytest -q
scripts/verify_current_state.sh
```

## Status desta entrega

`PARCIAL` até a execução de `scripts/verify_current_state.sh` no ambiente local do repositório.
