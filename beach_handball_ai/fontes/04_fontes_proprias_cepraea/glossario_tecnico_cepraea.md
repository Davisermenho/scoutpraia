---
status: base_interna_elaborada_v0
tipo: fonte_propria_cepraea
uso_previsto: glossario_operacional
escopo: "linguagem interna alinhada ao ScoutPraia v0.1"
fonte_base:
  - docs/taxonomy_dictionary.md
  - docs/evidence_matrix.md
  - docs/Contrato_Operacional.md
  - scoutpraia/ui_labels.py
observacao: "Glossario interno de trabalho. Nao substituir regra oficial IHF/CBHb. Termos internos de playbook podem estar formalizados aqui sem ainda virarem evento, KPI ou automacao do app."
---

# Glossario Tecnico CEPRAEA

## Regra de uso

- Quando houver conflito entre regra oficial e linguagem interna, prevalece a regra oficial.
- Quando um termo interno ainda nao estiver operacionalizado no ScoutPraia, ele deve ser tratado como `convencao_interna_pendente`.
- Termo interno nao vira KPI final sozinho. Para isso, precisa estar alinhado a `docs/taxonomy_dictionary.md`, `docs/evidence_matrix.md` e `docs/validation_protocol.md`.

## Termos operacionais alinhados ao app

### Giro

Definicao:
Arremesso com giro associado ao evento `spin_shot`.

Uso no treino:
Treinar como mecanismo de finalizacao de 2 pontos quando a mecanica do giro estiver claramente visivel.

Criterio de execucao:
Registrar como giro apenas quando o movimento de giro fizer parte da finalizacao observavel.

Erros comuns:
- chamar de giro qualquer arremesso de 2 pontos sem confirmacao visual da mecanica
- confundir com fallback generico `two_point_attempt`

Fonte de regra relacionada:
`SRC-IHF-RULES`

Fonte tecnica relacionada:
`docs/taxonomy_dictionary.md`

Observacao CEPRAEA:
Se houver duvida no video, usar o fallback generico de 2 pontos e revisar depois.

### Aerea

Definicao:
Finalizacao em inflight associada aos eventos `inflight_attempt` e `inflight_goal`.

Uso no treino:
Treinar temporizacao, recepcao no ar e conclusao sem contato com o solo antes da finalizacao.

Criterio de execucao:
So marcar como aerea quando a atleta recebe/controla no ar e finaliza antes de tocar o solo.

Erros comuns:
- marcar passe alto sem finalizacao
- marcar finalizacao apos contato com o solo

Fonte de regra relacionada:
`SRC-IHF-RULES`

Fonte tecnica relacionada:
`SRC-NOTATIONAL-BH`

Observacao CEPRAEA:
Aerea e giro sao mecanismos tecnicos diferentes e nao devem ser agregados numa mesma categoria interna.

### Shoot-out

Definicao:
Situacao regulamentar especial resolvida pelos eventos `shootout_attempt`, `shootout_goal`, `shootout_miss` e `save_shootout`.

Uso no treino:
Treinar decisao, execucao sob pressao e leitura da goleira/defensora no corredor do shoot-out.

Criterio de execucao:
Marcar somente em fluxo proprio de shoot-out, nunca em jogo corrido.

Erros comuns:
- misturar shoot-out com `six_metre_throw`
- registrar defesa de jogo corrido como `save_shootout`

Fonte de regra relacionada:
`SRC-IHF-RULES`

Fonte tecnica relacionada:
`docs/Contrato_Operacional.md`

Observacao CEPRAEA:
No scout atual, shoot-out e tratado como bloco proprio de analise e nao deve ser diluido em conversao ofensiva comum.

### Especialista

Definicao:
Atleta atuando na funcao de especialista, ligada aos eventos `specialist_attempt` e `specialist_goal`.

Uso no treino:
Avaliar uso tatico do recurso de 2 pontos, frequencia de acionamento e eficiencia especifica.

Criterio de execucao:
So usar quando a funcao de especialista estiver visivel no video ou operacionalmente confirmada.

Erros comuns:
- chamar qualquer gol de 2 pontos de gol da especialista
- registrar especialista sem confirmacao visual/operacional

Fonte de regra relacionada:
`SRC-IHF-RULES`

Fonte tecnica relacionada:
`docs/taxonomy_dictionary.md`

Observacao CEPRAEA:
A especialista e tratada como papel funcional de pontuacao e precisa ficar separada de inflight, giro e shoot-out.

### Defensora

Definicao:
No contexto interno atual, termo funcional para a atleta que executa tarefa defensiva observavel. No shoot-out, pode designar a atleta que defende a tentativa naquele fluxo especifico.

Uso no treino:
Descrever responsabilidade defensiva em recortes de video e feedback.

Criterio de execucao:
No scout estruturado, preferir eventos observaveis (`block`, `steal`, `forced_error`, `save`, `save_shootout`) em vez do rotulo genérico "defensora".

Erros comuns:
- usar "defensora" como evento
- substituir evento observavel por interpretacao posicional vaga

Fonte de regra relacionada:
`docs/Contrato_Operacional.md`

Fonte tecnica relacionada:
`docs/evidence_matrix.md`

Observacao CEPRAEA:
`Defensora` e rotulo funcional interno; nao e evento nem KPI por si so.

### Goleira

Definicao:
Atleta em funcao de goleira ligada a eventos como `save`, `save_shootout`, `goalkeeper_distribution` e, em contratos especificos, `goalkeeper_save` e `goalkeeper_goal_allowed`.

Uso no treino:
Avaliar defesa, reposicao, ciclo com especialista e resposta a 6 metros/shoot-out.

Criterio de execucao:
Diferenciar defesa da goleira de bloqueio de jogadora de linha.

Erros comuns:
- registrar bloqueio de linha como defesa da goleira
- misturar papel de goleira em jogo corrido com papel de defensora do shoot-out sem contexto

Fonte de regra relacionada:
`SRC-IHF-RULES`

Fonte tecnica relacionada:
`docs/Contrato_Operacional.md`

Observacao CEPRAEA:
A goleira e avaliada por defesa, gol sofrido e distribuicao; nao apenas por defesas isoladas.

### Bloqueio

Definicao:
Bloqueio de arremesso por defensora de linha, associado ao evento `block`.

Uso no treino:
Medir acao defensiva de linha que altera ou impede a trajetoria do arremesso.

Criterio de execucao:
Se a goleira e responsavel direta pela defesa, preferir `save`.

Erros comuns:
- chamar qualquer contestacao de arremesso de bloqueio
- marcar defesa da goleira como bloqueio

Fonte de regra relacionada:
`docs/taxonomy_dictionary.md`

Fonte tecnica relacionada:
`SRC-NOTATIONAL-BH`

Observacao CEPRAEA:
Bloqueio e evento observavel; interpretacao tática sobre "boa defesa" vem depois.

### Transicao

Definicao:
Fase de passagem ataque-defesa ou defesa-ataque ligada aos eventos `fast_break_for`, `fast_break_against`, `transition_recovery_good` e `transition_recovery_bad`.

Uso no treino:
Avaliar velocidade de reorganizacao, exposicao defensiva e aproveitamento de vantagem.

Criterio de execucao:
Usar apenas quando houver contexto claro de transicao, nao em ataque posicional normal.

Erros comuns:
- chamar qualquer ataque rapido de transicao
- misturar transicao com perda sem finalizacao sem evidencia do contexto

Fonte de regra relacionada:
`SRC-NOTATIONAL-BH`

Fonte tecnica relacionada:
`docs/taxonomy_dictionary.md`

Observacao CEPRAEA:
Transicao no ScoutPraia atual ainda depende de leitura contextual disciplinada; evitar inflar o conceito.

### Golden Goal

Definicao:
Metodo oficial em que o primeiro gol decide o periodo/continuidade, conforme regra vigente.

Uso no treino:
Preparar tomada de decisao em fase de altissima criticidade temporal.

Criterio de execucao:
Tratar sempre como situacao regulamentar especifica, nunca como rotulo generico para "momento decisivo".

Erros comuns:
- usar "Golden Goal" como metafora tática fora do contexto oficial

Fonte de regra relacionada:
`SRC-IHF-RULES`

Fonte tecnica relacionada:
`docs/sources/regras.md`

Observacao CEPRAEA:
No scout, Golden Goal e situacao de regra, nao categoria interna de emocao ou importancia.

### Jogo passivo

Definicao:
Perda ou advertencia relacionada a passividade ofensiva, com destaque para a regra de 4 passes apos o sinal.

Uso no treino:
Corrigir ritmo de circulacao e tomada de decisao apos pre-aviso arbitral.

Criterio de execucao:
No fluxo atual, usar subtipo especifico quando houver base observavel para `passive_play_turnover`.

Erros comuns:
- chamar ataque lento de jogo passivo sem sinal/contexto
- usar como justificativa subjetiva para qualquer perda

Fonte de regra relacionada:
`SRC-IHF-RULES`

Fonte tecnica relacionada:
`IHF_UPDATE_BH_2026_04`

Observacao CEPRAEA:
A mudanca IHF 2026 sobre 4 passes deve ser citada quando o tema for regra.

### 6 metros

Definicao:
Tiro de 6 metros ligado ao evento `six_metre_throw`.

Uso no treino:
Avaliar execucao ofensiva e resposta da goleira em situacao de alta conversao esperada.

Criterio de execucao:
Nao misturar com shoot-out.

Erros comuns:
- tratar 6 metros como shoot-out
- registrar 6 metros como arremesso comum sem subtipo

Fonte de regra relacionada:
`SRC-IHF-RULES`

Fonte tecnica relacionada:
`scoutpraia/services/analytics_service.py`

Observacao CEPRAEA:
No relatorio, 6 metros merece leitura propria pelo impacto no desempenho da goleira e da finalizadora.

### Substituicao

Definicao:
Troca de atletas conforme area de substituicao e regras vigentes.

Uso no treino:
Monitorar erro de troca e ciclo funcional entre especialista e goleira quando aplicavel.

Criterio de execucao:
Em evento de erro, usar categoria de perda por substituicao.

Erros comuns:
- tratar troca tática comum como erro
- nao distinguir substituicao regular de `substitution_error_turnover`

Fonte de regra relacionada:
`SRC-IHF-RULES`

Fonte tecnica relacionada:
`docs/Contrato_Operacional.md`

Observacao CEPRAEA:
Substituicao e mecanismo operacional chave no beach handball e precisa ser observada com disciplina.

### Pontuacao de 1 ponto

Definicao:
Gol comum que vale 1 ponto.

Uso no treino:
Separar finalizacao regular de mecanismos especiais de 2 pontos.

Criterio de execucao:
Nao somar como 2 pontos sem base regulamentar clara.

Erros comuns:
- atribuir 2 pontos a gol comum

Fonte de regra relacionada:
`SRC-IHF-RULES`

Fonte tecnica relacionada:
`docs/evidence_matrix.md`

Observacao CEPRAEA:
Pontuacao e coluna estrutural do scout; erro aqui contamina todo KPI ofensivo.

### Pontuacao de 2 pontos

Definicao:
Gol especial de 2 pontos, incluindo mecanismos como especialista, giro, inflight ou situacoes regulamentares especificas.

Uso no treino:
Ler eficiencia, perfil tecnico e uso tatico dos mecanismos de 2 pontos.

Criterio de execucao:
Sempre que possivel, preferir categoria especifica (`specialist_goal`, `inflight_goal`, etc.) ao fallback generico.

Erros comuns:
- agrupar todos os gols de 2 pontos sem mecanismo
- classificar mecanismo sem evidencia

Fonte de regra relacionada:
`SRC-IHF-RULES`

Fonte tecnica relacionada:
`docs/evidence_matrix.md`

Observacao CEPRAEA:
O fallback `two_point_goal` continua util, mas a leitura tática melhora quando o mecanismo fica separado.

## Termos internos formalizados para nomenclatura e playbook

Regra de uso desta secao:

- os termos abaixo podem ser usados como linguagem interna CEPRAEA
- eles nao viram evento ou KPI so por estarem definidos aqui
- quando o termo ainda nao tiver campo proprio no app, tratar como convencao interna formalizada, nao como automacao pronta

### 3:0

Definicao:
Sistema defensivo interno com tres defensoras compactas proximas a linha de 6 metros, priorizando fechamento de centro, cobertura lateral coordenada e protecao do corredor frontal.

Uso no treino:
Treinar comunicacao de bloco, deslocamento lateral conjunto, cobertura de pivô e sincronizacao entre bloqueio de linha e leitura da goleira.

Criterio de execucao:
Usar como convencao interna quando o plano defensivo pedir bloco compacto. No scout estruturado atual, a leitura deve continuar sustentada por eventos observaveis como `block`, `forced_error`, `save` e `defensive_breakdown`.

Erros comuns:
- chamar qualquer defesa baixa de `3:0` sem observar alinhamento real das tres defensoras
- tratar o rotulo tatico como se ele substituisse o evento observavel

Fonte de regra relacionada:
`SRC-IHF-RULES`

Fonte tecnica relacionada:
`docs/evidence_matrix.md`

Observacao CEPRAEA:
No CEPRAEA adulto feminino, `3:0` nomeia uma base de bloco compacto. Ainda nao e evento nem KPI nativo do ScoutPraia v0.1.

### 2:1

Definicao:
Sistema defensivo interno com duas defensoras de base e uma defensora avancada para pressionar a armacao adversaria, especialmente a especialista.

Uso no treino:
Treinar pressao orientada sobre a circulacao central, corte de linha de passe e inducao de erro ou jogo passivo sem perder a cobertura da base.

Criterio de execucao:
Usar como convencao interna quando houver uma atleta avancada claramente destacada. No app atual, a analise continua dependente dos eventos observaveis de defesa e de revisao em clipe.

Erros comuns:
- confundir pressao ocasional de uma jogadora com sistema `2:1`
- usar o rotulo para encobrir desorganizacao defensiva

Fonte de regra relacionada:
`SRC-IHF-RULES`

Fonte tecnica relacionada:
`docs/evidence_matrix.md`

Observacao CEPRAEA:
No CEPRAEA, `2:1` nomeia uma variacao agressiva de pressao. Ainda nao e classificacao automatica do ScoutPraia v0.1.

### 4:0

Definicao:
Sistema ofensivo interno sem pivô fixa, com quatro jogadoras de linha em circulacao e amplitude maxima para gerar vantagem, troca de corredor e criacao de finalizacao de 2 pontos.

Uso no treino:
Treinar ritmo de circulacao, largura ofensiva, cruzamentos, passe extra e leitura do melhor mecanismo de finalizacao.

Criterio de execucao:
Usar como convencao interna quando a equipe atacar sem referencia fixa infiltrada. No scout atual, a sustentacao analitica deve continuar em eventos e KPIs observaveis, nao no rotulo em si.

Erros comuns:
- chamar qualquer ataque aberto de `4:0` sem circulacao real
- usar o rotulo como justificativa para posse estagnada ou sem progressao

Fonte de regra relacionada:
`SRC-IHF-RULES`

Fonte tecnica relacionada:
`docs/taxonomy_dictionary.md`

Observacao CEPRAEA:
No CEPRAEA, `4:0` tambem pode aparecer como `Ataque em Carrossel`. E convencao interna formalizada, nao evento do app.

### Devolucao

Definicao:
Acao interna de passe e retorno imediato da bola para a mesma jogadora ou para a continuidade da combinacao curta, com intencao de criar infiltracao, passe final ou mecanismo de 2 pontos.

Uso no treino:
Treinar tabela curta, passe extra e desmarque rapido para quebrar pressao e acelerar a criacao ofensiva.

Criterio de execucao:
Usar como linguagem de playbook e feedback de treino. No scout estruturado, nao classificar `devolucao` como evento ou KPI autonomo sem nova formalizacao taxonomica.

Erros comuns:
- chamar qualquer segundo passe de `devolucao`
- transformar a palavra em categoria estatistica sem evidencia operacional

Fonte de regra relacionada:
`SRC-IHF-RULES`

Fonte tecnica relacionada:
`docs/Contrato_Operacional.md`

Observacao CEPRAEA:
`Devolucao` esta formalizada como nomenclatura interna de combinacao ofensiva. Continua fora da taxonomia ativa do app.

### Ultimos 15 segundos

Definicao:
Recorte temporal critico do set em que decisao, controle emocional e disciplina de contato precisam respeitar com rigor a regra vigente e as atualizacoes IHF 2026.

Uso no treino:
Treinar posse sob pressao, escolha de risco, organizacao defensiva sem contato indevido e execucao de protocolo situacional de fim de set.

Criterio de execucao:
Quando o contexto for regra, prevalece a fonte normativa IHF. Quando o contexto for playbook CEPRAEA, o termo pode organizar estrategia interna de conservacao de posse ou pressao final, sempre sem ser apresentado como regra autonoma.

Erros comuns:
- tratar `ultimos 15 segundos` como metafora ampla para qualquer momento decisivo
- misturar protocolo interno de fim de set com a regra oficial sem citar a fonte

Fonte de regra relacionada:
`IHF_UPDATE_BH_2026_04`

Fonte tecnica relacionada:
`docs/evidence_matrix.md`

Observacao CEPRAEA:
No CEPRAEA, esse termo organiza protocolo interno de clutch time. Nao e evento do app nem KPI final.
