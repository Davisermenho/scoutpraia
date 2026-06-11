---

titulo: CHUNKS_FINAIS_RAG_IHF_RULES_BH_2026_PT

source_id_normativo: IHF_RULES_BH_2026_EN

source_id_operacional: IHF_RULES_BH_2026_PT_TRANSLATION

fonte_complementar: IHF_UPDATE_BH_2026 quando aplicável

idioma: pt-BR

tipo: chunks finais para RAG

status: versao_inicial_para_ingestao_controlada

regra_de_conflito: prevalece o PDF oficial IHF em inglês

regra_de_lacuna: se não estiver nos chunks liberados, responder “não encontrado nas fontes processadas” ou consultar diretamente o PDF oficial IHF

base_de_controle: matriz_chunks_final

criado_em: 2026-06-10

---

# CHUNKS FINAIS — RAG IHF BEACH HANDBALL 2026

## Instrução obrigatória para o agente

Estas unidades só podem ser usadas dentro do escopo declarado em cada chunk. Chunks com ressalva não autorizam generalização para a regra inteira. Se a pergunta depender de trecho bloqueado na matriz, o agente deve responder: “não encontrado nas fontes processadas” ou consultar diretamente o PDF oficial IHF.

## CHUNK_P01_001 — Prólogo e filosofia do Jogo Limpo

status: liberado

fonte_base: IHF_RULES_BH_2026_EN / PT_TRANSLATION

uso_no_agente: responder sobre filosofia, fair play e aplicação geral das regras.

Conteúdo: As regras se aplicam igualmente a participantes femininos e masculinos, exceto na Regra 3, relativa ao tamanho da bola. A filosofia do Beach Handball se baseia no Jogo Limpo: respeitar a saúde, a integridade física e o corpo dos jogadores; respeitar o espírito e a filosofia do jogo; respeitar a fluência do jogo; não tolerar vantagem obtida por violações; e promover verdadeiro espírito esportivo. Infrações marcadas durante o jogo devem ser tratadas contra jogadores individualmente, não como faltas coletivas da equipe.

## CHUNK_P01_002 — Regra 1: quadra, areia, linhas, balizas, mesa e substituição

status: liberado

fonte_base: IHF_RULES_BH_2026_EN / PT_TRANSLATION

uso_no_agente: responder sobre dimensões, segurança, areia, iluminação, balizas, mesa e área de substituição.

Conteúdo: A quadra é um retângulo de 27 m x 12 m, com área de jogo e duas áreas de gol. A areia deve ser nivelada, plana, uniforme, livre de pedras, conchas e objetos perigosos, com pelo menos 40 cm de profundidade. Deve haver zona de segurança de 3 m ao redor. Para jogos noturnos, a iluminação mínima é de 400 lux. As linhas pertencem às áreas que delimitam; as linhas da área de gol ficam a 6 m e paralelas às linhas de gol. As balizas ficam no centro das linhas de gol, com 2 m de altura e 3 m de largura interna. A mesa do cronometrista e secretário fica no meio de uma linha lateral, ao menos 3 m para fora dela, permitindo visão das áreas de substituição. A área de substituição dos jogadores de linha tem 15 m por cerca de 3 m, fora das linhas laterais.

## CHUNK_P01_003 — Regra 2: início, tempo, Gol de Ouro, Shoot-out, sinal final, time-out e team time-out

status: liberado

fonte_base: IHF_RULES_BH_2026_EN / PT_TRANSLATION

ressalva: time-out e team time-out revisados pela fonte normativa em inglês devido extração incompleta da tradução PT.

uso_no_agente: responder sobre início do jogo, períodos, sinal final, tempo técnico e cartão verde.

Conteúdo: Antes da partida há sorteio para escolha de lado da quadra ou área de substituição. Após o intervalo, as equipes trocam de lado, mas não trocam as áreas de substituição. Cada período e o Gol de Ouro começam com tiro de árbitro. O jogo tem dois períodos pontuados separadamente, cada um com 10 minutos, e intervalo de 5 minutos. Se um período termina empatado, usa-se Gol de Ouro. O vencedor de cada período recebe 1 ponto. Se a mesma equipe vence os dois períodos, vence por 2–0; se cada equipe vence um período, a decisão é por Shoot-out. O tempo termina com sinal automático do placar ou cronometrista; se o sinal não soar, árbitro, cronometrista ou delegado apitam. Infrações durante time-out têm as mesmas consequências das infrações durante o tempo de jogo. O time-out usa três apitos curtos e Sinal Manual nº 14; o reinício ocorre com apito. Cada equipe tem direito a um team time-out de 1 minuto por período, solicitado com cartão verde visível, apenas quando a equipe tem posse da bola.

## CHUNK_P02_001 — Regra 3: bola

status: liberado

fonte_base: IHF_RULES_BH_2026_EN

uso_no_agente: responder sobre tamanho, peso, quantidade de bolas e reposição.

Conteúdo: O jogo é disputado com bola de borracha redonda e não escorregadia. A bola masculina pesa 350–370 g e tem circunferência de 54–56 cm. A bola feminina pesa 280–300 g e tem circunferência de 50–52 cm. Bola menor pode ser usada em jogos de crianças. Antes de cada jogo, pelo menos 4 bolas regulamentares devem estar disponíveis. Quando a bola sai da quadra, o goleiro indicado pelo árbitro deve colocar bola substituta em jogo rapidamente para reduzir interrupções.

## CHUNK_P02_002 — Regra 4: composição, elegibilidade, oficiais e substituições

status: liberado

fonte_base: IHF_RULES_BH_2026_EN

uso_no_agente: responder sobre equipe, mínimo de atletas, oficiais, entrada tardia e área de substituição.

Conteúdo: Uma equipe consiste, em princípio, em até 10 jogadores. Pelo menos 6 jogadores devem estar presentes no início. Se o número de jogadores elegíveis cair abaixo de 4, o jogo é interrompido/descontinuado e a outra equipe é considerada vencedora. No máximo 4 jogadores por equipe podem estar em quadra: 3 de linha e 1 goleiro. Os demais são substitutos. Jogador ou oficial está autorizado a participar se presente no início e inscrito na súmula. Quem chega depois deve obter autorização do cronometrista/secretário e ser inserido na súmula. A equipe pode usar até 4 oficiais, mas apenas 2 ficam na área de substituição; os outros ficam atrás da área de substituição, fora da zona de segurança, salvo assistência autorizada por lesão.

## CHUNK_P02_003 — Regra 4: uniformes, numeração e equipamentos

status: liberado

fonte_base: IHF_RULES_BH_2026_EN + IHF_UPDATE_BH_2026

ressalva: detalhes finos do apêndice de uniforme ficam na Parte 06.

uso_no_agente: responder sobre números, contraste, jogar descalço, meias, sand socks e equipamentos.

Conteúdo: Jogadores devem usar números visíveis de pelo menos 12 x 10 cm, entre 1 e 99, com contraste claro em relação ao uniforme. Os números devem estar na frente e nas costas. Todos jogam descalços. São permitidas meias esportivas comuns de tecido ou bandagens de suporte. Sand socks e calçados sintéticos ou de borracha permanecem proibidos. Se mais de um atleta usa meias, elas devem ser da mesma cor. Equipamentos de proteção devem ser macios; elementos rígidos de plástico ou metal não são permitidos. Mangas de compressão, calças térmicas, kinesio tape e bandagens podem ser permitidas conforme as condições da atualização IHF 2026.

## CHUNK_P03_001 — Regra 5: goleiro fora da área

status: liberado

fonte_base: IHF_RULES_BH_2026_EN

ressalva: não contém lista integral da Regra 5.

uso_no_agente: responder sobre goleiro fora da área e sujeição às regras de jogador de linha.

Conteúdo: O goleiro pode deixar a área de gol sem a bola e participar do jogo na área de jogo. Ao fazer isso, passa a estar sujeito às regras aplicáveis aos jogadores na área de jogo. O goleiro é considerado fora da área de gol assim que qualquer parte do corpo toca a areia fora da linha da área de gol.

## CHUNK_P03_002 — Regra 5/6/12: tiro de goleiro, segundo toque e própria área

status: liberado

fonte_base: IHF_RULES_BH_2026_EN

uso_no_agente: responder sobre tiro de goleiro, própria área e segundo toque.

Conteúdo: Quando a bola termina na área de gol, o goleiro deve colocá-la em jogo por tiro de goleiro. Após executar tiro de goleiro, o goleiro não pode tocar a bola novamente até que ela toque outro jogador. Se um jogador joga a bola para a própria área de gol, as decisões podem ser: gol, se a bola entra no gol; tiro livre, se a bola fica parada na área ou se o goleiro toca a bola e ela não entra; tiro lateral, se a bola sai pela linha de fundo externa.

## CHUNK_P03_003 — Regra 6: área de gol e bola na área

status: liberado

fonte_base: IHF_RULES_BH_2026_EN

uso_no_agente: responder sobre invasão, bola na área, bola no ar e reinícios.

Conteúdo: Apenas o goleiro pode entrar na área de gol, salvo exceções da regra. A área de gol inclui a linha da área de gol. Um jogador de linha entra na área quando toca a área ou a linha com qualquer parte do corpo. A bola pertence ao goleiro quando está na área de gol, salvo exceções. A bola parada ou rolando na área pode ser jogada, mas jogador de linha não pode entrar na área para jogá-la; se entrar, o reinício é tiro livre. É permitido jogar a bola no ar acima da área de gol, exceto em tiro de goleiro.

## CHUNK_P03_004 — Regra 7: posse, bola em jogo, ações com a bola, drible/quique

status: liberado

fonte_base: IHF_RULES_BH_2026_EN

uso_no_agente: responder sobre jogar a bola, 3 segundos, partes do corpo e drible.

Conteúdo: Posse de bola inclui situações em que o jogo continua com tiro de goleiro, lateral, tiro livre ou tiro de 6 metros. Bola em jogo significa que o jogador tem contato com a bola ou que a equipe está em posse. É permitido arremessar, receber, parar, empurrar ou bater na bola usando mãos abertas ou fechadas, braços, cabeça, tronco, coxas e joelhos. É permitido mergulhar para disputar bola parada ou rolando na areia. É permitido segurar a bola por no máximo 3 segundos, inclusive quando está na areia. O quique/drible começa quando o jogador toca a bola com qualquer parte do corpo e a direciona para a areia. Depois que a bola toca outro jogador ou a baliza, o jogador pode tocar/quicar a bola e pegá-la novamente.

## CHUNK_P03_005 — Regra 7: jogo passivo e 4 passes

status: liberado

fonte_base: IHF_RULES_BH_2026_EN + IHF_UPDATE_BH_2026

ressalva: sempre citar atualização 2026 quando falar de 4 passes.

uso_no_agente: responder sobre passivo, advertência e tiro livre após máximo de 4 passes.

Conteúdo: Não é permitido manter a bola em posse sem tentativa reconhecível de atacar ou arremessar ao gol. Também não é permitido atrasar repetidamente a execução de tiro livre, lateral ou tiro de goleiro. Essa conduta é jogo passivo e deve ser punida com tiro livre contra a equipe em posse. Quando os árbitros reconhecem tendência de jogo passivo, mostram o sinal de advertência. Após essa advertência, pela atualização IHF 2026, se nenhum arremesso ao gol for realizado após no máximo 4 passes, deve ser marcado tiro livre contra a equipe atacante.

## CHUNK_P03_BLOCK_001 — BLOQUEADO: Regra 5 integral do goleiro

status: bloqueado

fonte_base: PDF IHF oficial não extraído integralmente pelo conector

uso_no_agente: não responder com base processada.

decisao: A lista integral de permissões e proibições do goleiro na Regra 5 não está processada integralmente. Se a pergunta depender dessa lista completa, responder “não encontrado nas fontes processadas” ou consultar diretamente o PDF oficial IHF.

## CHUNK_P04_001 — Regra 8: ações não permitidas e condutas de oficiais

status: liberado

fonte_base: IHF_RULES_BH_2026_EN

ressalva: não contém taxonomia integral da Regra 8.

uso_no_agente: responder sobre puxar bola, bloquear com membros, segurar, empurrar e oficial em quadra.

Conteúdo: Não é permitido puxar ou bater na bola que está nas mãos do adversário; bloquear ou forçar o adversário para longe usando braços, mãos ou pernas; restringir, segurar, empurrar, correr ou saltar contra o adversário. Oficial de equipe, em geral, não pode entrar na quadra durante o jogo; essa violação é conduta antidesportiva e o jogo reinicia com tiro livre para os adversários.

## CHUNK_P04_002 — Regra 8: últimos 15 segundos, Golden Goal e cabeça da goleira

status: liberado

fonte_base: IHF_RULES_BH_2026_EN + IHF_UPDATE_BH_2026

uso_no_agente: responder sobre 6m, desqualificação com/sem relatório e arremesso na cabeça da goleira.

Conteúdo: Nos últimos 15 segundos de ambos os períodos ou no Golden Goal, infrações específicas podem gerar desqualificação e tiro de 6 metros. Infrações enquadradas na Regra 8:7 geram desqualificação com relatório escrito mais tiro de 6 metros. Infrações enquadradas na Regra 8:5 geram desqualificação sem relatório escrito mais tiro de 6 metros. A atualização IHF 2026 protege a goleira quando a bola atinge primeiro a cabeça em situação prevista; a regra exige que a cabeça seja o primeiro ponto de contato, não se aplica se a bola toca outra parte do corpo antes, nem se a goleira move a cabeça em direção à bola.

## CHUNK_P04_003 — Regra 9: pontuação 1/2, gol espetacular, aérea, 6m e reinício após gol

status: liberado

fonte_base: IHF_RULES_BH_2026_EN

uso_no_agente: responder sobre gols de 1 e 2 pontos, aérea/in-flight, slap/push, 6m e tiro de goleiro após gol.

Conteúdo: Gols criativos ou espetaculares são concedidos com dois pontos. Gol em tiro de 6 metros vale dois pontos. Após um gol, o jogo é reiniciado com tiro de goleiro. Um gol em in-flight/aérea vale dois pontos somente se o jogador em voo controla a bola e arremessa ao gol enquanto está no ar. Se o jogador apenas dá tapa/slap ou empurra/push a bola para dentro do gol, o gol vale um ponto.

## CHUNK_P04_004 — Regra 9: Shoot-out procedimento base

status: liberado_com_ressalva

fonte_base: IHF_RULES_BH_2026_EN

ressalva: detalhes de 5 atletas/renomeação não confirmados no PDF principal processado.

uso_no_agente: responder somente sobre sorteio, lados, equipe que começa, mesma bola e permanência na área.

Conteúdo: A decisão por Shoot-out deve ocorrer com número igual de tentativas para cada equipe. Os árbitros usam sorteio por moeda para determinar escolha dos lados e qual equipe começa. A equipe atacante, composta por goleiro e jogador de linha/arremessador, assume sua posição primeiro. Todos os arremessos devem ser executados com a mesma bola para ambas as equipes. Jogadores envolvidos no Shoot-out devem permanecer em sua área de substituição; quem já executou seu arremesso retorna para a área de substituição.

## CHUNK_P04_BLOCK_001 — BLOQUEADO: Regra 8 taxonomia integral

status: bloqueado

fonte_base: PDF IHF oficial não extraído integralmente

uso_no_agente: não responder com base processada.

decisao: A taxonomia integral das condutas disciplinares da Regra 8 não está processada. Se a pergunta depender da classificação completa entre conduta antidesportiva, gravemente antidesportiva e extremamente antidesportiva, responder “não encontrado nas fontes processadas” ou consultar diretamente o PDF oficial IHF.

## CHUNK_P05_001 — Regra 10: Tiro de Árbitro

status: liberado

fonte_base: IHF_RULES_BH_2026_EN

uso_no_agente: responder sobre início de período, Golden Goal e centro da quadra.

Conteúdo: Cada período e o Golden Goal começam com tiro de árbitro. O tiro de árbitro é executado no centro da quadra. Um árbitro lança a bola verticalmente após o sinal de apito do segundo árbitro, que fica posicionado fora da linha lateral oposta à mesa.

## CHUNK_P05_002 — Regra 11: Tiro de Lateral

status: liberado

fonte_base: IHF_RULES_BH_2026_EN

uso_no_agente: responder sobre lateral, local, pé na linha e distância de 1 metro.

Conteúdo: O tiro de lateral é executado sem apito dos árbitros, salvo exceção prevista. É cobrado pelos adversários da equipe cujo jogador tocou por último na bola antes de ela cruzar a linha. A cobrança ocorre do ponto onde a bola cruzou a linha lateral. O executante deve manter um pé sobre a linha lateral até a bola sair de sua mão. Ele não pode colocar a bola no chão e pegá-la novamente, nem quicar e pegar de novo. Defensores devem manter distância mínima de 1 metro.

## CHUNK_P05_003 — Regra 12: Tiro de Goleiro

status: liberado

fonte_base: IHF_RULES_BH_2026_EN

uso_no_agente: responder sobre bola na área, execução pelo goleiro e substituição do goleiro.

Conteúdo: A bola que termina na área de gol deve ser recolocada em jogo pelo goleiro por tiro de goleiro. Em substituição do goleiro, o tiro de goleiro deve ser executado pelo goleiro que está saindo, e ele só pode deixar a quadra depois de executar esse tiro.

## CHUNK_P05_004 — Regra 14: Tiro de 6m por clara chance, apito indevido e vantagem

status: liberado

fonte_base: IHF_RULES_BH_2026_EN

ressalva: Regra 14 integral não processada.

uso_no_agente: responder apenas sobre clara chance, apito indevido e vantagem.

Conteúdo: Um tiro de 6 metros é concedido quando uma clara chance de gol é destruída em qualquer lugar da quadra por jogador ou oficial adversário. Também é concedido quando há apito indevido no momento de clara chance de gol. Se o atacante mantém controle total da bola e do corpo apesar da infração, não há razão para conceder 6 metros, mesmo que depois ele não aproveite a chance. Se o atacante marca gol apesar da interferência ilegal, também não há razão para conceder 6 metros.

## CHUNK_P05_005 — Regra 15: execução dos tiros, segundo toque, gol direto e apito

status: liberado_com_ressalva

fonte_base: IHF_RULES_BH_2026_EN

ressalva: Regra 15 integral não processada.

uso_no_agente: responder apenas sobre itens conferidos.

Conteúdo: Um tiro é considerado executado quando a bola deixa a mão do executante, ressalvada a exceção do tiro de goleiro. A bola não pode ser entregue ou tocada por companheiro do executante no momento da execução. O executante não pode tocar a bola novamente até que ela tenha tocado outro jogador ou a baliza, com exceção do tiro de goleiro conforme regra específica. Um gol pode ser marcado diretamente de qualquer tiro, exceto nas exceções de tiro de goleiro e tiro de árbitro. O apito é obrigatório para reinício em tiro de 6 metros e em situações específicas, como reinício após time-out.

## CHUNK_P05_006 — Regra 16: substituição irregular, agressão, time-out obrigatório e punições parciais

status: liberado_com_ressalva

fonte_base: IHF_RULES_BH_2026_EN

ressalva: taxonomia integral da Regra 16 não processada.

uso_no_agente: responder sobre pontos confirmados de punição.

Conteúdo: Em substituição irregular, se o jogo precisar ser interrompido, o reinício é tiro livre ou tiro de 6 metros para os adversários conforme o caso; o jogador culpado é punido com suspensão. Agressão durante o tempo de jogo é punida com desqualificação e relatório escrito. Para punições das Regras 16:1, 16:2 e 16:6, tempo de jogo inclui time-outs, Golden Goal e Shoot-out, mas não intervalos. O time-out é obrigatório em suspensão/desqualificação de jogador, tiro de 6 metros, team time-out, apito do cronometrista ou delegado, consultas entre árbitros e suspensão/desqualificação de oficial. Infrações ao Regulamento da Área de Substituição podem gerar advertência verbal, suspensão ou desqualificação. Se jogador entra enquanto cumpre suspensão, recebe suspensão adicional imediata e isso causa desqualificação.

## CHUNK_P05_007 — Regra 17: decisões finais dos árbitros e comunicação

status: liberado_com_ressalva

fonte_base: IHF_RULES_BH_2026_EN

ressalva: atribuições completas da Regra 17 não processadas.

uso_no_agente: responder apenas sobre decisão final, recurso e quem fala com árbitros.

Conteúdo: Decisões tomadas pelos árbitros, inclusive com base em recomendações dos delegados, a partir de observações de fatos ou julgamentos, são finais. Recursos só podem ser apresentados contra decisões que não estejam em conformidade com as regras. Durante o jogo, apenas os respectivos oficiais responsáveis das equipes têm direito de se dirigir aos árbitros.

## CHUNK_P05_008 — Regra 18: mesa, cronometrista e secretário em pontos conferidos

status: liberado_com_ressalva

fonte_base: IHF_RULES_BH_2026_EN

ressalva: atribuições completas da Regra 18 não processadas.

uso_no_agente: responder sobre mesa, visualização da área de substituição e sinal final.

Conteúdo: A mesa do cronometrista e secretário deve permitir visão das áreas de substituição. O tempo de jogo termina com o sinal automático do relógio público ou do cronometrista. Se esse sinal não soar, árbitro, cronometrista ou delegado apita para indicar o fim do tempo de jogo. O secretário tem responsabilidade por súmula, entrada de jogadores que chegam depois do início e registro de jogadores sem direito de participação nos trechos conferidos.

## CHUNK_P05_BLOCK_001 — BLOQUEADO: Regra 13 Tiro Livre integral

status: bloqueado

fonte_base: PDF IHF oficial não extraído integralmente

uso_no_agente: não responder com base processada.

decisao: A Regra 13 integral não está processada. Se a pergunta depender do Tiro Livre integral, responder “não encontrado nas fontes processadas” ou consultar diretamente o PDF oficial IHF.

## CHUNK_P05_BLOCK_002 — BLOQUEADO: integralidades das Regras 16, 17 e 18

status: bloqueado

fonte_base: PDF IHF oficial não extraído integralmente

uso_no_agente: não responder com base processada.

decisao: A taxonomia completa da Regra 16 e as atribuições completas das Regras 17 e 18 não estão processadas. Se a pergunta depender dessas integralidades, responder “não encontrado nas fontes processadas” ou consultar diretamente o PDF oficial IHF.

## CHUNK_P06_001 — Apêndices oficiais: existência e integração às regras

status: liberado

fonte_base: IHF_RULES_BH_2026_EN + página IHF

uso_no_agente: responder que sinais, esclarecimentos, área de substituição, uniforme, areia e iluminação são apêndices oficiais.

Conteúdo: As Regras IHF de Beach Handball 2026 incluem os apêndices Referee Hand Signals, Clarifications to the Rules of the Game, Substitution Area Regulations, Athlete Uniform Regulations e Sand Quality and Lighting Regulations. Esses apêndices devem ser observados junto às regras do jogo.

## CHUNK_P06_002 — Apêndice: área de substituição e oficiais

status: liberado

fonte_base: IHF_RULES_BH_2026_EN

uso_no_agente: responder sobre área de substituição, oficiais permitidos e permanência no Shoot-out.

Conteúdo: A área de substituição dos jogadores de linha tem 15 m de comprimento e cerca de 3 m de largura, localizada fora das linhas laterais. Jogadores de linha entram apenas por essa área. Goleiro e jogadores de linha podem sair pelo caminho mais curto do lado da área de substituição da própria equipe; goleiros entram pela linha lateral da área de gol da própria equipe, pelo lado da área de substituição. A equipe pode usar até 4 oficiais, mas apenas 2 permanecem na área de substituição. Durante o Shoot-out, jogadores de linha envolvidos permanecem na área de substituição e retornam para ela após arremessar.

## CHUNK_P06_003 — Apêndice: uniforme, numeração, jogar descalço, meias e calçados

status: liberado

fonte_base: IHF_RULES_BH_2026_EN + IHF_UPDATE_BH_2026

ressalva: tabelas completas de uniforme não processadas.

uso_no_agente: responder sobre regras textuais confirmadas de uniforme e calçados.

Conteúdo: O apêndice Athlete Uniform Regulations é parte integral das regras. Números devem ser visíveis, com pelo menos 12 x 10 cm, de 1 a 99, contrastando com o uniforme, na frente e nas costas. Jogadores jogam descalços. São permitidas meias esportivas comuns de tecido ou bandagens de suporte. Outros calçados, incluindo sintéticos ou de borracha, não são permitidos. Sand socks permanecem proibidos conforme atualização IHF 2026.

## CHUNK_P06_004 — Apêndice: areia e iluminação básica

status: liberado_com_ressalva

fonte_base: IHF_RULES_BH_2026_EN

ressalva: detalhes integrais do apêndice não processados; usar Regra 1 para critérios básicos.

uso_no_agente: responder sobre areia segura, 40 cm e iluminação 400 lux.

Conteúdo: O apêndice Sand Quality and Lighting Regulations existe como parte do conjunto oficial. Nos critérios já confirmados pela Regra 1, a superfície deve ser de areia nivelada, plana e uniforme, livre de pedras, conchas e objetos que ofereçam risco. A areia deve ter pelo menos 40 cm de profundidade. Para competições noturnas, a iluminação mínima da área de jogo deve ser de 400 lux.

## CHUNK_P06_BLOCK_001 — BLOQUEADO VISUAL: Referee Hand Signals

status: bloqueado_visual

fonte_base: PDF IHF exige conferência visual

uso_no_agente: não responder forma visual dos sinais com base textual.

decisao: Os sinais manuais dos árbitros dependem de figuras/diagramas do PDF. A extração textual confirma a existência do apêndice, mas não captura com segurança a forma visual de cada sinal. Antes de criar chunks visuais, é obrigatório realizar conferência visual do PDF.

## BLOQUEIOS GERAIS PARA O AGENTE

1. Se a resposta depender de chunk bloqueado ou bloqueado_visual, não inferir.

2. Responder: “não encontrado nas fontes processadas” ou consultar diretamente o PDF oficial IHF.

3. Chunks com `liberado_com_ressalva` só podem ser usados dentro do escopo descrito no próprio chunk.

4. Quando houver conflito entre tradução PT, resumo operacional e PDF IHF em inglês, prevalece o PDF oficial IHF em inglês.

5. Quando a pergunta envolver atualização IHF 2026, citar a fonte complementar `IHF_UPDATE_BH_2026`.
