# Fontes do ScoutPraia

Este diretório registra as fontes usadas para construir e revisar a taxonomia, os KPIs e os relatórios do ScoutPraia.

Regra de uso:

- regra oficial prevalece sobre interpretação prática
- evidência científica sustenta indicadores, mas não substitui validação em vídeo
- decisão técnica do treinador deve ser identificada como decisão prática
- hipótese sem fonte ou sem teste não entra como KPI final

## Fontes iniciais

| Código | Tipo | Fonte | Arquivo local | Uso no ScoutPraia |
| --- | --- | --- | --- | --- |
| `SRC-IHF-RULES` | regra oficial | IHF Rules of the Game — Beach Handball | `ihf_rules_beach_handball.pdf` | pontuação, set, shoot-out, ações especiais e critérios oficiais |
| `SRC-NOTATIONAL-BH` | literatura científica | Notational analysis of beach handball; Women's beach handball game statistics | `notational_analysis_bh_iannaccone_2022.pdf`; `womens_bh_statistics_kazan_2022.pdf` | indicadores de finalização, zonas, eficiência e padrões de jogo |
| `SRC-OBS-MEASUREMENT` | metodologia | A Primer on Observational Measurement; Development and Validation of an Observational Game Analysis Tool with Artificial Intelligence for Handball: Handball.ai | `primer_observational_measurement_2017.html`; `validation_observational_instrument_handball_2023.html` | confiabilidade, validade e controle de ambiguidade observacional |
| `SRC-RAG-LEWIS` | IA/RAG | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | ausente (Fase 2) | uso de fontes externas para reduzir dependência da memória interna da IA |
| `SRC-RAG-STRUCTURED` | IA/RAG | Reducing hallucination in structured outputs via Retrieval-Augmented Generation | `2024.naacl-industry.19.pdf` | auditoria de saídas estruturadas, como taxonomias, campos e relatórios |
| `SRC-OPENAI-EVALS` | avaliação de IA | OpenAI Evals / Working with evals | `Working-with-evals.md` | referência conceitual para ciclo de teste, medição de erro e iteração de prompts; plataforma oficial em deprecação |
| `SRC-SYNTHESIS-BH` | curadoria secundária (síntese interna) | Scout de Handebol de Areia: Fontes Fortes | `Scout de Handebol de Areia_ Fontes Fortes.md` | mapa de pesquisa para `SRC-NOTATIONAL-BH` e `SRC-OBS-MEASUREMENT`; thresholds para `validation_protocol.md`; não citar como fonte primária |

## Artefatos derivados (não são fontes primárias)

| Arquivo | Origem | Limitações | Quando usar |
| --- | --- | --- | --- |
| `regras.md` | derivado textual de `SRC-IHF-RULES` com artefatos de extração | cabeçalhos de página interrompem texto; seções de imagem ausentes; qualidade inferior ao PDF | somente busca textual local e pré-indexação de Fase 2; nunca preferir ao PDF para consultas normativas |

## Links

- IHF Rules of the Game — Beach Handball: https://www.ihf.info/sites/default/files/2026-03/09B%20-%20Rules%20of%20the%20Game_Beach%20Handball_E.pdf
- Notational analysis of beach handball (DOI `10.5114/hm.2021.101757`): https://hummov.awf.wroc.pl/Notational-analysis-of-beach-handball%2C130277%2C0%2C2.html
- Women's beach handball game statistics (DOI `10.26582/k.54.1.12`): https://hrcak.srce.hr/clanak/403495
- A Primer on Observational Measurement (DOI `10.1177/1073191116635807`): https://pmc.ncbi.nlm.nih.gov/articles/PMC5426358/
- Development and Validation of an Observational Game Analysis Tool with Artificial Intelligence for Handball: Handball.ai (DOI `10.3390/s23156714`): https://pmc.ncbi.nlm.nih.gov/articles/PMC10422213/
- Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks: https://arxiv.org/abs/2005.11401
- Reducing hallucination in structured outputs via Retrieval-Augmented Generation: https://aclanthology.org/2024.naacl-industry.19/
- OpenAI Evals: https://developers.openai.com/api/docs/guides/evals

## Notas de uso

- `Working-with-evals.md` é um snapshot local da documentação oficial usada para rastreabilidade de `SRC-OPENAI-EVALS`.
- Esse arquivo registra que a plataforma Evals está em deprecação e ficará `read-only` em `2026-10-31`, com desligamento previsto para `2026-11-30`.
- No ScoutPraia, `SRC-OPENAI-EVALS` deve ser usado como referência conceitual de avaliação, não como dependência estratégica do MVP nem como requisito de plataforma futura.
