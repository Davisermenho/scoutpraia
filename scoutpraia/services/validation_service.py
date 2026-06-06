import json

from sqlmodel import Session, select

from scoutpraia.models.event import Event
from scoutpraia.models.taxonomy import EventDefinition, TaxonomyVersion
from scoutpraia.models.validation import CodingAgreement, CodingSession


def event_signature(event: Event) -> tuple[str, int | None, str | None, int]:
    return (event.event_type, event.player_id, event.zone, event.points_value)


def agreement_percent(first: list[Event], second: list[Event]) -> float:
    total = max(len(first), len(second))
    if total == 0:
        return 0.0
    matches = 0
    for index in range(total):
        left = first[index] if index < len(first) else None
        right = second[index] if index < len(second) else None
        if left is None or right is None:
            continue
        if event_signature(left) == event_signature(right):
            matches += 1
    return round((matches / total) * 100, 2)


def list_events_without_operational_definition(
    session: Session,
    taxonomy_version_id: int,
) -> list[EventDefinition]:
    definitions = session.exec(
        select(EventDefinition).where(
            EventDefinition.taxonomy_version_id == taxonomy_version_id,
            EventDefinition.active == True,
        )
    ).all()
    return [
        definition
        for definition in definitions
        if not _has_operational_definition(definition)
    ]


def taxonomy_is_approved(session: Session, taxonomy_version_id: int) -> bool:
    taxonomy = session.get(TaxonomyVersion, taxonomy_version_id)
    if taxonomy is None:
        raise ValueError(f"Taxonomia não encontrada: {taxonomy_version_id}")
    return taxonomy.status == "approved"


def validate_taxonomy_for_final_report(
    session: Session,
    taxonomy_version_id: int,
) -> None:
    if not taxonomy_is_approved(session, taxonomy_version_id):
        raise ValueError(
            f"Taxonomia {taxonomy_version_id} não está aprovada para relatório final."
        )


def compare_coding_sessions(
    session: Session,
    first_session_id: int,
    second_session_id: int,
    first_events: list[Event],
    second_events: list[Event],
    approval_threshold: float = 85.0,
    notes: str | None = None,
) -> CodingAgreement:
    first_session = _get_coding_session(session, first_session_id)
    second_session = _get_coding_session(session, second_session_id)

    if first_session.match_id != second_session.match_id:
        raise ValueError("As sessões de marcação precisam pertencer ao mesmo jogo.")
    if first_session.taxonomy_version_id != second_session.taxonomy_version_id:
        raise ValueError("As sessões de marcação precisam usar a mesma taxonomia.")

    divergences = _build_divergences(first_events, second_events)
    agreement = agreement_percent(first_events, second_events)
    comparison_type = _resolve_comparison_type(first_session, second_session)

    persisted_agreement = CodingAgreement(
        match_id=first_session.match_id,
        taxonomy_version_id=first_session.taxonomy_version_id,
        comparison_type=comparison_type,
        agreement_percent=agreement,
        total_events_compared=max(len(first_events), len(second_events)),
        total_disagreements=len(divergences),
        disagreements_json=json.dumps(
            {
                "first_session_id": first_session.id,
                "second_session_id": second_session.id,
                "divergences": divergences,
            },
            ensure_ascii=True,
            sort_keys=True,
        ),
        approved=agreement >= approval_threshold,
        notes=notes,
    )
    session.add(persisted_agreement)
    session.commit()
    session.refresh(persisted_agreement)
    return persisted_agreement


def _has_operational_definition(definition: EventDefinition) -> bool:
    required_fields = [
        definition.definition,
        definition.decision_rule,
    ]
    return all(value is not None and value.strip() for value in required_fields)


def _get_coding_session(session: Session, session_id: int) -> CodingSession:
    coding_session = session.get(CodingSession, session_id)
    if coding_session is None:
        raise ValueError(f"Sessão de marcação não encontrada: {session_id}")
    return coding_session


def _resolve_comparison_type(
    first_session: CodingSession,
    second_session: CodingSession,
) -> str:
    if (
        first_session.session_type == "primary"
        and second_session.session_type == "intraobserver_retest"
    ) or (
        second_session.session_type == "primary"
        and first_session.session_type == "intraobserver_retest"
    ):
        return "intraobserver"
    return "interobserver"


def _build_divergences(
    first_events: list[Event],
    second_events: list[Event],
) -> list[dict[str, object]]:
    divergences: list[dict[str, object]] = []
    total = max(len(first_events), len(second_events))
    for index in range(total):
        left = first_events[index] if index < len(first_events) else None
        right = second_events[index] if index < len(second_events) else None
        left_signature = event_signature(left) if left is not None else None
        right_signature = event_signature(right) if right is not None else None
        if left_signature == right_signature:
            continue
        divergences.append(
            {
                "index": index,
                "first_event_id": left.id if left is not None else None,
                "second_event_id": right.id if right is not None else None,
                "first_signature": left_signature,
                "second_signature": right_signature,
            }
        )
    return divergences
