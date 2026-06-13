---
doc_id: FLOW_019
title: "Manual Determinístico — Fluxo IA Atacante × Defensor"
status: active
version: "0.9.0"
authority_level: 3
category: FLOW
owner: Davi Sermenho
created_at: "2026-06-12"
last_updated: "2026-06-13"
repository: Davisermenho/scoutpraia
document_id: IA-AD-MANUAL-001
timezone: America/Sao_Paulo
purpose: ensinar, definir e operacionalizar o Fluxo IA Atacante × Defensor
primary_rule: nenhuma etapa pode ser executada sem entrada, saída, critério de aceite e evidência verificável
termination_keyword: TERMINATE
max_iterations_default: 4
minimum_agents: atacante, defensor
optional_agents: juiz_validador, operador_humano
implementation_appendix: Python + LangGraph + VS Code + OpenAI API
---

# Manual Determinístico — Fluxo IA Atacante × Defensor

## Resumo Executivo

Manual determinístico do Fluxo IA Atacante × Defensor para revisar e fortalecer documentos, planos e especificações por meio de ciclos controlados de ataque crítico e defesa corretiva, com critério de encerramento explícito (TERMINATE).

## Objetivo

Ensinar e padronizar o uso do Fluxo IA Atacante × Defensor, definindo papéis, entradas/saídas obrigatórias, critérios de aceite e limite de iterações para produzir versões mais robustas e rastreáveis.

## 1. Natureza deste documento

Este documento é um manual determinístico do Fluxo IA Atacante × Defensor.

Ele não é apenas um plano de implementação técnica. Ele define, em linguagem normativa e operacional, como o fluxo deve funcionar, quais papéis existem, quais entradas são obrigatórias, quais saídas são aceitas, quais falhas invalidam uma rodada, quais critérios encerram o ciclo e quais evidências tornam uma tarefa ou decisão aceitável.

Sempre que houver conflito entre liberdade criativa do modelo e regra deste manual, prevalece a regra do manual.

## 2. Objetivo do manual

Ensinar e padronizar o uso do Fluxo IA Atacante × Defensor para melhorar planos, documentos, manuais, especificações, estratégias e arquiteturas, submetendo-os a um ciclo controlado de ataque crítico e defesa corretiva.

O objetivo não é fazer dois modelos conversarem indefinidamente. O objetivo é produzir uma versão mais forte, clara, executável e resistente a falhas, com critérios de validação explícitos e evidências rastreáveis.

## 3. Definição determinística do fluxo

O Fluxo IA Atacante × Defensor é um processo iterativo no qual:

1. Um documento inicial é entregue como Draft Zero.
2. O Atacante procura falhas, lacunas, contradições, riscos, dependências frágeis e pontos de quebra.
3. O Atacante não corrige o documento.
4. O Defensor recebe o documento e o relatório do Atacante.
5. O Defensor corrige as falhas sem alterar o objetivo principal.
6. A versão corrigida volta ao Atacante.
7. O ciclo termina quando o Atacante retorna TERMINATE ou quando o limite de iterações é atingido.

A lógica do fluxo é: documento → ataque → defesa → reataque → encerramento ou nova defesa.

## 4. Princípios obrigatórios

### 4.1 Separação de papéis

O Atacante e o Defensor não podem executar a mesma função.

- O Atacante deve quebrar, invalidar, tensionar e encontrar fragilidade.
- O Defensor deve corrigir, blindar, completar e tornar executável.

Se o Atacante sugerir solução, a rodada deve ser marcada como inválida.

Se o Defensor mudar o objetivo principal do documento para escapar da crítica, a rodada deve ser marcada como inválida.

### 4.2 Rastreabilidade

Toda alteração relevante precisa poder ser rastreada até:

- uma falha apontada;
- uma evidência verificável;
- uma decisão de correção;
- um critério de aceite.

### 4.3 Determinismo operacional

O fluxo deve produzir saídas previsíveis em estrutura, mesmo que o conteúdo varie conforme o caso. O modelo pode raciocinar, mas não pode improvisar formato, omitir campos obrigatórios ou encerrar sem critério.

### 4.4 Evidência antes de execução

Nenhuma tarefa, regra, dependência técnica, premissa operacional ou decisão de arquitetura pode ser aceita se não houver fonte especializada verificável ou justificativa explícita baseada no próprio documento analisado.

## 5. Quando usar o fluxo

Use o Fluxo IA Atacante × Defensor quando o documento precisar ser resistente a erro, ambiguidade ou falha de execução.

Casos recomendados:

- plano de implementação;
- manual técnico;
- especificação de engenharia;
- arquitetura de software;
- playbook operacional;
- documentação de processo;
- estratégia esportiva, pedagógica ou organizacional;
- checklist de validação;
- contrato, regra ou matriz de decisão.

## 6. Quando não usar o fluxo

Não use o fluxo quando:

- o documento é apenas criativo e não precisa de validação;
- não existe objetivo definido;
- não existem fontes ou critérios para avaliar a resposta;
- o usuário deseja apenas estilo, tom ou formatação;
- o custo de execução é maior que o risco de erro;
- a crítica adversarial pode gerar burocracia inútil.

## 7. Artefatos obrigatórios

Todo ciclo deve produzir ou atualizar os seguintes artefatos:

1. Draft Zero.
2. Pacote de entrada.
3. Registro de fontes.
4. Prompt do Atacante.
5. Relatório do Atacante.
6. Prompt do Defensor.
7. Documento revisado pelo Defensor.
8. Log de mudanças.
9. Decisão de continuação ou parada.
10. Registro final de validação.

Se qualquer artefato obrigatório estiver ausente, o ciclo não pode ser declarado concluído.

## 8. Pacote de entrada obrigatório

Antes da primeira rodada, o operador deve montar o Pacote de Entrada.

### 8.1 Estrutura do Pacote de Entrada

```markdown
# INPUT_PACKAGE

## Documento-alvo
[conteúdo do documento que será atacado]

## Objetivo principal
[objetivo que não pode ser alterado]

## Escopo permitido
[o que pode ser alterado]

## Escopo proibido
[o que não pode ser alterado]

## Público-alvo
[quem usará o documento]

## Critérios de sucesso
[como saber que a versão final ficou melhor]

## Fontes obrigatórias
[lista de fontes que devem ser respeitadas]

## Restrições
[limites de tempo, custo, tecnologia, linguagem, formato]
```

### 8.2 Regra de bloqueio por entrada incompleta

Se o objetivo principal estiver ausente, o fluxo deve parar antes do ataque.

Se o escopo proibido estiver ausente, o Defensor pode modificar indevidamente o documento. Nesse caso, a rodada deve ser classificada como risco de drift.

Se as fontes obrigatórias estiverem ausentes, o Atacante deve limitar suas críticas a consistência interna, clareza, completude e viabilidade lógica.

## 9. Registro de fontes fortes

O registro de fontes deve existir antes da execução do fluxo.

### 9.1 Estrutura obrigatória

| source_id | título | organização/autoria | tipo | link | uso permitido | nível de confiança |
|---|---|---|---|---|---|---|
| SRC-001 | Improving Factuality and Reasoning in Language Models through Multiagent Debate | Du et al. | Artigo acadêmico | https://arxiv.org/abs/2305.14325 | justificar debate multiagente | Alto |
| SRC-002 | Constitutional AI: Harmlessness from AI Feedback | Bai et al. / Anthropic | Artigo acadêmico | https://arxiv.org/abs/2212.08073 | justificar crítica e revisão por princípios | Alto |
| SRC-003 | LangGraph Quickstart | LangChain | Documentação oficial | https://docs.langchain.com/oss/python/langgraph/quickstart | justificar grafo, nós, estado e conditional edges | Alto |
| SRC-004 | AutoGen AgentChat Agents | Microsoft | Documentação oficial | https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/agents.html | justificar agentes e system messages | Alto |
| SRC-005 | Python environments in VS Code | Microsoft | Documentação oficial | https://code.visualstudio.com/docs/python/environments | justificar ambiente Python no VS Code | Alto |
| SRC-006 | venv — Creation of virtual environments | Python Software Foundation | Documentação oficial | https://docs.python.org/3/library/venv.html | justificar ambiente virtual | Alto |
| SRC-007 | OpenAI Production Best Practices | OpenAI | Documentação oficial | https://platform.openai.com/docs/guides/production-best-practices | justificar segurança, custos, monitoramento e produção | Alto |

### 9.2 Regra de uso das fontes

Uma fonte só pode justificar uma task se o uso declarado estiver relacionado ao conteúdo da fonte. Não é permitido usar uma fonte de ambiente virtual para justificar design de prompt, nem usar artigo acadêmico para justificar comando de terminal.

## 10. Papel determinístico do Atacante

### 10.1 Função

O Atacante existe para encontrar falhas reais ou plausíveis que possam quebrar o documento no mundo real.

### 10.2 O Atacante deve procurar

- contradições internas;
- lacunas de execução;
- ausência de critérios de aceite;
- dependências externas não tratadas;
- riscos técnicos;
- riscos financeiros;
- riscos de custo e latência;
- prompts ambíguos;
- objetivos não preservados;
- excesso de complexidade;
- alucinação colaborativa;
- falta de evidência;
- ausência de rollback ou falha segura.

### 10.3 O Atacante não pode

- corrigir o documento;
- reescrever trechos;
- propor solução;
- suavizar crítica para agradar;
- atacar gosto estético se o escopo não for design;
- inventar premissas sem sinalizar incerteza;
- considerar falha algo que não tem impacto prático.

### 10.4 Saída obrigatória do Atacante

```markdown
# RELATÓRIO DO ATACANTE

## Status da rodada
[FAIL | PASS_TERMINATE | BLOQUEADO]

## Falhas encontradas
### FALHA-001 — [nome da falha]
- Severidade: [crítica | alta | média | baixa]
- Tipo: [lógica | execução | evidência | custo | segurança | escopo | ambiguidade]
- Trecho afetado: [referência]
- Por que quebra ou fragiliza o plano: [explicação]
- Evidência usada: [source_id ou evidência interna]
- Critério para considerar resolvida: [condição objetiva]

## Decisão
[Enviar ao Defensor | TERMINATE | Bloquear por falta de entrada]
```

### 10.5 Critério para falha válida

Uma falha só é válida se cumprir pelo menos uma condição:

- impede execução;
- aumenta risco de erro;
- gera ambiguidade operacional;
- contradiz objetivo declarado;
- viola fonte especializada;
- deixa uma decisão sem critério de aceite;
- cria custo ou dependência não controlada.

Falhas de gosto, estilo ou preferência só são válidas se o escopo do documento incluir linguagem, design ou experiência do usuário.

## 11. Papel determinístico do Defensor

### 11.1 Função

O Defensor existe para corrigir as falhas válidas apontadas pelo Atacante e entregar uma versão mais robusta do documento.

### 11.2 O Defensor deve

- corrigir cada falha válida;
- preservar o objetivo principal;
- manter rastreabilidade entre falha e correção;
- adicionar critérios de aceite quando ausentes;
- adicionar fontes quando uma task não tiver evidência;
- reduzir ambiguidade;
- simplificar excesso de complexidade;
- declarar quando uma falha do Atacante é inválida e por quê.

### 11.3 O Defensor não pode

- apagar o objetivo original;
- mudar o problema para escapar da crítica;
- aceitar falha falsa sem validação;
- criar solução sem critério de aceite;
- aumentar complexidade sem justificar;
- ocultar trade-offs;
- declarar concluído sem prova.

### 11.4 Saída obrigatória do Defensor

```markdown
# RESPOSTA DO DEFENSOR

## Status da defesa
[CORRIGIDO | PARCIAL | BLOQUEADO]

## Correções aplicadas
### CORREÇÃO-001 — referente à FALHA-001
- Ação aplicada: [descrição]
- Trecho alterado: [referência]
- Justificativa: [por que corrige]
- Evidência: [source_id]
- Critério de aceite: [condição objetiva]

## Falhas rejeitadas
### FALHA-XXX
- Motivo da rejeição: [explicação]
- Evidência: [source_id ou lógica interna]

## Documento revisado
[versão completa ou trecho revisado]

## Próxima decisão
[Voltar ao Atacante | Solicitar revisão humana | Encerrar]
```

## 12. Juiz validador opcional

O Juiz Validador é opcional, mas recomendado quando o documento tiver impacto alto.

Ele não cria conteúdo e não corrige. Sua função é verificar se:

- o Atacante respeitou seu papel;
- o Defensor corrigiu sem desviar o objetivo;
- todas as falhas têm evidência;
- todas as correções têm critério de aceite;
- o ciclo pode continuar ou encerrar.

Se não houver Juiz Validador, essa função deve ser assumida pelo Operador Humano.

## 13. Gates determinísticos do ciclo

### GATE-00 — Entrada mínima

O ciclo só inicia se houver documento-alvo e objetivo principal.

### GATE-01 — Fonte mínima

Toda regra técnica deve ter fonte especializada ou justificativa interna verificável.

### GATE-02 — Ataque válido

O relatório do Atacante deve conter status, falhas, severidade, evidência e critério de resolução.

### GATE-03 — Defesa válida

A resposta do Defensor deve mapear cada correção para uma falha.

### GATE-04 — Preservação de objetivo

Qualquer alteração que modifique o objetivo principal deve ser rejeitada.

### GATE-05 — Parada

O ciclo só encerra por:

- `TERMINATE` emitido pelo Atacante;
- `max_iterations` atingido;
- bloqueio por ausência de entrada essencial;
- decisão humana registrada.

### GATE-06 — Evidência final

A versão final deve conter log de mudanças e critérios de aceite atendidos.

## 14. Critérios de parada

O fluxo deve parar quando uma das condições ocorrer:

1. O Atacante retorna `TERMINATE` sem falhas relevantes.
2. O limite máximo de iterações é atingido.
3. O Defensor não consegue corrigir sem alterar o objetivo.
4. Uma falha depende de informação externa ausente.
5. O custo, latência ou risco ultrapassa o limite definido.
6. O Operador Humano interrompe o ciclo.

O Atacante não pode usar `TERMINATE` se ainda houver falha crítica, alta ou média sem resolução.

## 15. Controle de severidade

| Severidade | Definição | Ação obrigatória |
|---|---|---|
| Crítica | impede execução ou causa erro grave | corrigir antes de continuar |
| Alta | ameaça funcionamento no mundo real | corrigir ou justificar exceção |
| Média | gera ambiguidade ou risco moderado | corrigir se não aumentar complexidade excessiva |
| Baixa | melhora clareza, estilo ou manutenção | corrigir apenas se estiver no escopo |

## 16. Formato determinístico de task

Toda task do manual deve seguir este formato:

```markdown
## TASK-000 — [nome]
- Chunk: [CHUNK-XX]
- Tipo: [manual | regra | prompt | validação | implementação | segurança]
- Ação: [verbo no infinitivo]
- Justificativa: [por que precisa existir]
- Evidência: [source_id + link]
- Entrada necessária: [input]
- Saída esperada: [output]
- Critério de aceite: [condição objetiva]
- Prova de conclusão: [log, arquivo, trecho, teste ou validação]
- Status: [pendente | em execução | concluída | bloqueada]
```

Task sem evidência deve ser bloqueada.

Task sem critério de aceite não pode ser executada.

Task sem prova de conclusão não pode ser marcada como concluída.

## 17. Chunks operacionais

### CHUNK-00 — Fundamentos do método
Define objetivo, escopo, papéis, artefatos e princípios.

### CHUNK-01 — Entrada e fontes
Define Pacote de Entrada e Registro de Fontes.

### CHUNK-02 — Ataque
Define regras, prompt, relatório e critérios de falha válida.

### CHUNK-03 — Defesa
Define regras, prompt, relatório e critérios de correção válida.

### CHUNK-04 — Iteração e parada
Define loop, gates, severidade, max_iterations e TERMINATE.

### CHUNK-05 — Validação
Define Juiz, Operador Humano, critérios de aceite e definição de DONE.

### CHUNK-06 — Implementação técnica
Define como materializar o fluxo em Python, LangGraph e VS Code.

## 18. Tasks determinísticas do manual

| task_id | chunk | ação | evidência | critério de aceite |
|---|---|---|---|---|
| TASK-001 | CHUNK-00 | Definir objetivo principal do fluxo | SRC-001 | Objetivo declara ataque, defesa e melhoria iterativa |
| TASK-002 | CHUNK-00 | Separar Atacante e Defensor em papéis exclusivos | SRC-001, SRC-004 | Atacante não corrige; Defensor não ataca |
| TASK-003 | CHUNK-01 | Criar Pacote de Entrada obrigatório | SRC-007 | Pacote contém documento, objetivo, escopo, fontes e restrições |
| TASK-004 | CHUNK-01 | Criar Registro de Fontes Fortes | SRC-001, SRC-002, SRC-003, SRC-004 | Toda fonte tem ID, tipo, link e uso permitido |
| TASK-005 | CHUNK-02 | Criar prompt determinístico do Atacante | SRC-001, SRC-004 | Prompt tem papel, proibições, critérios e formato de saída |
| TASK-006 | CHUNK-02 | Criar relatório obrigatório do Atacante | SRC-001, SRC-002 | Toda falha tem severidade, tipo, evidência e resolução esperada |
| TASK-007 | CHUNK-03 | Criar prompt determinístico do Defensor | SRC-002, SRC-004 | Prompt preserva objetivo e corrige falhas válidas |
| TASK-008 | CHUNK-03 | Criar relatório obrigatório do Defensor | SRC-002 | Correções são mapeadas para falhas |
| TASK-009 | CHUNK-04 | Definir critério `TERMINATE` | SRC-003 | Fluxo encerra com palavra-chave válida |
| TASK-010 | CHUNK-04 | Definir `max_iterations` | SRC-003, SRC-007 | Loop encerra ao atingir limite |
| TASK-011 | CHUNK-05 | Definir Juiz ou Operador Humano | SRC-007 | Há validação final independente |
| TASK-012 | CHUNK-05 | Definir DONE determinístico | SRC-007 | DONE exige prova objetiva |
| TASK-013 | CHUNK-06 | Implementar grafo com `StateGraph` | SRC-003 | Código possui estado, nós, edges e conditional edges |
| TASK-014 | CHUNK-06 | Criar ambiente Python isolado | SRC-005, SRC-006 | `.venv` ativo e dependências instaladas |
| TASK-015 | CHUNK-06 | Proteger credenciais | SRC-007 | `.env` fora do Git e sem chave no código |

## 19. Prompt oficial do Atacante

```markdown
# PAPEL
Você é o ATACANTE do Fluxo IA Atacante × Defensor.

# MISSÃO
Executar um ataque técnico, lógico e operacional contra o documento-alvo. Sua função é encontrar falhas que possam impedir, fragilizar, confundir ou quebrar o funcionamento do plano no mundo real.

# PROIBIÇÕES
Você não pode corrigir o documento.
Você não pode propor solução.
Você não pode reescrever trechos.
Você não pode atacar gosto estético fora do escopo.
Você não pode inventar premissas como se fossem fatos.

# CRITÉRIOS DE ATAQUE
Avalie:
1. objetivo;
2. completude;
3. consistência interna;
4. viabilidade de execução;
5. fontes e evidências;
6. riscos e dependências;
7. critérios de aceite;
8. custo, latência e segurança;
9. risco de drift;
10. risco de alucinação colaborativa.

# SAÍDA OBRIGATÓRIA
Use exatamente a estrutura:

# RELATÓRIO DO ATACANTE
## Status da rodada
[FAIL | PASS_TERMINATE | BLOQUEADO]

## Falhas encontradas
### FALHA-001 — [nome]
- Severidade:
- Tipo:
- Trecho afetado:
- Por que quebra ou fragiliza:
- Evidência:
- Critério para resolver:

## Decisão
[Enviar ao Defensor | TERMINATE | Bloquear]

# REGRA DE TERMINATE
Responda TERMINATE somente se não houver falhas críticas, altas ou médias sem resolução.
```

## 20. Prompt oficial do Defensor

```markdown
# PAPEL
Você é o DEFENSOR do Fluxo IA Atacante × Defensor.

# MISSÃO
Corrigir o documento com base no relatório do Atacante, preservando o objetivo principal e fortalecendo a execução no mundo real.

# OBRIGAÇÕES
Você deve corrigir toda falha válida.
Você deve rejeitar falhas inválidas com justificativa.
Você deve preservar o objetivo principal.
Você deve adicionar critério de aceite quando faltar.
Você deve adicionar fonte quando a task exigir evidência.
Você deve reduzir ambiguidade.

# PROIBIÇÕES
Você não pode mudar o objetivo principal.
Você não pode fingir que corrigiu.
Você não pode apagar uma falha sem justificar.
Você não pode declarar DONE sem prova objetiva.

# SAÍDA OBRIGATÓRIA
# RESPOSTA DO DEFENSOR
## Status da defesa
[CORRIGIDO | PARCIAL | BLOQUEADO]

## Correções aplicadas
### CORREÇÃO-001 — referente à FALHA-001
- Ação aplicada:
- Justificativa:
- Evidência:
- Critério de aceite:
- Prova esperada:

## Falhas rejeitadas
### FALHA-XXX
- Motivo:
- Evidência:

## Documento revisado
[conteúdo revisado]

## Próxima decisão
[Voltar ao Atacante | Revisão humana | Encerrar]
```

## 21. Exemplo determinístico mínimo

### 21.1 Draft Zero

```markdown
Plano: Criar uma cafeteria 24h sem funcionários.
Orçamento: R$ 50.000.
Operação: cliente entra por aplicativo próprio e compra em máquinas de autoatendimento.
```

### 21.2 Saída esperada do Atacante

```markdown
# RELATÓRIO DO ATACANTE
## Status da rodada
FAIL

## Falhas encontradas
### FALHA-001 — Orçamento incompatível
- Severidade: alta
- Tipo: viabilidade financeira
- Trecho afetado: orçamento e operação
- Por que quebra ou fragiliza: aplicativo próprio, acesso eletrônico e máquinas premium podem exceder o orçamento.
- Evidência: análise de viabilidade interna; exigir fonte de custos na versão real.
- Critério para resolver: substituir por solução mais barata ou apresentar orçamento comprovado.

### FALHA-002 — Manutenção física ignorada
- Severidade: crítica
- Tipo: operação
- Trecho afetado: sem funcionários
- Por que quebra ou fragiliza: máquinas exigem limpeza, reposição e manutenção.
- Evidência: lógica operacional interna.
- Critério para resolver: incluir rotina de manutenção e responsável.

## Decisão
Enviar ao Defensor
```

### 21.3 Saída esperada do Defensor

```markdown
# RESPOSTA DO DEFENSOR
## Status da defesa
CORRIGIDO

## Correções aplicadas
### CORREÇÃO-001 — referente à FALHA-001
- Ação aplicada: remover aplicativo próprio da fase 1 e usar controle de acesso por solução existente.
- Justificativa: reduz custo inicial e dependência técnica.
- Evidência: fonte de orçamento a coletar.
- Critério de aceite: custo estimado dentro do orçamento.

### CORREÇÃO-002 — referente à FALHA-002
- Ação aplicada: incluir manutenção terceirizada diária.
- Justificativa: elimina premissa falsa de operação sem qualquer intervenção humana.
- Evidência: rotina operacional definida.
- Critério de aceite: responsável e frequência registrados.

## Próxima decisão
Voltar ao Atacante
```

## 22. Definição determinística de DONE

O fluxo só pode ser marcado como DONE quando:

- o documento final preserva o objetivo principal;
- não existem falhas críticas, altas ou médias abertas;
- todas as correções foram mapeadas para falhas;
- toda task tem fonte ou justificativa verificável;
- o Atacante retornou TERMINATE ou o limite foi atingido com decisão humana;
- o log de mudanças foi registrado;
- os riscos residuais foram declarados.

Formato obrigatório:

```text
DONE_CHECK
Objetivo preservado: SIM/NÃO
Falhas críticas abertas: SIM/NÃO
Falhas altas abertas: SIM/NÃO
Falhas médias abertas: SIM/NÃO
Correções rastreáveis: SIM/NÃO
Fontes registradas: SIM/NÃO
Critério de parada válido: SIM/NÃO
Riscos residuais declarados: SIM/NÃO
Resultado: DONE | NÃO DONE
```

## 23. Apêndice técnico — Implementação em LangGraph

A implementação técnica deve ser tratada como apêndice, não como centro do manual.

Estrutura mínima:

```python
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    plan: str
    critique: str
    iterations: int

MAX_ITERATIONS = 4
TERMINATION_KEYWORD = "TERMINATE"

def should_continue(state: AgentState) -> Literal["continue", "end"]:
    if TERMINATION_KEYWORD in state["critique"].upper():
        return "end"
    if state["iterations"] >= MAX_ITERATIONS:
        return "end"
    return "continue"
```

A implementação completa deve conter:

- `attacker_node`;
- `defender_node`;
- `StateGraph`;
- `add_node`;
- `add_edge`;
- `add_conditional_edges`;
- `compile`;
- `invoke`;
- logs de execução.

## 24. Apêndice técnico — Ambiente de execução

Comandos mínimos:

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Linux/macOS
source .venv/bin/activate

pip install langgraph langchain-core langchain-openai python-dotenv
pip freeze > requirements.txt
```

Arquivos mínimos:

```text
app.py
.env
.gitignore
requirements.txt
runs.log
```

`.gitignore` mínimo:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

## 25. Erros proibidos

O fluxo não pode ser considerado válido se ocorrer qualquer uma destas falhas:

- Atacante corrige em vez de atacar.
- Defensor altera o objetivo principal.
- Falha sem severidade.
- Falha sem critério de resolução.
- Correção sem referência à falha.
- Task sem fonte.
- Task sem critério de aceite.
- DONE sem prova.
- Loop sem limite.
- API key no código.
- Custo sem monitoramento.
- Documento final sem riscos residuais.

## 26. Regra final do manual

O Fluxo IA Atacante × Defensor não é uma conversa livre entre modelos.

Ele é um protocolo controlado de crítica, correção, revalidação e encerramento.

A força do método não está apenas em usar dois LLMs. Está em impor papéis separados, formatos obrigatórios, gates, fontes verificáveis, critérios de aceite, limite de iteração e prova objetiva de conclusão.

