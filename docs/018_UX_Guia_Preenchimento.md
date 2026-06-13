---
doc_id: UX_018
title: "Guia de Preenchimento da Marcação"
status: active
version: "1.0.0"
authority_level: 3
category: UX
owner: Davi Sermenho
created_at: "2026-06-01"
last_updated: "2026-06-13"
repository: Davisermenho/scoutpraia
tipo: guia_operacional_humano
destinatário: operador_humano
uso_por_agente: "NÃO — este guia é para o usuário humano, não para implementação"
nota: "Agentes não devem usar este guia como referência de código; ver scoutpraia/pages/tagging.py"
---

# Guia de Preenchimento — Marcação no ScoutPraia

## Resumo Executivo

Guia operacional para o usuário humano usar a página de marcação do ScoutPraia: como preencher campos, registrar eventos e informar timestamps corretamente. Exclusivo para uso humano — não para agentes.

## Objetivo

Ensinar ao operador (treinador ou analista) o uso correto da tela de marcação do ScoutPraia, campo a campo, com o fluxo correto de preenchimento durante um jogo.

> **AVISO PARA AGENTES:** este documento é um guia operacional para o usuário humano.
> Não use este guia para tomar decisões de implementação ou arquitetura.
> Para implementação: ver `docs/003_PLAN_Passos_Implementacao_IA.md`.
> Para a página de marcação: ver `scoutpraia/pages/tagging.py`.

---

Objetivo: explicar como usar a página `Marcação` do ScoutPraia, como preencher cada campo, como registrar eventos e como informar corretamente o tempo (`timestamp`).

Importante:

- este guia é operacional; ele ensina o uso da tela
- ele não substitui a validação formal da taxonomia em `docs/006_TAX_Dicionario_Taxonomia.md`
- a taxonomia atual `ScoutPraia v0.1` ainda está em `draft`

---

## 1. Lógica geral da marcação

Na prática, o fluxo correto é:

1. selecionar o jogo
2. selecionar a taxonomia
3. criar o `set`, quando necessário
4. criar a `posse`, quando necessário
5. registrar os `eventos` da jogada
6. revisar o `Histórico recente`
7. localizar e corrigir qualquer evento salvo, se necessário

Regra prática:

- `set` organiza o jogo por período
- `posse` organiza a sequência ofensiva/defensiva
- `evento` registra a ação específica observada no vídeo

---

## 2. O que é `set`

No ScoutPraia, `set` é o bloco oficial do jogo.

Use `set` para:

- separar o jogo em partes oficiais
- filtrar eventos depois
- consolidar KPIs por set
- manter contexto correto dos relatórios

### Como preencher `Novo set`

Campos:

- `Número do set`
  - use `1`, `2`, `3`...
- `Início do set`
  - aceita segundos ou formato de vídeo como `00:17.5`
- `Fim do set`
  - aceita segundos ou formato de vídeo como `00:31.5`

### Exemplo

Se o segundo set começa em `17,5` segundos e termina em `31,52` segundos:

- `Número do set` = `2`
- `Início do set` = `00:17.5`
- `Fim do set` = `00:31.5`

Depois clique em `Salvar set`.

### O que deve acontecer após `Salvar set`

Se a tela estiver correta:

- aparece a mensagem `Set X salvo.`
- o campo `Número do set` já muda para o próximo número esperado
- `Início do set` volta para `00:00`
- `Fim do set` volta para `00:00`
- o novo set passa a aparecer no bloco `Set para editar ou excluir`

Se aparecer erro visual logo após salvar, não repita o clique sem conferir primeiro se o set já foi criado no seletor de edição.

### Quando usar `Sem set`

Use `Sem set` apenas se:

- você ainda não criou os sets
- está fazendo um registro muito preliminar

Para uso correto do scout, o ideal é **não deixar evento importante sem set**.

---

## 3. O que é `posse`

No ScoutPraia, `posse` é a sequência em que uma equipe controla a bola até o desfecho da jogada.

Exemplos de fim de posse:

- gol
- erro técnico
- perda de posse
- defesa seguida de recuperação
- bola fora com troca de posse

Use `posse` para:

- agrupar eventos da mesma jogada
- calcular métricas por posse
- separar ataque da equipe e da adversária

### Como preencher `Nova posse`

Campos:

- `Equipe da posse`
  - `Equipe` se a posse é do seu time
  - `Adversária` se a posse é do outro time
- `Set da posse`
  - escolha o set em que a posse aconteceu
- `Início da posse`
  - momento em que a posse começa
- `Fim da posse`
  - momento em que a posse termina
- `Resultado da posse`
  - texto curto, por exemplo:
    - `gol`
    - `erro técnico`
    - `arremesso para fora`
    - `gol sofrido`
- `Pontos feitos`
  - pontos marcados pela equipe dona da posse
- `Pontos sofridos`
  - pontos sofridos pela equipe dona da posse

### Exemplo de posse da equipe

- `Equipe da posse` = `Equipe`
- `Set da posse` = `Set 1`
- `Início da posse` = `02:31`
- `Fim da posse` = `02:38.4`
- `Resultado da posse` = `gol`
- `Pontos feitos` = `1`
- `Pontos sofridos` = `0`

### Exemplo de posse da adversária

- `Equipe da posse` = `Adversária`
- `Set da posse` = `Set 1`
- `Início da posse` = `03:23`
- `Fim da posse` = `03:28.6`
- `Resultado da posse` = `erro forçado`
- `Pontos feitos` = `0`
- `Pontos sofridos` = `0`

### O que deve acontecer após `Salvar posse`

Se a tela estiver correta:

- aparece a mensagem `Posse X salva.`
- `Equipe da posse` preserva a seleção feita antes de salvar
- `Set da posse` preserva a seleção feita antes de salvar
- `Início da posse` volta para `00:00`
- `Fim da posse` volta para `00:00`
- `Resultado da posse` volta vazio
- `Pontos feitos` volta para `0`
- `Pontos sofridos` volta para `0`
- a nova posse passa a aparecer no bloco `Posse para editar ou excluir`

Se aparecer erro visual logo após salvar, não repita o clique sem conferir primeiro se a posse já foi criada no seletor de edição.

### Quando usar `Sem posse`

Use `Sem posse` apenas se:

- você ainda não criou a posse
- o registro é provisório
- o evento é contextual e ficou solto no vídeo

Para análise de posse, o ideal é **não deixar jogadas principais sem posse**.

---

## 4. Como preencher `Registrar evento`

Cada evento é uma ação observada no vídeo.

### 4.1 Campo `Set`

Use o set em que a ação aconteceu.

Exemplo:

- ação ocorreu no primeiro set
- selecione `Set 1`

### 4.2 Campo `Timestamp do vídeo`

Este campo aceita diretamente o formato que você lê no vídeo.

Exemplos corretos:

- `00:00.7`
- `00:02.4`
- `00:17.5`
- `02:25`
- `14:05`
- `145`
- `845`

Exemplos incorretos:

- `8m12s`
- `2min25`
- texto livre sem padrão

### Como usar na prática

1. dê play no vídeo
2. pause no momento da ação
3. leia o tempo do player
4. digite no campo `Timestamp do vídeo`

Importante:

- o player do Streamlit no MVP **não captura o tempo automaticamente**
- mas a UI agora converte `MM:SS`, `HH:MM:SS` ou segundos internamente
- a tela também oferece ajuste rápido:
  - `-1s`
  - `-0.5s`
  - `+0.5s`
  - `+1s`

### 4.3 Campo `Evento`

Escolha a ação observada.

Exemplos:

- `Tentativa de finalização`
- `Gol marcado`
- `Erro técnico`
- `Perda de posse`
- `Parada defensiva`
- `Gol sofrido`

Regra prática:

- se houve arremesso, normalmente existe pelo menos uma `Tentativa de finalização`
- se a bola entrou, pode haver também `Gol marcado`

### 4.4 Campo `Lado`

- `Equipe` = ação do seu time
- `Adversária` = ação do outro time

Use este campo com atenção, porque ele afeta:

- histórico
- KPIs
- relatórios
- tendências da adversária

### 4.5 Campo `Atleta`

Selecione a atleta principal da ação.

Exemplos:

- quem arremessou
- quem roubou a bola
- quem bloqueou
- quem cometeu o erro técnico

Se você não tiver certeza, pode deixar `Sem atleta`, mas isso reduz a utilidade do scout individual.

### 4.6 Campo `Atleta secundária`

Use quando outra atleta teve participação direta relevante.

Exemplos:

- assistência
- passe decisivo
- participação complementar da jogada

Se não houver, deixe `Sem atleta`.

### 4.7 Campo `Zona`

Use a zona em que a ação principal ocorreu.

Exemplos:

- `Ponta esquerda`
- `Meia esquerda`
- `Centro`
- `Meia direita`
- `Ponta direita`
- `Corredor do shoot-out`

Se a zona não estiver clara, use `Sem zona`.

### 4.8 Campo `Posse`

Selecione a posse à qual o evento pertence.

Exemplo:

- se o evento ocorreu dentro da posse `Posse 4 — Equipe`
- selecione exatamente essa posse

### 4.9 Campo `Pontos`

Use:

- `0` quando o evento não pontua
- `1` quando vale 1 ponto
- `2` quando vale 2 pontos

Exemplos:

- `Tentativa de finalização` sem gol → `0`
- `Gol marcado` comum → `1`
- `Gol de 2 pontos` → `2`

### 4.10 Campo `Subtipo`

Campo opcional para detalhar a ação.

Exemplos:

- `spin`
- `inflight`
- `transição`
- `passe errado`

### 4.11 Campo `Desfecho`

Campo opcional para descrever o resultado da ação.

Exemplos:

- `gol`
- `para fora`
- `defesa da goleira`
- `perda de posse`

### 4.12 Campo `Notas`

Campo livre para observações úteis.

Use para:

- contexto do lance
- dúvida de marcação
- observação para revisão futura

Evite transformar `Notas` em lugar de registrar o evento corretamente.

---

## 5. Como usar os `Botões rápidos`

Os `Botões rápidos` **não salvam o evento sozinhos**.

Eles apenas:

- preenchem rapidamente o tipo de `Evento`

Depois disso você ainda precisa:

1. revisar o `Timestamp do vídeo`
2. revisar `Lado`
3. preencher atleta, zona, posse e pontos quando aplicável
4. clicar em `Salvar evento`

Observação ergonômica:

- a tela preserva a seleção corrente de `Set`, `Atleta`, `Atleta secundária`, `Zona`, `Posse` e `Pontos`
- isso evita repetir o mesmo preenchimento a cada jogada da mesma sequência

### Defaults úteis da tela

Ao abrir a página `Marcação` com jogo já cadastrado:

- `Set` tende a abrir no set mais recente disponível
- `Posse` tende a abrir na posse mais recente do set selecionado
- `Número do set` em `Novo set` abre no próximo número esperado
- após criar `set` ou `posse`, os formulários de `Sets e posses` devem resetar de forma previsível sem erro de UI

---

## 6. Como revisar e corrigir

Use o bloco `Histórico recente` para conferir se o evento entrou corretamente.

Verifique:

- tempo
- evento
- atleta
- lado
- zona
- pontos

Se qualquer evento ficou errado:

1. vá em `Localizar evento`
2. use, se necessário:
   - `Filtrar por set`
   - `Filtrar por lado`
   - `Filtrar por tipo de evento`
   - `Buscar evento`
3. use `Evento anterior` e `Próximo evento` quando houver mais de um resultado
4. selecione o item em `Evento para editar ou excluir`
5. ajuste os campos
6. clique em `Atualizar evento selecionado`

Se o evento precisa ser removido:

- selecione o item correto e clique em `Excluir evento selecionado`

Se o problema estiver no `set`:

1. use `Set para editar ou excluir`
2. ajuste os campos do set selecionado
3. clique em `Atualizar set selecionado`

Se o problema estiver na `posse`:

1. use `Posse para editar ou excluir`
2. ajuste os campos da posse selecionada
3. clique em `Atualizar posse selecionada`

---

## 7. Três exemplos operacionais de jogadas

Os exemplos abaixo são **exemplos práticos de uso da tela**. Eles servem para ensinar o preenchimento. Não substituem a validação observacional formal.

### Jogada 1 — Ataque da equipe com gol comum

Situação:

- a equipe recupera a bola
- organiza o ataque
- a atleta finaliza do centro
- a bola entra

#### Set e posse

**Set**

- `Número do set` = `1`
- `Início do set` = `00:00`
- `Fim do set` = `10:00`

**Posse**

- `Equipe da posse` = `Equipe`
- `Set da posse` = `Set 1`
- `Início da posse` = `02:31`
- `Fim da posse` = `02:36`
- `Resultado da posse` = `gol`
- `Pontos feitos` = `1`
- `Pontos sofridos` = `0`

#### Evento 1

- `Set` = `Set 1`
- `Timestamp do vídeo` = `02:34.8`
- `Evento` = `Tentativa de finalização`
- `Lado` = `Equipe`
- `Atleta` = atleta que arremessou
- `Atleta secundária` = `Sem atleta`
- `Zona` = `Centro`
- `Posse` = posse criada acima
- `Pontos` = `0`
- `Subtipo` = vazio ou `ataque posicional`
- `Desfecho` = `gol`

#### Evento 2

- `Set` = `Set 1`
- `Timestamp do vídeo` = `02:35`
- `Evento` = `Gol marcado`
- `Lado` = `Equipe`
- `Atleta` = mesma atleta finalizadora
- `Zona` = `Centro`
- `Posse` = mesma posse
- `Pontos` = `1`
- `Desfecho` = `bola na rede`

### Jogada 2 — Ataque da equipe com erro técnico

Situação:

- a equipe inicia a posse
- tenta circular a bola
- ocorre passe errado sem finalização
- a adversária recupera

#### Posse

- `Equipe da posse` = `Equipe`
- `Set da posse` = `Set 1`
- `Início da posse` = `03:23`
- `Fim da posse` = `03:26.2`
- `Resultado da posse` = `erro técnico`
- `Pontos feitos` = `0`
- `Pontos sofridos` = `0`

#### Evento

- `Set` = `Set 1`
- `Timestamp do vídeo` = `03:25.9`
- `Evento` = `Erro técnico`
- `Lado` = `Equipe`
- `Atleta` = atleta que errou o passe ou recepção
- `Atleta secundária` = `Sem atleta`
- `Zona` = `Meia esquerda`, `Centro` ou `Sem zona`, conforme o lance
- `Posse` = posse criada acima
- `Pontos` = `0`
- `Subtipo` = `passe errado`
- `Desfecho` = `perda de posse`
- `Notas` = opcional

Se você quiser registrar a perda de posse de forma adicional:

- crie outro evento `Perda de posse` logo em seguida

### Jogada 3 — Ataque da adversária terminado por ação defensiva da equipe

Situação:

- a adversária começa a posse
- cria tentativa de finalização
- a goleira defende
- a equipe recupera o controle

#### Posse

- `Equipe da posse` = `Adversária`
- `Set da posse` = `Set 1`
- `Início da posse` = `04:08`
- `Fim da posse` = `04:13.4`
- `Resultado da posse` = `defesa da goleira`
- `Pontos feitos` = `0`
- `Pontos sofridos` = `0`

#### Evento 1

- `Set` = `Set 1`
- `Timestamp do vídeo` = `04:12.8`
- `Evento` = `Tentativa de finalização`
- `Lado` = `Adversária`
- `Atleta` = se conhecida, a finalizadora adversária
- `Zona` = por exemplo `Ponta esquerda`
- `Posse` = posse da adversária
- `Pontos` = `0`
- `Desfecho` = `defendida`

#### Evento 2

- `Set` = `Set 1`
- `Timestamp do vídeo` = `04:12.9`
- `Evento` = `Defesa da goleira`
- `Lado` = `Equipe`
- `Atleta` = goleira da equipe
- `Zona` = mesma zona da finalização ou `Sem zona`
- `Posse` = posse da adversária
- `Pontos` = `0`
- `Desfecho` = `bola defendida`

#### Evento 3

- `Set` = `Set 1`
- `Timestamp do vídeo` = `04:13.1`
- `Evento` = `Parada defensiva`
- `Lado` = `Equipe`
- `Atleta` = atleta principal da ação, se fizer sentido
- `Posse` = mesma posse
- `Pontos` = `0`
- `Desfecho` = `posse encerrada sem gol`

---

## 8. Regras práticas para não travar o fluxo

Use este padrão:

- sempre preencher `Set`
- sempre preencher `Timestamp do vídeo`
- sempre definir `Lado`
- usar `Posse` sempre que a jogada estiver clara
- preencher `Atleta` quando houver segurança
- preencher `Zona` quando a observação estiver clara
- usar `Pontos` corretamente

Se estiver em dúvida:

- prefira registrar o essencial corretamente
- use `Notas` para marcar incerteza
- revise o evento salvo logo depois

---

## 9. Erros comuns

### Erro 1 — Achar que `MM:SS` é inválido

Correto:

- `02:31`
- `00:17.5`
- `01:02:25`
- `151`

### Erro 2 — Clicar no botão rápido e achar que já salvou

Errado:

- clicar em `Tentativa de finalização` e sair da tela

Certo:

- clicar no botão rápido
- revisar o formulário
- clicar em `Salvar evento`

### Erro 3 — Não diferenciar equipe e adversária

Errado:

- registrar evento da adversária como `Equipe`

Certo:

- revisar sempre o campo `Lado`

### Erro 4 — Não criar posse quando a jogada está clara

Errado:

- registrar todos os eventos como `Sem posse`

Certo:

- criar posse para as jogadas principais

---

## 10. Fluxo mínimo recomendado para começar

Se você estiver começando agora, use este roteiro:

1. criar `Set 1`
2. criar uma `Posse` da equipe
3. registrar uma `Tentativa de finalização`
4. registrar `Gol marcado` ou `Finalização para fora`
5. conferir o `Histórico recente`
6. localizar e corrigir o evento necessário, se houver erro
7. repetir o processo

Depois da marcação:

1. abrir `Relatórios`
2. gerar `coletivo`
3. gerar `individual`
4. gerar `adversária`

---

## 11. Referências internas úteis

- uso operacional da taxonomia: `docs/006_TAX_Dicionario_Taxonomia.md`
- protocolo humano de validação: `docs/007_PROT_Protocolo_Validacao.md`
- estado real do projeto e evidências: `docs/004_PROG_Progresso_Implementacao.md`
- implementação da página: `scoutpraia/pages/tagging.py`
