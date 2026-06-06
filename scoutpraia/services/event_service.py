from sqlmodel import Session, select

from scoutpraia.models.event import Event
from scoutpraia.models.taxonomy import EventDefinition
from scoutpraia.utils.zones import ZONES


def validate_event(session: Session, event: Event) -> None:
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


def create_event(session: Session, event: Event) -> Event:
    validate_event(session, event)
    session.add(event)
    session.commit()
    session.refresh(event)
    return event
