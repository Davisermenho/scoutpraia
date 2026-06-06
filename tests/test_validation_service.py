import json

from sqlmodel import Session, SQLModel, create_engine, select

from scoutpraia.core.database import import_models
from scoutpraia.models.event import Event
from scoutpraia.models.match import Match
from scoutpraia.models.player import Player
from scoutpraia.models.taxonomy import EventDefinition
from scoutpraia.models.validation import CodingAgreement, CodingSession
from scoutpraia.services.taxonomy_service import seed_taxonomy
from scoutpraia.services.validation_service import (
    compare_coding_sessions,
    list_events_without_operational_definition,
    taxonomy_is_approved,
    validate_taxonomy_for_final_report,
)


def create_test_engine(tmp_path):
    import_models()
    engine = create_engine(f"sqlite:///{tmp_path / 'validation.db'}")
    SQLModel.metadata.create_all(engine)
    return engine


def create_validation_fixture(session: Session) -> tuple[int, int, int, int, int]:
    taxonomy = seed_taxonomy(session)
    match = Match(competition_name="Amistoso")
    player = Player(name="Ana", shirt_number=7)
    session.add(match)
    session.add(player)
    session.commit()
    session.refresh(match)
    session.refresh(player)

    first_session = CodingSession(
        match_id=match.id,
        taxonomy_version_id=taxonomy.id,
        coder_name="Analista A",
        session_type="primary",
    )
    second_session = CodingSession(
        match_id=match.id,
        taxonomy_version_id=taxonomy.id,
        coder_name="Analista A",
        session_type="intraobserver_retest",
    )
    session.add(first_session)
    session.add(second_session)
    session.commit()
    session.refresh(first_session)
    session.refresh(second_session)

    return taxonomy.id, match.id, player.id, first_session.id, second_session.id


def test_compare_coding_sessions_persists_divergence_and_reproves_threshold(
    tmp_path,
) -> None:
    engine = create_test_engine(tmp_path)

    with Session(engine) as session:
        taxonomy_id, match_id, player_id, first_session_id, second_session_id = (
            create_validation_fixture(session)
        )
        first_events = [
            Event(
                match_id=match_id,
                taxonomy_version_id=taxonomy_id,
                event_type="shot_attempt",
                player_id=player_id,
                team_side="team",
                timestamp_second=10,
                zone="center",
                points_value=0,
            ),
            Event(
                match_id=match_id,
                taxonomy_version_id=taxonomy_id,
                event_type="goal_scored",
                player_id=player_id,
                team_side="team",
                timestamp_second=20,
                zone="left_wing",
                points_value=1,
            ),
        ]
        second_events = [
            Event(
                match_id=match_id,
                taxonomy_version_id=taxonomy_id,
                event_type="shot_attempt",
                player_id=player_id,
                team_side="team",
                timestamp_second=10,
                zone="center",
                points_value=0,
            ),
            Event(
                match_id=match_id,
                taxonomy_version_id=taxonomy_id,
                event_type="goal_scored",
                player_id=player_id,
                team_side="team",
                timestamp_second=20,
                zone="right_wing",
                points_value=2,
            ),
        ]

        agreement = compare_coding_sessions(
            session,
            first_session_id=first_session_id,
            second_session_id=second_session_id,
            first_events=first_events,
            second_events=second_events,
            approval_threshold=75.0,
        )
        persisted_agreement = session.exec(
            select(CodingAgreement).where(CodingAgreement.id == agreement.id)
        ).one()

    payload = json.loads(persisted_agreement.disagreements_json or "{}")

    assert persisted_agreement.comparison_type == "intraobserver"
    assert persisted_agreement.total_events_compared == 2
    assert persisted_agreement.total_disagreements == 1
    assert persisted_agreement.agreement_percent == 50.0
    assert persisted_agreement.approved is False
    assert payload["first_session_id"] == first_session_id
    assert payload["second_session_id"] == second_session_id
    assert len(payload["divergences"]) == 1


def test_taxonomy_approval_and_missing_operational_definition(tmp_path) -> None:
    engine = create_test_engine(tmp_path)

    with Session(engine) as session:
        taxonomy = seed_taxonomy(session)
        incomplete_definition = EventDefinition(
            taxonomy_version_id=taxonomy.id,
            event_type="custom_event",
            definition="",
            include_when="",
            exclude_when="",
            decision_rule="",
            evidence_type="practical_hypothesis",
            active=True,
        )
        session.add(incomplete_definition)
        session.commit()

        missing_definitions = list_events_without_operational_definition(
            session, taxonomy.id
        )
        missing_event_types = {
            definition.event_type for definition in missing_definitions
        }
        approved_before = taxonomy_is_approved(session, taxonomy.id)

        taxonomy.status = "approved"
        session.add(taxonomy)
        session.commit()

        approved_after = taxonomy_is_approved(session, taxonomy.id)
        validate_taxonomy_for_final_report(session, taxonomy.id)

    assert approved_before is False
    assert approved_after is True
    assert missing_event_types == {"custom_event"}
