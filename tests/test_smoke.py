from pathlib import Path
import subprocess

from sqlmodel import SQLModel

from scoutpraia.core.database import create_db_and_tables, import_models
from scoutpraia.core.paths import safe_join, safe_slug
from scoutpraia.services.clip_service import clip_window
from scoutpraia.services.taxonomy_service import EVENT_DEFINITIONS, seed_taxonomy
from scoutpraia.services.video_service import probe_video_metadata, resolve_binary
from scoutpraia.utils.timecode import (
    format_seconds_for_input,
    seconds_to_timecode,
    timecode_to_seconds,
)
from sqlmodel import Session, select
from scoutpraia.core.database import engine
from scoutpraia.models.taxonomy import EventDefinition


def test_package_imports() -> None:
    import scoutpraia

    assert "ScoutPraia" in (scoutpraia.__doc__ or "")


def test_database_initializes() -> None:
    create_db_and_tables()
    assert Path("data/scoutpraia.db").exists()


def test_import_models_is_idempotent() -> None:
    import_models()
    import_models()


def test_import_models_is_safe_with_preloaded_metadata(monkeypatch) -> None:
    import scoutpraia.core.database as database
    from scoutpraia.models.clip import Clip

    assert Clip.__tablename__ in SQLModel.metadata.tables
    monkeypatch.setattr(database, "_MODELS_IMPORTED", False)

    database.import_models()

    assert "clips" in SQLModel.metadata.tables


def test_taxonomy_seed_is_idempotent() -> None:
    create_db_and_tables()
    with Session(engine) as session:
        taxonomy = seed_taxonomy(session)
        seed_taxonomy(session)
        definitions = session.exec(
            select(EventDefinition).where(
                EventDefinition.taxonomy_version_id == taxonomy.id
            )
        ).all()

    assert len(definitions) == len(EVENT_DEFINITIONS)
    assert {definition.event_type for definition in definitions} == {
        definition["event_type"] for definition in EVENT_DEFINITIONS
    }


def test_paths_are_safe() -> None:
    assert safe_slug("Argentina Set 1") == "argentina-set-1"
    assert safe_join(Path("storage/reports"), "relatorio.html").name == "relatorio.html"


def test_timecode_helpers() -> None:
    assert seconds_to_timecode(75) == "00:01:15"
    assert timecode_to_seconds("01:15") == 75
    assert timecode_to_seconds("02:25.4") == 145.4
    assert timecode_to_seconds("145,4") == 145.4
    assert timecode_to_seconds("01:02:25") == 3745
    assert format_seconds_for_input(145) == "02:25"
    assert format_seconds_for_input(145.4) == "02:25.4"


def test_clip_window_protects_negative_start() -> None:
    assert clip_window("shootout_goal", 3) == (0.0, 8)


def test_video_metadata_uses_real_ffprobe(tmp_path: Path) -> None:
    ffmpeg = resolve_binary("ffmpeg")
    video_path = tmp_path / "smoke.mp4"
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-f",
            "lavfi",
            "-i",
            "color=c=black:s=16x16:d=1",
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

    metadata = probe_video_metadata(video_path)

    assert metadata.duration_seconds >= 1
    assert metadata.width == 16
    assert metadata.height == 16
    assert metadata.codec == "h264"
