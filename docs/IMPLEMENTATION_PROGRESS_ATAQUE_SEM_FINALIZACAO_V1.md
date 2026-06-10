# Progresso — Ataque sem Finalização v1.0

Data: 2026-06-09
Status: `PARCIAL`

## O que foi implementado

- `scoutpraia/services/attack_no_shot_contract.py`
- `tests/test_attack_no_shot_contract.py`
- `docs/Plano_Implementacao_Tecnica_Ataque_Sem_Finalizacao_v1_0.md`

## Escopo implementado

Somente o módulo **Ataque sem Finalização v1.0**, com os eventos:

- `technical_error_unforced`
- `technical_error_forced`
- `offensive_foul`
- `goal_area_invasion_attack`
- `passive_play_turnover`
- `bad_substitution_attack`
- `turnover_unclassified`

## Testes criados

- resultado automático `lost_possession_no_shot` para todos os eventos;
- pontos sempre `0`;
- bloqueio de evento fora do módulo;
- bloqueio de `finish_type_code`;
- bloqueio de `goal_zone`;
- bloqueio de pontos diferentes de zero;
- subtipo técnico obrigatório para erros técnicos;
- subtipo de passivo obrigatório;
- subtipo de substituição obrigatório;
- `review_marker` obrigatório para `turnover_unclassified`;
- `review_marker` obrigatório para `substitution_violation_other`;
- derivação de `defense_forced_error` para `technical_error_forced`;
- `TESTE-OBS-01` de consistência intraobservador.

## Prova executada neste ciclo

A execução completa de `scripts/verify_current_state.sh` não foi rodada neste ambiente via GitHub connector.

Validação parcial realizada:

- leitura da estrutura do repositório correto `Davisermenho/scoutpraia`;
- criação dos arquivos no branch correto;
- verificação sintática local isolada do módulo Python por `py_compile` em ambiente sandbox.

## Comandos obrigatórios para concluir a validação

Rodar na raiz do repositório local:

```bash
python3 -m pytest tests/test_attack_no_shot_contract.py -q
python3 -m pytest -q
scripts/verify_current_state.sh
```

## Pendências reais

- Rodar os testes no ambiente local do repositório.
- Rodar `scripts/verify_current_state.sh`.
- Atualizar `docs/IMPLEMENTATION_PROGRESS.md` principal após a execução reproduzível local.
- Só mudar o status de `PARCIAL` para `FUNCIONANDO COM EVIDÊNCIA` depois dos comandos passarem.
