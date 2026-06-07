# Protocolo de Validação do ScoutPraia

Objetivo: transformar a taxonomia em instrumento observacional confiável antes de usar KPIs como referência estável.

## Escopo inicial

Validar `ScoutPraia v0.1` com 1 jogo completo em vídeo.

## Procedimento

1. Marcar o jogo completo usando a taxonomia `ScoutPraia v0.1`.
2. Exportar os eventos marcados.
3. Após pelo menos 24 horas, remarcar uma amostra do mesmo jogo.
4. Se houver outro analista disponível, pedir marcação independente da mesma amostra.
5. Comparar divergências por evento, atleta, zona e valor em pontos.
6. Ajustar definições operacionais ambíguas.
7. Gerar `ScoutPraia v0.2`.
8. Repetir a validação nos campos alterados.
9. Congelar `ScoutPraia v1.0` quando os campos centrais estiverem estáveis.

## Amostra mínima recomendada

- 5 posses de ataque posicionado
- 5 transições ofensivas
- 5 transições defensivas
- 5 finalizações de 2 pontos
- 5 erros técnicos
- 5 ações defensivas
- 5 shoot-outs, se houver no jogo

## Critérios de aprovação

| Critério | Aprovação prática |
| --- | --- |
| clareza | o evento é entendido sem explicação adicional |
| rapidez | o evento pode ser marcado durante revisão de vídeo sem travar o fluxo |
| consistência | remarcação gera resultado semelhante |
| utilidade | o KPI ajuda decisão de treino, jogo ou feedback individual |
| aderência à regra | não contradiz regra oficial |
| especificidade | respeita beach handball, sem importar lógica de quadra sem ajuste |

## Saída da validação

Cada divergência deve gerar uma decisão:

- manter evento
- ajustar definição
- fundir com outro evento
- dividir em subtipos
- remover do MVP
- manter como hipótese prática fora do KPI final

---

## Protocolo operacional repetível para validação humana

Objetivo: executar um ensaio humano reproduzível do fluxo crítico do MVP no navegador real, cobrindo `Marcação` e `Relatórios` com vídeo local verdadeiro.

### Quando usar

Usar este protocolo sempre que houver uma destas condições:

- mudança relevante na página `Marcação`
- mudança relevante na página `Relatórios`
- mudança em `event_service.py`, `analytics_service.py` ou `report_service.py`
- revisão antes de declarar o MVP operacionalmente utilizável

### Pré-requisitos

1. A raiz do repositório está limpa ou com mudanças intencionais conhecidas.
2. `scripts/verify_current_state.sh` passa antes do ensaio.
3. Existe ao menos 1 vídeo real em `storage/videos/`.
4. Existe 1 jogo cadastrado com vídeo associado ou o operador irá cadastrá-lo no início do ensaio.
5. O operador conhece a taxonomia usada e aceita que a versão `draft` não prova KPI final estável.

### Preparação obrigatória

Rodar:

```bash
scripts/verify_current_state.sh
scripts/run_scout.sh --port 8516
```

Abrir no navegador local:

```text
http://localhost:8516
```

Se preferir não abrir o navegador automaticamente:

```bash
scripts/run_scout.sh --port 8516 --no-browser
```

Registrar antes de começar:

- data e hora
- `git_head`
- nome do vídeo real
- id do jogo
- taxonomia selecionada

### Amostra operacional mínima humana

Para um ensaio ser considerado válido, o operador deve marcar no mínimo:

- 1 jogo real com vídeo carregado
- 1 sequência contínua de revisão com pelo menos 10 eventos novos
- pelo menos 3 eventos do time
- pelo menos 3 eventos da adversária
- pelo menos 2 timestamps distintos
- pelo menos 2 tipos de evento distintos
- pelo menos 1 geração de relatório coletivo
- pelo menos 1 geração de relatório individual
- pelo menos 1 geração de relatório de adversária

Se possível, preferir uma amostra mais rica:

- 1 set completo ou trecho operacional de 5 a 10 minutos
- marcação com posse, zona, atleta e pontos quando aplicável

### Roteiro de execução

#### Etapa 1 — Conferência inicial

1. Abrir `Dashboard`.
2. Confirmar que a aplicação carrega sem erro visível.
3. Confirmar que o jogo real aparece em `Jogos` ou `Dashboard`.

#### Etapa 2 — Conferência de cadastro

1. Abrir `Jogos`.
2. Confirmar:
   - jogo selecionável
   - vídeo associado ao jogo
   - atleta(s) e adversária cadastradas

#### Etapa 3 — Marcação humana

1. Abrir `Marcação`.
2. Selecionar o jogo real.
3. Confirmar que o player de vídeo está renderizado.
4. Marcar manualmente a amostra mínima.
5. Variar deliberadamente:
   - timestamps
   - lado `team/opponent`
   - tipo de evento
   - zona, quando aplicável
   - seleção de set e posse, quando aplicável
6. A cada evento salvo, conferir:
   - mensagem de sucesso
   - atualização do histórico recente
7. Ao final, validar:
   - edição de pelo menos 1 evento via bloco `Localizar evento`
   - uso de pelo menos 1 filtro do editor (`set`, `lado`, `tipo` ou busca)
   - exclusão de pelo menos 1 evento selecionado, se isso não comprometer a amostra
8. Se o ensaio usar sets e posses explícitos, validar também:
   - edição de pelo menos 1 set ou posse
   - bloqueio esperado de exclusão quando houver vínculo operacional

#### Etapa 4 — Relatórios pela interface

1. Abrir `Relatórios`.
2. Selecionar o mesmo jogo.
3. Confirmar que a prévia de KPIs carrega sem travamento.
4. Gerar:
   - relatório coletivo
   - relatório individual
   - relatório de adversária
5. Confirmar na própria UI:
   - mensagem de sucesso
   - aumento da lista `Arquivos gerados`
   - presença do arquivo recém-gerado

#### Etapa 5 — Evidência final

Registrar:

- total de eventos do jogo após o ensaio
- total de relatórios do jogo após o ensaio
- nome dos 3 relatórios mais recentes
- screenshots das páginas:
  - `Marcação`
  - `Relatórios`
- limitações reais encontradas

### Evidência mínima obrigatória

O ensaio só conta como executado quando houver todas as evidências abaixo:

| Evidência | Obrigatória |
| --- | --- |
| `scripts/verify_current_state.sh` passando antes ou depois do ensaio | sim |
| URL local aberta em navegador real | sim |
| pelo menos 1 screenshot de `Marcação` | sim |
| pelo menos 1 screenshot de `Relatórios` | sim |
| contagem final de eventos do jogo | sim |
| contagem final de relatórios do jogo | sim |
| nomes dos relatórios gerados | sim |
| registro de limitações reais | sim |

### Critérios de aceite do ensaio humano

O ensaio é `APROVADO` quando:

- a UI carrega sem erro fatal
- o operador consegue salvar a amostra mínima de eventos
- o histórico da página reflete os eventos salvos
- pelo menos 1 edição de evento funciona
- os filtros do editor localizam o evento correto
- os 3 relatórios são gerados pela interface
- os arquivos aparecem em `storage/reports/`
- o operador consegue abrir ou baixar o HTML gerado

O ensaio é `REPROVADO` quando ocorrer qualquer um destes casos:

- a aplicação trava
- o vídeo não renderiza
- salvar evento falha repetidamente
- o histórico não reflete o que foi salvo
- a geração de qualquer um dos 3 relatórios falha
- o arquivo aparece na UI, mas não existe em disco

### Modelo de registro do resultado

Preencher ao final:

```text
data_utc=
git_head=
video_file=
match_id=
taxonomy=
new_events_count=
final_event_count=
new_reports_count=
final_report_count=
recent_reports=
screenshots=
limitations=
decision=APROVADO|REPROVADO|PARCIAL
```

### Regra de honestidade

Se a automação de navegador ou o operador conseguirem apenas parte do fluxo:

- registrar como `PARCIAL`
- separar claramente o que foi provado do que não foi provado
- não promover esse ensaio a validação operacional completa do MVP
