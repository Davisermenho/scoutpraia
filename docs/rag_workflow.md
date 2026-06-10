---
tipo: fluxo_rag
fase_atual: 1
RAG_liberado: false
critério_fase_2: "MVP funcional completo + G5 aprovado + fontes locais indexadas"
última_atualização: 2026-06-10
nota: "RAG (Fase 2) MUST NOT ser implementado antes do MVP funcional com G5 aprovado"
---

# Fluxo de Fontes, IA e RAG

## RESTRIÇÃO CRÍTICA

```
MUST NOT: implementar RAG (Fase 2) antes do MVP estar funcional com G5 aprovado
MUST NOT: usar RAG para decidir evento automaticamente durante marcação
MUST NOT: inventar regra de taxonomia sem fonte registrada em docs/sources/README.md
MUST NOT: gerar relatório sem indicar versão da taxonomia usada
MUST NOT: alterar evento approved sem nova versão de taxonomia
```

**RAG está liberado:** NÃO — `RAG_liberado: false`

**Critério para liberar Fase 2:** MVP funcional completo com G5 aprovado.

---

O RAG não é necessário para a marcação inicial do MVP. No ScoutPraia, ele deve funcionar como camada de auditoria e consulta de fontes.

## Fase 1 — Manual, sem RAG

Usar enquanto há poucas fontes.

1. registrar fontes em `docs/sources/README.md`
2. transformar fonte em decisão na `docs/evidence_matrix.md`
3. criar ou ajustar definição em `docs/taxonomy_dictionary.md`
4. validar definição em vídeo com `docs/validation_protocol.md`
5. aprovar apenas campos úteis, observáveis e consistentes

## Fase 2 — RAG local

**BLOQUEADA.** Critério de desbloqueio — todos os itens abaixo devem ser verdadeiros:

```
[ ] G5 aprovado (validação humana com screenshots documentada)
[ ] taxonomia ScoutPraia v0.1 com pelo menos 1 campo approved
[ ] marcação operacional com vídeo real funcionando
[ ] geração real de clipes com ffmpeg funcionando
[ ] relatórios coletivo, individual e adversária funcionando
[ ] fontes em docs/sources/ verificadas e registradas em sources/README.md
```

Quando desbloqueada, componentes sugeridos:

- pasta de documentos fonte (já existe em `docs/sources/`)
- indexador local (a definir)
- busca por trecho relevante com citação obrigatória
- prompt de auditoria com exigência de fontes, conflitos e inferências
- registro da decisão final na `docs/evidence_matrix.md`

## Usos corretos da IA/RAG

- verificar se um campo tem fonte suficiente
- identificar conflito entre regra oficial e definição prática
- revisar se um KPI depende de evento ainda em `draft`
- gerar relatório usando apenas dados marcados e definições aprovadas
- sugerir ajustes de taxonomia após divergências de validação

## Usos que devem ser evitados no MVP

- decidir evento automaticamente durante marcação rápida
- inventar regra sem fonte
- transformar hipótese prática em KPI final
- gerar relatório sem apontar versão da taxonomia
- alterar definição aprovada sem nova versão

## Contrato mínimo para prompts

Todo prompt de auditoria deve exigir e retornar:

| Campo obrigatório | Exemplo de saída esperada |
| --- | --- |
| fontes usadas | `SRC-IHF-RULES Rule 9`, `SRC-NOTATIONAL-BH Iannaccone 2022 p.3` |
| itens sem evidência | `spin_shot: fonte presente, sem validação em vídeo` |
| conflitos encontrados | `defensive_breakdown: definição interpretativa conflita com critério de objetividade de SRC-OBS-MEASUREMENT` |
| inferências feitas | `zone atribuída por posição visual — sem confirmação oficial` |
| recomendação | `manter` \| `ajustar definição` \| `fundir com X` \| `dividir em Y/Z` \| `remover` \| `manter como hipótese` |

Prompt de auditoria não deve retornar apenas recomendação sem citar as fontes e conflitos que a sustentam.
