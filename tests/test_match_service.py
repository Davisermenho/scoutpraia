from datetime import date
from pathlib import Path
import subprocess

from sqlmodel import Session, SQLModel, create_engine, select

from scoutpraia.core.database import import_models
from scoutpraia.models.match import Match
from scoutpraia.models.opponent import Opponent
from scoutpraia.models.player import Player
from scoutpraia.services.match_service import (
    create_match_with_video,
    create_opponent,
    create_player,
)
from scoutpraia.services.video_service import resolve_binary


def create_test_engine(tmp_path: Path):
    import_models()
    engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}")
    SQLModel.metadata.create_all(engine)
    return engine


def create_test_video(tmp_path: Path) -> Path:
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
