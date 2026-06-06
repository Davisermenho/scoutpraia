import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from scoutpraia.core.config import settings


SUPPORTED_VIDEO_EXTENSIONS = {".mp4", ".mov"}


@dataclass(frozen=True)
class VideoMetadata:
    duration_seconds: float
    width: int | None
    height: int | None
    fps: float | None
    codec: str | None


def resolve_binary(binary: str) -> str:
    configured = Path(binary)
    if configured.exists():
        return str(configured)

    from_path = shutil.which(binary)
    if from_path:
        return from_path

    local_binary = Path("bin") / binary
    if local_binary.exists():
        return str(local_binary)

    raise FileNotFoundError(f"Binário não encontrado: {binary}")


def validate_video_path(video_path: str | Path) -> Path:
    path = Path(video_path)
    if not path.exists():
        raise FileNotFoundError(f"Vídeo não encontrado: {path}")
    if path.suffix.lower() not in SUPPORTED_VIDEO_EXTENSIONS:
        raise ValueError("Formato inválido. Use .mp4 ou .mov.")
    return path


def _parse_fps(frame_rate: str | None) -> float | None:
    if not frame_rate or frame_rate == "0/0":
        return None
    if "/" not in frame_rate:
        return float(frame_rate)
    numerator, denominator = frame_rate.split("/", maxsplit=1)
    denominator_value = float(denominator)
    if denominator_value == 0:
        return None
    return round(float(numerator) / denominator_value, 3)


def probe_video_metadata(video_path: str | Path) -> VideoMetadata:
    path = validate_video_path(video_path)
    ffprobe = resolve_binary(settings.ffprobe_binary)
    command = [
        ffprobe,
        "-v",
        "error",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(path),
    ]
    result = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    video_stream = next(
        (stream for stream in payload.get("streams", []) if stream.get("codec_type") == "video"),
        {},
    )
    duration = payload.get("format", {}).get("duration") or video_stream.get("duration") or 0
    return VideoMetadata(
        duration_seconds=round(float(duration), 3),
        width=video_stream.get("width"),
        height=video_stream.get("height"),
        fps=_parse_fps(video_stream.get("avg_frame_rate")),
        codec=video_stream.get("codec_name"),
    )
