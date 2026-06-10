from __future__ import annotations

EVENT_TYPE_LABELS = {
    "shot_attempt": "Tentativa de finalização",
    "goal_scored": "Gol marcado",
    "shot_missed": "Finalização para fora",
    "technical_error": "Erro técnico",
    "turnover": "Perda de posse",
    "assist": "Assistência",
    "two_point_attempt": "Tentativa de 2 pontos",
    "two_point_goal": "Gol de 2 pontos",
    "specialist_attempt": "Tentativa da especialista",
    "specialist_goal": "Gol da especialista",
    "simple_shot": "Arremesso simples",
    "spin_shot": "Arremesso com giro",
    "inflight_shot": "Arremesso em inflight",
    "goalkeeper_shot": "Arremesso da goleira",
    "six_metre_throw": "Tiro de 6 metros",
    "inflight_attempt": "Tentativa em inflight",
    "inflight_goal": "Gol em inflight",
    "ball_control_turnover": "Perda por erro de controle",
    "offensive_foul_turnover": "Perda por falta de ataque",
    "passive_play_turnover": "Perda por jogo passivo",
    "substitution_error_turnover": "Perda por erro de troca",
    "defensive_stop": "Parada defensiva",
    "steal": "Roubo de bola",
    "block": "Bloqueio",
    "forced_error": "Erro forçado",
    "goal_conceded": "Gol sofrido",
    "defensive_breakdown": "Falha defensiva",
    "save": "Defesa da goleira",
    "save_shootout": "Defesa no shoot-out",
    "goalkeeper_distribution": "Reposição da goleira",
    "fast_break_for": "Contra-ataque a favor",
    "fast_break_against": "Contra-ataque sofrido",
    "transition_recovery_good": "Boa recomposição",
    "transition_recovery_bad": "Má recomposição",
    "shootout_attempt": "Tentativa de shoot-out",
    "shootout_goal": "Gol de shoot-out",
    "shootout_miss": "Shoot-out perdido",
    "timeout": "Pedido de tempo",
    "set_end": "Fim do set",
}

TEAM_SIDE_LABELS = {
    "team": "Equipe",
    "opponent": "Adversária",
}

DIRECTION_LABELS = {
    "left": "Esquerda",
    "right": "Direita",
    "center": "Centro",
}

ZONE_LABELS = {
    "left_wing": "Ponta esquerda",
    "left_half": "Meia esquerda",
    "center": "Centro",
    "right_half": "Meia direita",
    "right_wing": "Ponta direita",
    "6m_left": "6m esquerda",
    "6m_center": "6m centro",
    "6m_right": "6m direita",
    "shootout_lane": "Corredor do shoot-out",
}

REPORT_TYPE_LABELS = {
    "collective": "coletivo",
    "individual": "individual",
    "opponent": "adversária",
}

KPI_LABELS = {
    "points_total": "Pontos totais",
    "goals_total": "Gols totais",
    "offensive_possessions": "Posses ofensivas",
    "defensive_possessions": "Posses defensivas",
    "points_per_possession": "Pontos por posse",
    "goals_per_possession": "Gols por posse",
    "offensive_conversion_rate": "Conversão ofensiva",
    "conversion_rate": "Taxa de conversão",
    "technical_error_rate": "Taxa de erro técnico",
    "defensive_stops_per_possession": "Paradas defensivas por posse",
    "critical_warnings": "Alertas críticos",
    "set_performance": "Desempenho por set",
    "specialist_efficiency": "Eficiência da especialista",
    "shot_attempts": "Tentativas de finalização",
    "shot_conversion_rate": "Conversão de finalização",
    "goals_by_zone": "Gols por zona",
    "technical_errors": "Erros técnicos",
    "preferred_attack_side": "Lado preferencial de ataque",
    "most_frequent_shooter_player_id": "Atleta que mais finaliza",
    "top_two_point_scorer_player_id": "Atleta com mais gols de 2 pontos",
    "pressure_error_rate": "Taxa de erro sob pressão",
    "transition_vulnerability": "Vulnerabilidade na transição",
    "shootout_efficiency": "Eficiência no shoot-out",
}

COLUMN_LABELS = {
    "id": "ID",
    "timestamp": "Tempo (s)",
    "event_type": "Evento",
    "player": "Atleta",
    "team_side": "Lado",
    "zone": "Zona",
    "points_value": "Pontos",
    "metric": "Métrica",
    "value": "Valor",
    "set": "Set",
}


def event_type_label(value: str | None) -> str:
    return _translate(value, EVENT_TYPE_LABELS)


def team_side_label(value: str | None) -> str:
    return _translate(value, TEAM_SIDE_LABELS)


def direction_label(value: str | None) -> str:
    return _translate(value, DIRECTION_LABELS)


def zone_label(value: str | None) -> str:
    return _translate(value, ZONE_LABELS)


def report_type_label(value: str | None) -> str:
    return _translate(value, REPORT_TYPE_LABELS)


def kpi_label(value: str | None) -> str:
    return _translate(value, KPI_LABELS)


def column_label(value: str | None) -> str:
    return _translate(value, COLUMN_LABELS)


def display_value_label(value: object) -> object:
    if isinstance(value, str):
        if value in EVENT_TYPE_LABELS:
            return event_type_label(value)
        if value in TEAM_SIDE_LABELS:
            return team_side_label(value)
        if value in ZONE_LABELS:
            return zone_label(value)
        if value in DIRECTION_LABELS:
            return direction_label(value)
    return value


def _translate(value: str | None, labels: dict[str, str]) -> str:
    if value is None:
        return "n/d"
    if value in labels:
        return labels[value]
    return value.replace("_", " ").strip().capitalize()
