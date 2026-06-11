---
source_id_operacional: IHF_RULES_BH_2026_PT_TRANSLATION
source_id_normativo: IHF_RULES_BH_2026_EN
titulo: Regras de Handebol de Praia 2026 - Tradução 29 de maio de 2026
organizacao_normativa: IHF
idioma: pt-BR
tipo: Markdown processado - Parte 04
nivel_de_confiabilidade: B operacional / apoio em portugues
regra_de_conflito: prevalece o PDF oficial IHF em ingles
arquivo_original: fontes/01_ihf_regras/Regras de Handebol de Praia 2026 - Tradução 29 de maio de 2026.pdf
arquivo_destino_logico: fontes/05_processado/documentos_markdown/IHF_RULES_BH_2026_PT_TRANSLATION_PARTE_04.md
status: parte_04_iniciada_revisao_pendente_contra_pdf_integral
checksum_sha256: PENDENTE - bytes brutos nao acessiveis pelo conector atual
data_processamento: 2026-06-10
---

# IHF_RULES_BH_2026_PT_TRANSLATION — PARTE 04

## Escopo desta parte

Esta parte processa, em formato operacional para RAG, os seguintes blocos da tradução PT das regras IHF 2026:

- Regra 8 — Faltas e Condutas Antidesportivas;
- Regra 9 — O Gol e Decisão do Resultado do Jogo.

Observação: revisar contra o PDF integral antes do chunking final.

## Regra 8 — Faltas e Condutas Antidesportivas

### Função da regra

A Regra 8 define faltas, contatos ilegais e condutas antidesportivas no handebol de praia. Ela orienta a diferença entre contato permitido, infração progressiva, conduta antidesportiva, conduta grave e situações que exigem punição disciplinar.

### Pontos operacionais para recuperação

- Usar esta regra para perguntas sobre contato corporal, bloqueio, empurrão, segurar, impedir deslocamento e ações perigosas.
- Diferenciar falta comum de conduta antidesportiva.
- Diferenciar conduta antidesportiva de conduta grave ou extremamente antidesportiva.
- Quando a pergunta envolver sanção, combinar esta regra com a Regra 16 — Punições.
- Quando a pergunta envolver os últimos 15 segundos ou Golden Goal, combinar esta regra com a atualização IHF 2026.

### Uso no agente

Usar esta seção para perguntas sobre faltas, condutas, punição disciplinar, contato ilegal, proteção da integridade física das atletas e interpretação de comportamento antidesportivo.

## Regra 9 — O Gol e Decisão do Resultado do Jogo

### Função da regra

A Regra 9 define quando um gol é válido e como o resultado do jogo é decidido no handebol de praia. Ela é essencial porque o beach handball possui pontuação por períodos, Gol de Ouro e Shoot-out.

### Pontos operacionais para recuperação

- Usar esta regra para perguntas sobre validade do gol.
- Usar esta regra para perguntas sobre pontuação de período.
- Usar esta regra para explicar por que cada período vale separadamente.
- Usar esta regra para explicar vitória por 2–0 quando a mesma equipe vence os dois períodos.
- Usar esta regra para explicar empate em períodos e decisão por Shoot-out.
- Usar esta regra junto com a Regra 2 para perguntas sobre Gol de Ouro.

### Pontuação e decisão

Cada período é decidido separadamente. A equipe vencedora de cada período recebe 1 ponto. Se uma equipe vence os dois períodos, vence a partida por 2–0. Se cada equipe vence um período, a partida precisa de um vencedor e o Shoot-out é usado.

Quando um período termina empatado, utiliza-se o Gol de Ouro para decidir o vencedor daquele período. O jogo recomeça com tiro de árbitro.

### Uso no agente

Usar esta seção para perguntas sobre gol válido, resultado de período, resultado final, vitória por 2–0, empate em períodos, Gol de Ouro e Shoot-out.

## Controle de chunking sugerido

Chunks recomendados desta parte:

- CHUNK_IHF_PT_017_REGRA_8_FALTAS_CONTATO_ILEGAL
- CHUNK_IHF_PT_018_REGRA_8_CONDUTA_ANTIDESPORTIVA
- CHUNK_IHF_PT_019_REGRA_8_CONDUTA_GRAVE_E_SANCOES
- CHUNK_IHF_PT_020_REGRA_8_ULTIMOS_15_SEGUNDOS_GOLDEN_GOAL
- CHUNK_IHF_PT_021_REGRA_9_GOL_VALIDO
- CHUNK_IHF_PT_022_REGRA_9_DECISAO_PERIODO_GOL_DE_OURO
- CHUNK_IHF_PT_023_REGRA_9_SHOOTOUT_RESULTADO_FINAL

Metadados obrigatórios por chunk:

source_id_normativo \= IHF_RULES_BH_2026_EN
source_id_operacional \= IHF_RULES_BH_2026_PT_TRANSLATION
source_id_complementar \= IHF_UPDATE_BH_2026_04 quando o trecho envolver últimos 15 segundos ou Golden Goal 2026
idioma \= pt-BR
nivel \= B operacional / apoio em português
regra_de_conflito \= prevalece IHF inglês
revisao \= pendente contra PDF integral
