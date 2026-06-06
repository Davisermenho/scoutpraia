import subprocess
from pathlib import Path

from sqlmodel import Session

from scoutpraia.core.config import settings
from scoutpraia.core.paths import ensure_storage_dirs, safe_join, safe_slug
from scoutpraia.models.clip import Clip
from scoutpraia.models.event import Event
from scoutpraia.models.match import Match, SetSegment
from scoutpraia.models.player import Player
from scoutpraia.services.video_service import resolve_binary, validate_video_path
from scoutpraia.utils.timecode import seconds_to_timecode


class ClipGenerationError(RuntimeError):
    pass


def clip_window(event_type: str, timestamp_second: float) -> tuple[float, float]:
    before, after = 6, 4
    if "transition" in event_type or "fast_break" in event_type:
        before, after = 10, 6
    elif "shootout" in event_type:
        before, after = 8, 5
    start = max(0.0, timestamp_second - before)
    end = timestamp_second + after
    return start, end


def clip_filename(match_label: str, set_number: int, timestamp: str, event_type: str, athlete: str) -> str:
    return (
        f"{safe_slug(match_label)}_set{set_number}_{safe_slug(timestamp)}_"
        f"{safe_slug(event_type)}_{safe_slug(athlete)}.mp4"
    )


def generate_event_clip(
    session: Session,
    event_id: int,
    output_dir: str | Path | None = None,
) -> Clip:
    event = session.get(Event, event_id)
    if event is None:
        raise ValueError(f"Evento não encontrado: {event_id}")

    match = session.get(Match, event.match_id)
    if match is None:
        raise ValueError(f"Jogo não encontrado: {event.match_id}")
    if not match.video_path:
        raise ValueError(f"Jogo sem vídeo associado: {match.id}")

    video_path = validate_video_path(match.video_path)
    set_number = _event_set_number(session, event)
    athlete = _event_athlete_label(session, event)
    match_label = match.competition_name or f"jogo-{match.id}"
    timestamp = seconds_to_timecode(event.timestamp_second)
    start_second, end_second = clip_window(event.event_type, event.timestamp_second)
    filename = clip_filename(
        match_label=match_label,
        set_number=set_number,
        timestamp=timestamp,
        event_type=event.event_type,
        athlete=athlete,
    )
    target_dir = Path(output_dir) if output_dir is not None else settings.clip_dir
    ensure_storage_dirs()
    target_dir.mkdir(parents=True, exist_ok=True)
    clip_path = safe_join(target_dir, filename)

    _run_ffmpeg_clip(
        video_path=video_path,
        clip_path=clip_path,
        start_second=start_second,
        end_second=end_second,
    )

    clip = Clip(
        match_id=event.match_id,
        event_id=event.id,
        player_id=event.player_id,
        clip_path=str(clip_path),
        start_second=start_second,
        end_second=end_second,
        label=event.event_type,
    )
    session.add(clip)
    session.commit()
    session.refresh(clip)
    return clip


def _event_set_number(session: Session, event: Event) -> int:
    if event.set_id is None:
        return 0
    set_segment = session.get(SetSegment, event.set_id)
    if set_segment is None:
        return 0
    return set_segment.set_number


def _event_athlete_label(session: Session, event: Event) -> str:
    if event.player_id is None:
        return "sem-atleta"
    player = session.get(Player, event.player_id)
    if player is None:
        return f"atleta-{event.player_id}"
    if player.shirt_number is None:
        return player.name
    return f"{player.name}-{player.shirt_number}"


def _run_ffmpeg_clip(
    video_path: Path,
    clip_path: Path,
    start_second: float,
    end_second: float,
) -> None:
    ffmpeg = resolve_binary(settings.ffmpeg_binary)
    command = [
        ffmpeg,
        "-y",
        "-ss",
        f"{start_second:.3f}",
        "-to",
        f"{end_second:.3f}",
        "-i",
        str(video_path),
        "-map",
        "0:v:0",
        "-map",
        "0:a?",
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        str(clip_path),
    ]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or exc.stdout.strip() or str(exc)
        raise ClipGenerationError(f"Falha ao gerar clipe com ffmpeg: {detail}") from exc
