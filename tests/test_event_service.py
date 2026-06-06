from sqlmodel import Session, SQLModel, create_engine

from scoutpraia.core.database import import_models
from scoutpraia.models.event import Event
from scoutpraia.models.match import Match, Possession, SetSegment
from scoutpraia.models.player import Player
from scoutpraia.services.event_service import (
    create_event,
    delete_event,
    list_events_by_match,
    update_event,
)
from scoutpraia.services.taxonomy_service import seed_taxonomy


def create_test_engine(tmp_path):
    import_models()
    engine = create_engine(f"sqlite:///{tmp_path / 'events.db'}")
    SQLModel.metadata.create_all(engine)
    return engine


def create_event_fixture(session: Session) -> tuple[int, int, int, int, int]:
    taxonomy = seed_taxonomy(session)
    player = Player(name="Ana", shirt_number=7)
    secondary_player = Player(name="Bia", shirt_number=9)
    match = Match(competition_name="Amistoso")
    session.add(player)
    session.add(secondary_player)
    session.add(match)
    session.commit()
    session.refresh(player)
    session.refresh(secondary_player)
    session.refresh(match)

    set_segment = SetSegment(match_id=match.id, set_number=1)
    possession = Possession(match_id=match.id, team_side="team")
    session.add(set_segment)
    session.add(possession)
    session.commit()
    session.refresh(set_segment)
    session.refresh(possession)

    return taxonomy.id, match.id, set_segment.id, possession.id, player.id


def test_create_list_update_and_delete_event(tmp_path) -> None:
    engine = create_test_engine(tmp_path)

    with Session(engine) as session:
        taxonomy_id, match_id, set_id, possession_id, player_id = create_event_fixture(
            session
        )

        event = create_event(
            session,
            Event(
                match_id=match_id,
                set_id=set_id,
                possession_id=possession_id,
                taxonomy_version_id=taxonomy_id,
                event_type="shot_attempt",
                player_id=player_id,
                team_side="team",
                timestamp_second=12.5,
                zone="center",
                points_value=0,
            ),
        )

        listed_events = list_events_by_match(session, match_id)
        updated_event = update_event(
            session,
            event.id,
            event_type="goal_scored",
            outcome="goal",
            points_value=1,
        )
        removed = delete_event(session, event.id)
        empty_events = list_events_by_match(session, match_id)

    assert len(listed_events) == 1
    assert listed_events[0].id == event.id
    assert updated_event.event_type == "goal_scored"
    assert updated_event.points_value == 1
    assert removed is True
    assert empty_events == []


def test_event_validation_rejects_invalid_taxonomy_zone_and_points(tmp_path) -> None:
    engine = create_test_engine(tmp_path)

    with Session(engine) as session:
        taxonomy_id, match_id, set_id, possession_id, player_id = create_event_fixture(
            session
        )

        invalid_taxonomy_event = Event(
            match_id=match_id,
            set_id=set_id,
            possession_id=possession_id,
            taxonomy_version_id=taxonomy_id,
            event_type="evento_inexistente",
            player_id=player_id,
            team_side="team",
            timestamp_second=1,
            zone="center",
        )
        invalid_zone_event = Event(
            match_id=match_id,
            taxonomy_version_id=taxonomy_id,
            event_type="shot_attempt",
            player_id=player_id,
            team_side="team",
            timestamp_second=1,
            zone="meia_esquerda",
        )
        invalid_two_point_event = Event(
            match_id=match_id,
            taxonomy_version_id=taxonomy_id,
            event_type="two_point_goal",
            player_id=player_id,
            team_side="team",
            timestamp_second=1,
            zone="center",
            points_value=1,
        )
        invalid_non_scoring_event = Event(
            match_id=match_id,
            taxonomy_version_id=taxonomy_id,
            event_type="shot_attempt",
            player_id=player_id,
            team_side="team",
            timestamp_second=1,
            zone="center",
            points_value=1,
        )
        valid_two_point_event = Event(
            match_id=match_id,
            taxonomy_version_id=taxonomy_id,
            event_type="two_point_goal",
            player_id=player_id,
            team_side="team",
            timestamp_second=2,
            zone="center",
            points_value=2,
        )

        failures = []
        for event in [
            invalid_taxonomy_event,
            invalid_zone_event,
            invalid_two_point_event,
            invalid_non_scoring_event,
        ]:
            try:
                create_event(session, event)
            except ValueError as exc:
                failures.append(str(exc))

        persisted_event = create_event(session, valid_two_point_event)

    assert len(failures) == 4
    assert any("taxonomia" in failure for failure in failures)
    assert any("Zona inválida" in failure for failure in failures)
    assert any("points_value igual a 2" in failure for failure in failures)
    assert any("não deve registrar points_value" in failure for failure in failures)
    assert persisted_event.points_value == 2
