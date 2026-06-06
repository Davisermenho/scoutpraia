from scoutpraia.models.event import Event


def event_signature(event: Event) -> tuple[str, int | None, str | None, int]:
    return (event.event_type, event.player_id, event.zone, event.points_value)


def agreement_percent(first: list[Event], second: list[Event]) -> float:
    total = min(len(first), len(second))
    if total == 0:
        return 0.0
    matches = 0
    for left, right in zip(first[:total], second[:total], strict=False):
        if event_signature(left) == event_signature(right):
            matches += 1
    return round((matches / total) * 100, 2)
