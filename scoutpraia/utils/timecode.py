def seconds_to_timecode(seconds: float) -> str:
    total = max(0, int(seconds))
    hours = total // 3600
    minutes = (total % 3600) // 60
    secs = total % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def format_seconds_for_input(seconds: float | None) -> str:
    if seconds is None:
        return ""
    safe_seconds = max(0.0, float(seconds))
    whole_seconds = int(safe_seconds)
    fractional = round(safe_seconds - whole_seconds, 1)
    hours = whole_seconds // 3600
    minutes = (whole_seconds % 3600) // 60
    secs = whole_seconds % 60
    if hours > 0:
        base = f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        base = f"{minutes:02d}:{secs:02d}"
    if fractional > 0:
        decimal = f"{fractional:.1f}".split(".")[1]
        return f"{base}.{decimal}"
    return base


def timecode_to_seconds(timecode: str) -> float:
    normalized = timecode.strip().replace(",", ".")
    if not normalized:
        raise ValueError("Informe um tempo válido.")
    if ":" not in normalized:
        return _parse_plain_seconds(normalized)

    parts = normalized.split(":")
    if len(parts) == 2:
        minutes = _parse_int_component(parts[0], "minutos")
        seconds = _parse_seconds_component(parts[1])
        _validate_clock_component(seconds, "segundos")
        return minutes * 60 + seconds
    if len(parts) == 3:
        hours = _parse_int_component(parts[0], "horas")
        minutes = _parse_int_component(parts[1], "minutos")
        seconds = _parse_seconds_component(parts[2])
        _validate_clock_component(minutes, "minutos")
        _validate_clock_component(seconds, "segundos")
        return hours * 3600 + minutes * 60 + seconds
    raise ValueError("Use segundos, MM:SS ou HH:MM:SS.")


def _parse_plain_seconds(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise ValueError("Use segundos, MM:SS ou HH:MM:SS.") from exc
    if parsed < 0:
        raise ValueError("O tempo não pode ser negativo.")
    return parsed


def _parse_int_component(value: str, label: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ValueError(f"Componente inválido de {label}.") from exc
    if parsed < 0:
        raise ValueError(f"O valor de {label} não pode ser negativo.")
    return parsed


def _parse_seconds_component(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise ValueError("Componente inválido de segundos.") from exc
    if parsed < 0:
        raise ValueError("O valor de segundos não pode ser negativo.")
    return parsed


def _validate_clock_component(value: float, label: str) -> None:
    if value >= 60:
        raise ValueError(f"O valor de {label} deve ser menor que 60.")
