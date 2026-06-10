from __future__ import annotations

from pathlib import Path

from sqlmodel import Session, select
from streamlit.testing.v1 import AppTest

from scoutpraia.models.event import Event
from scoutpraia.models.taxonomy import EventDefinition
from tests.test_streamlit_pages import (
    button_by_label,
    configure_page_modules,
    seed_ui_fixture,
    selectbox_by_label,
    tagging_page_app_script,
    text_input_by_label,
)


def _add_v1_event_definition(session: Session, taxonomy_id: int, event_type: str) -> None:
    session.add(
        EventDefinition(
            taxonomy_version_id=taxonomy_id,
            event_type=event_type,
            definition=f"definição de teste para {event_type}",
        )
    )
    session.commit()


def test_tagging_page_creates_finalization_v1_event_with_derived_points(
    monkeypatch, tmp_path: Path
) -> None:
    engine = configure_page_modules(monkeypatch, tmp_path)
    with Session(engine) as session:
        fixture = seed_ui_fixture(session, tmp_path)
        for event_type in (
            "simple_shot",
            "spin_shot",
            "inflight_shot",
            "goalkeeper_shot",
            "six_metre_throw",
        ):
            _add_v1_event_definition(session, fixture["taxonomy_id"], event_type)

    at = AppTest.from_string(tagging_page_app_script(tmp_path / "pages.db", tmp_path / "reports"))
    at.run()

    assert any(button.label == "Arremesso simples" for button in at.button)

    selectbox_by_label(at, "Evento").set_value("simple_shot")
    at.run()

    text_input_by_label(at, "Timestamp do vídeo").set_value("00:14")
    selectbox_by_label(at, "Atleta").set_value("Maria (#9)")
    selectbox_by_label(at, "Resultado da finalização").set_value("goal")
    selectbox_by_label(at, "Papel da arremessadora").set_value("specialist")
    selectbox_by_label(at, "Profundidade da origem do arremesso").set_value(
        "nine_metre_band"
    )
    selectbox_by_label(at, "Corredor da quadra").set_value("left_lane")
    button_by_label(at, "Salvar evento").click()
    at.run()

    assert len(at.exception) == 0
    assert any("salvo" in item.value for item in at.success)
    assert any(element.label == "Pontos calculados" for element in at.text_input)

    with Session(engine) as session:
        event = session.exec(select(Event).where(Event.event_type == "simple_shot")).one()

    assert event.points_value == 2
    assert event.derived_points == 2
    assert event.result_possession == "goal"
    assert event.scorer_role == "specialist"
    assert event.court_lane == "left_lane"
    assert event.shot_origin_depth == "nine_metre_band"
