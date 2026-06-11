---
source_id_operacional: IHF_RULES_BH_2026_PT_TRANSLATION
source_id_normativo: IHF_RULES_BH_2026_EN
titulo: Regras de Handebol de Praia 2026 - Tradução 29 de maio de 2026
organizacao_normativa: IHF
idioma: pt-BR
tipo: Markdown processado - Parte 03
nivel_de_confiabilidade: B operacional / apoio em portugues
regra_de_conflito: prevalece o PDF oficial IHF em ingles
arquivo_original: fontes/01_ihf_regras/Regras de Handebol de Praia 2026 - Tradução 29 de maio de 2026.pdf
arquivo_destino_logico: fontes/05_processado/documentos_markdown/IHF_RULES_BH_2026_PT_TRANSLATION_PARTE_03.md
status: parte_03_iniciada_revisao_pendente_contra_pdf_integral
checksum_sha256: PENDENTE - bytes brutos nao acessiveis pelo conector atual
data_processamento: 2026-06-10
---

# IHF_RULES_BH_2026_PT_TRANSLATION — PARTE 03

## Escopo desta parte

Esta parte processa, em formato operacional para RAG, os seguintes blocos da tradução PT das regras IHF 2026:

- Regra 5 — O Goleiro;
- Regra 6 — A Área de Gol;
- Regra 7 — Jogando a Bola e Jogo Passivo.

Observação: revisar contra o PDF integral antes do chunking final.

## Regra 5 — O Goleiro

### Função da regra

A Regra 5 define as ações permitidas e proibidas ao goleiro no handebol de praia, especialmente em relação à área de gol, participação no jogo e transições entre função de goleiro e jogador de linha.

### Pontos operacionais para recuperação

- O goleiro tem permissões específicas dentro da área de gol.
- Fora da área de gol, o goleiro deve respeitar as regras aplicáveis aos jogadores de linha.
- A entrada e saída do goleiro deve respeitar a área própria de substituição, conforme a Regra 1 e a Regra 4.
- Em perguntas sobre substituição de goleiro, combinar esta regra com as regras de área de substituição.

### Uso no agente

Usar esta seção para perguntas sobre o que o goleiro pode ou não pode fazer, entrada e saída de goleiro, participação fora da área e relação entre goleiro e jogador de linha/especialista.

## Regra 6 — A Área de Gol

### Função da regra

A Regra 6 define o uso da área de gol no handebol de praia. Ela estabelece quem pode estar na área de gol, como a bola pode ser jogada nessa região e quais consequências existem quando jogadores de linha invadem ou usam a área indevidamente.

### Pontos operacionais para recuperação

- A área de gol tem regras específicas e deve ser tratada como zona especial da quadra.
- O goleiro possui permissões próprias dentro da área de gol.
- Jogadores de linha não devem usar a área de gol para obter vantagem indevida.
- Situações envolvendo invasão, defesa, arremesso, posse e reinício devem ser respondidas com base nesta regra e nas regras de tiro de meta, tiro livre e tiro de 6 metros quando aplicável.

### Uso no agente

Usar esta seção para perguntas sobre invasão da área, bola na área de gol, ação do goleiro, vantagem obtida na área e reinício correto após infração na área de gol.

## Regra 7 — Jogando a Bola e Jogo Passivo

### Função da regra

A Regra 7 define como a bola pode ser jogada, controlada, passada, conduzida e disputada. Também trata do jogo passivo, ou seja, situações em que uma equipe mantém a posse sem intenção clara de atacar ou arremessar ao gol.

### Pontos operacionais para recuperação

- Usar esta regra para perguntas sobre posse, condução, passe, controle da bola e ações permitidas com a bola.
- Usar esta regra junto com a atualização IHF 2026 para responder sobre jogo passivo.
- A atualização IHF 2026 esclarece que, após o gesto de advertência de jogo passivo, a equipe tem no máximo quatro passes para arremessar ao gol.
- Se a equipe não arremessar dentro desse limite, deve ser marcado tiro livre contra a equipe em posse.
- A regra também deve ser usada quando houver dúvida sobre atrasar reinício, evitar clara chance de gol ou passar a bola deliberadamente em vez de finalizar.

### Uso no agente

Usar esta seção para perguntas sobre jogar a bola, limite de posse, jogo passivo, advertência de passivo, quatro passes após advertência, perda de posse e tiro livre por passividade.

## Controle de chunking sugerido

Chunks recomendados desta parte:

- CHUNK_IHF_PT_011_REGRA_5_GOLEIRO_PERMISSOES
- CHUNK_IHF_PT_012_REGRA_5_GOLEIRO_SUBSTITUICAO_ESPECIALISTA
- CHUNK_IHF_PT_013_REGRA_6_AREA_DE_GOL_USO_E_INVASAO
- CHUNK_IHF_PT_014_REGRA_6_AREA_DE_GOL_REINICIO
- CHUNK_IHF_PT_015_REGRA_7_JOGANDO_A_BOLA
- CHUNK_IHF_PT_016_REGRA_7_JOGO_PASSIVO_ATUALIZACAO_2026

Metadados obrigatórios por chunk:

source_id_normativo \= IHF_RULES_BH_2026_EN
source_id_operacional \= IHF_RULES_BH_2026_PT_TRANSLATION
source_id_complementar \= IHF_UPDATE_BH_2026_04 quando o trecho envolver jogo passivo 2026
idioma \= pt-BR
nivel \= B operacional / apoio em português
regra_de_conflito \= prevalece IHF inglês
revisao \= pendente contra PDF integral
