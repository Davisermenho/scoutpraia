from sqlmodel import Session, SQLModel, create_engine, select

from scoutpraia.core.database import import_models
from scoutpraia.models.taxonomy import EventDefinition
from scoutpraia.services.taxonomy_service import seed_taxonomy


def create_test_engine(tmp_path):
    import_models()
    engine = create_engine(f"sqlite:///{tmp_path / 'taxonomy.db'}")
    SQLModel.metadata.create_all(engine)
    return engine


def test_seed_taxonomy_adds_specialist_events_and_updates_existing_definitions(
    tmp_path,
) -> None:
    engine = create_test_engine(tmp_path)

    with Session(engine) as session:
        taxonomy = seed_taxonomy(session)
        two_point_attempt = session.exec(
            select(EventDefinition).where(
                EventDefinition.taxonomy_version_id == taxonomy.id,
                EventDefinition.event_type == "two_point_attempt",
            )
        ).one()
        two_point_attempt.include_when = "definição antiga"
        session.add(two_point_attempt)
        session.commit()

        seed_taxonomy(session)

        specialist_attempt = session.exec(
            select(EventDefinition).where(
                EventDefinition.taxonomy_version_id == taxonomy.id,
                EventDefinition.event_type == "specialist_attempt",
            )
        ).one()
        specialist_goal = session.exec(
            select(EventDefinition).where(
                EventDefinition.taxonomy_version_id == taxonomy.id,
                EventDefinition.event_type == "specialist_goal",
            )
        ).one()
        updated_two_point_attempt = session.exec(
            select(EventDefinition).where(
                EventDefinition.taxonomy_version_id == taxonomy.id,
                EventDefinition.event_type == "two_point_attempt",
            )
        ).one()

    assert specialist_attempt.event_type == "specialist_attempt"
    assert specialist_goal.event_type == "specialist_goal"
    assert "especialista" not in updated_two_point_attempt.include_when.lower()
    assert "shoot-out" not in updated_two_point_attempt.include_when.lower()
