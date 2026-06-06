import json
from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine, select

from scoutpraia.core.database import import_models
from scoutpraia.models.clip import Clip
from scoutpraia.models.event import Event
from scoutpraia.models.match import Match, Possession, SetSegment
from scoutpraia.models.opponent import Opponent
from scoutpraia.models.player import Player
from scoutpraia.models.report import Report
from scoutpraia.models.taxonomy import TaxonomyVersion
from scoutpraia.services.event_service import create_event
from scoutpraia.services.report_service import (
    build_collective_report_payload,
    generate_collective_report,
    generate_individual_report,
    generate_opponent_report,
)
from scoutpraia.services.taxonomy_service import seed_taxonomy


def create_test_engine(tmp_path: Path):
    import_models()
    engine = create_engine(f"sqlite:///{tmp_path / 'reports.db'}")
    SQLModel.metadata.create_all(engine)
    return engine


def touch_file(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("clip", encoding="utf-8")


def seed_report_fixture(session: Session, tmp_path: Path) -> dict[str, int]:
    taxonomy = seed_taxonomy(session)
    taxonomy.status = "approved"

    opponent = Opponent(name="Argentina", category="adulto")
    team_player = Player(name="Maria", shirt_number=9, primary_role="especialista")
    helper_player = Player(name="Ana", shirt_number=7, primary_role="defensora")
    opponent_player = Player(name="Opp Shooter", shirt_number=13)

    match = Match(
        competition_name="Circuito Sul",
        opponent_id=None,
        final_score_team=2,
        final_score_opponent=1,
    )
    session.add(opponent)
    session.add(team_player)
    session.add(helper_player)
    session.add(opponent_player)
    session.add(match)
    session.commit()
    session.refresh(opponent)
    session.refresh(team_player)
    session.refresh(helper_player)
    session.refresh(opponent_player)
    session.refresh(match)

    match.opponent_id = opponent.id
    session.add(match)
    session.commit()
    session.refresh(match)

    set_segment = SetSegment(match_id=match.id, set_number=1)
    team_possession = Possession(match_id=match.id, set_id=1, team_side="team")
    opponent_possession = Possession(match_id=match.id, set_id=1, team_side="opponent")
    session.add(set_segment)
    session.commit()
    session.refresh(set_segment)

    team_possession.set_id = set_segment.id
    opponent_possession.set_id = set_segment.id
    session.add(team_possession)
    session.add(opponent_possession)
    session.commit()
    session.refresh(team_possession)
    session.refresh(opponent_possession)

    team_attempt = create_event(
        session,
        Event(
            match_id=match.id,
            set_id=set_segment.id,
            possession_id=team_possession.id,
            taxonomy_version_id=taxonomy.id,
            event_type="shot_attempt",
            player_id=team_player.id,
            team_side="team",
            timestamp_second=10,
            zone="left_wing",
            points_value=0,
        ),
    )
    team_goal = create_event(
        session,
        Event(
            match_id=match.id,
            set_id=set_segment.id,
            possession_id=team_possession.id,
            taxonomy_version_id=taxonomy.id,
            event_type="goal_scored",
            player_id=team_player.id,
            secondary_player_id=helper_player.id,
            team_side="team",
            timestamp_second=11,
            zone="left_wing",
            points_value=1,
        ),
    )
    opponent_attempt = create_event(
        session,
        Event(
            match_id=match.id,
            set_id=set_segment.id,
            possession_id=opponent_possession.id,
            taxonomy_version_id=taxonomy.id,
            event_type="shot_attempt",
            player_id=opponent_player.id,
            team_side="opponent",
            timestamp_second=30,
            zone="right_half",
            points_value=0,
        ),
    )
    opponent_goal = create_event(
        session,
        Event(
            match_id=match.id,
            set_id=set_segment.id,
            possession_id=opponent_possession.id,
            taxonomy_version_id=taxonomy.id,
            event_type="goal_scored",
            player_id=opponent_player.id,
            team_side="opponent",
            timestamp_second=31,
            zone="right_half",
            points_value=1,
        ),
    )

    team_clip_path = tmp_path / "clips" / "team_goal.mp4"
    opponent_clip_path = tmp_path / "clips" / "opponent_goal.mp4"
    touch_file(team_clip_path)
    touch_file(opponent_clip_path)

    session.add(
        Clip(
            match_id=match.id,
            event_id=team_goal.id,
            player_id=team_player.id,
            clip_path=str(team_clip_path),
            start_second=5,
            end_second=15,
            label="goal_scored",
        )
    )
    session.add(
        Clip(
            match_id=match.id,
            event_id=opponent_goal.id,
            player_id=opponent_player.id,
            clip_path=str(opponent_clip_path),
            start_second=26,
            end_second=35,
            label="goal_scored",
        )
    )
    session.commit()

    return {
        "taxonomy_id": taxonomy.id,
        "match_id": match.id,
        "team_player_id": team_player.id,
        "opponent_player_id": opponent_player.id,
        "team_attempt_id": team_attempt.id,
        "opponent_attempt_id": opponent_attempt.id,
    }


def test_report_service_generates_html_and_persists_payloads(tmp_path: Path) -> None:
    engine = create_test_engine(tmp_path)
    report_dir = tmp_path / "reports"

    with Session(engine) as session:
        fixture = seed_report_fixture(session, tmp_path)

        collective = generate_collective_report(
            session,
            match_id=fixture["match_id"],
            output_dir=report_dir,
        )
        individual = generate_individual_report(
            session,
            match_id=fixture["match_id"],
            player_id=fixture["team_player_id"],
            output_dir=report_dir,
        )
        opponent = generate_opponent_report(
            session,
            match_id=fixture["match_id"],
            output_dir=report_dir,
        )
        persisted_reports = session.exec(select(Report).order_by(Report.id)).all()

    assert len(persisted_reports) == 3
    assert collective.report_type == "collective"
    assert individual.report_type == "individual"
    assert opponent.report_type == "opponent"

    collective_html = Path(collective.file_path).read_text(encoding="utf-8")
    individual_html = Path(individual.file_path).read_text(encoding="utf-8")
    opponent_html = Path(opponent.file_path).read_text(encoding="utf-8")

    assert "Taxonomia: ScoutPraia v0.1 (approved)" in collective_html
    assert "../clips/team_goal.mp4" in collective_html
    assert "../clips/opponent_goal.mp4" in collective_html

    assert "Atleta: Maria" in individual_html
    assert "../clips/team_goal.mp4" in individual_html

    assert "Adversária: Argentina" in opponent_html
    assert "../clips/opponent_goal.mp4" in opponent_html

    collective_payload = json.loads(collective.payload_json)
    individual_payload = json.loads(individual.payload_json)
    opponent_payload = json.loads(opponent.payload_json)

    assert collective_payload["taxonomy_version"] == "ScoutPraia v0.1"
    assert collective_payload["summary"]["clips_total"] == 2
    assert individual_payload["player_name"] == "Maria"
    assert opponent_payload["opponent_name"] == "Argentina"


def test_report_payload_requires_unambiguous_taxonomy(tmp_path: Path) -> None:
    engine = create_test_engine(tmp_path)

    with Session(engine) as session:
        fixture = seed_report_fixture(session, tmp_path)
        second_taxonomy = TaxonomyVersion(name="ScoutPraia v0.2", status="approved")
        session.add(second_taxonomy)
        session.commit()
        session.refresh(second_taxonomy)

        session.add(
            Event(
                match_id=fixture["match_id"],
                taxonomy_version_id=second_taxonomy.id,
                event_type="timeout",
                team_side="team",
                timestamp_second=99,
                zone="center",
                points_value=0,
            )
        )
        session.commit()

        try:
            build_collective_report_payload(session, match_id=fixture["match_id"])
        except ValueError as exc:
            message = str(exc)
        else:
            message = ""

    assert "múltiplas versões de taxonomia" in message
