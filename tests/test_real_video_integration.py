from pathlib import Path

import pytest
from sqlmodel import Session, SQLModel, create_engine, select

from scoutpraia.core.database import import_models
from scoutpraia.models.match import Match
from scoutpraia.services.match_service import create_match_with_video, create_opponent
from scoutpraia.services.video_service import probe_video_metadata


def first_real_video() -> Path | None:
    video_dir = Path("storage/videos")
    if not video_dir.exists():
        return None
    return next(iter(sorted(video_dir.glob("*.mp4"))), None)


def test_real_video_metadata_is_extracted_when_available() -> None:
    video_path = first_real_video()
    if video_path is None:
        pytest.skip("Nenhum vídeo real disponível em storage/videos/.")

    metadata = probe_video_metadata(video_path)

    assert metadata.duration_seconds > 0
    assert metadata.width is not None and metadata.width > 0
    assert metadata.height is not None and metadata.height > 0
    assert metadata.fps is not None and metadata.fps > 0
    assert metadata.codec is not None


def test_real_video_metadata_can_be_persisted_when_available(tmp_path: Path) -> None:
    video_path = first_real_video()
    if video_path is None:
        pytest.skip("Nenhum vídeo real disponível em storage/videos/.")

    import_models()
    engine = create_engine(f"sqlite:///{tmp_path / 'real_video.db'}")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        opponent = create_opponent(session, name="Adversária real")
        match = create_match_with_video(
            session,
            video_path=video_path,
            opponent_id=opponent.id,
            competition_name="Validação com vídeo real",
        )
        persisted_match = session.exec(select(Match).where(Match.id == match.id)).one()

    assert persisted_match.video_path == str(video_path)
    assert persisted_match.duration_seconds is not None
    assert persisted_match.duration_seconds > 0
    assert persisted_match.video_width is not None
    assert persisted_match.video_width > 0
    assert persisted_match.video_height is not None
    assert persisted_match.video_height > 0
    assert persisted_match.video_fps is not None
    assert persisted_match.video_fps > 0
    assert persisted_match.video_codec is not None
