from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine, select
from streamlit.testing.v1 import AppTest

import scoutpraia.core.database as database
import scoutpraia.pages.dashboard as dashboard_page
import scoutpraia.pages.reports as reports_page
import scoutpraia.pages.tagging as tagging_page
import scoutpraia.pages.matches as matches_page
import scoutpraia.pages.opponents as opponents_page
import scoutpraia.services.report_service as report_service
from scoutpraia.core.config import Settings
from scoutpraia.core.database import import_models
from scoutpraia.models.event import Event
from scoutpraia.models.match import Match, MatchRoster, Possession, SetSegment
from scoutpraia.models.opponent import Opponent
from scoutpraia.models.player import Player
from scoutpraia.models.report import Report
from scoutpraia.services.event_service import create_event
from scoutpraia.services.taxonomy_service import seed_taxonomy


def create_test_engine(tmp_path: Path):
    import_models()
    engine = create_engine(f"sqlite:///{tmp_path / 'pages.db'}")
    SQLModel.metadata.create_all(engine)
    return engine


def configure_page_modules(monkeypatch, tmp_path: Path):
    engine = create_test_engine(tmp_path)
    monkeypatch.setattr(database, "engine", engine)
    monkeypatch.setattr(dashboard_page, "engine", engine)
    monkeypatch.setattr(matches_page, "engine", engine)
    monkeypatch.setattr(opponents_page, "engine", engine)
    monkeypatch.setattr(tagging_page, "engine", engine)
    monkeypatch.setattr(reports_page, "engine", engine)
    monkeypatch.setattr(
        report_service,
        "settings",
        Settings(
            db_path=tmp_path / "pages.db",
            video_dir=tmp_path / "videos",
            clip_dir=tmp_path / "clips",
            report_dir=tmp_path / "reports",
            thumbnail_dir=tmp_path / "thumbs",
            ffmpeg_binary="ffmpeg",
            ffprobe_binary="ffprobe",
        ),
    )
    return engine


def tagging_page_app_script(db_path: Path, report_dir: Path) -> str:
    return f"""
from pathlib import Path
from sqlmodel import create_engine
import scoutpraia.core.database as database
import scoutpraia.pages.tagging as tagging_page
import scoutpraia.services.report_service as report_service
from scoutpraia.core.config import Settings

engine = create_engine("sqlite:///{db_path}")
database.engine = engine
tagging_page.engine = engine
report_service.settings = Settings(
    db_path=Path({str(db_path)!r}),
    video_dir=Path({str(report_dir.parent / 'videos')!r}),
    clip_dir=Path({str(report_dir.parent / 'clips')!r}),
    report_dir=Path({str(report_dir)!r}),
    thumbnail_dir=Path({str(report_dir.parent / 'thumbs')!r}),
    ffmpeg_binary="ffmpeg",
    ffprobe_binary="ffprobe",
)
tagging_page.render()
"""


def reports_page_app_script(db_path: Path, report_dir: Path) -> str:
    return f"""
from pathlib import Path
from sqlmodel import create_engine
import scoutpraia.core.database as database
import scoutpraia.pages.reports as reports_page
import scoutpraia.services.report_service as report_service
from scoutpraia.core.config import Settings

engine = create_engine("sqlite:///{db_path}")
database.engine = engine
reports_page.engine = engine
report_service.settings = Settings(
    db_path=Path({str(db_path)!r}),
    video_dir=Path({str(report_dir.parent / 'videos')!r}),
    clip_dir=Path({str(report_dir.parent / 'clips')!r}),
    report_dir=Path({str(report_dir)!r}),
    thumbnail_dir=Path({str(report_dir.parent / 'thumbs')!r}),
    ffmpeg_binary="ffmpeg",
    ffprobe_binary="ffprobe",
)
reports_page.render()
"""


def dashboard_page_app_script(db_path: Path, report_dir: Path) -> str:
    return f"""
from pathlib import Path
from sqlmodel import create_engine
import scoutpraia.core.database as database
import scoutpraia.pages.dashboard as dashboard_page
import scoutpraia.services.report_service as report_service
from scoutpraia.core.config import Settings

engine = create_engine("sqlite:///{db_path}")
database.engine = engine
dashboard_page.engine = engine
report_service.settings = Settings(
    db_path=Path({str(db_path)!r}),
    video_dir=Path({str(report_dir.parent / 'videos')!r}),
    clip_dir=Path({str(report_dir.parent / 'clips')!r}),
    report_dir=Path({str(report_dir)!r}),
    thumbnail_dir=Path({str(report_dir.parent / 'thumbs')!r}),
    ffmpeg_binary="ffmpeg",
    ffprobe_binary="ffprobe",
)
dashboard_page.render()
"""


def opponents_page_app_script(db_path: Path, report_dir: Path) -> str:
    return f"""
from pathlib import Path
from sqlmodel import create_engine
import scoutpraia.core.database as database
import scoutpraia.pages.opponents as opponents_page
import scoutpraia.services.report_service as report_service
from scoutpraia.core.config import Settings

engine = create_engine("sqlite:///{db_path}")
database.engine = engine
opponents_page.engine = engine
report_service.settings = Settings(
    db_path=Path({str(db_path)!r}),
    video_dir=Path({str(report_dir.parent / 'videos')!r}),
    clip_dir=Path({str(report_dir.parent / 'clips')!r}),
    report_dir=Path({str(report_dir)!r}),
    thumbnail_dir=Path({str(report_dir.parent / 'thumbs')!r}),
    ffmpeg_binary="ffmpeg",
    ffprobe_binary="ffprobe",
)
opponents_page.render()
"""


def seed_ui_fixture(session: Session, tmp_path: Path) -> dict[str, int]:
    taxonomy = seed_taxonomy(session)
    taxonomy.status = "approved"
    opponent = Opponent(name="Argentina", category="adulto")
    player = Player(name="Maria", shirt_number=9, primary_role="especialista")
    helper = Player(name="Ana", shirt_number=7, primary_role="defensora")
    match = Match(competition_name="Circuito Sul", opponent_id=None)
    session.add(opponent)
    session.add(player)
    session.add(helper)
    session.add(match)
    session.commit()
    session.refresh(opponent)
    session.refresh(player)
    session.refresh(helper)
    session.refresh(match)

    match.opponent_id = opponent.id
    session.add(match)
    session.commit()
    session.refresh(match)

    set_segment = SetSegment(match_id=match.id, set_number=1)
    session.add(set_segment)
    session.commit()
    session.refresh(set_segment)

    possession = Possession(match_id=match.id, set_id=set_segment.id, team_side="team")
    session.add(possession)
    session.commit()
    session.refresh(possession)

    roster_entries = [
        MatchRoster(match_id=match.id, player_id=player.id, available=True),
        MatchRoster(match_id=match.id, player_id=helper.id, available=True),
    ]
    for entry in roster_entries:
        session.add(entry)
    session.commit()

    create_event(
        session,
        Event(
            match_id=match.id,
            set_id=set_segment.id,
            possession_id=possession.id,
            taxonomy_version_id=taxonomy.id,
            event_type="shot_attempt",
            player_id=player.id,
            team_side="team",
            timestamp_second=10,
            zone="left_wing",
            points_value=0,
        ),
    )

    clip_path = tmp_path / "clips" / "goal_clip.mp4"
    clip_path.parent.mkdir(parents=True, exist_ok=True)
    clip_path.write_text("clip", encoding="utf-8")

    return {
        "taxonomy_id": taxonomy.id,
        "match_id": match.id,
        "set_id": set_segment.id,
        "possession_id": possession.id,
        "player_id": player.id,
        "helper_id": helper.id,
    }


def test_tagging_page_renders_empty_state(monkeypatch, tmp_path: Path) -> None:
    configure_page_modules(monkeypatch, tmp_path)

    at = AppTest.from_string(tagging_page_app_script(tmp_path / "pages.db", tmp_path / "reports"))
    at.run()

    assert len(at.exception) == 0
    assert "Nenhum jogo cadastrado. Cadastre um jogo na página Jogos." in [
        item.value for item in at.info
    ]


def test_tagging_page_create_update_and_delete_selected_event(monkeypatch, tmp_path: Path) -> None:
    engine = configure_page_modules(monkeypatch, tmp_path)
    with Session(engine) as session:
        fixture = seed_ui_fixture(session, tmp_path)
        extra_possession = Possession(
            match_id=fixture["match_id"],
            set_id=fixture["set_id"],
            team_side="opponent",
            start_second=15,
            end_second=19,
        )
        session.add(extra_possession)
        session.commit()
        session.refresh(extra_possession)

    at = AppTest.from_string(tagging_page_app_script(tmp_path / "pages.db", tmp_path / "reports"))
    at.run()

    assert any(button.label == "Tentativa de finalização" for button in at.button)

    selectbox_by_label(at, "Set").set_value(f"Set 1 (id {fixture['set_id']})")
    text_input_by_label(at, "Timestamp do vídeo").set_value("00:12.5")
    selectbox_by_label(at, "Evento").set_value("goal_scored")
    radio_by_label(at, "Lado").set_value("team")
    selectbox_by_label(at, "Atleta").set_value("Maria (#9)")
    selectbox_by_label(at, "Atleta secundária").set_value("Ana (#7)")
    selectbox_by_label(at, "Zona").set_value("left_wing")
    selectbox_by_label(at, "Posse").set_value(f"Posse {fixture['possession_id']} — Equipe")
    selectbox_by_label(at, "Pontos").set_value(1)
    button_by_label(at, "Salvar evento").click()
    at.run()

    assert len(at.exception) == 0
    assert any("Evento" in item.value and "salvo" in item.value for item in at.success)

    selectbox_by_label(at, "Evento para editar ou excluir").set_value(1)
    selectbox_by_label(at, "Evento do registro").set_value("technical_error")
    selectbox_by_label(at, "Atleta secundária do evento").set_value("Ana (#7)")
    selectbox_by_label(at, "Posse do evento").set_value(
        f"Posse {extra_possession.id} — Adversária"
    )
    selectbox_by_label(at, "Pontos do evento").set_value(0)
    button_by_label(at, "Atualizar evento selecionado").click()
    at.run()

    assert any("atualizado" in item.value for item in at.success)
    with Session(engine) as session:
        updated_event = session.get(Event, 1)
    assert updated_event is not None
    assert updated_event.event_type == "technical_error"
    assert updated_event.secondary_player_id == fixture["helper_id"]
    assert updated_event.possession_id == extra_possession.id

    button_by_label(at, "Excluir evento selecionado").click()
    at.run()

    assert any("excluído" in item.value for item in at.success)
    with Session(engine) as session:
        events = session.exec(select(Event).where(Event.match_id == fixture["match_id"])).all()
    assert len(events) == 1
    assert events[0].event_type == "goal_scored"


def test_tagging_page_update_and_delete_selected_set(monkeypatch, tmp_path: Path) -> None:
    engine = configure_page_modules(monkeypatch, tmp_path)
    with Session(engine) as session:
        fixture = seed_ui_fixture(session, tmp_path)
        removable_set = SetSegment(
            match_id=fixture["match_id"],
            set_number=2,
            start_second=20,
            end_second=40,
        )
        session.add(removable_set)
        session.commit()
        session.refresh(removable_set)

    at = AppTest.from_string(tagging_page_app_script(tmp_path / "pages.db", tmp_path / "reports"))
    at.run()

    selectbox_by_label(at, "Set para editar ou excluir").set_value(removable_set.id)
    number_input_by_label(at, "Número do set selecionado").set_value(3)
    text_input_by_label(at, "Início do set selecionado").set_value("00:01")
    text_input_by_label(at, "Fim do set selecionado").set_value("00:19")
    button_by_label(at, "Atualizar set selecionado").click()
    at.run()

    assert any("Set 3 atualizado." in item.value for item in at.success)

    at = AppTest.from_string(tagging_page_app_script(tmp_path / "pages.db", tmp_path / "reports"))
    at.run()
    selectbox_by_label(at, "Set para editar ou excluir").set_value(removable_set.id)
    button_by_label(at, "Excluir set selecionado").click()
    at.run()

    assert any(f"Set {removable_set.id} excluído." in item.value for item in at.success)

    with Session(engine) as session:
        protected = session.get(SetSegment, fixture["set_id"])
        deleted = session.get(SetSegment, removable_set.id)
    assert protected is not None
    assert protected.set_number == 1
    assert deleted is None


def test_tagging_page_update_and_delete_selected_possession(
    monkeypatch, tmp_path: Path
) -> None:
    engine = configure_page_modules(monkeypatch, tmp_path)
    with Session(engine) as session:
        fixture = seed_ui_fixture(session, tmp_path)
        removable_possession = Possession(
            match_id=fixture["match_id"],
            set_id=fixture["set_id"],
            team_side="team",
            start_second=20,
            end_second=28,
            result="entrada",
            points_scored=0,
            points_conceded=0,
        )
        session.add(removable_possession)
        session.commit()
        session.refresh(removable_possession)

    at = AppTest.from_string(tagging_page_app_script(tmp_path / "pages.db", tmp_path / "reports"))
    at.run()

    selectbox_by_label(at, "Posse para editar ou excluir").set_value(removable_possession.id)
    radio_by_label(at, "Equipe da posse selecionada").set_value("opponent")
    selectbox_by_label(at, "Set da posse selecionada").set_value(f"Set 1 (id {fixture['set_id']})")
    text_input_by_label(at, "Início da posse selecionada").set_value("00:21")
    text_input_by_label(at, "Fim da posse selecionada").set_value("00:30")
    text_input_by_label(at, "Resultado da posse selecionada").set_value("saída editada")
    number_input_by_label(at, "Pontos feitos da posse").set_value(2)
    number_input_by_label(at, "Pontos sofridos da posse").set_value(1)
    button_by_label(at, "Atualizar posse selecionada").click()
    at.run()

    assert any(
        f"Posse {removable_possession.id} atualizada." in item.value for item in at.success
    )

    at = AppTest.from_string(tagging_page_app_script(tmp_path / "pages.db", tmp_path / "reports"))
    at.run()
    selectbox_by_label(at, "Posse para editar ou excluir").set_value(removable_possession.id)
    button_by_label(at, "Excluir posse selecionada").click()
    at.run()

    assert any(
        f"Posse {removable_possession.id} excluída." in item.value for item in at.success
    )

    with Session(engine) as session:
        protected = session.get(Possession, fixture["possession_id"])
        deleted = session.get(Possession, removable_possession.id)
    assert protected is not None
    assert protected.id == fixture["possession_id"]
    assert deleted is None


def test_tagging_page_filters_and_navigates_event_editor(
    monkeypatch, tmp_path: Path
) -> None:
    engine = configure_page_modules(monkeypatch, tmp_path)
    with Session(engine) as session:
        fixture = seed_ui_fixture(session, tmp_path)
        second_set = SetSegment(match_id=fixture["match_id"], set_number=2)
        session.add(second_set)
        session.commit()
        session.refresh(second_set)
        second_set_id = second_set.id

        opponent_possession = Possession(
            match_id=fixture["match_id"],
            set_id=second_set.id,
            team_side="opponent",
        )
        session.add(opponent_possession)
        session.commit()
        session.refresh(opponent_possession)

        team_event = create_event(
            session,
            Event(
                match_id=fixture["match_id"],
                set_id=fixture["set_id"],
                possession_id=fixture["possession_id"],
                taxonomy_version_id=fixture["taxonomy_id"],
                event_type="technical_error",
                player_id=fixture["helper_id"],
                team_side="team",
                timestamp_second=20,
                points_value=0,
                notes="evento-time",
            ),
        )
        opponent_event = create_event(
            session,
            Event(
                match_id=fixture["match_id"],
                set_id=second_set.id,
                possession_id=opponent_possession.id,
                taxonomy_version_id=fixture["taxonomy_id"],
                event_type="shot_attempt",
                player_id=fixture["helper_id"],
                team_side="opponent",
                timestamp_second=30,
                points_value=0,
                notes="evento-adversaria",
            ),
        )
        team_event_id = team_event.id
        opponent_event_id = opponent_event.id

    at = AppTest.from_string(tagging_page_app_script(tmp_path / "pages.db", tmp_path / "reports"))
    at.run()

    selectbox_by_label(at, "Filtrar por lado").set_value("Equipe")
    button_by_label(at, "Evento anterior").click()
    at.run()

    text_area_by_label(at, "Notas do evento").set_value("navegado-para-evento-1")
    button_by_label(at, "Atualizar evento selecionado").click()
    at.run()

    with Session(engine) as session:
        first_event = session.get(Event, 1)
        second_event = session.get(Event, team_event_id)
    assert first_event is not None
    assert second_event is not None
    assert first_event.notes == "navegado-para-evento-1"
    assert second_event.notes == "evento-time"

    at = AppTest.from_string(tagging_page_app_script(tmp_path / "pages.db", tmp_path / "reports"))
    at.run()
    selectbox_by_label(at, "Filtrar por set").set_value(f"Set 2 (id {second_set_id})")
    selectbox_by_label(at, "Filtrar por lado").set_value("Adversária")
    text_input_by_label(at, "Buscar evento").set_value("evento-adversaria")
    at.run()

    button_by_label(at, "Excluir evento selecionado").click()
    at.run()

    assert any(f"Evento {opponent_event_id} excluído." in item.value for item in at.success)
    with Session(engine) as session:
        deleted_event = session.get(Event, opponent_event_id)
        preserved_team_event = session.get(Event, team_event_id)
    assert deleted_event is None
    assert preserved_team_event is not None


def test_tagging_page_applies_event_form_defaults_and_quick_timestamp_controls(
    monkeypatch, tmp_path: Path
) -> None:
    engine = configure_page_modules(monkeypatch, tmp_path)
    with Session(engine) as session:
        fixture = seed_ui_fixture(session, tmp_path)

    at = AppTest.from_string(tagging_page_app_script(tmp_path / "pages.db", tmp_path / "reports"))
    at.run()

    assert number_input_by_label(at, "Número do set").value == 2
    assert selectbox_by_label(at, "Set").value == f"Set 1 (id {fixture['set_id']})"
    assert selectbox_by_label(at, "Posse").value == f"Posse {fixture['possession_id']} — Equipe"

    button_by_label(at, "+1s").click()
    at.run()

    selectbox_by_label(at, "Evento").set_value("goal_scored")
    radio_by_label(at, "Lado").set_value("team")
    selectbox_by_label(at, "Atleta").set_value("Maria (#9)")
    selectbox_by_label(at, "Atleta secundária").set_value("Ana (#7)")
    selectbox_by_label(at, "Zona").set_value("left_wing")
    selectbox_by_label(at, "Pontos").set_value(1)
    text_input_by_label(at, "Subtipo").set_value("spin")
    text_input_by_label(at, "Desfecho").set_value("gol")
    text_area_by_label(at, "Notas").set_value("teste-ergonomia")
    button_by_label(at, "Salvar evento").click()
    at.run()

    assert any("Evento 2 salvo." in item.value for item in at.success)
    with Session(engine) as session:
        created_event = session.get(Event, 2)
    assert created_event is not None
    assert created_event.set_id == fixture["set_id"]
    assert created_event.possession_id == fixture["possession_id"]
    assert created_event.timestamp_second == 1.0
    assert created_event.event_subtype == "spin"
    assert created_event.outcome == "gol"
    assert created_event.notes == "teste-ergonomia"

    assert text_input_by_label(at, "Timestamp do vídeo").value == "00:01"
    assert selectbox_by_label(at, "Set").value == f"Set 1 (id {fixture['set_id']})"
    assert selectbox_by_label(at, "Atleta").value == "Maria (#9)"
    assert text_input_by_label(at, "Subtipo").value == "spin"
    assert text_input_by_label(at, "Desfecho").value == "gol"
    assert text_area_by_label(at, "Notas").value == "teste-ergonomia"


def test_reports_page_generates_reports_via_ui(monkeypatch, tmp_path: Path) -> None:
    engine = configure_page_modules(monkeypatch, tmp_path)
    with Session(engine) as session:
        fixture = seed_ui_fixture(session, tmp_path)

    at = AppTest.from_string(reports_page_app_script(tmp_path / "pages.db", tmp_path / "reports"))
    at.run()

    assert len(at.exception) == 0
    assert any(header.value == "Relatórios" for header in at.header)

    button_by_label(at, "Gerar coletivo").click()
    at.run()
    assert any("Relatório coletivo gerado" in item.value for item in at.success)

    button_by_label(at, "Gerar individual").click()
    at.run()
    assert any("Relatório individual gerado" in item.value for item in at.success)

    button_by_label(at, "Gerar adversária").click()
    at.run()
    assert any("Relatório de adversária gerado" in item.value for item in at.success)
    assert any("3 relatório(s) gerado(s) para este jogo." in item.value for item in at.caption)

    with Session(engine) as session:
        reports = session.exec(select(Report).where(Report.match_id == fixture["match_id"])).all()
    assert len(reports) == 3
    assert all(Path(report.file_path).exists() for report in reports)


def test_dashboard_page_renders_recent_summary(monkeypatch, tmp_path: Path) -> None:
    engine = configure_page_modules(monkeypatch, tmp_path)
    with Session(engine) as session:
        seed_ui_fixture(session, tmp_path)

    at = AppTest.from_string(
        dashboard_page_app_script(tmp_path / "pages.db", tmp_path / "reports")
    )
    at.run()

    assert len(at.exception) == 0
    assert any(header.value == "Dashboard" for header in at.header)
    assert any(metric.label == "Jogos cadastrados" for metric in at.metric)


def test_opponents_page_renders_history_and_trends(monkeypatch, tmp_path: Path) -> None:
    engine = configure_page_modules(monkeypatch, tmp_path)
    with Session(engine) as session:
        fixture = seed_ui_fixture(session, tmp_path)
        create_event(
            session,
            Event(
                match_id=fixture["match_id"],
                set_id=fixture["set_id"],
                possession_id=None,
                taxonomy_version_id=fixture["taxonomy_id"],
                event_type="forced_error",
                player_id=None,
                team_side="opponent",
                timestamp_second=20,
                zone="left_half",
                points_value=0,
            ),
        )

    at = AppTest.from_string(
        opponents_page_app_script(tmp_path / "pages.db", tmp_path / "reports")
    )
    at.run()

    assert len(at.exception) == 0
    assert any(header.value == "Adversárias" for header in at.header)
    assert any(subheader.value == "Histórico de jogos" for subheader in at.subheader)


def selectbox_by_label(at: AppTest, label: str):
    for element in at.selectbox:
        if element.label == label:
            return element
    raise AssertionError(f"Selectbox não encontrado: {label}")


def number_input_by_label(at: AppTest, label: str):
    for element in at.number_input:
        if element.label == label:
            return element
    raise AssertionError(f"Number input não encontrado: {label}")


def radio_by_label(at: AppTest, label: str):
    for element in at.radio:
        if element.label == label:
            return element
    raise AssertionError(f"Radio não encontrado: {label}")


def text_input_by_label(at: AppTest, label: str):
    for element in at.text_input:
        if element.label == label:
            return element
    raise AssertionError(f"Text input não encontrado: {label}")


def text_area_by_label(at: AppTest, label: str):
    for element in at.text_area:
        if element.label == label:
            return element
    raise AssertionError(f"Text area não encontrado: {label}")


def button_by_label(at: AppTest, label: str):
    for element in at.button:
        if element.label == label:
            return element
    raise AssertionError(f"Button não encontrado: {label}")
