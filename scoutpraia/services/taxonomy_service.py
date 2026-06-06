from sqlmodel import Session, select

from scoutpraia.models.taxonomy import EventDefinition, TaxonomyVersion


TAXONOMY_NAME = "ScoutPraia v0.1"

EVENT_DEFINITIONS = [
    {
        "event_type": "shot_attempt",
        "definition": "tentativa de finalização contra o gol adversário",
        "include_when": "há arremesso ou ação clara de finalização",
        "exclude_when": "passe, finta sem arremesso ou posse interrompida antes da finalização",
        "decision_rule": "se a intenção principal é finalizar, marcar tentativa",
        "evidence_type": "scientific_literature",
    },
    {
        "event_type": "goal_scored",
        "definition": "finalização que resulta em gol válido",
        "include_when": "placar deve subir para a equipe",
        "exclude_when": "gol anulado ou erro de registro do placar",
        "decision_rule": "confirmar valor em points_value",
        "evidence_type": "official_rule",
    },
    {
        "event_type": "shot_missed",
        "definition": "finalização sem gol e sem defesa da goleira",
        "include_when": "bola vai para fora, trave ou ação sem intervenção da goleira",
        "exclude_when": "defesa clara da goleira",
        "decision_rule": "se a goleira altera a trajetória, preferir save",
        "evidence_type": "scientific_literature",
    },
    {
        "event_type": "technical_error",
        "definition": "perda de posse sem arremesso causada por erro técnico ou tomada de decisão",
        "include_when": "posse acaba por passe errado, recepção falha, condução/violação ou erro não finalizador",
        "exclude_when": "arremesso defendido, bola fora em finalização ou roubo claro",
        "decision_rule": "se a posse acaba sem arremesso e sem ação defensiva clara, marcar erro técnico",
        "evidence_type": "practical_hypothesis",
    },
    {
        "event_type": "turnover",
        "definition": "qualquer perda de posse antes de uma nova posse da própria equipe",
        "include_when": "adversária passa a controlar a bola",
        "exclude_when": "fim de set, gol marcado ou bola parada sem mudança de posse",
        "decision_rule": "usar como categoria ampla; subtipo explica a causa",
        "evidence_type": "coach_decision",
    },
    {
        "event_type": "assist",
        "definition": "passe imediatamente relacionado ao gol",
        "include_when": "passe cria finalização convertida",
        "exclude_when": "passe anterior sem relação direta com o gol",
        "decision_rule": "marcar atleta secundária como assistente",
        "evidence_type": "coach_decision",
    },
    {
        "event_type": "two_point_attempt",
        "definition": "tentativa de ação que pode valer 2 pontos",
        "include_when": "spin, inflight, especialista/goleira ou shoot-out conforme regra aplicável",
        "exclude_when": "arremesso comum",
        "decision_rule": "separar tentativa de conversão",
        "evidence_type": "official_rule",
    },
    {
        "event_type": "two_point_goal",
        "definition": "gol válido de 2 pontos",
        "include_when": "ação especial resulta em gol confirmado",
        "exclude_when": "gol comum, gol anulado ou erro de pontuação",
        "decision_rule": "points_value deve ser 2",
        "evidence_type": "official_rule",
    },
    {
        "event_type": "spin_shot",
        "definition": "tentativa de finalização com giro característico",
        "include_when": "atleta executa giro antes da finalização",
        "exclude_when": "finta com giro sem arremesso",
        "decision_rule": "se houver dúvida, registrar como two_point_attempt e revisar em vídeo",
        "evidence_type": "official_rule",
    },
    {
        "event_type": "inflight_attempt",
        "definition": "tentativa em que atleta recebe/controla no ar e finaliza antes de tocar o solo",
        "include_when": "finalização ocorre no ar após passe/recepção",
        "exclude_when": "passe alto sem finalização ou finalização após contato com o solo",
        "decision_rule": "contar apenas com tentativa de finalização",
        "evidence_type": "official_rule",
    },
    {
        "event_type": "inflight_goal",
        "definition": "inflight_attempt convertido em gol válido",
        "include_when": "finalização aérea resulta em gol",
        "exclude_when": "gol comum ou gol anulado",
        "decision_rule": "points_value deve refletir a regra aplicável",
        "evidence_type": "official_rule",
    },
    {
        "event_type": "defensive_stop",
        "definition": "posse adversária encerrada sem gol por ação defensiva relevante",
        "include_when": "defesa força arremesso ruim, perda ou interrupção favorável",
        "exclude_when": "erro adversário sem pressão clara",
        "decision_rule": "marcar quando a defesa altera claramente a qualidade da posse",
        "evidence_type": "coach_decision",
    },
    {
        "event_type": "steal",
        "definition": "recuperação direta de posse por ação defensiva",
        "include_when": "atleta intercepta ou toma a bola",
        "exclude_when": "bola perdida sem controle defensivo imediato",
        "decision_rule": "precisa haver ganho de posse claro",
        "evidence_type": "scientific_literature",
    },
    {
        "event_type": "block",
        "definition": "bloqueio de arremesso pela defesa de linha",
        "include_when": "defensor altera ou impede a trajetória do arremesso",
        "exclude_when": "defesa da goleira",
        "decision_rule": "se a goleira é responsável pela defesa, usar save",
        "evidence_type": "scientific_literature",
    },
    {
        "event_type": "forced_error",
        "definition": "erro adversário causado por pressão defensiva clara",
        "include_when": "pressão força passe ruim, violação ou perda",
        "exclude_when": "erro sem pressão identificável",
        "decision_rule": "se não houver evidência clara de pressão, não marcar",
        "evidence_type": "practical_hypothesis",
    },
    {
        "event_type": "goal_conceded",
        "definition": "gol sofrido pela equipe",
        "include_when": "adversária marca gol válido",
        "exclude_when": "gol anulado",
        "decision_rule": "registrar valor em pontos concedidos",
        "evidence_type": "official_rule",
    },
    {
        "event_type": "defensive_breakdown",
        "definition": "falha coletiva ou individual que gera finalização clara adversária",
        "include_when": "há desorganização, troca perdida ou cobertura ausente",
        "exclude_when": "gol sofrido sem falha identificável",
        "decision_rule": "manter em testing por ser interpretativo",
        "evidence_type": "practical_hypothesis",
    },
    {
        "event_type": "save",
        "definition": "defesa da goleira em finalização adversária",
        "include_when": "goleira altera ou impede gol em arremesso",
        "decision_rule": "marcar quando a goleira altera ou impede gol em arremesso",
        "evidence_type": "scientific_literature",
    },
    {
        "event_type": "save_shootout",
        "definition": "defesa da goleira em shoot-out",
        "include_when": "goleira defende em situação de shoot-out",
        "decision_rule": "só usar em situação de shoot-out",
        "evidence_type": "official_rule",
    },
    {
        "event_type": "goalkeeper_distribution",
        "definition": "reposição/passe da goleira que inicia ataque",
        "include_when": "reposição gera posse organizada ou vantagem clara",
        "decision_rule": "marcar quando gerar posse organizada ou vantagem clara",
        "evidence_type": "coach_decision",
    },
    {
        "event_type": "fast_break_for",
        "definition": "transição ofensiva rápida favorável",
        "include_when": "posse rápida gera finalização ou vantagem clara",
        "decision_rule": "marcar quando posse rápida gera finalização ou vantagem clara",
        "evidence_type": "coach_decision",
    },
    {
        "event_type": "fast_break_against",
        "definition": "transição ofensiva rápida da adversária",
        "include_when": "adversária finaliza ou cria vantagem clara em transição",
        "decision_rule": "marcar quando adversária finaliza ou cria vantagem clara em transição",
        "evidence_type": "coach_decision",
    },
    {
        "event_type": "transition_recovery_good",
        "definition": "recuperação defensiva eficiente na transição",
        "include_when": "equipe impede vantagem clara da adversária",
        "decision_rule": "marcar quando equipe impede vantagem clara da adversária",
        "evidence_type": "coach_decision",
    },
    {
        "event_type": "transition_recovery_bad",
        "definition": "falha de recomposição na transição",
        "include_when": "adversária obtém finalização clara por atraso defensivo",
        "decision_rule": "marcar quando adversária obtém finalização clara por atraso defensivo",
        "evidence_type": "coach_decision",
    },
    {
        "event_type": "shootout_attempt",
        "definition": "tentativa em shoot-out",
        "include_when": "qualquer tentativa de shoot-out",
        "decision_rule": "marcar todas as tentativas, convertidas ou não",
        "evidence_type": "official_rule",
    },
    {
        "event_type": "shootout_goal",
        "definition": "shoot-out convertido",
        "include_when": "shoot-out resulta em gol válido",
        "decision_rule": "points_value deve refletir regra aplicável",
        "evidence_type": "official_rule",
    },
    {
        "event_type": "shootout_miss",
        "definition": "shoot-out não convertido",
        "include_when": "shoot-out sem gol",
        "decision_rule": "separar defesa da goleira com save_shootout quando aplicável",
        "evidence_type": "official_rule",
    },
    {
        "event_type": "timeout",
        "definition": "pedido de tempo registrado no vídeo",
        "include_when": "timeout é identificado no vídeo",
        "decision_rule": "marcar timestamp para contexto do relatório",
        "evidence_type": "official_rule",
    },
    {
        "event_type": "set_end",
        "definition": "fim do set",
        "include_when": "set termina",
        "decision_rule": "marcar placar e timestamp final do set",
        "evidence_type": "official_rule",
    },
]


def seed_taxonomy(session: Session) -> TaxonomyVersion:
    taxonomy = session.exec(
        select(TaxonomyVersion).where(TaxonomyVersion.name == TAXONOMY_NAME)
    ).first()

    if taxonomy is None:
        taxonomy = TaxonomyVersion(
            name=TAXONOMY_NAME,
            status="draft",
            notes="Taxonomia inicial derivada do dicionário operacional.",
        )
        session.add(taxonomy)
        session.commit()
        session.refresh(taxonomy)

    for definition_data in EVENT_DEFINITIONS:
        existing = session.exec(
            select(EventDefinition).where(
                EventDefinition.taxonomy_version_id == taxonomy.id,
                EventDefinition.event_type == definition_data["event_type"],
            )
        ).first()
        if existing is None:
            session.add(
                EventDefinition(
                    taxonomy_version_id=taxonomy.id,
                    **definition_data,
                )
            )

    session.commit()
    session.refresh(taxonomy)
    return taxonomy
