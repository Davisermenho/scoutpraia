# Fluxo de Fontes, IA e RAG

O RAG não é necessário para a marcação inicial do MVP. No ScoutPraia, ele deve funcionar como camada de auditoria e consulta de fontes.

## Fase 1 — Manual, sem RAG

Usar enquanto há poucas fontes.

1. registrar fontes em `docs/sources/README.md`
2. transformar fonte em decisão na `docs/evidence_matrix.md`
3. criar ou ajustar definição em `docs/taxonomy_dictionary.md`
4. validar definição em vídeo com `docs/validation_protocol.md`
5. aprovar apenas campos úteis, observáveis e consistentes

## Fase 2 — RAG local

Usar quando houver muitas fontes ou necessidade de auditoria recorrente.

Componentes sugeridos:

- pasta de documentos fonte
- indexador local
- busca por trecho relevante
- prompt de auditoria com citação obrigatória
- registro da decisão final na matriz de evidência

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

Todo prompt de auditoria deve exigir:

- fontes usadas
- itens sem evidência
- conflitos encontrados
- inferências feitas
- recomendação de manter, ajustar, remover ou testar
