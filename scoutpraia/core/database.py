from collections.abc import Generator
from importlib import import_module

from sqlalchemy import text

from sqlmodel import Session, SQLModel, create_engine

from scoutpraia.core.config import settings
from scoutpraia.core.paths import ensure_storage_dirs


DATABASE_URL = f"sqlite:///{settings.db_path}"
engine = create_engine(DATABASE_URL, echo=False)
_MODELS_IMPORTED = False

MODEL_IMPORT_PLAN = (
    ("scoutpraia.models.clip", {"clips"}),
    ("scoutpraia.models.event", {"events"}),
    ("scoutpraia.models.match", {"matches", "match_roster", "sets", "possessions"}),
    ("scoutpraia.models.opponent", {"opponents"}),
    ("scoutpraia.models.player", {"players"}),
    ("scoutpraia.models.report", {"reports"}),
    ("scoutpraia.models.taxonomy", {"taxonomy_versions", "event_definitions"}),
    ("scoutpraia.models.team", {"teams"}),
    ("scoutpraia.models.validation", {"coding_sessions", "coding_agreements"}),
)


LIGHTWEIGHT_SQLITE_COLUMNS = {
    "matches": {
        "video_width": "INTEGER",
        "video_height": "INTEGER",
        "video_fps": "REAL",
        "video_codec": "TEXT",
    },
}


def import_models() -> None:
    global _MODELS_IMPORTED
    if _MODELS_IMPORTED:
        return
    existing_tables = set(SQLModel.metadata.tables)
    for module_name, table_names in MODEL_IMPORT_PLAN:
        if table_names.issubset(existing_tables):
            continue
        import_module(module_name)
        existing_tables = set(SQLModel.metadata.tables)
    _MODELS_IMPORTED = True


def create_db_and_tables() -> None:
    ensure_storage_dirs()
    import_models()
    SQLModel.metadata.create_all(engine)
    ensure_lightweight_schema_updates()


def ensure_lightweight_schema_updates() -> None:
    with engine.begin() as connection:
        for table_name, columns in LIGHTWEIGHT_SQLITE_COLUMNS.items():
            existing_rows = connection.execute(text(f"PRAGMA table_info({table_name})"))
            existing_columns = {row[1] for row in existing_rows}
            for column_name, column_type in columns.items():
                if column_name not in existing_columns:
                    connection.execute(
                        text(
                            f"ALTER TABLE {table_name} "
                            f"ADD COLUMN {column_name} {column_type}"
                        )
                    )


def seed_initial_data() -> None:
    create_db_and_tables()
    from scoutpraia.services.taxonomy_service import seed_taxonomy

    with Session(engine) as session:
        seed_taxonomy(session)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


if __name__ == "__main__":
    seed_initial_data()
    print(f"Banco inicializado em {settings.db_path}")
