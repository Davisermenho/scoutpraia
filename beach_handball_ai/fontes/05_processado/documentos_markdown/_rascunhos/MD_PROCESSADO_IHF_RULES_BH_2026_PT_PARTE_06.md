---
source_id_operacional: IHF_RULES_BH_2026_PT_TRANSLATION
source_id_normativo: IHF_RULES_BH_2026_EN
titulo: Regras de Handebol de Praia 2026 - Tradução 29 de maio de 2026
organizacao_normativa: IHF
idioma: pt-BR
tipo: Markdown processado - Parte 06
nivel_de_confiabilidade: B operacional / apoio em portugues
regra_de_conflito: prevalece o PDF oficial IHF em ingles
arquivo_original: fontes/01_ihf_regras/Regras de Handebol de Praia 2026 - Tradução 29 de maio de 2026.pdf
arquivo_destino_logico: fontes/05_processado/documentos_markdown/IHF_RULES_BH_2026_PT_TRANSLATION_PARTE_06.md
status: parte_06_iniciada_revisao_pendente_contra_pdf_integral
checksum_sha256: PENDENTE - bytes brutos nao acessiveis pelo conector atual
data_processamento: 2026-06-10
---

# IHF_RULES_BH_2026_PT_TRANSLATION — PARTE 06

## Escopo desta parte

Esta parte processa, em formato operacional para RAG, os apêndices normativos associados às Regras IHF de Handebol de Praia 2026:

- Sinais Manuais dos Árbitros;
- Esclarecimentos às Regras do Jogo;
- Regulamento da Área de Substituição;
- Regulamento do Uniforme dos Atletas;
- Regulamento da Qualidade da Areia e da Iluminação.

Observação: revisar contra o PDF integral antes do chunking final.

## Apêndice — Sinais Manuais dos Árbitros

### Função do apêndice

Os sinais manuais padronizam a comunicação dos árbitros durante o jogo. Eles servem para tornar decisões compreensíveis para atletas, comissões, mesa e público.

### Uso no agente

Usar este bloco para perguntas sobre sinalização arbitral, comunicação visual de decisões, indicação de tiros, punições, gol, jogo passivo, time-out e outras decisões de arbitragem.

## Apêndice — Esclarecimentos às Regras do Jogo

### Função do apêndice

Os esclarecimentos ajudam a interpretar situações específicas das regras. Devem ser usados quando a regra principal não for suficiente para responder uma situação concreta.

### Uso no agente

Usar este bloco para perguntas de interpretação, casos-limite, aplicação prática das regras, decisões em situações incomuns e dúvidas sobre o espírito da regra.

## Apêndice — Regulamento da Área de Substituição

### Função do apêndice

O regulamento da área de substituição detalha como jogadores e goleiros devem entrar e sair, como a mesa controla substituições e quais condutas podem gerar infrações.

### Pontos operacionais para recuperação

- Jogadores de linha devem entrar pela área de substituição da equipe.
- Goleiros entram pela linha lateral da área de gol de sua própria equipe, pelo lado da área de substituição.
- O controle da área de substituição envolve mesa, árbitros e oficiais conforme o caso.
- Substituições irregulares devem ser avaliadas conforme as regras de punição e reinício.

### Uso no agente

Usar este bloco para perguntas sobre substituição, entrada e saída de atletas, troca de goleiro/especialista, infração de substituição e atuação da mesa na área de substituição.

## Apêndice — Regulamento do Uniforme dos Atletas

### Função do apêndice

O regulamento do uniforme estabelece padrões de identificação, segurança, cores, numeração e equipamentos permitidos ou proibidos.

### Relação com atualização IHF 2026

Deve ser lido junto com a atualização IHF 2026, que esclarece regras sobre numeração, meias, sand socks, calçados, itens rígidos, mangas de compressão, calças térmicas, kinesio tape e bandagens.

### Uso no agente

Usar este bloco para perguntas sobre uniforme, número, contraste, equipamentos, proteção, meias, itens proibidos, sand socks e padronização visual da equipe.

## Apêndice — Regulamento da Qualidade da Areia e da Iluminação

### Função do apêndice

O regulamento da qualidade da areia e da iluminação define condições mínimas para segurança, visibilidade e praticabilidade do jogo.

### Pontos operacionais para recuperação

- A areia deve ser adequada ao jogo, nivelada, segura e sem objetos que causem lesão.
- A profundidade, textura e compactação da areia influenciam segurança e desempenho.
- A iluminação deve permitir visibilidade suficiente para atletas, árbitros, mesa e público.
- Para jogos noturnos, usar o parâmetro de iluminação previsto nas regras e no apêndice.

### Uso no agente

Usar este bloco para perguntas sobre segurança da quadra, areia, profundidade, objetos perigosos, iluminação, jogos noturnos e condições mínimas para realização da partida.

## Controle de chunking sugerido

Chunks recomendados desta parte:

- CHUNK_IHF_PT_033_APENDICE_SINAIS_MANUAIS_ARBITROS
- CHUNK_IHF_PT_034_APENDICE_ESCLARECIMENTOS_REGRAS
- CHUNK_IHF_PT_035_APENDICE_AREA_DE_SUBSTITUICAO
- CHUNK_IHF_PT_036_APENDICE_UNIFORME_ATLETAS
- CHUNK_IHF_PT_037_APENDICE_AREIA_ILUMINACAO

Metadados obrigatórios por chunk:

source_id_normativo \= IHF_RULES_BH_2026_EN
source_id_operacional \= IHF_RULES_BH_2026_PT_TRANSLATION
source_id_complementar \= IHF_UPDATE_BH_2026_04 quando o trecho envolver equipamentos 2026
idioma \= pt-BR
nivel \= B operacional / apoio em português
regra_de_conflito \= prevalece IHF inglês
revisao \= pendente contra PDF integral

## Status do processamento inicial das regras

Com esta parte, o processamento inicial da tradução PT das Regras IHF 2026 cobre:

- Parte 01 — metadados, índice, prólogo, Regra 1 e início da Regra 2;
- Parte 02 — continuação da Regra 2, Regra 3 e Regra 4;
- Parte 03 — Regra 5, Regra 6 e Regra 7;
- Parte 04 — Regra 8 e Regra 9;
- Parte 05 — Regras 10 a 18;
- Parte 06 — apêndices.

Próxima etapa recomendada: revisão cruzada contra o PDF integral antes de criar os chunks finais.
