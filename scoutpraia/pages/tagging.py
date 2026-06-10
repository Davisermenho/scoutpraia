from __future__ import annotations

from collections.abc import Iterable

import streamlit as st
from sqlmodel import Session, select

from scoutpraia.contracts.events_v1 import FINALIZATION_V1, NO_SHOT_ATTACK_V1
from scoutpraia.core.database import create_db_and_tables, engine
from scoutpraia.models.event import Event
from scoutpraia.models.match import Match, Possession, SetSegment
from scoutpraia.models.player import Player
from scoutpraia.models.taxonomy import EventDefinition, TaxonomyVersion
from scoutpraia.services.event_service import (
    create_event,
    delete_event,
    list_events_by_match,
    update_event,
)
from scoutpraia.services.finalization_contract_service import (
    ALLOWED_RESULTS_BY_EVENT as FINALIZATION_ALLOWED_RESULTS,
    FinalizationContractError,
    derive_points as derive_finalization_points,
)
from scoutpraia.services.match_service import (
    delete_possession,
    delete_set_segment,
    list_match_roster,
    list_matches,
    list_players,
    update_possession,
    update_set_segment,
)
from scoutpraia.services.no_shot_attack_contract_service import (
    ALLOWED_CAUSE_DETAILS_BY_EVENT,
    NO_SHOT_ATTACK_COMPAT_EVENT_TYPES,
    NoShotAttackContractError,
    PASSIVE_PLAY_APPROVED_SUBTYPES,
    validate_record as validate_no_shot_attack_record,
)
from scoutpraia.ui_labels import (
    column_label,
    display_value_label,
    event_type_label,
    team_side_label,
    zone_label,
)
from scoutpraia.utils.timecode import format_seconds_for_input, timecode_to_seconds
from scoutpraia.utils.zones import ZONES


QUICK_EVENT_TYPES = [
    "shot_attempt",
    "goal_scored",
    "two_point_goal",
    "specialist_attempt",
    "specialist_goal",
    "technical_error",
    "turnover",
    "assist",
    "defensive_stop",
    "steal",
    "block",
    "save",
    "goal_conceded",
    "shootout_goal",
]
TIME_INPUT_HELP = "Aceita segundos, MM:SS ou HH:MM:SS. Exemplos: 145, 02:25, 01:02:25, 02:25.4."
FINALIZATION_EVENT_TYPES = tuple(
    event_contract.event_code for event_contract in FINALIZATION_V1.primary_events
)
NO_SHOT_ATTACK_EVENT_TYPES = tuple(
    dict.fromkeys(
        [event_contract.event_code for event_contract in NO_SHOT_ATTACK_V1.primary_events]
        + sorted(NO_SHOT_ATTACK_COMPAT_EVENT_TYPES)
    )
)
RUNNING_FINALIZATION_EVENT_TYPES = frozenset(
    {"simple_shot", "spin_shot", "inflight_shot", "goalkeeper_shot"}
)
ORDERED_FINALIZATION_RESULTS = [
    "goal",
    "save",
    "shot_wide",
    "shot_blocked",
    "rebound_live",
    "execution_invalid_6m",
]
SCORER_ROLE_OPTIONS = ["field_player", "specialist", "goalkeeper"]
COURT_LANE_OPTIONS = ["left_lane", "center_lane", "right_lane"]
SHOT_ORIGIN_DEPTH_OPTIONS = [
    "six_metre_line",
    "nine_metre_band",
    "long_range",
]
CHOICE_LABELS = {
    "goal": "Gol",
    "save": "Defesa",
    "shot_wide": "Para fora",
    "shot_blocked": "Bloqueado",
    "rebound_live": "Rebote vivo",
    "execution_invalid_6m": "Execução inválida de 6m",
    "lost_possession_no_shot": "Perda de posse sem arremesso",
    "field_player": "Jogadora de linha",
    "specialist": "Especialista",
    "goalkeeper": "Goleira",
    "left_lane": "Corredor esquerdo",
    "center_lane": "Corredor central",
    "right_lane": "Corredor direito",
    "six_metre_line": "Linha dos 6m",
    "nine_metre_band": "Faixa dos 9m",
    "long_range": "Longa distância",
    "bad_pass": "Passe errado",
    "bad_reception": "Recepção falha",
    "travelling": "Andada",
    "double_dribble": "Duplo drible",
    "foot_or_leg_contact": "Bola no pé/perna",
    "foot_fault": "Violação de pé",
    "ball_handling_error": "Erro de manejo",
    "ball_out_by_attack": "Bola fora pelo ataque",
    "three_seconds": "3 segundos",
    "area_invasion": "Invasão de área",
    "offensive_foul": "Falta de ataque",
    "line_violation": "Violação de linha",
    "forewarning_expired": "Aviso de passivo expirado",
    "clear_chance_refused": "Chance clara recusada",
    "illegal_substitution": "Troca irregular",
    "early_entry": "Entrada antecipada",
    "wrong_substitution_zone": "Zona de troca incorreta",
    "extra_player": "Jogadora a mais",
    "goalkeeper_specialist_exchange_error": "Erro na troca goleira-especialista",
    "substitution_violation_other": "Outra infração de substituição",
    "extra_attacker_entry_error": "Erro de entrada da atacante extra",
}


# The rest of this module is intentionally identical to the previous version.
# Only imports/constants above changed to keep legacy no-shot attack events working
# while the official contract uses attack_no_shot_v1 event codes.
