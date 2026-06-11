# Plano de ação validado

## 1. Criar o Registro de Fontes Fortes

### Objetivo

Criar uma base auditável chamada `fontes_oficiais`, onde cada documento usado pelo agente tenha origem, versão, tema, confiabilidade e permissão de uso.

Fontes de entrada obrigatórias para esse registro:

- `docs/sources/` como catálogo canônico já usado pelo ScoutPraia
- `beach_handball_ai/fontes/` como corpus operacional de trabalho

Regra operacional:

- `docs/sources/README.md` permanece como referência canônica do repositório
- `fontes_oficiais` deve manter rastreabilidade entre códigos `SRC-*` do repositório e `source_id` do corpus operacional

A IHF mantém uma página oficial de **Rules of the Game - Beach Handball** e indica que devem ser observados também os apêndices de sinais dos árbitros, esclarecimentos das regras, área de substituição, uniforme dos atletas, qualidade da areia e iluminação. ([ihf.info](https://www.ihf.info/node/4653))

Além disso, a IHF publicou mudanças para o Beach Handball com entrada em vigor em **1º de abril de 2026**, incluindo ajustes sobre jogo passivo, últimos 15 segundos, Golden Goal, arremesso na cabeça da goleira e equipamentos. ([ihf.info](https://www.ihf.info/media-center/news/new-rules-beach-handball-and-wheelchair-handball-be-observed-1-april-and-1-july))

### Estrutura da pasta

```text
beach_handball_ai/
  beach_handball_ai/fontes
    00_registro/
      fontes_oficiais.csv
      fontes_oficiais.xlsx
    01_ihf_regras/
      regras_ihf_beach_handball_2026.pdf
      apendice_sinais_arbitros.pdf
      esclarecimentos_regras.pdf
      area_substituicao.pdf
      uniformes_atletas.pdf
      qualidade_areia_iluminacao.pdf
      atualizacoes_ihf_2026.md
    02_ehf_tecnico/
      refereeing_beach_handball.pdf
      shootout_psychological_pressure.pdf
      ultimate_school_handball_2025.pdf
      mini_beach_handball_info_sheet.pdf
    03_cbhb_brasil/
      regulamento_cbhb_2026.pdf
      regras_cbhb_handebol_praia.pdf
      regulamento_circuito_brasileiro.pdf
    04_fontes_proprias_cepraea/
      glossario_tecnico_cepraea.md
      playbook_cepraea.md
      scout_schema.md
      criterios_taticos_cepraea.md
    05_processado/
      documentos_markdown/
      chunks_jsonl/
      manifest_checksums.json
```

### Tabela `fontes_oficiais`

Use os campos que você definiu, mas acrescente alguns campos de controle para impedir bagunça e fonte solta.

```csv
source_id,título,organização,tipo,data,versão,link,uso_permitido,tema,nível_de_confiabilidade,observação,arquivo_local,status,checksum_sha256,data_coleta
```

### Níveis de confiabilidade

| Nível | Tipo de fonte | Uso no agente |
| :---: | --- | --- |
| A | IHF oficial: regras, apêndices, atualizações oficiais | Pode fundamentar resposta normativa |
| A | CBHb oficial: regulamentos nacionais e arbitragem no Brasil | Pode fundamentar competições brasileiras |
| B | EHF oficial: publicações técnicas, educacionais e pesquisa | Pode fundamentar treino, arbitragem e formação |
| C | Material próprio CEPRAEA: glossário, playbook, scout | Pode fundamentar linguagem interna e método da equipe |
| D | Artigos, blogs, vídeos, redes sociais | Não entra como "fonte forte"; só referência secundária |
| Rejeitada | Fonte sem autoria, sem data, cópia antiga ou material desatualizado | Não entra no RAG |

## 2. Onde encontrar o material

### 2.1 Regras oficiais IHF Beach Handball

Fonte principal: página oficial da IHF de regras do Beach Handball. Baixe o PDF vigente e os apêndices indicados na própria página: sinais dos árbitros, esclarecimentos, área de substituição, uniforme, areia e iluminação. ([ihf.info](https://www.ihf.info/node/4653))

Registro sugerido:

```csv
IHF_RULES_BH_2026,Rules of the Game - Beach Handball,IHF,Regra oficial,2026-03-01,2026,link oficial IHF,uso interno educacional,regra,A,Documento normativo principal,beach_handball_ai/fontes01_ihf_regras/regras_ihf_beach_handball_2026.pdf,validado,,2026-06-10
```

### 2.2 Atualizações IHF publicadas em 2026

Fonte principal: notícia oficial da IHF sobre novas regras do Beach Handball em vigor a partir de **1º de abril de 2026**. Essa fonte deve virar um arquivo próprio `atualizacoes_ihf_2026.md`, porque ela explica mudanças que podem alterar respostas sobre regra, arbitragem e interpretação. ([ihf.info](https://www.ihf.info/media-center/news/new-rules-beach-handball-and-wheelchair-handball-be-observed-1-april-and-1-july))

Registro sugerido:

```csv
IHF_UPDATE_BH_2026_04,New rules for beach handball to be observed from 1 April 2026,IHF,Atualização oficial,2026-03-13,2026,link oficial IHF,uso interno educacional,regra,A,Atualizações sobre jogo passivo, últimos 15s, Golden Goal, cabeça da goleira e uniforme,beach_handball_ai/fontes01_ihf_regras/atualizacoes_ihf_2026.md,validado,,2026-06-10
```

### 2.3 Materiais técnicos EHF/IHF

Fonte principal EHF: página **EHF Beach Handball Publications**. Ela reúne publicações sobre arbitragem, pressão psicológica em shoot-outs, ensino do jogo em escolas e mini beach handball. ([beach.eurohandball.com](https://beach.eurohandball.com/education-teaching/publications/))

Baixar primeiro:

- `Refereeing in Beach Handball`
- `Understanding Psychological Pressure in Beach Handball Shootouts`
- `Ultimate School Handball 2025`
- `Mini Beach Handball Info Sheet 2020`

Esses materiais entram como **nível B**, porque são fontes oficiais e técnicas, mas não substituem regra oficial IHF.

### 2.4 Materiais CBHb

> A CBHb deve entrar porque você atua no Brasil e competições nacionais/estaduais podem ter regulamento próprio. A página do Departamento Técnico da CBHb lista documentos como **Regulamento 2026** e regulamentos específicos; a Diretoria de Arbitragem lista materiais de regras de jogo de handebol de praia. ([CBHb](https://cbhb.org.br/governanca/141/departamento-tecnico?utm_source=chatgpt.com))

Use a CBHb para:

- regulamento brasileiro
- regras adotadas no Brasil
- sistema de disputa
- exigências de inscrição
- critérios administrativos
- documentos de arbitragem nacional

### 2.5 Glossário técnico próprio

Esse material você não "encontra": você cria.

Arquivo: `glossario_tecnico_cepraea.md`

Estrutura obrigatória:

```md
# Glossário Técnico CEPRAEA

## Giro

Definição:
Uso no treino:
Critério de execução:
Erros comuns:
Fonte de regra relacionada:
Fonte técnica relacionada:
Observação CEPRAEA:

## Aérea

Definição:
Uso no treino:
Critério de execução:
Erros comuns:
Fonte de regra relacionada:
Fonte técnica relacionada:
Observação CEPRAEA:

## Shoot-out

Definição:
Uso no treino:
Critério de execução:
Erros comuns:
Fonte de regra relacionada:
Fonte técnica relacionada:
Observação CEPRAEA:
```

Termos iniciais:

- giro
- aérea
- shoot-out
- especialista
- defensora
- goleira
- `3:0`
- `2:1`
- `4:0`
- devolução
- bloqueio
- transição
- Golden Goal
- jogo passivo
- últimos 15 segundos
- `6 metros`
- substituição
- pontuação de 1 ponto
- pontuação de 2 pontos

## 3. Construir primeiro o agente textual

### Decisão técnica correta

Comece com **agente textual + RAG**, não com vídeo. A própria documentação da OpenAI descreve retrieval como busca semântica em dados próprios usando vector stores, capaz de encontrar resultados semanticamente parecidos mesmo com poucas palavras iguais. ([OpenAI Developers](https://developers.openai.com/api/docs/guides/retrieval))

Para o MVP local, use **Chroma**. A documentação do Chroma confirma que ele armazena textos, embeddings e metadados em coleções, além de permitir consulta por similaridade. ([Chroma Docs](https://docs.trychroma.com/docs/overview/getting-started))

Use **Postgres/pgvector** quando o projeto evoluir para produção, banco relacional, dashboard, usuários, histórico e scout estruturado. O pgvector permite armazenar vetores junto com outros dados no Postgres e fazer busca de similaridade exata ou aproximada. ([GitHub](https://github.com/pgvector/pgvector))

## 4. Implementação do MVP textual

### Etapa 1 - Criar o registro real das fontes

Entregáveis:

- `beach_handball_ai/fontes00_registro/fontes_oficiais.csv`
- `beach_handball_ai/fontes00_registro/fontes_oficiais.xlsx`
- `beach_handball_ai/fontes05_processado/manifest_checksums.json`

Critério de aceite:

Aprovado se:

- toda fonte tiver `source_id` único
- toda fonte tiver organização
- toda fonte tiver data ou versão
- toda fonte tiver tema
- toda fonte tiver nível de confiabilidade
- toda fonte tiver arquivo local
- nenhuma fonte D ou rejeitada entrar no RAG principal

* Registrar as fontes em `docs/sources` 
* Registrar as fontes em `beach_handball_ai/fontes/`

### Etapa 2 - Converter documentos para texto limpo

Cada PDF deve virar `.md` ou `.txt` em `beach_handball_ai/fontes05_processado/documentos_markdown/`, mantendo o `source_id` original para rastreabilidade.

Exemplo:

```text
regras_ihf_beach_handball_2026.pdf
-> regras_ihf_beach_handball_2026.md
```

Critério de aceite:

Aprovado se:

- o texto extraído preserva títulos
- tabelas importantes foram revisadas manualmente
- regras e apêndices continuam identificáveis
- cada trecho mantém o `source_id` original
- documentos antigos ficam marcados como desatualizados

* `beach_handball_ai/fontes/01_ihf_regras/`
* `beach_handball_ai/fontes/02_ehf_tecnico/`
* `beach_handball_ai/fontes/03_cbhb_brasil/`
* `beach_handball_ai/fontes/04_fontes_proprias_cepraea/`
* `docs/sources` 

### Etapa 3 - Separar por tema

Cada trecho precisa receber metadados:

```json
{
  "source_id": "IHF_RULES_BH_2026",
  "tema": "regra",
  "subtema": "jogo_passivo",
  "organizacao": "IHF",
  "versao": "2026",
  "confiabilidade": "A",
  "arquivo": "regras_ihf_beach_handball_2026.md"
}
```

Temas obrigatórios:

- regra
- arbitragem
- técnica
- tática
- treino
- scout
- nomenclatura
- análise_de_adversário
- cepraea_playbook

Critério de aceite:

Aprovado se:

- 100% dos chunks têm `source_id`
- 100% dos chunks têm tema
- 100% dos chunks têm nível de confiabilidade
- nenhum chunk entra no banco sem metadados

### Etapa 4 - Criar chunks

Tamanho recomendado:

- `500 a 900` tokens por chunk
- sobreposição: `80 a 120` tokens

Regra prática:

- não quebrar uma regra no meio
- não separar título da explicação
- não misturar regra oficial com opinião do treinador no mesmo chunk

Critério de aceite:

Aprovado se:

- cada chunk tem texto compreensível sozinho
- cada chunk aponta para `source_id`
- chunks de regras são separados dos chunks do playbook CEPRAEA
- chunks antigos ou substituídos ficam com `status=deprecated`

### Etapa 5 - Gerar embeddings e salvar no Chroma

Coleções recomendadas:

- `bh_regras`
- `bh_tecnico`
- `bh_glossario`
- `bh_playbook_cepraea`
- `bh_scout`

Metadados obrigatórios por documento:

```json
{
  "source_id": "",
  "titulo": "",
  "organizacao": "",
  "tema": "",
  "nivel_confiabilidade": "",
  "versao": "",
  "data": "",
  "arquivo_local": ""
}
```

Critério de aceite:

- consulta por "jogo passivo" retorna fonte IHF
- consulta por "shoot-out" retorna regra IHF e material EHF
- consulta por "4:0 CEPRAEA" retorna glossário/playbook próprio
- consulta sobre tema inexistente retorna vazio ou baixa confiança

### Etapa 5.1 - Teste de recuperação antes do LLM

Antes de testar o agente completo, execute a busca no Chroma sem resposta do LLM. O objetivo é validar se o banco vetorial recupera as fontes certas.

Para cada pergunta-teste, registrar: pergunta, `top_k` retornado, `source_id` retornado, score/distância, se a fonte correta apareceu no top 3 e se apareceu fonte indevida.

Critério de aceite:

- pelo menos 90% das perguntas respondíveis retornam a fonte correta no top 3
- 100% das perguntas normativas sobre regra retornam IHF antes de EHF/CEPRAEA
- perguntas sem base retornam baixa confiança ou nenhum documento suficiente
- se a recuperação falhar, corrigir fonte, chunk, metadado ou embedding antes de alterar o prompt

### Etapa 6 - Criar regra de resposta do agente

System instruction correta:

```text
Você é um agente textual de apoio ao treinador de handebol de areia.

Responda apenas com base nas fontes recuperadas no contexto.
Toda resposta técnica deve citar source_id, título e organização da fonte.
Quando as fontes não sustentarem a resposta, diga:
"Não encontrado nas fontes disponíveis."
Não use conhecimento geral para completar lacunas.
Não misture handebol de quadra com handebol de areia sem fonte explícita.
Quando houver conflito entre fontes, priorize:
1. IHF vigente;
2. CBHb vigente para competições brasileiras;
3. EHF técnico/educacional;
4. documentos próprios CEPRAEA, apenas para nomenclatura interna.
Quando um termo tiver uso oficial e uso interno CEPRAEA: responder primeiro a definição oficial se a pergunta for sobre regra; responder a definição CEPRAEA se a pergunta citar "no CEPRAEA", "nosso playbook" ou "nossa nomenclatura"; nunca apresentar convenção interna como regra oficial.
```

Critério de aceite:

Aprovado se:

- toda resposta vem com fonte
- perguntas sem base documental recebem "não encontrado"
- o agente não inventa regra
- o agente diferencia regra oficial de convenção interna CEPRAEA

### Etapa 7 - Criar o teste de 30 perguntas

Monte uma planilha:

```csv
id,pergunta,tema,resposta_esperada_tipo,resposta_esperada_resumo,source_id_esperado,deve_responder,deve_recusar,criterio_de_aprovacao,observação
```

#### 30 perguntas-teste

##### Regras oficiais IHF

1. O que caracteriza jogo passivo no Beach Handball?
2. Quantos passes a equipe tem após o sinal de advertência de jogo passivo?
3. O que mudou nas regras de Beach Handball em 1º de abril de 2026?
4. O que acontece se uma equipe interfere deliberadamente nos últimos 15 segundos?
5. Como funciona a punição em situação de Golden Goal?
6. O que acontece se um arremesso livre atinge primeiro a cabeça da goleira?
7. Quais equipamentos são permitidos ou proibidos para atletas na areia?
8. As atletas podem jogar com calçado sintético ou de borracha?
9. O número do uniforme precisa ter contraste visível?
10. Quais apêndices devem ser consultados junto com as regras oficiais?

##### Arbitragem e interpretação

11. Onde encontrar sinais oficiais dos árbitros?
12. Onde encontrar esclarecimentos oficiais das regras?
13. Onde encontrar regras sobre área de substituição?
14. Onde encontrar regras sobre uniforme das atletas?
15. Onde encontrar regras sobre qualidade da areia e iluminação?

##### Técnica e materiais EHF

16. Qual fonte técnica pode ser usada para estudar arbitragem no Beach Handball?
17. Qual fonte pode apoiar estudo de pressão psicológica em shoot-outs?
18. Qual fonte pode apoiar ensino inicial do Beach Handball?
19. Qual fonte pode apoiar trabalho com crianças e mini beach handball?
20. Uma publicação EHF substitui a regra oficial da IHF?

##### Glossário próprio CEPRAEA

21. O que o CEPRAEA chama de "devolução"?
22. O que o CEPRAEA define como sistema ofensivo `4:0`?
23. O que o CEPRAEA define como defesa `3:0`?
24. O que o CEPRAEA define como defesa `2:1`?
25. Qual a diferença entre "aérea" e "giro" no glossário do CEPRAEA?

##### Perguntas que o agente deve recusar

26. Qual foi o treino secreto da seleção alemã antes da final?
27. Qual atleta do CEPRAEA está fisicamente desgastada sem dados de carga?
28. Qual sistema tático garante vitória contra qualquer adversário?
29. Qual regra inventada permite jogar com tênis na areia?
30. Qual jogadora será mais eficiente no próximo jogo sem histórico ou scout?

Critério de aprovação:

Aprovado se:

- 30/30 respostas citam `source_id` ou recusam corretamente
- 0 resposta sem fonte
- 0 regra inventada
- 0 mistura indevida entre regra IHF e convenção CEPRAEA
- pelo menos 5 perguntas sem resposta documental são recusadas corretamente

### Etapa 8 - Criar relatório de avaliação

Arquivo:

`avaliacoes/eval_mvp_textual_001.md`

Modelo:

```md
# Avaliação MVP Textual 001

Data:
Versão do banco:
Quantidade de fontes:
Quantidade de chunks:
Modelo usado:
Banco vetorial:

## Resultado geral

Perguntas testadas: 30
Respostas corretas com fonte:
Recusas corretas:
Alucinações:
Erros de fonte:
Aprovado: sim/não

## Falhas encontradas

- pergunta:
- resposta do agente:
- erro:
- correção necessária:

## Decisão

[ ] Liberado para uso interno
[ ] Reprovado
[ ] Requer nova ingestão de fontes
```

## 5. Ordem correta de execução

1. Baixar regras e apêndices oficiais da IHF.
2. Registrar atualizações IHF de 2026.
3. Baixar publicações EHF técnicas e educacionais.
4. Baixar regulamentos e documentos CBHb relevantes.
5. Criar glossário técnico próprio CEPRAEA.
6. Criar `fontes_oficiais.csv`.
7. Converter PDFs para Markdown.
8. Criar chunks com metadados.
9. Gerar embeddings.
10. Salvar no Chroma.
11. Criar prompt restritivo do agente.
12. Criar as 30 perguntas-teste.
13. Rodar teste de recuperação no Chroma sem LLM.
14. Rodar avaliação do agente textual com as 30 perguntas preenchidas.
15. Corrigir fontes, chunks ou prompt.
16. Só liberar o agente textual quando passar no teste de recuperação, no teste de 30 perguntas e no relatório `eval_mvp_textual_001.md`.

## 6. Resultado final esperado

Ao final, você não terá "uma IA que promete entender handebol de areia". Você terá um **agente textual auditável**, que:

- consulta fontes oficiais
- separa regra, técnica, tática, treino, scout e glossário
- responde com fonte
- recusa quando não tem base
- diferencia IHF, EHF, CBHb e CEPRAEA
- passa por teste objetivo antes de ser usado

## 7. Estratégia de Busca e Validação de Fontes

### 7.1 Protocolo de Busca Ativa (Fontes Nível A)

- **IHF (Normas):** acessar [https://www.ihf.info/beach-handball/rules](https://www.ihf.info/beach-handball/rules). Priorizar download de PDFs vigentes com selo `2026`.
- **CBHb (Nacional):** acessar [https://cbhb.org.br/](https://cbhb.org.br/) -> Governança -> Departamento Técnico. Buscar regulamentos de competições brasileiras 2026.
- **Critério de Validação:** Nível A não depende apenas do domínio do site. Nível A é reservado para documentos normativos oficiais e vigentes da IHF e para regulamentos oficiais vigentes da CBHb quando o contexto for competição brasileira. EHF entra como Nível B para material técnico, educacional, pesquisa e arbitragem, salvo quando o documento for regulamento oficial de competição EHF aplicável ao caso. Documentos técnicos anteriores a 2026 podem ser aceitos se forem oficiais, relevantes e não conflitarem com a regra vigente.

### 7.2 Taxonomia de Fontes (Cobertura Completa)

- **Pilar Regulamentar:** documentos oficiais IHF e CBHb.
- **Pilar Técnico-Tática:** estudos científicos sobre análise notacional, eficácia de arremessos e tomada de decisão só entram no registro quando tiverem título completo, autores, ano, periódico, DOI ou URL, modalidade estudada, amostra, conclusão principal, limitação e uso permitido no agente.
- **Pilar Fisiológico:** estudos sobre carga externa/interna e monitoramento com sensores entram apenas como fonte científica documentada; não podem fundamentar diagnóstico individual de atleta sem dados reais coletados da própria atleta.
- **Pilar Biomecânico:** estudos sobre prevenção de lesões, técnica de goleira, salto, aterrissagem e deslocamento na areia devem ser registrados com referência completa. Enquanto não houver referência completa, ficam como pendência e não entram no RAG principal.

### 7.3 Tabela de Fontes por Categoria

| Categoria | Fonte de Consulta (URL) | Nível de Confiabilidade | Uso no Agente |
| :--- | :--- | :---: | :---: |
| Regras Oficiais | `ihf.info/beach-handball/rules` | A | Normativo |
| Publicações Técnicas | `beach.eurohandball.com/education-teaching/publications/` | B | Técnico |
| Estudos de Desempenho | revistas acadêmicas (Apunts, Frontiers) | C | Referência Científica |

## 8. Status atual do documento

**STATUS: APROVADO COM CORREÇÕES APLICADAS.**

Observação operacional: o documento agora pode orientar a execução do Registro de Fontes Fortes e do MVP textual, mas o agente só pode ser liberado após: preenchimento da planilha de 30 perguntas com respostas esperadas, teste de recuperação no Chroma, relatório `eval_mvp_textual_001.md` e ausência de alucinação nos critérios definidos.
