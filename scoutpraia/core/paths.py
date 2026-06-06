import re
from pathlib import Path

from scoutpraia.core.config import settings


STORAGE_DIRS = [
    settings.db_path.parent,
    settings.video_dir,
    settings.clip_dir,
    settings.report_dir,
    settings.thumbnail_dir,
]


def ensure_storage_dirs() -> None:
    for path in STORAGE_DIRS:
        path.mkdir(parents=True, exist_ok=True)


def safe_slug(value: str) -> str:
    normalized = value.strip().lower()
    normalized = re.sub(r"[^a-z0-9_-]+", "-", normalized)
    normalized = re.sub(r"-+", "-", normalized).strip("-")
    return normalized or "sem-nome"


def safe_join(base_dir: Path, filename: str) -> Path:
    candidate = (base_dir / filename).resolve()
    base = base_dir.resolve()
    if base not in candidate.parents and candidate != base:
        raise ValueError("Caminho fora do diretório permitido.")
    return candidate
