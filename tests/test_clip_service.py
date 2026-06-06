from pathlib import Path
import subprocess

from sqlmodel import Session, SQLModel, create_engine, select

from scoutpraia.core.database import import_models
from scoutpraia.models.clip import Clip
from scoutpraia.models.event import Event
from scoutpraia.models.match import Match, SetSegment
from scoutpraia.models.player import Player
from scoutpraia.services.clip_service import generate_event_clip
from scoutpraia.services.event_service import create_event
from scoutpraia.services.taxonomy_service import seed_taxonomy
from scoutpraia.services.video_service import probe_video_metadata, resolve_binary


def create_test_engine(tmp_path: Path):
    import_models()
    engine = create_engine(f"sqlite:///{tmp_path / 'clips.db'}")
    SQLModel.metadata.create_all(engine)
    return engine


def create_test_video(tmp_path: Path) -> Path:
    video_path = tmp_path / "source.mp4"
    subprocess.run(
        [
            resolve_binary("ffmpeg"),
            "-y",
            "-f",
            "lavfi",
            "-i",
            "color=c=red:s=64x36:d=4",
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


def test_generate_event_clip_runs_ffmpeg_and_persists_clip(tmp_path: Path) -> None:
    engine = create_test_engine(tmp_path)
    video_path = create_test_video(tmp_path)
    clip_dir = tmp_path / "clips"

    with Session(engine) as session:
        taxonomy = seed_taxonomy(session)
        player = Player(name="Ana", shirt_number=7)
        match = Match(competition_name="Amistoso", video_path=str(video_path))
        session.add(player)
        session.add(match)
        session.commit()
        session.refresh(player)
        session.refresh(match)

        set_segment = SetSegment(match_id=match.id, set_number=1)
        session.add(set_segment)
        session.commit()
        session.refresh(set_segment)

        event = create_event(
            session,
            Event(
                match_id=match.id,
                set_id=set_segment.id,
                taxonomy_version_id=taxonomy.id,
                event_type="shot_attempt",
                player_id=player.id,
                team_side="team",
                timestamp_second=2,
                zone="center",
                points_value=0,
            ),
        )
        event_id = event.id
        clip = generate_event_clip(session, event_id=event.id, output_dir=clip_dir)
        persisted_clip = session.exec(select(Clip).where(Clip.id == clip.id)).one()

    clip_path = Path(persisted_clip.clip_path)
    metadata = probe_video_metadata(clip_path)

    assert clip_path.exists()
    assert clip_path.name == "amistoso_set1_00-00-02_shot_attempt_ana-7.mp4"
    assert persisted_clip.event_id == event_id
    assert persisted_clip.start_second == 0.0
    assert persisted_clip.end_second == 6
    assert metadata.duration_seconds > 0
    assert metadata.width == 64
    assert metadata.height == 36
