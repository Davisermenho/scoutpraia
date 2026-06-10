from __future__ import annotations

from sqlalchemy import text
from sqlmodel import Session, SQLModel, create_engine, select

from scoutpraia.core import database
from scoutpraia.core.database import import_models
from scoutpraia.models.event import Event
from scoutpraia.models.match import Match, Possession, SetSegment
from scoutpraia.models.opponent import Opponent
from scoutpraia.models.player import Player
from scoutpraia.models.taxonomy import EventDefinition, TaxonomyVersion


def create_test_engine(tmp_path):
    import_models()
    engine = create_engine(f"sqlite:///{tmp_path / 'event-v1.db'}")
    SQLModel.metadata.create_all(engine)
    return engine


def test_event_model_persists_v1_explicit_fields(tmp_path) -> None:
    engine = create_test_engine(tmp_path)

    with Session(engine) as session:
        opponent = Opponent(name="Uruguai", category="adulto")
        player = Player(name="Ana", shirt_number=7, primary_role="especialista")
        taxonomy = TaxonomyVersion(name="ScoutPraia v0.1", status="draft")
        session.add(opponent)
        session.add(player)
        session.add(taxonomy)
        session.commit()
        session.refresh(opponent)
        session.refresh(player)
        session.refresh(taxonomy)

        event_definition = EventDefinition(
            taxonomy_version_id=taxonomy.id,
            event_type="simple_shot",
            definition="finalizacao simples em contrato v1",
        )
        match = Match(opponent_id=opponent.id, competition_name="Circuito Sul")
        session.add(event_definition)
        session.add(match)
        session.commit()
        session.refresh(match)

        set_segment = SetSegment(match_id=match.id, set_number=1)
        possession = Possession(match_id=match.id, team_side="team")
        session.add(set_segment)
        session.add(possession)
        session.commit()
        session.refresh(set_segment)
        session.refresh(possession)

        event = Event(
            match_id=match.id,
            set_id=set_segment.id,
            possession_id=possession.id,
            taxonomy_version_id=taxonomy.id,
            event_type="simple_shot",
            player_id=player.id,
            team_side="team",
            timestamp_second=33.1,
            points_value=2,
            result_possession="goal",
            scorer_role="specialist",
            court_lane="left_lane",
            shot_origin_depth="nine_metre_band",
            goal_zone="high_left",
            trajectory_visible=True,
            derived_points=2,
            review_marker=True,
        )
        session.add(event)
        session.commit()

        persisted_event = session.exec(select(Event)).one()

    assert persisted_event.result_possession == "goal"
    assert persisted_event.scorer_role == "specialist"
    assert persisted_event.court_lane == "left_lane"
    assert persisted_event.shot_origin_depth == "nine_metre_band"
    assert persisted_event.goal_zone == "high_left"
    assert persisted_event.trajectory_visible is True
    assert persisted_event.derived_points == 2
    assert persisted_event.review_marker is True


def test_lightweight_schema_update_adds_v1_event_columns_to_existing_sqlite_table(
    tmp_path, monkeypatch
) -> None:
    db_path = tmp_path / "legacy-event-schema.db"
    engine = create_engine(f"sqlite:///{db_path}")

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE TABLE matches (
                    id INTEGER PRIMARY KEY,
                    opponent_id INTEGER,
                    competition_name TEXT,
                    phase TEXT,
                    played_at TEXT,
                    location TEXT,
                    video_path TEXT
                )
                """
            )
        )
        connection.execute(
            text(
                """
                CREATE TABLE events (
                    id INTEGER PRIMARY KEY,
                    match_id INTEGER NOT NULL,
                    set_id INTEGER,
                    possession_id INTEGER,
                    taxonomy_version_id INTEGER NOT NULL,
                    event_type TEXT NOT NULL,
                    event_subtype TEXT,
                    player_id INTEGER,
                    secondary_player_id INTEGER,
                    team_side TEXT NOT NULL,
                    timestamp_second REAL NOT NULL,
                    outcome TEXT,
                    zone TEXT,
                    points_value INTEGER NOT NULL,
                    notes TEXT
                )
                """
            )
        )

    monkeypatch.setattr(database, "engine", engine)
    database.ensure_lightweight_schema_updates()

    with engine.begin() as connection:
        event_columns = {
            row[1] for row in connection.execute(text("PRAGMA table_info(events)"))
        }

    assert {
        "result_possession",
        "scorer_role",
        "court_lane",
        "shot_origin_depth",
        "goal_zone",
        "trajectory_visible",
        "derived_points",
        "review_marker",
    }.issubset(event_columns)
