from scoutpraia.core.paths import safe_slug


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
