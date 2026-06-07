# Guia de Preenchimento — Marcação no ScoutPraia

Objetivo: explicar como usar a página `Marcação` do ScoutPraia, como preencher cada campo, como registrar eventos e como informar corretamente o tempo (`timestamp`).

Importante:

- este guia é operacional; ele ensina o uso da tela
- ele não substitui a validação formal da taxonomia em `docs/taxonomy_dictionary.md`
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
7. corrigir o último evento, se necessário

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

Se o último evento ficou errado:

1. vá em `Editar ou excluir último evento`
2. ajuste os campos
3. clique em `Atualizar último evento`

Se o evento precisa ser removido:

- clique em `Excluir último evento`

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
- revise o último evento logo depois

---

## 9. Erros comuns

### Erro 1 — Digitar tempo em `mm:ss`

Errado:

- `02:31`

Certo:

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
6. corrigir o último evento, se necessário
7. repetir o processo

Depois da marcação:

1. abrir `Relatórios`
2. gerar `coletivo`
3. gerar `individual`
4. gerar `adversária`

---

## 11. Referências internas úteis

- uso operacional da taxonomia: `docs/taxonomy_dictionary.md`
- protocolo humano de validação: `docs/validation_protocol.md`
- estado real do projeto e evidências: `docs/IMPLEMENTATION_PROGRESS.md`
- implementação da página: `scoutpraia/pages/tagging.py`
