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


def test_tagging_page_creates_no_shot_attack_v1_event(monkeypatch, tmp_path: Path) -> None:
    engine = configure_page_modules(monkeypatch, tmp_path)
    with Session(engine) as session:
        fixture = seed_ui_fixture(session, tmp_path)
        for event_type in (
            "ball_control_turnover",
            "offensive_foul_turnover",
            "passive_play_turnover",
            "substitution_error_turnover",
        ):
            _add_v1_event_definition(session, fixture["taxonomy_id"], event_type)

    at = AppTest.from_string(tagging_page_app_script(tmp_path / "pages.db", tmp_path / "reports"))
    at.run()

    assert any(button.label == "Perda por erro de controle" for button in at.button)

    selectbox_by_label(at, "Evento").set_value("ball_control_turnover")
    at.run()

    text_input_by_label(at, "Timestamp do vídeo").set_value("00:22")
    selectbox_by_label(at, "Atleta").set_value("Maria (#9)")
    selectbox_by_label(at, "Resultado da posse").set_value("lost_possession_no_shot")
    selectbox_by_label(at, "Causa da perda de posse").set_value("bad_pass")
    button_by_label(at, "Salvar evento").click()
    at.run()

    assert len(at.exception) == 0
    assert any("salvo" in item.value for item in at.success)
    assert any(element.label == "Pontos calculados" for element in at.text_input)

    with Session(engine) as session:
        event = session.exec(
            select(Event).where(Event.event_type == "ball_control_turnover")
        ).one()

    assert event.points_value == 0
    assert event.derived_points == 0
    assert event.result_possession == "lost_possession_no_shot"
    assert event.event_subtype == "bad_pass"
