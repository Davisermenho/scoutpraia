from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine, select
from streamlit.testing.v1 import AppTest

import scoutpraia.core.database as database
import scoutpraia.pages.reports as reports_page
import scoutpraia.pages.tagging as tagging_page
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


def test_tagging_page_create_update_and_delete_last_event(monkeypatch, tmp_path: Path) -> None:
    engine = configure_page_modules(monkeypatch, tmp_path)
    with Session(engine) as session:
        fixture = seed_ui_fixture(session, tmp_path)

    at = AppTest.from_string(tagging_page_app_script(tmp_path / "pages.db", tmp_path / "reports"))
    at.run()

    selectbox_by_label(at, "Set").set_value(f"Set 1 (id {fixture['set_id']})")
    number_input_by_label(at, "Timestamp manual (s)").set_value(12.5)
    selectbox_by_label(at, "Evento").set_value("goal_scored")
    radio_by_label(at, "Lado").set_value("team")
    selectbox_by_label(at, "Atleta").set_value("Maria (#9)")
    selectbox_by_label(at, "Atleta secundária").set_value("Ana (#7)")
    selectbox_by_label(at, "Zona").set_value("left_wing")
    selectbox_by_label(at, "Posse").set_value(f"Posse {fixture['possession_id']} — team")
    selectbox_by_label(at, "Pontos").set_value(1)
    button_by_label(at, "Salvar evento").click()
    at.run()

    assert len(at.exception) == 0
    assert any("Evento" in item.value and "salvo" in item.value for item in at.success)

    selectbox_by_label(at, "Evento do último registro").set_value("technical_error")
    selectbox_by_label(at, "Pontos do último evento").set_value(0)
    button_by_label(at, "Atualizar último evento").click()
    at.run()

    assert any("atualizado" in item.value for item in at.success)

    button_by_label(at, "Excluir último evento").click()
    at.run()

    assert any("excluído" in item.value for item in at.success)
    with Session(engine) as session:
        events = session.exec(select(Event).where(Event.match_id == fixture["match_id"])).all()
    assert len(events) == 1


def test_reports_page_generates_collective_report(monkeypatch, tmp_path: Path) -> None:
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
    with Session(engine) as session:
        reports = session.exec(select(Report).where(Report.match_id == fixture["match_id"])).all()
    assert len(reports) == 1
    assert Path(reports[0].file_path).exists()


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


def button_by_label(at: AppTest, label: str):
    for element in at.button:
        if element.label == label:
            return element
    raise AssertionError(f"Button não encontrado: {label}")
