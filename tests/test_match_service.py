from datetime import date
from pathlib import Path
import subprocess

from sqlmodel import Session, SQLModel, create_engine, select

from scoutpraia.core.database import import_models
from scoutpraia.models.match import Match
from scoutpraia.models.opponent import Opponent
from scoutpraia.models.player import Player
from scoutpraia.services.match_service import (
    add_player_to_match,
    create_match_with_video,
    create_opponent,
    create_player,
    delete_match,
    delete_opponent,
    delete_player,
    list_match_roster,
    remove_player_from_match,
    update_match_with_video,
    update_opponent,
    update_player,
)
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
