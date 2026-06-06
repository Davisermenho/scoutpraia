import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    db_path: Path = Path(os.getenv("SCOUTPRAIA_DB_PATH", "data/scoutpraia.db"))
    video_dir: Path = Path(os.getenv("SCOUTPRAIA_VIDEO_DIR", "storage/videos"))
    clip_dir: Path = Path(os.getenv("SCOUTPRAIA_CLIP_DIR", "storage/clips"))
    report_dir: Path = Path(os.getenv("SCOUTPRAIA_REPORT_DIR", "storage/reports"))
    thumbnail_dir: Path = Path(
        os.getenv("SCOUTPRAIA_THUMBNAIL_DIR", "storage/thumbnails")
    )
    ffmpeg_binary: str = os.getenv("FFMPEG_BINARY", "ffmpeg")
    ffprobe_binary: str = os.getenv("FFPROBE_BINARY", "ffprobe")


settings = Settings()
