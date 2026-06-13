---
doc_id: RAG_016
title: "Plano de Organização de Fontes RAG"
status: active
version: "3.0.0"
authority_level: 2
category: RAG
owner: Davi Sermenho
created_at: "2026-06-08"
last_updated: "2026-06-13"
repository: Davisermenho/scoutpraia
tipo: plano_organização_fontes
data_elaboração: 2026-06-08
plan_version_ref: "beach_handball_ai_rag_action_plan_v1.6"
status_ações:
  A1_deletar_morto: CONCLUÍDO
  A2_registrar_regras_md: CONCLUÍDO
  A3_registrar_fontes_fortes: CONCLUÍDO
  A4_baixar_notacional: CONCLUÍDO
  A5_baixar_obs_measurement: CONCLUÍDO
  A6_atualizar_readme: CONCLUÍDO
  A7_coluna_fonte_dicionário: CONCLUÍDO
gaps_residuais:
  G1: RESOLVIDO
  G2: FASE_2_ATIVA
  G3: FASE_2_ATIVA
  G4: RESOLVIDO
  G5: RESOLVIDO_2026-06-12
  G6: MONITORADO
  G7: RESOLVIDO
nota: "Fase 2 desbloqueada em 2026-06-12 (G5 aprovado). Plano v1.6 incorporado na seção 8."
---

# Plano de Organização de Fontes — ScoutPraia

## Resumo Executivo

Plano executado de organização das fontes RAG do ScoutPraia (v2). Todas as 7 ações concluídas; único gap residual ativo era G5 (validação humana), agora fechado.

## Objetivo

Organizar, registrar e validar as fontes primárias do ScoutPraia (regras IHF, literatura notacional, metodologia observacional) para suportar a Fase 2 RAG após o MVP completo.

**Versão:** 2 (corrigida após revisão crítica com evidências)
**Data de elaboração:** `2026-06-08`
**Baseado em estado verificado:** leitura direta de todos os arquivos citados. Toda afirmação tem linha-fonte identificada.
**Para execução por:** agente de IA ou operador humano seguindo as ações em ordem.

---

## Sumário de gaps ativos

| Gap | Status | Próxima ação |
| --- | --- | --- |
| G1 — Taxonomia integralmente em `draft` | RESOLVIDO (2026-06-09) | — |
| G2 — `SRC-RAG-LEWIS` sem arquivo local | DIFERIDO — Fase 2 | iniciar Fase 2 RAG |
| G3 — `SRC-OPENAI-EVALS` em deprecação | DIFERIDO — Fase 2 | substituir na Fase 2 |
| G4 — `008_AUDIT_Matriz_Evidencias.md` sem `SRC-SYNTHESIS-BH` | RESOLVIDO | — |
| G5 — Validação observacional humana | **ABERTO** | executar protocolo em `docs/007_PROT_Protocolo_Validacao.md` |
| G6 — Distinção `SRC` vs `coach_decision` no dicionário | MONITORADO | coluna Fonte já presente; revisar na próxima rodada G1 |
| G7 — `007_PROT_Protocolo_Validacao.md` sem critérios numéricos | RESOLVIDO (2026-06-08) | — |

## Estrutura esperada ao final da execução

```
docs/
├── sources/
│   ├── README.md                                    # registro mestre (A6)
│   ├── ihf_rules_beach_handball.pdf                 # SRC-IHF-RULES
│   ├── regras.md                                    # derivado de SRC-IHF-RULES (A2)
│   ├── 2024.naacl-industry.19.pdf                   # SRC-RAG-STRUCTURED
│   ├── Scout de Handebol de Areia_ Fontes Fortes.md # SRC-SYNTHESIS-BH (A3)
│   ├── Working-with-evals.md                        # SRC-OPENAI-EVALS
│   ├── notational_analysis_bh_iannaccone_2022.pdf   # SRC-NOTATIONAL-BH (A4)
│   ├── womens_bh_statistics_kazan_2022.pdf          # SRC-NOTATIONAL-BH (A4)
│   ├── primer_observational_measurement_2017.html   # SRC-OBS-MEASUREMENT (A5)
│   └── validation_observational_instrument_handball_2023.html  # SRC-OBS-MEASUREMENT (A5)
```

**Removido:** `docs/sources/Plano de Pesquisa para Scout Esportivo.md` (A1 — CONCLUÍDO)

---

## 0. Inventário verificado

### 0.1 Arquivos em `docs/sources/`

Verificado por: `ls -la /home/davis/SCOUT/docs/sources/`

| Arquivo | Tamanho | Registrado em README? | Status atual |
| --- | --- | --- | --- |
| `README.md` | 2 157 bytes | — (é o registro) | presente, incompleto |
| `ihf_rules_beach_handball.pdf` | 22 MB | sim → `SRC-IHF-RULES` | presente, canônico |
| `regras.md` | 110 KB | **não** | presente, não registrado |
| `2024.naacl-industry.19.pdf` | 831 KB | sim → `SRC-RAG-STRUCTURED` | presente, canônico |
| `Scout de Handebol de Areia_ Fontes Fortes.md` | 55 KB | **não** | presente, funcional |
| `Working-with-evals.md` | 60 KB | **não** | presente, funcional |
| `notational_analysis_bh_iannaccone_2022.pdf` | 3.6 MB | **não** | presente, baixado em A4 |
| `womens_bh_statistics_kazan_2022.pdf` | 767 KB | **não** | presente, baixado em A4 |
| `primer_observational_measurement_2017.html` | 181 KB | **não** | presente, salvo em A5 |
| `validation_observational_instrument_handball_2023.html` | 260 KB | **não** | presente, salvo em A5 |

### 0.2 Fontes registradas em `docs/sources/README.md`

Verificado por: Read `docs/sources/README.md:14–22`

| Código | Tipo | Arquivo local? | Status operacional |
| --- | --- | --- | --- |
| `SRC-IHF-RULES` | regra oficial | `ihf_rules_beach_handball.pdf` ✓ | ativo, verificável localmente |
| `SRC-NOTATIONAL-BH` | literatura científica | `notational_analysis_bh_iannaccone_2022.pdf`; `womens_bh_statistics_kazan_2022.pdf` ✓ | ativo e verificável localmente |
| `SRC-OBS-MEASUREMENT` | metodologia | `primer_observational_measurement_2017.html`; `validation_observational_instrument_handball_2023.html` ✓ | ativo e verificável localmente |
| `SRC-RAG-LEWIS` | IA/RAG | **ausente** — URL somente | diferido (Fase 2) |
| `SRC-RAG-STRUCTURED` | IA/RAG | `2024.naacl-industry.19.pdf` ✓ | diferido (Fase 2), verificável |
| `SRC-OPENAI-EVALS` | avaliação de IA | `Working-with-evals.md` ✓ | diferido (Fase 2), verificável localmente, mas plataforma em deprecação |

### 0.3 Referências cruzadas ativas

Verificado por: leitura direta de `docs/008_AUDIT_Matriz_Evidencias.md` e `docs/007_PROT_Protocolo_Validacao.md`

| Arquivo | Cita | Linhas de evidência |
| --- | --- | --- |
| `008_AUDIT_Matriz_Evidencias.md` | `SRC-IHF-RULES` | linhas 35–38: `set_number`, `points_value`, `two_point_goal`, `shootout_attempt` |
| `008_AUDIT_Matriz_Evidencias.md` | `SRC-NOTATIONAL-BH` | linhas 39–41: `spin_shot`, `inflight_goal`, `zone` (status `testing`) |
| `008_AUDIT_Matriz_Evidencias.md` | `SRC-OBS-MEASUREMENT` | linha 42: `technical_error` (status `draft`) |
| `007_PROT_Protocolo_Validacao.md` | `SRC-OBS-MEASUREMENT` | linha 65: "exigência de confiabilidade observacional" (referência geral, sem thresholds numéricos) |
| `007_PROT_Protocolo_Validacao.md` | `SRC-IHF-RULES`, `SRC-NOTATIONAL-BH` | linhas 66–67 |
| `003_PLAN_Passos_Implementacao_IA.md` | todos os SRC | linhas 26–41: tabela de fontes validadoras §0.2 |
| `009_RAG_Workflow_Fontes.md` | `docs/sources/README.md` | linha 9: Fase 1, passo 1 |

---

## 1. Diagnóstico — 7 problemas identificados

### P1 — Arquivo morto presente em `docs/sources/`

**Arquivo:** `Plano de Pesquisa para Scout Esportivo.md`

**Evidência verificada:**
- Não registrado em `sources/README.md` (Read `sources/README.md:14–22` — sem menção ao arquivo).
- Descreve PostgreSQL, MongoDB, ClickHouse, CQRS, AWS Step Functions, CRDTs distribuídos — `003_PLAN_Passos_Implementacao_IA.md:11–24` proíbe explicitamente PostgreSQL, FastAPI, deploy, multiusuário, Docker, React.
- Verificação de referências cruzadas operacionais: fora deste próprio plano (`docs/016_RAG_Plano_Organizacao_Fontes.md`), não há menção ao arquivo em contratos, serviços, testes, scripts ou demais documentos do repo.

**Conclusão:** sem uso funcional no repo; contradiz restrições arquiteturais explícitas.

---

### P2 — Arquivo funcional não registrado em `docs/sources/`

**Arquivo:** `Scout de Handebol de Areia_ Fontes Fortes.md`

**Evidência de que é funcional (verificada linha a linha):**

1. **Mapeia artigos concretos para SRC-NOTATIONAL-BH e SRC-OBS-MEASUREMENT:**
   - Iannaccone (2022): `Scout Fontes Fortes.md:194` — URL verificável
   - Women's BH Statistics (Kazan 2018): `Scout Fontes Fortes.md:177` — URL verificável
   - Throwing performance: `Scout Fontes Fortes.md:181` — URL verificável
   - Validation with Handball.ai: `Scout Fontes Fortes.md:190` — URL verificável
   - O'Donoghue Research Methods: `Scout Fontes Fortes.md:187`

2. **Fornece thresholds numéricos que NÃO existem em `007_PROT_Protocolo_Validacao.md`:**
   - Kappa > 0,81: `Scout Fontes Fortes.md:145`
   - ICC > 0,90: `Scout Fontes Fortes.md:144`
   - Cronbach α: `Scout Fontes Fortes.md:143`
   - Verificação de ausência: `grep -n "kappa\|Kappa\|ICC\|0\.81\|0\.90\|Cronbach" docs/007_PROT_Protocolo_Validacao.md` → **retorna zero resultados** (somente linha 65 cita `SRC-OBS-MEASUREMENT` como referência geral, sem números).
   - **Isso cria o gap G7** (ver seção 4): `007_PROT_Protocolo_Validacao.md` está incompleto sem critérios numéricos.

3. **O fluxo "fonte → evidência → regra → campo → validação"** descrito em `Scout Fontes Fortes.md:7` é idêntico ao fluxo de `009_RAG_Workflow_Fontes.md:8–12` (Fase 1, passos 1–5), verificado por leitura de ambos.

**Papel correto do arquivo:** síntese/curadoria secundária — não é fonte primária equivalente a paper científico ou regra oficial. Ver impacto em A3.

**Impacto de não registrar:** agente não sabe que o arquivo existe. O mapa de pesquisa para SRC-NOTATIONAL-BH e SRC-OBS-MEASUREMENT fica invisível.

---

### P3 — `regras.md` presente mas sem papel formal

**Arquivo:** `regras.md`

**Evidência verificada:**
- Não registrado em `sources/README.md` (Read `sources/README.md:14–22` — sem menção).
- É um **derivado textual com artefatos de extração** das regras IHF: cabeçalhos de página (`IX. Rules of the Game for Beach Handball / 1 MARCH 2026`) aparecem no meio do texto das regras em múltiplos pontos; seções de imagem (hand signals, diagramas de quadra) viram blocos de linhas em branco.
- **Nota sobre a formulação:** "conteúdo idêntico ao PDF" seria forte demais — o correto é "derivado textual com artefatos de extração do mesmo documento fonte".

**Consequência prática:** agente que lê o diretório não sabe qual arquivo é canônico para as regras IHF.

---

### P4 — `SRC-NOTATIONAL-BH` e `SRC-OBS-MEASUREMENT` sem arquivo local

**Evidência verificada:**
- `sources/README.md:17`: `SRC-NOTATIONAL-BH` — URL `https://hummov.awf.wroc.pl/...` (sem arquivo local).
- `sources/README.md:18`: `SRC-OBS-MEASUREMENT` — URL `https://pmc.ncbi.nlm.nih.gov/articles/PMC5426358/` (sem arquivo local).
- `008_AUDIT_Matriz_Evidencias.md:39–41`: cita `SRC-NOTATIONAL-BH` para `spin_shot`, `inflight_goal`, `zone` com status `testing`.
- `008_AUDIT_Matriz_Evidencias.md:42`: cita `SRC-OBS-MEASUREMENT` para `technical_error` com status `draft`.
- Critério de `007_PROT_Protocolo_Validacao.md:59`: `draft → testing` exige "fonte registrada" — agora há arquivo local verificável para ambos os códigos.

**Nota adicional sobre `SRC-OBS-MEASUREMENT`:** a URL registrada (`A Primer on Observational Measurement`, PMC5426358) é uma fonte metodológica geral, não específica de handebol de praia. O arquivo `Scout Fontes Fortes.md:190` aponta para uma fonte mais específica e validante para este domínio: "Development and Validation of Observational Game Analysis Tool with AI for Handball" (PMC10422213), que fornece Kappa = 0,889 em contexto de handebol.

---

### P5 — `006_TAX_Dicionario_Taxonomia.md` sem coluna de fonte

**Evidência verificada:**
- Read `docs/006_TAX_Dicionario_Taxonomia.md:10–54`: tabelas têm colunas `Evento | Definição | Marcar quando | Não marcar quando | Regra de decisão | Status` — sem coluna `Fonte`.
- `008_AUDIT_Matriz_Evidencias.md` e `006_TAX_Dicionario_Taxonomia.md` são documentos separados; o agente precisa ler os dois para rastrear por que um evento existe.
- `003_PLAN_Passos_Implementacao_IA.md:26–41`: exige que eventos sejam sustentados por fontes específicas.

---

### P6 — `sources/README.md` não mapeia código de fonte para arquivo local

**Evidência verificada:**
- Read `sources/README.md:14–22`: colunas `Código | Tipo | Fonte | Uso no ScoutPraia` — sem coluna de arquivo local.
- `ihf_rules_beach_handball.pdf` e `2024.naacl-industry.19.pdf` existem no disco mas não aparecem na tabela.

---

### P7 — Itens `testing` com fonte sem arquivo local

**Evidência verificada:**
- `008_AUDIT_Matriz_Evidencias.md:39–41`: `spin_shot`, `inflight_goal`, `zone` com status `testing` citam `SRC-NOTATIONAL-BH` (sem arquivo local).
- `007_PROT_Protocolo_Validacao.md:59`: `draft → testing` exige "fonte registrada" — URL é uma forma de registro, tecnicamente satisfeita.
- **Conclusão:** os itens podem permanecer `testing`; a auditabilidade local melhora quando o arquivo for baixado, mas não há invalidade formal.

---

## 2. Ações ordenadas

As ações A1–A3 e A6 são independentes de downloads externos. A4 e A5 requerem acesso à internet.

---

### Ação A1 — Deletar arquivo morto `[CONCLUÍDO]`

**Path:** `docs/sources/Plano de Pesquisa para Scout Esportivo.md`

**Comando:**
```bash
rm "docs/sources/Plano de Pesquisa para Scout Esportivo.md"
```

**Evidência que valida:**
- Não registrado em `sources/README.md` (verificado).
- Contradiz `003_PLAN_Passos_Implementacao_IA.md:11–24`.
- Zero referências em outros arquivos do repo.

**Impacto:** sem efeito em cascata. O diretório fica mais limpo.

**Gaps introduzidos:** nenhum.

---

### Ação A2 — Registrar `regras.md` como artefato derivado com limitações `[CONCLUÍDO]`

**Ação:** adicionar seção "Artefatos derivados" em `docs/sources/README.md`.

**Por que manter em vez de deletar:**
- Já existe como texto plano pesquisável — util para `grep` e pré-indexação de Fase 2.
- Regenerar a partir do PDF quando necessário custaria trabalho equivalente.
- A limitação documentada é mais honesta que a deleção silenciosa.

**Por que não usar como fonte primária:**
- Seções de imagem (hand signals, diagramas) ausentes — apenas linhas em branco.
- Cabeçalhos de página interrompem o texto das regras.
- Para consultas normativas, sempre preferir o PDF.

**Conteúdo a adicionar no README:**

```markdown
## Artefatos derivados (não são fontes primárias)

| Arquivo | Origem | Limitações | Quando usar |
| --- | --- | --- | --- |
| `regras.md` | derivado textual de `SRC-IHF-RULES` com artefatos de extração | cabeçalhos de página interrompem texto; seções de imagem ausentes (hand signals, diagramas); qualidade inferior ao PDF | somente busca textual local e pré-indexação Fase 2; nunca preferir ao PDF para consultas normativas |
```

**Impacto:**
- Agente sabe exatamente o que é o arquivo e quando usá-lo.
- Elimina conflito silencioso de interpretação entre PDF e `.md`.

**Gaps introduzidos:** nenhum.

---

### Ação A3 — Registrar `Scout de Handebol de Areia_ Fontes Fortes.md` como curadoria secundária `[CONCLUÍDO]`

**Path:** `docs/sources/Scout de Handebol de Areia_ Fontes Fortes.md` (manter nome atual)

**Código de fonte:** `SRC-SYNTHESIS-BH`

**Classificação:** síntese interna / curadoria secundária — **não é fonte primária**. Não deve ser citada no mesmo nível normativo de regra oficial ou paper científico revisado por pares.

**Papel correto:**
- Mapa de pesquisa que identifica os artigos a baixar para `SRC-NOTATIONAL-BH` e `SRC-OBS-MEASUREMENT`.
- Fornece thresholds numéricos (Kappa > 0,81; ICC > 0,90) que devem ser incorporados em `007_PROT_Protocolo_Validacao.md` com citação das fontes primárias que os embasam (ver G7).
- Descreve o fluxo "fonte → evidência → regra → campo → validação" — idêntico a `009_RAG_Workflow_Fontes.md` Fase 1.

**Linha a adicionar na tabela principal de `sources/README.md`:**

| Código | Tipo | Fonte | Arquivo local | Uso no ScoutPraia |
| --- | --- | --- | --- | --- |
| `SRC-SYNTHESIS-BH` | curadoria secundária (síntese interna) | Scout de Handebol de Areia: Fontes Fortes | `Scout de Handebol de Areia_ Fontes Fortes.md` | mapa de pesquisa para SRC-NOTATIONAL-BH e SRC-OBS-MEASUREMENT; thresholds de validação a incorporar em `007_PROT_Protocolo_Validacao.md`; **não citar como fonte primária** |

**Evidência que sustenta o papel (verificada):**
- Mapeia artigos concretos: `Scout Fontes Fortes.md:177, 181, 187, 190, 194`.
- Fornece Kappa > 0,81 e ICC > 0,90: `Scout Fontes Fortes.md:143–145`.
- `007_PROT_Protocolo_Validacao.md` não contém esses números (verificado por `grep` — zero resultados).
- Fluxo de Fase 1 em `009_RAG_Workflow_Fontes.md:8–12` coincide com `Scout Fontes Fortes.md:7`.

**Impacto:**
- Documenta o papel do arquivo sem inflar seu status epistemológico.
- Habilita A7 que referencia `SRC-SYNTHESIS-BH`.
- Abre G7: `007_PROT_Protocolo_Validacao.md` precisa ser atualizado com critérios numéricos.

**Gaps introduzidos:** G7 (ver seção 4).

---

### Ação A4 — Baixar arquivos para `SRC-NOTATIONAL-BH` `[CONCLUÍDO]`

**Papel da fonte:** indicadores de finalização, zonas, eficiência e padrões de jogo no handebol de praia.

**Verificação de licença antes de baixar:**
- Preferir origens com acesso aberto confirmado: PMC (NIH), Hrcak (open access), IRIS (repositório institucional aberto).
- Evitar baixar de ResearchGate ou agregadores — preferir publisher/repositório oficial.
- Registrar DOI quando existir, junto da URL canônica, mesmo quando o PDF for baixado.
- Se a licença for incerta, registrar apenas DOI + URL canônica no README sem versionar o PDF no Git.

**Artigos prioritários (identificados via `SRC-SYNTHESIS-BH`):**

| Prioridade | Artigo | URL canônica (origem confiável) | Nome de arquivo sugerido |
| --- | --- | --- | --- |
| 1 | Iannaccone (2022) "Notational Analysis of Beach Handball" | `https://iris.unicas.it/retrieve/de2a6154-4b59-86a2-e053-1705fe0a3017/78_Iannaccone%202022%20final.pdf` (IRIS — repositório institucional) | `notational_analysis_bh_iannaccone_2022.pdf` |
| 1 | "Women's Beach Handball Game Statistics" (Kazan 2018) | `https://hrcak.srce.hr/clanak/403495` (Hrcak — open access) | `womens_bh_statistics_kazan_2022.pdf` |
| 2 | "Analysis of Throwing Performance in Elite Women's BH" | `https://www.raco.cat/index.php/ApuntsEFD/article/download/373237/468661` (RACO — open access) | `throwing_performance_elite_womens_bh_2020.pdf` |

**Destino:** `docs/sources/`

**Instrução para o README após download:**
Atualizar linha `SRC-NOTATIONAL-BH`: adicionar coluna `Arquivo local` listando os PDFs baixados.

**Evidência que valida a prioridade:**
- `008_AUDIT_Matriz_Evidencias.md:39–41`: cita `SRC-NOTATIONAL-BH` para itens com status `testing`.
- `Scout Fontes Fortes.md:67–73`: modelo discriminante do Kazan 2018 identifica 5 variáveis preditoras de 80,6% dos resultados.
- `Scout Fontes Fortes.md:78–81`: estudo de arremesso confirma poder preditivo de `inflight_goal`.
- Iannaccone (2022) cobre zonas, padrões e eficiência — suporte para campo `zone` em `008_AUDIT_Matriz_Evidencias.md:41`.

**Impacto:**
- Itens `testing` tornam-se verificáveis localmente.
- Agente pode citar trecho da fonte ao validar definições em `006_TAX_Dicionario_Taxonomia.md`.

**Gaps introduzidos:** nenhum novo; fecha parte do P4.

---

### Ação A5 — Baixar arquivos para `SRC-OBS-MEASUREMENT` `[CONCLUÍDO]`

**Papel da fonte:** confiabilidade, validade e controle de ambiguidade observacional.

**Verificação de licença:** ambas as fontes abaixo são PMC (NIH), open access confirmado.

**Metadado preferencial:** registrar DOI junto da URL canônica no README, mesmo com PDF local presente.

**Artigos prioritários:**

| Prioridade | Artigo | URL canônica | Nome de arquivo sugerido |
| --- | --- | --- | --- |
| 1 | "A Primer on Observational Measurement" | `https://pmc.ncbi.nlm.nih.gov/articles/PMC5426358/` (PMC) | `primer_observational_measurement_2017.html` |
| 1 | "Development and Validation of Observational Game Analysis Tool with AI for Handball" | `https://pmc.ncbi.nlm.nih.gov/articles/PMC10422213/` (PMC) | `validation_observational_instrument_handball_2023.html` |

**Por que o segundo artigo é crítico:**
- Fornece Kappa = 0,889 e ICC ≥ 0,91 em contexto de handebol — mais específico do que o "Primer" metodológico geral.
- `Scout Fontes Fortes.md:143–145` usa esses números. `007_PROT_Protocolo_Validacao.md:65` cita `SRC-OBS-MEASUREMENT` sem números. Ter o arquivo local oficial permite ao agente verificar a origem dos thresholds.

**Destino:** `docs/sources/`

**Instrução para o README após download:**
Atualizar linha `SRC-OBS-MEASUREMENT`: adicionar coluna `Arquivo local` listando os arquivos locais baixados/salvos.

**Impacto:**
- `007_PROT_Protocolo_Validacao.md` ganha base local verificável para seus critérios (via G7).
- Fecha parte do P4.

**Gaps introduzidos:** habilita resolução de G7 (ver seção 4).

---

### Ação A6 — Atualizar `docs/sources/README.md` (consolidação) `[CONCLUÍDO]`

Executar após A1–A5 (ou em paralelo com A2–A3 se A4–A5 ainda não foram executadas).

**Mudanças necessárias:**

#### 6.1 — Adicionar coluna "Arquivo local" na tabela principal

Nova tabela (após todas as ações):

```markdown
| Código | Tipo | Fonte | Arquivo local | Uso no ScoutPraia |
| --- | --- | --- | --- | --- |
| `SRC-IHF-RULES` | regra oficial | IHF Rules — Beach Handball | `ihf_rules_beach_handball.pdf` | pontuação, set, shoot-out, ações especiais |
| `SRC-NOTATIONAL-BH` | literatura científica | Notational analysis of BH | `notational_analysis_bh_iannaccone_2022.pdf`, `womens_bh_statistics_kazan_2022.pdf` | indicadores de finalização, zonas, eficiência |
| `SRC-OBS-MEASUREMENT` | metodologia | Observational Measurement | `primer_observational_measurement_2017.html`, `validation_observational_instrument_handball_2023.html` | confiabilidade, validade, controle de ambiguidade |
| `SRC-RAG-LEWIS` | IA/RAG | RAG for Knowledge-Intensive NLP | ausente (Fase 2) | redução de dependência de memória interna |
| `SRC-RAG-STRUCTURED` | IA/RAG | Reducing hallucination via RAG | `2024.naacl-industry.19.pdf` | auditoria de saídas estruturadas (Fase 2) |
| `SRC-OPENAI-EVALS` | avaliação de IA | OpenAI Evals / Working with evals | `Working-with-evals.md` | ciclo de teste e medição de erro; referência conceitual, não dependência estratégica |
| `SRC-SYNTHESIS-BH` | curadoria secundária | Scout de Handebol de Areia: Fontes Fortes | `Scout de Handebol de Areia_ Fontes Fortes.md` | mapa de pesquisa; thresholds para `007_PROT_Protocolo_Validacao.md`; **não citar como fonte primária** |
```

#### 6.2 — Adicionar seção "Artefatos derivados" (ver A2)

#### 6.3 — Atualizar links para incluir os artigos baixados (após A4 e A5)

**Impacto:** elimina P3, P4, P6.

---

### Ação A7 — Adicionar coluna `Fonte` em `docs/006_TAX_Dicionario_Taxonomia.md` `[CONCLUÍDO]`

**Instrução:** adicionar coluna `Fonte` após `Regra de decisão` (antes de `Status`) em cada tabela do dicionário.

**Mapeamento evento → fonte:**

Verificado contra `008_AUDIT_Matriz_Evidencias.md`, `sources/README.md` e as regras IHF. A distinção `coach_decision` é usada quando não há base normativa ou científica verificável — conforme `008_AUDIT_Matriz_Evidencias.md:8–9` ("técnica: decisão prática do treinador").

**Eventos ofensivos:**

| Evento | Fonte | Base da atribuição |
| --- | --- | --- |
| `goal_scored`, `two_point_goal`, `two_point_attempt` | `SRC-IHF-RULES` | Rule 9 — pontuação por tipo de gol |
| `spin_shot` | `SRC-IHF-RULES`, `SRC-NOTATIONAL-BH` | Rule 9 (definição de gol espetacular) + estudos de arremesso |
| `inflight_attempt`, `inflight_goal` | `SRC-IHF-RULES`, `SRC-NOTATIONAL-BH` | Clarification No.1 (in-flight) + estudos de arremesso |
| `shot_attempt`, `shot_missed` | `SRC-IHF-RULES`, `SRC-OBS-MEASUREMENT` | Rule 9 (base normativa da ação) + operacionalização observacional para definição estanque |
| `technical_error`, `turnover` | `SRC-OBS-MEASUREMENT` | exige definição observável explícita para controle de ambiguidade — `008_AUDIT_Matriz_Evidencias.md:42` |
| `assist` | `SRC-OBS-MEASUREMENT`, `coach_decision` | sem base normativa em Rule IHF; categoria interpretativa — exige definição estanque por `SRC-OBS-MEASUREMENT` para reduzir ambiguidade |

**Eventos defensivos:**

| Evento | Fonte | Base da atribuição |
| --- | --- | --- |
| `defensive_stop`, `steal`, `block` | `SRC-OBS-MEASUREMENT`, `SRC-NOTATIONAL-BH` | padrões defensivos documentados em notational analysis + operacionalização observacional |
| `forced_error` | `SRC-OBS-MEASUREMENT`, `coach_decision` | exige pressão defensiva "clara" — julgamento interpretativo; base em metodologia observacional para limitar subjetividade |
| `goal_conceded` | `SRC-IHF-RULES` | Rule 9 — gol válido sofrido |
| `defensive_breakdown` | `coach_decision` | explicitamente interpretativo; `008_AUDIT_Matriz_Evidencias.md:44` o marca `draft` como "decisão do treinador" |

**Goleira, transição e situações especiais:**

| Evento | Fonte | Base da atribuição |
| --- | --- | --- |
| `save`, `goalkeeper_distribution` | `SRC-IHF-RULES`, `SRC-NOTATIONAL-BH` | Rule 5 (papel da goleira) + análise de impacto do goleiro em notational analysis |
| `save_shootout` | `SRC-IHF-RULES` | Rule 9.8–9.9 — shoot-out |
| `fast_break_for`, `fast_break_against` | `SRC-NOTATIONAL-BH` | padrões de transição em notational analysis |
| `transition_recovery_good`, `transition_recovery_bad` | `SRC-NOTATIONAL-BH`, `coach_decision` | padrões de transição + julgamento sobre qualidade de recomposição |
| `shootout_attempt`, `shootout_goal`, `shootout_miss` | `SRC-IHF-RULES` | Rule 9.8 — shoot-out |
| `timeout` | `SRC-IHF-RULES` | Rule 2.14 — time-out |
| `set_end` | `SRC-IHF-RULES` | Rule 2.4 — estrutura de sets (2 × 10 min) |

**Dependência:** A7 depende de A3 (para que `SRC-SYNTHESIS-BH` exista quando referenciado para thresholds de validação, embora `SRC-SYNTHESIS-BH` não apareça diretamente na coluna Fonte do dicionário — a coluna usa apenas os SRC primários).

**Impacto:** fecha P5. Dicionário passa a ser auto-documentado.

---

## 3. Análise de impacto consolidada

| Ação | Arquivos afetados | O que habilita | Risco |
| --- | --- | --- | --- |
| A1 (deletar morto) | `docs/sources/` (1 arquivo removido) | reduz ruído | nenhum — nada cita o arquivo |
| A2 (registrar regras.md) | `sources/README.md` | clareza sobre papel; evita conflito com PDF | nenhum |
| A3 (registrar Fontes Fortes) | `sources/README.md` | âncora para thresholds; visibilidade do mapa de pesquisa | risco P2 se não for classificado como secundário |
| A4 (baixar SRC-NOTATIONAL-BH) | `docs/sources/` (novos PDFs) + `sources/README.md` | itens `testing` verificáveis localmente; bases para G7 | nenhum se nomenclatura e licença seguirem padrão |
| A5 (baixar SRC-OBS-MEASUREMENT) | `docs/sources/` (novos PDFs) + `sources/README.md` | thresholds Kappa/ICC ganha fonte primária local; habilita G7 | nenhum se licença PMC confirmada |
| A6 (atualizar README) | `sources/README.md` | visibilidade completa de todos os arquivos | requer A1–A5 para precisão |
| A7 (coluna fonte no dicionário) | `docs/006_TAX_Dicionario_Taxonomia.md` | rastreabilidade direta evento → fonte | exige mapeamentos honestos para eventos interpretativos |

**Cascata crítica:**
- `A1 → A2 → A3 → A6`: independente de downloads, executável imediatamente.
- `A4 → A5 → A6`: depende de acesso externo.
- `A7`: pode ser executada em qualquer ordem; depende conceitualmente de A3 estar feito para que `SRC-SYNTHESIS-BH` exista no README.

---

## 4. Gaps residuais após execução de todas as ações

### G1 — Taxonomia integralmente em `draft` *(resolvido em 2026-06-09)*

**Causa original:** nenhum evento havia passado por validação em vídeo com decisão explícita de promoção.
**Resolução aplicada:** `two_point_goal` foi promovido de `draft` para `testing` no dicionário operacional, sincronizando o uso real em vídeo local, a definição operacional e a matriz de evidência.
**Evidência verificável usada para resolver o gap:**

- `docs/006_TAX_Dicionario_Taxonomia.md`: `two_point_goal` agora está em `testing`
- `docs/008_AUDIT_Matriz_Evidencias.md:38`: `two_point_goal` já estava documentado como `testing`
- banco local do jogo `match_id=1` contém marcação humana real de `two_point_goal` em eventos persistidos
- relatórios reais já gerados para `match_id=1` refletem uso de eventos de 2 pontos no fluxo operacional

**Nota importante:** esta resolução fecha apenas o gap “taxonomia integralmente em draft”. Ela **não** fecha `G5` nem converte a versão inteira da taxonomia em `approved`.

**Checklist operacional de fechamento:**

- [x] rodada com evidência de vídeo real já existente no banco local foi revisada
- [x] bloco de registro preenchido em `docs/007_PROT_Protocolo_Validacao.md`
- [x] revisão item a item concluída para o item objetivo mínimo desta rodada
- [x] pelo menos 1 item promovido de `draft` para `testing` ou `approved`
- [x] `docs/006_TAX_Dicionario_Taxonomia.md` atualizado
- [x] `docs/008_AUDIT_Matriz_Evidencias.md` atualizado, se necessário
- [x] nova versão de taxonomia criada, se houve mudança semântica *(não aplicável nesta rodada; sem mudança semântica)*
- [x] `docs/004_PROG_Progresso_Implementacao.md` atualizado com a decisão

### G2 — SRC-RAG-LEWIS sem arquivo local

**Causa:** diferido para Fase 2 (intencionalmente).
**Critério de resolução:** iniciar Fase 2 RAG conforme `009_RAG_Workflow_Fontes.md`.
**Impacto enquanto não resolvido:** nenhum para MVP.

### G3 — `SRC-OPENAI-EVALS` com arquivo local, mas plataforma em deprecação

**Causa:** `Working-with-evals.md` resolve a rastreabilidade local, porém o próprio documento oficial informa que a plataforma Evals entrará em `read-only` em `2026-10-31` e será desligada em `2026-11-30`.
**Critério de resolução:** manter `SRC-OPENAI-EVALS` apenas como referência conceitual para ciclo de avaliação e, quando a Fase 2 começar, preferir abordagem local/determinística ou substituto oficial vigente.
**Impacto enquanto não resolvido:** nenhum para o MVP atual, mas impede planejar dependência estrutural futura na plataforma Evals.

### G4 — `008_AUDIT_Matriz_Evidencias.md` não referencia `SRC-SYNTHESIS-BH`

**Causa:** A3 registra o arquivo, mas a matrix não foi atualizada.
**Critério de resolução:** após A3, revisar `008_AUDIT_Matriz_Evidencias.md` e adicionar `SRC-SYNTHESIS-BH` como fonte de suporte para `spin_shot`, `inflight_goal`, `two_point_goal`, `zone` (complementando os SRC primários já registrados).
**Nota:** `SRC-SYNTHESIS-BH` entra como fonte auxiliar (identificou os papers), não como substituto das fontes primárias.

### G5 — Validação observacional humana não executada

**Causa:** requer sessão humana com vídeo real.
**Critério de resolução:** roteiro em `docs/007_PROT_Protocolo_Validacao.md:73–314`.
**Impacto:** MVP não pode ser declarado completo — `010_AUDIT_Validacao_G5.md:160–168` confirma explicitamente.

**Checklist operacional de fechamento:**

- [ ] `scripts/verify_current_state.sh` passou antes do ensaio
- [ ] UI carregou sem erro fatal
- [ ] vídeo real renderizou
- [ ] `Salvar set` funcionou
- [ ] `Salvar posse` funcionou
- [ ] amostra mínima de eventos foi marcada
- [ ] pelo menos 1 edição de evento funcionou
- [ ] filtros localizaram o evento correto
- [ ] 3 relatórios foram gerados pela UI
- [ ] arquivos existem em `storage/reports/`
- [ ] screenshots foram anexados ou referenciados
- [ ] decisão final do ensaio foi registrada em `docs/007_PROT_Protocolo_Validacao.md`

### G6 — Eventos interpretativos em `006_TAX_Dicionario_Taxonomia.md` sem distinção clara entre `SRC` e `coach_decision`

**Causa:** após A7, a coluna Fonte existe, mas a distinção semântica entre "baseado em evidência científica" e "decisão prática do treinador" deve ser legível de relance.
**Critério de resolução:** ao executar A7, usar notação consistente: `coach_decision` é um valor válido na coluna Fonte (já reconhecido em `008_AUDIT_Matriz_Evidencias.md:8`), não uma lacuna a esconder.

### G7 — `007_PROT_Protocolo_Validacao.md` sem critérios numéricos de confiabilidade *(resolvido em 2026-06-08)*

**Estado atual:** resolvido.

**Como foi resolvido:**
- `docs/007_PROT_Protocolo_Validacao.md` passou a registrar critérios numéricos explícitos para:
  - `κ > 0.81`
  - `ICC >= 0.90`
  - `α >= 0.90`
- o protocolo agora também registra a ressalva metodológica correta:
  - os números são critério prático do ScoutPraia;
  - não são corte universal absoluto para toda a literatura observacional.

**Base verificável usada no fechamento:**
- `docs/sources/validation_observational_instrument_handball_2023.html`
- `docs/sources/Scout de Handebol de Areia_ Fontes Fortes.md`
- `docs/sources/primer_observational_measurement_2017.html`

---

## 5. Gate de conclusão do plano

O plano é considerado executado quando o gate canônico do repositório passa sem erro:

```bash
# Gate canônico obrigatório (definido em AGENTS.md e validado em 010_AUDIT_Validacao_G5.md:45)
scripts/verify_current_state.sh
```

Este script já verifica:
- higiene do repositório (sem arquivos proibidos versionados)
- importação do pacote Python
- inicialização do banco e seed idempotente da taxonomia
- testes automatizados (`pytest`)
- whitespace (`git diff --check`)

**Checks adicionais específicos deste plano** (executar após `verify_current_state.sh`):

```bash
# 1. Arquivo morto removido
[ ! -f "docs/sources/Plano de Pesquisa para Scout Esportivo.md" ] && echo "OK A1" || echo "FALHA A1"

# 2. SRC-SYNTHESIS-BH registrado no README
grep -q "SRC-SYNTHESIS-BH" docs/sources/README.md && echo "OK A3" || echo "FALHA A3"

# 3. regras.md formalizado como artefato derivado
grep -q "Artefatos derivados" docs/sources/README.md && echo "OK A2" || echo "FALHA A2"

# 4. README tem coluna Arquivo local
grep -q "Arquivo local" docs/sources/README.md && echo "OK A6" || echo "FALHA A6"

# 5. 006_TAX_Dicionario_Taxonomia.md tem coluna Fonte
grep -q "| Fonte |" docs/006_TAX_Dicionario_Taxonomia.md && echo "OK A7" || echo "FALHA A7"

# 6. Pelo menos um arquivo SRC-NOTATIONAL-BH baixado
ls docs/sources/notational_analysis_bh_iannaccone_2022.pdf 2>/dev/null && echo "OK A4" || echo "PENDENTE A4 (requer download)"

# 7. Pelo menos um arquivo SRC-OBS-MEASUREMENT baixado
ls docs/sources/primer_observational_measurement_2017.html docs/sources/validation_observational_instrument_handball_2023.html 2>/dev/null && echo "OK A5" || echo "PENDENTE A5 (requer download)"
```

Resultado esperado:
- `scripts/verify_current_state.sh`: todos os checks internos passando.
- Checks 1–5: todos `OK` (independentes de download).
- Checks 6–7: `OK` quando os downloads/snapshots locais forem executados; `PENDENTE` é estado válido se Fase 2 ainda não iniciou.

**Interpretação correta do gate:**
- **execução parcial válida do plano:** `scripts/verify_current_state.sh` passa, checks 1–5 estão `OK` e checks 6–7 podem estar `PENDENTE` quando A4/A5 ainda não foram executadas.
- **execução completa do plano:** `scripts/verify_current_state.sh` passa e os checks 1–7 estão todos `OK`, incluindo os downloads/documentação de A4 e A5.

---

## 6. Estrutura correta esperada ao final

```
docs/
├── 002_SPEC_MVP_Tecnico.md     # contrato de produto
├── 003_PLAN_Passos_Implementacao_IA.md                       # contrato de execução para agentes
├── 004_PROG_Progresso_Implementacao.md                       # histórico com evidências reais
├── 016_RAG_Plano_Organizacao_Fontes.md                     # este arquivo
├── 010_AUDIT_Validacao_G5.md                     # auditoria de evidências técnicas
├── 017_AUDIT_Fluxo_MVP_Agente.md                          # auditoria do fluxo de implementação
├── 008_AUDIT_Matriz_Evidencias.md                               # governança de evidência e status
├── 006_TAX_Dicionario_Taxonomia.md                           # dicionário com coluna Fonte (após A7)
├── 007_PROT_Protocolo_Validacao.md                           # protocolo + critérios numéricos (após G7)
├── 009_RAG_Workflow_Fontes.md                                  # fluxo de fontes, evidência e RAG
├── 018_UX_Guia_Preenchimento.md                   # guia operacional da UI Marcação
└── sources/
    ├── README.md                                    # registro mestre (após A6)
    ├── ihf_rules_beach_handball.pdf                 # SRC-IHF-RULES (primário)
    ├── regras.md                                    # derivado de SRC-IHF-RULES (A2)
    ├── 2024.naacl-industry.19.pdf                   # SRC-RAG-STRUCTURED (Fase 2)
    ├── Scout de Handebol de Areia_ Fontes Fortes.md # SRC-SYNTHESIS-BH (A3)
    ├── Working-with-evals.md                        # SRC-OPENAI-EVALS (referência conceitual; plataforma em deprecação)
    ├── notational_analysis_bh_iannaccone_2022.pdf   # SRC-NOTATIONAL-BH (A4)
    ├── womens_bh_statistics_kazan_2022.pdf          # SRC-NOTATIONAL-BH (A4)
    ├── throwing_performance_elite_womens_bh_2020.pdf# SRC-NOTATIONAL-BH (A4, opcional)
    ├── primer_observational_measurement_2017.html   # SRC-OBS-MEASUREMENT (A5)
    └── validation_observational_instrument_handball_2023.html # SRC-OBS-MEASUREMENT (A5)
```

**Removido ao final:** `docs/sources/Plano de Pesquisa para Scout Esportivo.md` (A1)

---

## 7. Header correto de cada arquivo

Verificado por leitura direta. Todos os headers abaixo já existem ou devem ser mantidos como estão.

| Path | H1 atual / esperado |
| --- | --- |
| `docs/sources/README.md` | `# Fontes do ScoutPraia` |
| `docs/008_AUDIT_Matriz_Evidencias.md` | `# Matriz de Evidência do ScoutPraia` |
| `docs/006_TAX_Dicionario_Taxonomia.md` | `# Dicionário Operacional da Taxonomia` |
| `docs/007_PROT_Protocolo_Validacao.md` | `# Protocolo de Validação do ScoutPraia` |
| `docs/009_RAG_Workflow_Fontes.md` | `# Fluxo de Fontes, IA e RAG` |
| `docs/003_PLAN_Passos_Implementacao_IA.md` | `# ScoutPraia — Plano de Implementação para IA` |
| `docs/010_AUDIT_Validacao_G5.md` | `# Auditoria de Evidências e Validação — ScoutPraia` |
| `docs/017_AUDIT_Fluxo_MVP_Agente.md` | `# Auditoria do Fluxo de Implementação do MVP — ScoutPraia` |
| `docs/sources/REF_S02_Fontes_Fortes_Handebol.md` | manter H1 original — não alterar |

---

## 8. Plano v1.6 — Registro de Fontes Fortes e MVP Textual RAG

> **Base:** `beach_handball_ai_rag_action_plan_v1.6` (aprovado_com_correcoes_aplicadas)
> **Incorporado em:** 2026-06-13

### 8.1 Estrutura de pastas `beach_handball_ai/fontes/`

```text
beach_handball_ai/
  fontes/
    00_registro/
      fontes_oficiais.md          ← registro canônico para agentes
      fontes_oficiais.csv         ← exportação derivada para scripts

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

    06_metodologia_rag_agentes/
      01_rag_recuperacao/
      02_reflection_self_refine/
      03_multiagente_debate/
      04_structured_output_schema/
      05_agent_benchmarks/
      06_frameworks_notebooks/
      07_videos_secundarios/
      manifest_metodologia.json

    07_video_visao_computacional/
      01_pose_estimation/
      02_multi_object_tracking/
      03_action_spotting/
      04_video_representation_learning/
      05_multimodal_sports_reasoning/
      manifest_video_cv.json

    08_ciencia_desempenho_beach_handball/
      01_analise_notacional/
      02_arremessos_finalizacao/
      03_tomada_decisao_contexto/
      04_estatisticas_jogo/
      05_carga_fisiologia_biomecanica/
      manifest_ciencia_bh.json
```

### 8.2 Registro canônico `fontes_oficiais.md`

O arquivo canônico de registro para leitura por agentes é `fontes/00_registro/fontes_oficiais.md`. O CSV é exportação derivada para scripts de ingestão — nunca fonte principal de compreensão do agente.

**Frontmatter obrigatório:**
```yaml
title: Registro de Fontes Oficiais
document_id: fontes_oficiais
version: v1.0
status: em_validacao
canonical_format: markdown
derived_exports: fontes_oficiais.csv
source_policy: Markdown é a fonte canônica; CSV é exportação técnica.
```

Cada fonte usa seção `### SOURCE_ID — Título` com tabela curta obrigatória:

| Campo | Valor |
|-------|-------|
| source_id | SOURCE_ID |
| nível | A/B/C/D/Rejeitada |
| coleção | nome_da_colecao |
| status | status_da_fonte |
| uso permitido | … |
| uso proibido | … |

Campos completos por fonte: `source_id`, `titulo`, `organizacao`, `tipo`, `data`, `versao`, `link`, `link_canonico`, `aliases`, `uso_permitido`, `uso_proibido`, `tema`, `subtema`, `nivel_de_confiabilidade`, `colecao_vetorial`, `arquivo_local`, `status`, `checksum_sha256`, `data_coleta`, `criterio_de_validacao`, `observacao`.

Fontes rejeitadas permanecem apenas para auditoria (`status: rejeitada`, `colecao_vetorial: fora_do_rag`).

### 8.3 Catálogo de fontes — status atual

| source_id | grupo | nível | coleção vetorial | status |
|-----------|-------|-------|-----------------|--------|
| IHF_RULES_BH_2026 | regra oficial | A | bh_regras | validado |
| IHF_UPDATE_BH_2026_04 | atualização oficial | A | bh_regras | validado |
| CBHB_REGULAMENTO_2026 | regulamento nacional | A | bh_regras | pendente_validacao |
| EHF_REFEREEING_BH | arbitragem técnica | B | bh_tecnico | pendente_validacao |
| EHF_SHOOTOUT_PRESSURE | técnica/psicologia | B | bh_tecnico | pendente_validacao |
| CEPRAEA_GLOSSARIO_TECNICO | fonte interna | C | bh_glossario | pendente_redacao |
| CEPRAEA_PLAYBOOK | fonte interna | C | bh_playbook_cepraea | pendente_redacao |
| CEPRAEA_SCOUT_SCHEMA | fonte interna | C | bh_scout | pendente_redacao |
| MET_JSON_SCHEMA_RUNTIME_VALIDATION_2025 | metodologia_structured_output | C | ai_metodologia_structured_output | pendente_validacao |
| MET_CHOPCHOP_SEMANTIC_CONSTRAINED_DECODING_2025 | metodologia_structured_output | C | ai_metodologia_structured_output | pendente_validacao |
| MET_CONTROLLABLE_GENERATION_LCR_2025 | metodologia_structured_output | B | ai_metodologia_structured_output | pendente_revisao_manual |
| MET_SELF_REFINE_2023 | metodologia_reflexao | B | ai_metodologia_reflexao | pendente_revisao_manual |
| MET_LONG_DOC_QA_COST_2026 | metodologia_rag | C | ai_metodologia_rag | pendente_validacao |
| MET_AGENT_WORKFLOW_DEPENDENCIES_2025 | metodologia_avaliacao_agentes | C | ai_metodologia_avaliacao_agentes | pendente_validacao |
| MET_TOOL_DECATHLON_2026 | metodologia_avaliacao_agentes | C | ai_metodologia_avaliacao_agentes | pendente_validacao_licenca |
| MET_DYFLOW_2025 | metodologia_agentes | C | ai_metodologia_avaliacao_agentes | pendente_validacao |
| MET_TYPE_CONSTRAINED_CODE_GEN_2025 | metodologia_structured_output | B | ai_metodologia_structured_output | pendente_revisao_manual |
| MET_LANGGRAPH_REFLECTION_NOTEBOOK | frameworks_notebooks | C | ai_frameworks_notebooks | pendente_fixar_commit |
| MET_AUTOGEN_GROUPCHAT_VIS_0_2 | frameworks_notebooks | C | ai_frameworks_notebooks | pendente_validacao_versao |
| MET_AG2_GROUPCHAT_VIS | frameworks_notebooks | C | ai_frameworks_notebooks | pendente_fixar_commit |
| MET_YOUTUBE_AGENT_REFLECTION_DYHWQM | videos_secundarios | D | fora_do_rag_principal | pendente_transcricao |
| MET_REFLEXION_2023 | metodologia_reflexao | C | ai_metodologia_reflexao | pendente_validacao |
| MET_MULTIAGENT_DEBATE_2023 | metodologia_multiagente | C | ai_metodologia_multiagente | pendente_validacao |
| MET_MLE_DOJO_2025 | metodologia_avaliacao_agentes | C | ai_metodologia_avaliacao_agentes | pendente_validacao_licenca |
| MET_QLASS_2025 | metodologia_agentes | B | ai_metodologia_avaliacao_agentes | pendente_revisao_manual |
| CV_UNITRACK_MOT_2026 | visao_computacional_tracking | C | ai_video_tracking | pendente_validacao |
| CV_COMBAT_SPORTS_POSE_2025 | visao_computacional_pose | C | ai_video_pose_estimation | pendente_validacao |
| CV_GST_3D_HUMAN_BODY_2025 | visao_computacional_3d_body | C | ai_video_pose_estimation | pendente_validacao |
| AI_SPORTR_MULTIMODAL_SPORTS_2026 | sports_multimodal_reasoning | C | ai_sports_multimodal_reasoning | pendente_validacao |
| DATA_SOCCERNET_BALL_ACTION_SPOTTING | action_spotting | C | ai_video_action_spotting | pendente_validacao_licenca |
| SCI_BH_WOMENS_GAME_STATS_KINESIOLOGY_2022 | beach_handball_estatisticas_jogo | B | bh_ciencia_estatisticas_jogo | pendente_revisao_manual_tabelas |
| SCI_BH_THROWING_PERFORMANCE_APUNTS_2020 | beach_handball_arremessos | B | bh_ciencia_arremessos | pendente_revisao_manual_tabelas |
| SCI_BH_NOTATIONAL_ANALYSIS_HUMMOV_2022 | beach_handball_analise_notacional | B | bh_ciencia_analise_notacional | pendente_revisao_manual_tabelas |
| SCI_BH_CONTEXTUAL_FACTORS_FRONTIERS_2019 | beach_handball_tomada_decisao | B | bh_ciencia_tomada_decisao | pendente_revisao_manual_tabelas |
| SCI_PMC5721173_PENDING | ciencia_esporte_pendente | Rejeitada | fora_do_rag | pendente_validacao_bibliografica |
| SCI_MOTRIZ_WR8RTPX_PENDING | ciencia_esporte_pendente | Rejeitada | fora_do_rag | pendente_validacao_bibliografica |
| SCI_PUBMED_34705619_PENDING | ciencia_esporte_pendente | Rejeitada | fora_do_rag | pendente_validacao_bibliografica |
| CV_MDPI_SENSORS_22083011_PENDING | visao_computacional_sensores_pendente | Rejeitada | fora_do_rag | pendente_validacao_bibliografica |
| CV_CVPR2023_COMPUTER_PENDING | visao_computacional_pendente | Rejeitada | fora_do_rag | pendente_validacao_bibliografica |
| CV_HRNET_HUMAN_POSE_2019 | visao_computacional_pose | B | ai_video_pose_estimation | pendente_revisao_manual_pdf |
| CV_VIDEOMAE_NEURIPS_2022 | video_representation_learning | B | ai_video_representation_learning | pendente_revisao_manual_pdf |
| MET_NAACL_INDUSTRY_2024_019 | metodologia_rag | C | ai_metodologia_rag | pendente_validacao_local |
| IHF_RULES_BH_LOCAL_PDF | regra oficial local | A | bh_regras | pendente_validacao_checksum |
| SCI_BH_NOTATIONAL_ANALYSIS_IANNACCONE_2022 | beach_handball_analise_notacional | B | bh_ciencia_analise_notacional | pendente_revisao_manual_tabelas |
| SCI_OBSERVATIONAL_MEASUREMENT_PRIMER_2017 | metodologia_observacional | C | ai_metodologia_rag | pendente_validacao_local |
| LOCAL_SOURCES_README | fonte_interna_corpus | C | ai_metodologia_rag | pendente_validacao_local |
| IHF_RULES_BH_DERIVED_REGRAS_MD | regra_derivada_local | C | bh_regras | pendente_rastrear_fonte_original |
| LOCAL_SCOUT_BH_FONTES_FORTES | fonte_interna_scout | C | bh_scout | pendente_validacao_local |
| SCI_VALIDATION_OBSERVATIONAL_INSTRUMENT_HANDBALL_2023 | metodologia_observacional | C | ai_metodologia_rag | pendente_validacao_local |
| SCI_BH_WOMENS_STATS_KAZAN_2022 | beach_handball_estatisticas_jogo | B | bh_ciencia_estatisticas_jogo | pendente_revisao_manual_tabelas |
| MET_OPENAI_WORKING_WITH_EVALS_LOCAL | metodologia_avaliacao_agentes | C | ai_metodologia_avaliacao_agentes | pendente_validacao_local |

### 8.4 Fontes locais em `docs/sources/`

| source_id | arquivo_local | nível | coleção | status |
|-----------|--------------|-------|---------|--------|
| MET_NAACL_INDUSTRY_2024_019 | `docs/sources/2024.naacl-industry.19.pdf` | C | ai_metodologia_rag | pendente_validacao_local |
| IHF_RULES_BH_LOCAL_PDF | `docs/sources/ihf_rules_beach_handball.pdf` | A | bh_regras | pendente_validacao_checksum |
| SCI_BH_NOTATIONAL_ANALYSIS_IANNACCONE_2022 | `docs/sources/notational_analysis_bh_iannaccone_2022.pdf` | B | bh_ciencia_analise_notacional | pendente_revisao_manual_tabelas |
| SCI_OBSERVATIONAL_MEASUREMENT_PRIMER_2017 | `docs/sources/primer_observational_measurement_2017.html` | C | ai_metodologia_rag | pendente_validacao_local |
| LOCAL_SOURCES_README | `docs/sources/README.md` | C | ai_metodologia_rag | pendente_validacao_local |
| IHF_RULES_BH_DERIVED_REGRAS_MD | `docs/sources/REF_S01_Regras_Oficiais_IHF_2026.md` | C | bh_regras | pendente_rastrear_fonte_original |
| LOCAL_SCOUT_BH_FONTES_FORTES | `docs/sources/REF_S02_Fontes_Fortes_Handebol.md` | C | bh_scout | pendente_validacao_local |
| SCI_VALIDATION_OBSERVATIONAL_INSTRUMENT_HANDBALL_2023 | `docs/sources/validation_observational_instrument_handball_2023.html` | C | ai_metodologia_rag | pendente_validacao_local |
| SCI_BH_WOMENS_STATS_KAZAN_2022 | `docs/sources/womens_bh_statistics_kazan_2022.pdf` | B | bh_ciencia_estatisticas_jogo | pendente_revisao_manual_tabelas |
| MET_OPENAI_WORKING_WITH_EVALS_LOCAL | `docs/sources/_deprecated/DEPR_S03_OpenAI_Evals.md` | C | ai_metodologia_avaliacao_agentes | deprecado — plataforma em shutdown nov/2026 |

**Regras de uso das fontes locais:**
- `IHF_RULES_BH_LOCAL_PDF` só permanece como nível A se o checksum confirmar cópia íntegra da regra vigente
- `IHF_RULES_BH_DERIVED_REGRAS_MD` é derivado local; não substitui o PDF oficial sem rastreabilidade
- PDFs científicos entram no RAG somente após revisão manual de tabelas, amostra, método e limitações
- Arquivos `.html` entram somente após extração limpa de título, autoria, ano e conteúdo principal
- `MET_OPENAI_WORKING_WITH_EVALS_LOCAL` está depreciado; a plataforma Evals encerra em nov/2026

### 8.5 Chunking

- **Tamanho:** 500–900 tokens; sobreposição de 80–120 tokens
- Regra oficial não pode ser quebrada no meio; título e explicação ficam no mesmo chunk
- Fontes de domínios diferentes não ficam no mesmo chunk (regra + ciência, IA + esporte)

**Tipos de chunk:** `chunk_normativo` | `chunk_tecnico` | `chunk_cepraea` | `chunk_cientifico_bh` | `chunk_metodologico_ai` | `chunk_video_cv`

**Metadados obrigatórios por chunk:**
```json
{
  "chunk_id": "",
  "source_id": "",
  "titulo": "",
  "organizacao": "",
  "tema": "",
  "subtema": "",
  "nivel_confiabilidade": "",
  "colecao_vetorial": "",
  "versao": "",
  "data": "",
  "arquivo_local": "",
  "uso_permitido": "",
  "uso_proibido": "",
  "status": ""
}
```

### 8.6 Critérios de avaliação (3 abas de perguntas)

**Aba perguntas_mvp_textual (30 perguntas — normativas IHF, arbitragem, EHF, CEPRAEA e recusa):**
- 30/30 respostas citam `source_id` ou recusam corretamente
- Zero resposta sem fonte; zero regra inventada; zero mistura IHF × CEPRAEA
- Pelo menos 5 perguntas sem base documental recusadas corretamente

**Aba perguntas_metodologia_agente (10 perguntas):**
- 10/10 citam `source_id` correto ou recusam
- Zero uso de fonte metodológica para regra esportiva

**Aba perguntas_video_ciencia_bh (12 perguntas):**
- 12/12 citam `source_id` correto ou recusam
- Zero uso de visão computacional para regra esportiva

**Relatório de avaliação:** `avaliacoes/eval_mvp_textual_001.md`

### 8.7 Ordem operacional da Fase 2

1. Registrar fontes oficiais IHF, CBHb, EHF e CEPRAEA em `fontes_oficiais.md`
2. Registrar fontes metodológicas de IA
3. Registrar fontes de visão computacional e ciência do Beach Handball
4. Validar links canônicos e aliases
5. Salvar cada fonte como arquivo local
6. Gerar checksum SHA-256
7. Preencher `fontes_oficiais.md` como registro canônico; gerar `fontes_oficiais.csv` como exportação derivada
8. Converter PDFs e páginas para Markdown limpo
9. Revisar manualmente tabelas científicas
10. Fixar commit hash de notebooks GitHub
11. Transcrever e revisar vídeos antes de qualquer ingestão
12. Criar chunks com metadados completos
13. Inserir chunks nas coleções vetoriais corretas
14. Rodar teste de recuperação sem LLM
15. Rodar avaliação do agente com as 3 abas de perguntas (52 total)
16. Corrigir fontes, chunks, metadados ou prompt quando houver falha
17. Liberar o MVP textual apenas após aprovação em `avaliacoes/eval_mvp_textual_001.md`

### 8.8 Definição de pronto — MVP textual RAG

- Registro canônico `fontes_oficiais.md` contém todas as fontes aceitas
- Fontes rejeitadas não entram no RAG
- Todos os chunks têm metadados completos
- Coleções vetoriais separadas por domínio
- Teste de recuperação aprova fontes corretas no top 3
- Perguntas sem base documental são recusadas
- Respostas técnicas citam `source_id`, título e organização
- Agente diferencia regra oficial, ciência, fonte metodológica, visão computacional e convenção CEPRAEA
- Relatório `avaliacoes/eval_mvp_textual_001.md` aprovado
