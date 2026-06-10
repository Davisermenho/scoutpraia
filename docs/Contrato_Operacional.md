\---  
title: Contrato Operacional — Eventos v1  
project: ScoutPraia  
version: eventos\_v1.0  
owner: Davi Sermenho  
last\_updated: 2026-06-10  
semantic\_source: Contrato\_Operacional.md  
implementation\_source: SCOUT\_DESIGN\_TEMPLATE  
repository: Davisermenho/scoutpraia  
status: em\_implementacao\_controlada  
\---

\# Contrato Operacional — Eventos v1

\#\# 1\. Objetivo

Este documento define as regras semânticas, taxonômicas e operacionais para os módulos v1 do ScoutPraia. Ele deve ser usado como referência controlada por humanos e agentes de IA.

Regra principal:

\`\`\`yaml  
global\_rule:  
  source\_priority:  
    1: "SCOUT\_DESIGN\_TEMPLATE"  
    2: "Contrato\_Operacional.md"  
    3: "Davisermenho/scoutpraia"  
  blocking\_rule: "Divergência entre fontes bloqueia implementação até correção."  
\`\`\`

\#\# 2\. Fontes de verdade

\`\`\`yaml  
sources:  
  semantic\_rules: "Contrato\_Operacional.md"  
  implementation\_structure: "SCOUT\_DESIGN\_TEMPLATE"  
  code\_and\_tests: "Davisermenho/scoutpraia"  
  evidence: "ACCEPTANCE\_EVIDENCE"  
  blocking\_rule: "Divergência entre fontes bloqueia implementação até correção."  
\`\`\`

\#\# 3\. Status dos módulos

\`\`\`yaml  
module\_status:  
  attack\_no\_shot\_v1:  
    name: "Ataque sem finalização v1.0"  
    status: "bloqueado\_por\_auditoria"  
    import\_rule: "importar\_v1"  
    evidence: \["EV-001", "EV-002", "EV-003", "EV-004", "EV-005"\]  
    evidence\_status: "pending\_or\_inconsistent"  
    issue: "Planilha antiga possui linhas com import\_rule\_v1=importar\_v1, mas ACCEPTANCE\_EVIDENCE ainda aponta EV-001 a EV-005 como pending e alguns caminhos de teste citados não existem no repositório atual."  
    blocking\_rule: "Não promover nem implementar até resolver evidências e nomenclatura entre planilha e código."

  finalization\_v1:  
    name: "Finalização v1.0"  
    status: "contrato\_validado"  
    import\_rule: "nao\_importar\_v1"  
    evidence: \["EV-006"\]  
    evidence\_status: "passed"  
    validated\_core\_events:  
      \- "simple\_shot"  
      \- "spin\_shot"  
      \- "inflight\_shot"  
      \- "goalkeeper\_shot"  
      \- "six\_metre\_throw"  
    auxiliary\_only:  
      \- "specialist\_finish\_role"  
    blocking\_rule: "Mesmo validado por contrato, não importar no app antes de implementação controlada e testes de integração."

  offensive\_creation\_v1:  
    name: "Criação ofensiva v1.0"  
    status: "contrato\_validado"  
    import\_rule: "nao\_importar\_v1"  
    evidence: \["EV-007"\]  
    evidence\_status: "passed"  
    validated\_core\_event: "assist\_to\_finalization"  
    reclassified\_auxiliary\_events:  
      \- "assist\_to\_inflight\_shot"  
      \- "pivot\_feed\_to\_shot"  
    review\_only\_events:  
      \- "advantage\_pass\_to\_free\_player"  
      \- "collective\_action\_creates\_shot"  
    blocking\_rule: "Mesmo validado por contrato, não importar no app antes de implementação controlada e testes de integração."

  defensive\_v1:  
    name: "Defensivo v1.0"  
    status: "contrato\_validado"  
    import\_rule: "nao\_importar\_v1"  
    evidence: \["EV-008"\]  
    evidence\_status: "passed"  
    validated\_core\_event: "line\_block\_shot"  
    review\_only\_events:  
      \- "defensive\_pressure\_forced\_error"  
      \- "steal\_or\_interception"  
    future\_events:  
      \- "defensive\_rebound\_recovery"  
    blocking\_rule: "Mesmo validado por contrato, não importar no app antes de implementação controlada e testes de integração."  
\`\`\`

\#\# 4\. Governança global

\`\`\`yaml  
global\_constraints:  
  forbidden\_actions:  
    \- "importar\_via\_category\_apenas"  
    \- "misturar\_ataque\_sem\_finalizacao\_com\_finalizacao"  
    \- "misturar\_transicao\_com\_ataque\_sem\_finalizacao"  
    \- "misturar\_criacao\_ofensiva\_com\_finalizacao"  
    \- "misturar\_defensivo\_com\_goleira"  
    \- "misturar\_defensivo\_com\_transicao"  
    \- "criar\_specialist\_shot"  
    \- "criar\_position\_code\_specialist"  
    \- "allow\_manual\_points\_in\_finalization"  
    \- "allow\_goal\_zone\_outside\_finalization"  
  activation\_rules:  
    \- "require\_implementation\_test\_evidence"  
    \- "require\_import\_rule\_v1\_explicit"  
    \- "require\_module\_contract\_status\_explicit"  
    \- "require\_contract\_scope\_explicit"  
\`\`\`

\#\# 5\. Taxonomias globais

\`\`\`yaml  
taxonomies:  
  systems:  
    valid\_codes: \["AT\_3X1", "AT\_4X0", "DEF\_3X0", "DEF\_2X1", "man\_to\_man"\]  
    context\_only: \["fast\_break\_attack", "specialist\_on\_court", "empty\_goal\_attack", "high\_press"\]  
    note: "Especialista é papel dinâmico, não sistema ou posição."

  court\_zones:  
    lanes: \["lane\_1\_outer\_left", "lane\_2\_inner\_left", "lane\_3\_central\_axis", "lane\_4\_inner\_right", "lane\_5\_outer\_right"\]  
    depth: \["depth\_0\_backcourt", "depth\_1\_far", "depth\_2\_mid", "depth\_3\_near\_area"\]  
    note: "Zona da quadra descreve localização espacial, não função tática."

  goal\_zones:  
    note: "Aplicável apenas à Finalização quando a trajetória ao gol for visível ou inferível com segurança."

  possession\_results:  
    global: \["goal", "save", "shot\_wide", "shot\_blocked", "lost\_possession\_no\_shot", "rebound\_live", "execution\_invalid\_6m"\]  
\`\`\`

\#\# 6\. Módulo attack\_no\_shot\_v1

\`\`\`yaml  
module\_attack\_no\_shot:  
  module\_id: "attack\_no\_shot\_v1"  
  name: "Ataque sem finalização v1.0"  
  definition: "Toda posse ofensiva sem arremesso intencional ao gol."  
  status: "bloqueado\_por\_auditoria"  
  import\_rule: "nao\_importar\_v1"  
  mandatory\_result: "lost\_possession\_no\_shot"  
  source\_tabs:  
    events: "EVENTOS"  
    fields: "CAMPOS\_AUXILIARES\_ATAQUE\_SEM\_FINALIZACAO"  
    tests: "TESTES\_ATAQUE\_SEM\_FINALIZACAO"  
  spreadsheet\_events\_expected:  
    \- "technical\_error\_unforced"  
    \- "technical\_error\_forced"  
    \- "offensive\_foul"  
    \- "goal\_area\_invasion\_attack"  
    \- "passive\_play\_turnover"  
    \- "bad\_substitution\_attack"  
    \- "turnover\_unclassified"  
  current\_blockers:  
    \- "EV-001 a EV-005 ainda não estão limpas no ACCEPTANCE\_EVIDENCE."  
    \- "Alguns caminhos de teste antigos citados na planilha não existem no GitHub atual."  
    \- "Registry do repositório usa nomes antigos/conservadores diferentes dos event\_codes oficiais da planilha."  
    \- "Linhas antigas da aba EVENTOS indicam import\_rule\_v1=importar\_v1; contrato operacional deve prevalecer como bloqueio até correção."  
  blocking\_rule: "Não implementar nem importar Ataque sem finalização v1.0 antes de resolver evidências e nomenclatura."  
\`\`\`

\#\# 7\. Módulo finalization\_v1

\`\`\`yaml  
module\_finalization:  
  module\_id: "finalization\_v1"  
  name: "Finalização v1.0"  
  definition: "Ação com arremesso intencional ao gol."  
  status: "contrato\_validado"  
  import\_rule: "nao\_importar\_v1"  
  evidence: "EV-006"  
  source\_tabs:  
    events: "EVENTOS"  
    fields: "CAMPOS\_AUXILIARES\_FINALIZACAO"  
    results\_by\_event: "RESULTADOS\_POR\_EVENTO\_FINALIZACAO"  
    scoring: "PONTUACAO\_FINALIZACAO"  
    tests: "TESTES\_FINALIZACAO"  
  core\_events:  
    simple\_shot:  
      ui\_type: "botao\_principal"  
      points\_rule: "1 se goal \+ field\_player; 2 se goal \+ specialist; 0 se não gol"  
    spin\_shot:  
      ui\_type: "botao\_principal"  
      points\_rule: "2 se goal; 0 se não gol"  
    inflight\_shot:  
      ui\_type: "botao\_principal"  
      points\_rule: "2 se goal; 0 se não gol"  
    goalkeeper\_shot:  
      ui\_type: "botao\_principal"  
      points\_rule: "2 se goal; 0 se não gol"  
    six\_metre\_throw:  
      ui\_type: "botao\_principal"  
      points\_rule: "2 se goal; 0 se não gol"  
  auxiliary\_only:  
    specialist\_finish\_role:  
      rule: "Especialista é função dinâmica via scorer\_role/offensive\_role; não é botão nem position\_code."  
  forbidden\_logic:  
    \- "Não criar specialist\_shot."  
    \- "Não criar position\_code=specialist."  
    \- "Não permitir pontos manuais divergentes da pontuação derivada."  
    \- "Não permitir lost\_possession\_no\_shot em Finalização."  
    \- "Não permitir six\_metre\_throw \+ shot\_blocked."  
    \- "Não permitir goalkeeper\_shot \+ shot\_blocked na v1.0."  
\`\`\`

\#\# 8\. Módulo offensive\_creation\_v1

\`\`\`yaml  
module\_offensive\_creation:  
  module\_id: "offensive\_creation\_v1"  
  name: "Criação ofensiva v1.0"  
  definition: "Ações ofensivas que criam, melhoram ou organizam condição de finalização, sem serem a finalização em si e sem serem perda de posse sem arremesso."  
  status: "contrato\_validado"  
  import\_rule: "nao\_importar\_v1"  
  evidence: "EV-007"  
  source\_tabs:  
    events: "EVENTOS"  
    fields: "CAMPOS\_AUXILIARES\_CRIACAO\_OFENSIVA"  
    results: "RESULTADOS\_CRIACAO\_OFENSIVA"  
    tests: "TESTES\_CRIACAO\_OFENSIVA"  
    versioning: "VERSIONAMENTO\_CRIACAO\_OFENSIVA"  
  active\_core\_event:  
    assist\_to\_finalization:  
      ui\_type: "botao\_principal"  
      rule: "Último passe que gera finalização imediata."  
      required\_result\_creation: "shot\_created"  
      allowed\_creation\_types: \["direct\_assist", "inflight\_setup", "pivot\_feed"\]  
      required\_fields:  
        \- "passer\_id"  
        \- "receiver\_id"  
        \- "system\_code"  
        \- "pass\_origin\_position"  
        \- "receiver\_position"  
        \- "pass\_origin\_zone"  
        \- "receiver\_zone"  
        \- "creation\_type"  
        \- "created\_finalization\_type"  
        \- "result\_creation"  
  reclassified\_auxiliary\_events:  
    assist\_to\_inflight\_shot:  
      maps\_to: "assist\_to\_finalization \+ creation\_type=inflight\_setup \+ created\_finalization\_type=inflight\_shot"  
      ui\_type: "campo\_auxiliar"  
      import\_rule: "nao\_importar\_v1"  
    pivot\_feed\_to\_shot:  
      maps\_to: "assist\_to\_finalization \+ creation\_type=pivot\_feed"  
      ui\_type: "campo\_auxiliar"  
      import\_rule: "nao\_importar\_v1"  
  review\_only\_events:  
    advantage\_pass\_to\_free\_player:  
      ui\_type: "botao\_secundario\_revisao"  
      required: \["created\_advantage", "result\_creation=clear\_chance\_created", "review\_marker=Sim"\]  
      reason: "Subjetivo sem exemplos reais suficientes; não liberar como botão ativo."  
    collective\_action\_creates\_shot:  
      ui\_type: "fallback\_revisao"  
      required: \["system\_code", "creation\_type", "result\_creation", "review\_marker=Sim"\]  
      reason: "Amplo demais para botão v1.0; usar apenas quando passe criador não for isolável."  
  location\_rules:  
    pass\_origin\_position: "POSIÇÕES"  
    receiver\_position: "POSIÇÕES"  
    pass\_origin\_zone: "ZONAS\_QUADRA"  
    receiver\_zone: "ZONAS\_QUADRA"  
    note: "Posição tática não substitui zona espacial; zona espacial não substitui posição tática."  
  forbidden\_logic:  
    \- "Criação ofensiva não calcula pontos."  
    \- "Não usar goal\_zone em Criação ofensiva."  
    \- "Não usar shot\_origin\_depth em Criação ofensiva."  
    \- "Não usar result\_possession sem linked\_finalization\_id."  
    \- "Não usar turnover\_after\_creation\_error como resultado ativo; perda sem arremesso pertence ao attack\_no\_shot\_v1."  
    \- "Não criar botões novos a partir de creation\_type."  
\`\`\`

\#\# 9\. Módulo defensive\_v1

\`\`\`yaml  
module\_defensive:  
  module\_id: "defensive\_v1"  
  name: "Defensivo v1.0"  
  definition: "Ações observáveis de jogadoras de linha defensiva que bloqueiam finalização, forçam erro ou recuperam/interceptam posse, sem misturar com Goleira, Transição ou Finalização."  
  status: "contrato\_validado"  
  import\_rule: "nao\_importar\_v1"  
  evidence: "EV-008"  
  source\_tabs:  
    events: "EVENTOS"  
    fields: "CAMPOS\_AUXILIARES\_DEFENSIVO"  
    results: "RESULTADOS\_DEFENSIVO"  
    tests: "TESTES\_DEFENSIVO"  
    versioning: "VERSIONAMENTO\_DEFENSIVO"  
  active\_core\_event:  
    line\_block\_shot:  
      ui\_type: "botao\_principal"  
      rule: "Bloqueio/interferência legal de jogadora de linha em finalização bloqueável."  
      required\_result\_defense: "shot\_blocked\_linked"  
      required\_link: "linked\_finalization\_id"  
      allowed\_linked\_finalization\_event\_code: \["simple\_shot", "spin\_shot", "inflight\_shot"\]  
      forbidden\_linked\_finalization\_event\_code: \["six\_metre\_throw", "goalkeeper\_shot"\]  
      required\_fields:  
        \- "defender\_id"  
        \- "defensive\_system\_code"  
        \- "defensive\_position\_code"  
        \- "linked\_finalization\_id"  
        \- "linked\_finalization\_event\_code"  
        \- "court\_lane"  
        \- "court\_depth"  
        \- "result\_defense"  
  review\_only\_events:  
    defensive\_pressure\_forced\_error:  
      ui\_type: "botao\_secundario\_revisao"  
      required: \["linked\_attack\_no\_shot\_id", "review\_marker=Sim"\]  
      reason: "Não duplicar technical\_error\_forced sem vínculo com attack\_no\_shot\_v1."  
    steal\_or\_interception:  
      ui\_type: "botao\_secundario\_revisao"  
      required: \["defensive\_control\_clear", "review\_marker=Sim"\]  
      reason: "Conecta com troca de posse e Transição; manter em revisão/futuro."  
  future\_events:  
    defensive\_rebound\_recovery:  
      ui\_type: "future\_module"  
      reason: "Depende de modelagem de Rebote/Transição."  
  defensive\_positions\_by\_system:  
    DEF\_3X0: \["def\_3x0\_cobertura", "def\_3x0\_base", "def\_3x0\_solta"\]  
    DEF\_2X1: \["def\_2x1\_cobertura", "def\_2x1\_avancada", "def\_2x1\_solta"\]  
  forbidden\_logic:  
    \- "Não usar Base no DEF\_2X1."  
    \- "Não usar Avançada no DEF\_3X0."  
    \- "Não usar name\_ui como defensive\_position\_code; usar position\_code."  
    \- "Não registrar defesa da goleira como Defensivo v1.0."  
    \- "Não registrar line\_block\_shot sem linked\_finalization\_id."  
    \- "Não permitir line\_block\_shot vinculado a six\_metre\_throw ou goalkeeper\_shot na v1.0."  
    \- "Não duplicar technical\_error\_forced sem linked\_attack\_no\_shot\_id."  
    \- "Não calcular pontos em Defensivo."  
    \- "Não usar goal\_zone, scorer\_role ou shot\_origin\_depth em Defensivo."  
\`\`\`

\#\# 10\. Evidências de aceitação

\`\`\`yaml  
acceptance\_tests:  
  EV-001:  
    command: "python3 \-m pytest tests/test\_attack\_no\_shot\_contract.py \-q"  
    expected\_result: "all tests passed"  
    actual\_result: "pending"  
    status: "pending"  
    module: "attack\_no\_shot\_v1"  
    note: "Comando/caminho precisa ser verificado no repositório atual."

  EV-002:  
    command: "python3 \-m pytest \-q"  
    expected\_result: "all tests passed"  
    actual\_result: "pending"  
    status: "pending"  
    module: "global"  
    note: "Validação global pendente no ACCEPTANCE\_EVIDENCE."

  EV-003:  
    command: "scripts/verify\_current\_state.sh"  
    expected\_result: "all checks passed"  
    actual\_result: "pending"  
    status: "pending"  
    module: "global"  
    note: "Obrigatório conforme governança antes de liberar implementação."

  EV-004:  
    command: "python3 \-m pytest tests/test\_attack\_no\_shot\_import\_scope.py \-q"  
    expected\_result: "all tests passed"  
    actual\_result: "pending"  
    status: "pending"  
    module: "attack\_no\_shot\_v1"  
    note: "Comando/caminho precisa ser verificado no repositório atual."

  EV-005:  
    command: "python3 \-m pytest tests/test\_eventos\_sheet\_scope.py \-q"  
    expected\_result: "all tests passed"  
    actual\_result: "pending"  
    status: "pending"  
    module: "sheet\_scope"  
    note: "Comando/caminho precisa ser verificado no repositório atual."

  EV-006:  
    command: "python3 \-m pytest tests/test\_finalization\_contract.py"  
    expected\_result: "29 passed"  
    actual\_result: "29 passed in 0.04s"  
    status: "passed"  
    executed\_by: "Davi Sermenho"  
    executed\_at: "2026-06-10"  
    module: "finalization\_v1"

  EV-007:  
    command: "python3 \-m pytest tests/test\_offensive\_creation\_contract.py"  
    expected\_result: "20 passed"  
    actual\_result: "20 passed in 0.04s"  
    status: "passed"  
    executed\_by: "Davi Sermenho"  
    executed\_at: "2026-06-10"  
    commit: "11da639bbdb5b90973972059424690cc28d66145"  
    module: "offensive\_creation\_v1"

  EV-008:  
    command: "python3 \-m pytest tests/test\_defensive\_contract.py \-q"  
    expected\_result: "28 passed"  
    actual\_result: "28 passed in 0.05s"  
    status: "passed"  
    executed\_by: "Davi Sermenho"  
    executed\_at: "2026-06-10"  
    commit: "7a93d7728c966f229cf253d8fc5ca3ead154138d"  
    module: "defensive\_v1"  
\`\`\`

\#\# 11\. Regras de liberação

\`\`\`yaml  
release\_rules:  
  current\_state: "contratos\_validados\_parcialmente"  
  app\_import\_status: "bloqueado"  
  import\_rule\_required\_for\_app: "importar\_v1"  
  current\_safe\_import\_rule: "nao\_importar\_v1"  
  blockers\_before\_app\_activation:  
    \- "Resolver EV-001 a EV-005."  
    \- "Alinhar attack\_no\_shot\_v1 entre planilha, contrato e registry do repositório."  
    \- "Atualizar registry do repositório para incluir offensive\_creation\_v1 e defensive\_v1, se esses módulos forem entrar no código central."  
    \- "Rodar python3 \-m pytest."  
    \- "Rodar scripts/verify\_current\_state.sh."  
    \- "Validar que nenhum módulo v1 é importado apenas por category."  
\`\`\`

\#\# 12\. Correção G0 — Ataque sem finalização v1.0  
\`\`\`yaml  
g0\_attack\_no\_shot\_alignment:  
  date: "2026-06-10"  
  module\_id: "attack\_no\_shot\_v1"  
  status: "contrato\_validado"  
  import\_rule\_v1: "importar\_v1"  
  official\_events: \["technical\_error\_unforced", "technical\_error\_forced", "offensive\_foul", "goal\_area\_invasion\_attack", "passive\_play\_turnover", "bad\_substitution\_attack", "turnover\_unclassified"\]  
  deprecated\_codes: \["ball\_control\_turnover", "offensive\_foul\_turnover", "substitution\_error\_turnover", "turnover\_cause\_detail"\]  
  repo\_commits: \["904868a", "ac033d6", "2df3044", "3ee9553", "e5c080a", "01cced7"\]  
  evidence\_pending\_execution: \["EV-001", "EV-002", "EV-003", "EV-004", "EV-005"\]  
  required\_commands: \["python3 \-m pytest tests/test\_attack\_no\_shot\_contract.py \-q", "python3 \-m pytest tests/test\_attack\_no\_shot\_import\_scope.py \-q", "python3 \-m pytest tests/test\_eventos\_sheet\_scope.py \-q", "python3 \-m pytest \-q", "scripts/verify\_current\_state.sh"\]  
  rule: "EV-001 a EV-005 só mudam para passed após execução local enviada pelo usuário."  
\`\`\`

\#\# 13\. Evidência aprovada — G0 Ataque sem finalização v1.0  
\`\`\`yaml  
g0\_attack\_no\_shot\_acceptance:  
  date: "2026-06-10"  
  git\_head: "5cf588c"  
  executed\_by: "Davi Sermenho"  
  module\_id: "attack\_no\_shot\_v1"  
  status\_after\_evidence: "contrato\_validado"  
  import\_rule\_v1: "importar\_v1"  
  evidence:  
    EV-001:  
      command: "python3 \-m pytest tests/test\_attack\_no\_shot\_contract.py \-q"  
      result: "25 passed in 0.05s"  
      status: "passed"  
    EV-002:  
      command: "python3 \-m pytest \-q"  
      result: "196 passed in 14.89s"  
      status: "passed"  
    EV-003:  
      command: "scripts/verify\_current\_state.sh"  
      result: "verde; 196 passed in 11.96s; hygiene/import/seed/git whitespace ok"  
      status: "passed"  
    EV-004:  
      command: "python3 \-m pytest tests/test\_attack\_no\_shot\_import\_scope.py \-q"  
      result: "4 passed in 0.03s"  
      status: "passed"  
    EV-005:  
      command: "python3 \-m pytest tests/test\_eventos\_sheet\_scope.py \-q"  
      result: "7 passed in 0.02s"  
      status: "passed"  
  compatibility\_note: "Códigos legados de UI foram mantidos como aliases temporários; os nomes oficiais continuam sendo os definidos no SCOUT\_DESIGN\_TEMPLATE."  
  seed\_note: "Taxonomia operacional padrão permanece ScoutPraia v0.1 draft com 31 eventos; G0 valida contrato/código, não troca automática do seed."  
\`\`\`  
