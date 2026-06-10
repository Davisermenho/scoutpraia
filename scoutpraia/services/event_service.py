from sqlmodel import Session, select

from scoutpraia.contracts.events_v1 import FINALIZATION_V1, NO_SHOT_ATTACK_V1
from scoutpraia.models.event import Event
from scoutpraia.models.match import Match, Possession, SetSegment
from scoutpraia.models.player import Player
from scoutpraia.models.taxonomy import EventDefinition
from scoutpraia.services.finalization_contract_service import (
    FinalizationContractError,
    validate_record as validate_finalization_record,
)
from scoutpraia.services.no_shot_attack_contract_service import (
    NO_SHOT_ATTACK_COMPAT_EVENT_TYPES,
    NoShotAttackContractError,
    validate_record as validate_no_shot_attack_record,
)
from scoutpraia.utils.zones import ZONES


SCORING_EVENTS = {
    "goal_scored",
    "goal_conceded",
    "two_point_goal",
    "specialist_goal",
    "inflight_goal",
    "shootout_goal",
}
TWO_POINT_ONLY_EVENTS = {"two_point_goal", "specialist_goal"}
FINALIZATION_V1_EVENT_TYPES = frozenset(
    event_contract.event_code for event_contract in FINALIZATION_V1.primary_events
)
NO_SHOT_ATTACK_V1_EVENT_TYPES = frozenset(NO_SHOT_ATTACK_COMPAT_EVENT_TYPES)
EVENT_UPDATE_FIELDS = {
    "set_id",
    "possession_id",
    "taxonomy_version_id",
    "event_type",
    "event_subtype",
    "player_id",
    "secondary_player_id",
    "team_side",
    "timestamp_second",
    "outcome",
    "zone",
    "points_value",
    "result_possession",
    "scorer_role",
    "court_lane",
    "shot_origin_depth",
    "goal_zone",
    "trajectory_visible",
    "derived_points",
    "review_marker",
    "notes",
}


def validate_event(session: Session, event: Event) -> None:
    if session.get(Match, event.match_id) is None:
        raise ValueError(f"Jogo não encontrado: {event.match_id}")

    if event.set_id is not None:
        set_segment = session.get(SetSegment, event.set_id)
        if set_segment is None or set_segment.match_id != event.match_id:
            raise ValueError(f"Set inválido para o jogo: {event.set_id}")

    if event.possession_id is not None:
        possession = session.get(Possession, event.possession_id)
        if possession is None or possession.match_id != event.match_id:
            raise ValueError(f"Posse inválida para o jogo: {event.possession_id}")

    if event.player_id is not None and session.get(Player, event.player_id) is None:
        raise ValueError(f"Atleta não encontrada: {event.player_id}")

    if (
        event.secondary_player_id is not None
        and session.get(Player, event.secondary_player_id) is None
    ):
        raise ValueError(f"Atleta secundária não encontrada: {event.secondary_player_id}")

    definition = session.exec(
        select(EventDefinition).where(
            EventDefinition.taxonomy_version_id == event.taxonomy_version_id,
            EventDefinition.event_type == event.event_type,
            EventDefinition.active == True,
        )
    ).first()
    if definition is None:
        raise ValueError(f"Evento fora da taxonomia ativa: {event.event_type}")
    if event.zone is not None and event.zone not in ZONES:
        raise ValueError(f"Zona inválida: {event.zone}")
    if event.timestamp_second < 0:
        raise ValueError("Timestamp do evento não pode ser negativo.")
    validate_points_value(event)


def validate_points_value(event: Event) -> None:
    if event.points_value not in {0, 1, 2}:
        raise ValueError("points_value deve ser 0, 1 ou 2.")

    if event.event_type in FINALIZATION_V1_EVENT_TYPES:
        _validate_finalization_v1_event(event)
        return

    if event.event_type in NO_SHOT_ATTACK_V1_EVENT_TYPES:
        _validate_no_shot_attack_v1_event(event)
        return

    if event.event_type in TWO_POINT_ONLY_EVENTS and event.points_value != 2:
        raise ValueError(f"{event.event_type} exige points_value igual a 2.")

    if event.event_type in SCORING_EVENTS and event.points_value == 0:
        raise ValueError(f"{event.event_type} exige points_value maior que 0.")

    if event.event_type not in SCORING_EVENTS and event.points_value != 0:
        raise ValueError(f"{event.event_type} não deve registrar points_value.")


def _validate_finalization_v1_event(event: Event) -> None:
    if not event.result_possession:
        raise ValueError("Finalização v1 exige result_possession.")
    if not event.scorer_role:
        raise ValueError("Finalização v1 exige scorer_role.")
    try:
        derived_points = validate_finalization_record(
            event_code=event.event_type,
            result_possession=event.result_possession,
            scorer_role=event.scorer_role,
            manual_points=event.points_value,
        )
    except FinalizationContractError as exc:
        raise ValueError(f"Contrato Finalização v1 inválido: {exc}") from exc

    event.derived_points = derived_points
    event.points_value = derived_points
    if event.outcome is None:
        event.outcome = event.result_possession


def _validate_no_shot_attack_v1_event(event: Event) -> None:
    if not event.result_possession:
        raise ValueError("Ataque sem finalização v1 exige result_possession.")
    passive_subtype = (
        event.event_subtype if event.event_type == "passive_play_turnover" else None
    )
    try:
        validate_no_shot_attack_record(
            event_code=event.event_type,
            result_possession=event.result_possession,
            team_in_possession=True,
            system_code=event.event_subtype,
            turnover_cause_detail=event.event_subtype,
            technical_error_subtype=event.event_subtype,
            passive_play_subtype=passive_subtype,
            passive_subtype=passive_subtype,
            substitution_error_subtype=event.event_subtype,
            shot_attempted=False,
            is_offensive_transition=False,
        )
    except NoShotAttackContractError as exc:
        raise ValueError(f"Contrato Ataque sem finalização v1 inválido: {exc}") from exc

    event.derived_points = 0
    event.points_value = 0
    if event.outcome is None:
        event.outcome = event.result_possession


def create_event(session: Session, event: Event) -> Event:
    validate_event(session, event)
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


def list_events_by_match(session: Session, match_id: int) -> list[Event]:
    return list(
        session.exec(
            select(Event)
            .where(Event.match_id == match_id)
            .order_by(Event.timestamp_second, Event.id)
        ).all()
    )


def update_event(session: Session, event_id: int, **changes: object) -> Event:
    event = session.get(Event, event_id)
    if event is None:
        raise ValueError(f"Evento não encontrado: {event_id}")

    invalid_fields = set(changes) - EVENT_UPDATE_FIELDS
    if invalid_fields:
        invalid_list = ", ".join(sorted(invalid_fields))
        raise ValueError(f"Campos de evento inválidos: {invalid_list}")

    for field_name, value in changes.items():
        setattr(event, field_name, value)

    validate_event(session, event)
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


def delete_event(session: Session, event_id: int) -> bool:
    event = session.get(Event, event_id)
    if event is None:
        return False

    session.delete(event)
    session.commit()
    return True
