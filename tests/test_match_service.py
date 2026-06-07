from datetime import date
from pathlib import Path
import subprocess

from sqlmodel import Session, SQLModel, create_engine, select

from scoutpraia.core.database import import_models
from scoutpraia.models.event import Event
from scoutpraia.models.match import Match, Possession, SetSegment
from scoutpraia.models.opponent import Opponent
from scoutpraia.models.player import Player
from scoutpraia.services.match_service import (
    add_player_to_match,
    create_match_with_video,
    create_opponent,
    create_player,
    delete_match,
    delete_opponent,
    delete_possession,
    delete_player,
    delete_set_segment,
    list_match_roster,
    remove_player_from_match,
    update_match_with_video,
    update_opponent,
    update_possession,
    update_player,
    update_set_segment,
)
from scoutpraia.services.taxonomy_service import seed_taxonomy
from scoutpraia.services.video_service import resolve_binary


def create_test_engine(tmp_path: Path):
    import_models()
    engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}")
    SQLModel.metadata.create_all(engine)
    return engine


def create_test_video(tmp_path: Path) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    video_path = tmp_path / "match.mp4"
    subprocess.run(
        [
            resolve_binary("ffmpeg"),
            "-y",
            "-f",
            "lavfi",
            "-i",
            "color=c=blue:s=32x18:d=1",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            str(video_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return video_path


def test_create_match_with_video_persists_metadata(tmp_path: Path) -> None:
    engine = create_test_engine(tmp_path)
    video_path = create_test_video(tmp_path)

    with Session(engine) as session:
        opponent = create_opponent(session, name="Argentina", category="adulto")
        player = create_player(
            session,
            name="Maria",
            shirt_number=9,
            primary_role="ponta",
        )
        match = create_match_with_video(
            session,
            video_path=video_path,
            match_date=date(2026, 6, 6),
            opponent_id=opponent.id,
            competition_name="Amistoso",
            phase="fase única",
        )

        persisted_match = session.exec(select(Match).where(Match.id == match.id)).one()
        persisted_opponent = session.exec(
            select(Opponent).where(Opponent.id == opponent.id)
        ).one()
        persisted_player = session.exec(select(Player).where(Player.id == player.id)).one()

    assert persisted_opponent.name == "Argentina"
    assert persisted_player.shirt_number == 9
    assert persisted_match.video_path == str(video_path)
    assert persisted_match.duration_seconds >= 1
    assert persisted_match.video_width == 32
    assert persisted_match.video_height == 18
    assert persisted_match.video_codec == "h264"


def test_match_roster_add_list_update_and_remove(tmp_path: Path) -> None:
    engine = create_test_engine(tmp_path)
    video_path = create_test_video(tmp_path)

    with Session(engine) as session:
        opponent = create_opponent(session, name="Uruguai")
        player = create_player(session, name="Ana", shirt_number=7)
        match = create_match_with_video(
            session,
            video_path=video_path,
            opponent_id=opponent.id,
        )
        match_id = match.id
        player_id = player.id

        roster_entry = add_player_to_match(
            session,
            match_id=match_id,
            player_id=player_id,
            available=True,
            starter=False,
        )
        updated_entry = add_player_to_match(
            session,
            match_id=match_id,
            player_id=player_id,
            available=True,
            starter=True,
        )
        roster = list_match_roster(session, match_id)
        removed = remove_player_from_match(session, match_id, player_id)
        empty_roster = list_match_roster(session, match_id)

    assert roster_entry.id == updated_entry.id
    assert len(roster) == 1
    assert roster[0].player_id == player_id
    assert roster[0].starter is True
    assert removed is True
    assert empty_roster == []


def test_update_and_delete_entities_with_dependency_guards(tmp_path: Path) -> None:
    engine = create_test_engine(tmp_path)
    video_path = create_test_video(tmp_path)
    second_video_path = create_test_video(tmp_path / "edited")

    with Session(engine) as session:
        removable_opponent = create_opponent(session, name="Chile")
        removable_player = create_player(session, name="Bruna", shirt_number=15)
        assert delete_opponent(session, removable_opponent.id) is True
        assert delete_player(session, removable_player.id) is True

        opponent = create_opponent(session, name="Argentina", category="adulto")
        player = create_player(session, name="Maria", shirt_number=9)
        match = create_match_with_video(
            session,
            video_path=video_path,
            match_date=date(2026, 6, 6),
            opponent_id=opponent.id,
            competition_name="Amistoso",
            phase="fase única",
        )
        add_player_to_match(session, match.id, player.id)

        updated_opponent = update_opponent(
            session,
            opponent.id,
            name="Argentina A",
            category="sub-20",
            notes="plano de jogo",
        )
        updated_player = update_player(
            session,
            player.id,
            name="Maria Silva",
            shirt_number=11,
            primary_role="especialista",
            active=False,
        )
        updated_match = update_match_with_video(
            session,
            match.id,
            video_path=second_video_path,
            match_date=date(2026, 6, 7),
            opponent_id=opponent.id,
            competition_name="Circuito",
            phase="semi",
            notes="jogo editado",
            final_score_team=2,
            final_score_opponent=1,
        )

        opponent_delete_error = ""
        player_delete_error = ""
        match_delete_error = ""
        try:
            delete_opponent(session, opponent.id)
        except ValueError as exc:
            opponent_delete_error = str(exc)
        try:
            delete_player(session, player.id)
        except ValueError as exc:
            player_delete_error = str(exc)
        try:
            delete_match(session, match.id)
        except ValueError as exc:
            match_delete_error = str(exc)

    assert updated_opponent.name == "Argentina A"
    assert updated_player.name == "Maria Silva"
    assert updated_player.active is False
    assert updated_match.competition_name == "Circuito"
    assert updated_match.final_score_team == 2
    assert updated_match.video_width == 32
    assert "jogos vinculados" in opponent_delete_error
    assert "vínculos operacionais" in player_delete_error
    assert "vínculos operacionais" in match_delete_error


def test_update_and_delete_set_segments_with_dependency_guards(tmp_path: Path) -> None:
    engine = create_test_engine(tmp_path)
    video_path = create_test_video(tmp_path)

    with Session(engine) as session:
        opponent = create_opponent(session, name="Argentina")
        match = create_match_with_video(session, video_path=video_path, opponent_id=opponent.id)
        removable_set = SetSegment(match_id=match.id, set_number=2, start_second=20, end_second=40)
        protected_set = SetSegment(match_id=match.id, set_number=1, start_second=0, end_second=19)
        session.add(removable_set)
        session.add(protected_set)
        session.commit()
        session.refresh(removable_set)
        session.refresh(protected_set)

        updated_set = update_set_segment(
            session,
            protected_set.id,
            set_number=1,
            start_second=1,
            end_second=18,
        )

        taxonomy = seed_taxonomy(session)
        possession = Possession(
            match_id=match.id,
            set_id=protected_set.id,
            team_side="team",
            start_second=2,
            end_second=8,
        )
        session.add(possession)
        session.commit()
        session.refresh(possession)

        event = Event(
            match_id=match.id,
            set_id=protected_set.id,
            possession_id=possession.id,
            taxonomy_version_id=taxonomy.id,
            event_type="shot_attempt",
            player_id=None,
            team_side="team",
            timestamp_second=5,
            points_value=0,
        )
        session.add(event)
        session.commit()

        removable_deleted = delete_set_segment(session, removable_set.id)
        protected_delete_error = ""
        try:
            delete_set_segment(session, protected_set.id)
        except ValueError as exc:
            protected_delete_error = str(exc)

    assert updated_set.start_second == 1
    assert updated_set.end_second == 18
    assert removable_deleted is True
    assert "vínculos operacionais" in protected_delete_error


def test_update_and_delete_possessions_with_dependency_guards(tmp_path: Path) -> None:
    engine = create_test_engine(tmp_path)
    video_path = create_test_video(tmp_path)

    with Session(engine) as session:
        opponent = create_opponent(session, name="Argentina")
        match = create_match_with_video(session, video_path=video_path, opponent_id=opponent.id)
        set_segment = SetSegment(match_id=match.id, set_number=1, start_second=0, end_second=40)
        session.add(set_segment)
        session.commit()
        session.refresh(set_segment)

        removable_possession = Possession(
            match_id=match.id,
            set_id=set_segment.id,
            team_side="team",
            start_second=1,
            end_second=5,
            result="initial",
            points_scored=0,
            points_conceded=0,
        )
        protected_possession = Possession(
            match_id=match.id,
            set_id=set_segment.id,
            team_side="opponent",
            start_second=6,
            end_second=9,
            result="protected",
            points_scored=1,
            points_conceded=0,
        )
        session.add(removable_possession)
        session.add(protected_possession)
        session.commit()
        session.refresh(removable_possession)
        session.refresh(protected_possession)

        updated_possession = update_possession(
            session,
            removable_possession.id,
            set_id=set_segment.id,
            team_side="opponent",
            start_second=2,
            end_second=7,
            result="edited",
            points_scored=2,
            points_conceded=1,
        )

        taxonomy = seed_taxonomy(session)
        event = Event(
            match_id=match.id,
            set_id=set_segment.id,
            possession_id=protected_possession.id,
            taxonomy_version_id=taxonomy.id,
            event_type="shot_attempt",
            player_id=None,
            team_side="opponent",
            timestamp_second=7,
            points_value=0,
        )
        session.add(event)
        session.commit()

        removable_deleted = delete_possession(session, removable_possession.id)
        protected_delete_error = ""
        try:
            delete_possession(session, protected_possession.id)
        except ValueError as exc:
            protected_delete_error = str(exc)

    assert updated_possession.team_side == "opponent"
    assert updated_possession.start_second == 2
    assert updated_possession.end_second == 7
    assert updated_possession.result == "edited"
    assert updated_possession.points_scored == 2
    assert updated_possession.points_conceded == 1
    assert removable_deleted is True
    assert "vínculos operacionais" in protected_delete_error
