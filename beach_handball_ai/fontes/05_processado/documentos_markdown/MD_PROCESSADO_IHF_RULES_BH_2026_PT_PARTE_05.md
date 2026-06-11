---
source_id_operacional: IHF_RULES_BH_2026_PT_TRANSLATION
source_id_normativo: IHF_RULES_BH_2026_EN
titulo: Regras de Handebol de Praia 2026 - Tradução 29 de maio de 2026
organizacao_normativa: IHF
idioma: pt-BR
tipo: Markdown processado - Parte 05
nivel_de_confiabilidade: B operacional / apoio em portugues
regra_de_conflito: prevalece o PDF oficial IHF em ingles
arquivo_original: fontes/01_ihf_regras/Regras de Handebol de Praia 2026 - Tradução 29 de maio de 2026.pdf
arquivo_destino_logico: fontes/05_processado/documentos_markdown/IHF_RULES_BH_2026_PT_TRANSLATION_PARTE_05.md
status: parte_05_iniciada_revisao_pendente_contra_pdf_integral
checksum_sha256: PENDENTE - bytes brutos nao acessiveis pelo conector atual
data_processamento: 2026-06-10
---

# IHF_RULES_BH_2026_PT_TRANSLATION — PARTE 05

## Escopo desta parte

Esta parte processa, em formato operacional para RAG, os seguintes blocos da tradução PT das regras IHF 2026:

- Regra 10 — Tiro de Árbitro;
- Regra 11 — Tiro de Lateral;
- Regra 12 — Tiro de Meta;
- Regra 13 — Tiro Livre;
- Regra 14 — Tiro de 6 Metros;
- Regra 15 — Instruções Gerais para Execução dos Tiros;
- Regra 16 — Punições;
- Regra 17 — Os Árbitros;
- Regra 18 — O Cronometrista e o Secretário.

Observação: revisar contra o PDF integral antes do chunking final.

## Regras 10 a 15 — Tiros e reinícios

### Função deste bloco

As Regras 10 a 15 organizam os reinícios do jogo e a execução dos tiros no handebol de praia.

### Regra 10 — Tiro de Árbitro

Usar para perguntas sobre início de período, reinício no Gol de Ouro e situações em que o árbitro deve reiniciar o jogo por meio do tiro de árbitro.

### Regra 11 — Tiro de Lateral

Usar para perguntas sobre saída da bola pela linha lateral, local de execução, posição dos jogadores e reinício correto pela lateral.

### Regra 12 — Tiro de Meta

Usar para perguntas sobre reinício pelo goleiro/equipe defensora, bola que sai pela linha de fundo e situações em que a posse deve reiniciar a partir da área de gol.

### Regra 13 — Tiro Livre

Usar para perguntas sobre infrações comuns, reinício após falta, jogo passivo, execução do tiro livre e local de cobrança.

### Regra 14 — Tiro de 6 Metros

Usar para perguntas sobre clara chance de gol impedida irregularmente, sanções que geram tiro de 6 metros e situações especiais dos últimos 15 segundos quando combinadas com a atualização IHF 2026.

### Regra 15 — Instruções Gerais para Execução dos Tiros

Usar para perguntas sobre posicionamento, apito, execução correta, infrações durante a cobrança e condições gerais de tiros de lateral, meta, livre e 6 metros.

## Regra 16 — Punições

### Função da regra

A Regra 16 define as punições disciplinares aplicáveis a jogadores e oficiais. Ela deve ser usada junto com a Regra 8 quando a pergunta envolver falta, conduta antidesportiva, conduta grave ou comportamento extremamente antidesportivo.

### Pontos operacionais para recuperação

- Usar para perguntas sobre advertência, exclusão/desqualificação e sanções disciplinares.
- Usar junto com Regra 8 para classificar gravidade da conduta.
- Usar junto com a atualização IHF 2026 para últimos 15 segundos, Golden Goal e arremesso na cabeça da goleira.
- Diferenciar consequência técnica do jogo, como tiro livre ou tiro de 6 metros, da punição disciplinar ao atleta/oficial.

### Uso no agente

Usar esta seção para perguntas sobre punição, sanção, desqualificação, conduta grave e consequências disciplinares de infrações.

## Regras 17 e 18 — Arbitragem, cronometrista e secretário

### Regra 17 — Os Árbitros

A Regra 17 define a autoridade, função e responsabilidades dos árbitros durante a partida. Deve ser usada para perguntas sobre decisão dos árbitros, sinalização, controle do jogo, aplicação de regras e autoridade para interromper, reiniciar ou punir situações conforme o regulamento.

### Regra 18 — O Cronometrista e o Secretário

A Regra 18 define responsabilidades da mesa, incluindo controle de tempo, registro, placar, substituições e apoio administrativo à arbitragem.

### Uso no agente

Usar estas seções para perguntas sobre quem controla o tempo, quem registra a súmula/boletim, quem controla substituições, quem decide em quadra e qual o papel da mesa em relação aos árbitros.

## Controle de chunking sugerido

Chunks recomendados desta parte:

- CHUNK_IHF_PT_024_REGRA_10_TIRO_DE_ARBITRO
- CHUNK_IHF_PT_025_REGRA_11_TIRO_DE_LATERAL
- CHUNK_IHF_PT_026_REGRA_12_TIRO_DE_META
- CHUNK_IHF_PT_027_REGRA_13_TIRO_LIVRE
- CHUNK_IHF_PT_028_REGRA_14_TIRO_DE_6_METROS
- CHUNK_IHF_PT_029_REGRA_15_EXECUCAO_DOS_TROS
- CHUNK_IHF_PT_030_REGRA_16_PUNICOES
- CHUNK_IHF_PT_031_REGRA_17_ARBITROS
- CHUNK_IHF_PT_032_REGRA_18_CRONOMETRISTA_SECRETARIO

Metadados obrigatórios por chunk:

source_id_normativo \= IHF_RULES_BH_2026_EN
source_id_operacional \= IHF_RULES_BH_2026_PT_TRANSLATION
source_id_complementar \= IHF_UPDATE_BH_2026_04 quando o trecho envolver últimos 15 segundos, Golden Goal, cabeça da goleira ou equipamentos 2026
idioma \= pt-BR
nivel \= B operacional / apoio em português
regra_de_conflito \= prevalece IHF inglês
revisao \= pendente contra PDF integral
