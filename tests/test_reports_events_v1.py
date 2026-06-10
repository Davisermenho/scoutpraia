from __future__ import annotations

from pathlib import Path

import pandas as pd
from sqlmodel import Session, SQLModel, create_engine

from scoutpraia.core.database import import_models
from scoutpraia.models.event import Event
from scoutpraia.models.match import Match, Possession, SetSegment
from scoutpraia.models.opponent import Opponent
from scoutpraia.models.player import Player
from scoutpraia.models.taxonomy import EventDefinition, TaxonomyVersion
from scoutpraia.services.analytics_service import collective_kpis
from scoutpraia.services.event_service import create_event
from scoutpraia.services.report_service import (
    build_collective_report_payload,
    build_individual_report_payload,
    build_opponent_report_payload,
    generate_collective_report,
)


def create_test_engine(tmp_path: Path):
    import_models()
    engine = create_engine(f"sqlite:///{tmp_path / 'reports-events-v1.db'}")
    SQLModel.metadata.create_all(engine)
    return engine


def _add_definition(session: Session, taxonomy_id: int, event_type: str) -> None:
    session.add(
        EventDefinition(
            taxonomy_version_id=taxonomy_id,
            event_type=event_type,
            definition=f"definição de teste para {event_type}",
        )
    )
    session.commit()


def seed_v1_report_fixture(session: Session) -> dict[str, int]:
    taxonomy = TaxonomyVersion(name="ScoutPraia v1-v1-tests", status="approved")
    opponent = Opponent(name="Chile", category="adulto")
    team_player = Player(name="Maria", shirt_number=9, primary_role="especialista")
    opponent_player = Player(name="Opp Shooter", shirt_number=13)
    match = Match(competition_name="Circuito V1", opponent_id=None)
    session.add(taxonomy)
    session.add(opponent)
    session.add(team_player)
    session.add(opponent_player)
    session.add(match)
    session.commit()
    session.refresh(taxonomy)
    session.refresh(opponent)
    session.refresh(team_player)
    session.refresh(opponent_player)
    session.refresh(match)

    match.opponent_id = opponent.id
    session.add(match)
    session.commit()
    session.refresh(match)

    for event_type in (
        "simple_shot",
        "spin_shot",
        "six_metre_throw",
        "ball_control_turnover",
        "passive_play_turnover",
        "substitution_error_turnover",
    ):
        _add_definition(session, taxonomy.id, event_type)

    set_segment = SetSegment(match_id=match.id, set_number=1)
    session.add(set_segment)
    session.commit()
    session.refresh(set_segment)

    team_possession_1 = Possession(match_id=match.id, set_id=set_segment.id, team_side="team")
    team_possession_2 = Possession(match_id=match.id, set_id=set_segment.id, team_side="team")
    team_possession_3 = Possession(match_id=match.id, set_id=set_segment.id, team_side="team")
    team_possession_4 = Possession(match_id=match.id, set_id=set_segment.id, team_side="team")
    team_possession_5 = Possession(match_id=match.id, set_id=set_segment.id, team_side="team")
    opponent_possession_1 = Possession(
        match_id=match.id, set_id=set_segment.id, team_side="opponent"
    )
    opponent_possession_2 = Possession(
        match_id=match.id, set_id=set_segment.id, team_side="opponent"
    )
    opponent_possession_3 = Possession(
        match_id=match.id, set_id=set_segment.id, team_side="opponent"
    )
    opponent_possession_4 = Possession(
        match_id=match.id, set_id=set_segment.id, team_side="opponent"
    )
    for possession in (
        team_possession_1,
        team_possession_2,
        team_possession_3,
        team_possession_4,
        team_possession_5,
        opponent_possession_1,
        opponent_possession_2,
        opponent_possession_3,
        opponent_possession_4,
    ):
        session.add(possession)
    session.commit()
    for possession in (
        team_possession_1,
        team_possession_2,
        team_possession_3,
        team_possession_4,
        team_possession_5,
        opponent_possession_1,
        opponent_possession_2,
        opponent_possession_3,
        opponent_possession_4,
    ):
        session.refresh(possession)

    create_event(
        session,
        Event(
            match_id=match.id,
            set_id=set_segment.id,
            possession_id=team_possession_1.id,
            taxonomy_version_id=taxonomy.id,
            event_type="simple_shot",
            player_id=team_player.id,
            team_side="team",
            timestamp_second=10,
            points_value=2,
            result_possession="goal",
            scorer_role="specialist",
            court_lane="left_lane",
            shot_origin_depth="nine_metre_band",
        ),
    )
    create_event(
        session,
        Event(
            match_id=match.id,
            set_id=set_segment.id,
            possession_id=team_possession_2.id,
            taxonomy_version_id=taxonomy.id,
            event_type="spin_shot",
            player_id=team_player.id,
            team_side="team",
            timestamp_second=20,
            points_value=0,
            result_possession="save",
            scorer_role="field_player",
            court_lane="center_lane",
            shot_origin_depth="long_range",
        ),
    )
    create_event(
        session,
        Event(
            match_id=match.id,
            set_id=set_segment.id,
            possession_id=team_possession_3.id,
            taxonomy_version_id=taxonomy.id,
            event_type="six_metre_throw",
            player_id=team_player.id,
            team_side="team",
            timestamp_second=30,
            points_value=0,
            result_possession="rebound_live",
            scorer_role="field_player",
        ),
    )
    create_event(
        session,
        Event(
            match_id=match.id,
            set_id=set_segment.id,
            possession_id=team_possession_4.id,
            taxonomy_version_id=taxonomy.id,
            event_type="ball_control_turnover",
            player_id=team_player.id,
            team_side="team",
            timestamp_second=40,
            points_value=0,
            result_possession="lost_possession_no_shot",
            event_subtype="bad_pass",
        ),
    )
    create_event(
        session,
        Event(
            match_id=match.id,
            set_id=set_segment.id,
            possession_id=team_possession_5.id,
            taxonomy_version_id=taxonomy.id,
            event_type="passive_play_turnover",
            player_id=team_player.id,
            team_side="team",
            timestamp_second=50,
            points_value=0,
            result_possession="lost_possession_no_shot",
            event_subtype="forewarning_expired",
        ),
    )
    create_event(
        session,
        Event(
            match_id=match.id,
            set_id=set_segment.id,
            possession_id=opponent_possession_1.id,
            taxonomy_version_id=taxonomy.id,
            event_type="simple_shot",
            player_id=opponent_player.id,
            team_side="opponent",
            timestamp_second=60,
            points_value=1,
            result_possession="goal",
            scorer_role="field_player",
            court_lane="right_lane",
            shot_origin_depth="nine_metre_band",
        ),
    )
    create_event(
        session,
        Event(
            match_id=match.id,
            set_id=set_segment.id,
            possession_id=opponent_possession_2.id,
            taxonomy_version_id=taxonomy.id,
            event_type="six_metre_throw",
            player_id=opponent_player.id,
            team_side="opponent",
            timestamp_second=70,
            points_value=0,
            result_possession="execution_invalid_6m",
            scorer_role="field_player",
        ),
    )
    create_event(
        session,
        Event(
            match_id=match.id,
            set_id=set_segment.id,
            possession_id=opponent_possession_3.id,
            taxonomy_version_id=taxonomy.id,
            event_type="substitution_error_turnover",
            player_id=opponent_player.id,
            team_side="opponent",
            timestamp_second=80,
            points_value=0,
            result_possession="lost_possession_no_shot",
            event_subtype="illegal_substitution",
        ),
    )
    create_event(
        session,
        Event(
            match_id=match.id,
            set_id=set_segment.id,
            possession_id=opponent_possession_4.id,
            taxonomy_version_id=taxonomy.id,
            event_type="simple_shot",
            player_id=opponent_player.id,
            team_side="opponent",
            timestamp_second=90,
            points_value=2,
            result_possession="goal",
            scorer_role="specialist",
            court_lane="left_lane",
            shot_origin_depth="nine_metre_band",
        ),
    )

    return {
        "taxonomy_id": taxonomy.id,
        "match_id": match.id,
        "team_player_id": team_player.id,
        "opponent_player_id": opponent_player.id,
    }


def test_collective_kpis_include_v1_breakdowns() -> None:
    events = pd.DataFrame(
        [
            {
                "event_type": "simple_shot",
                "team_side": "team",
                "points_value": 2,
                "result_possession": "goal",
                "scorer_role": "specialist",
                "event_subtype": None,
            },
            {
                "event_type": "spin_shot",
                "team_side": "team",
                "points_value": 0,
                "result_possession": "save",
                "scorer_role": "field_player",
                "event_subtype": None,
            },
            {
                "event_type": "six_metre_throw",
                "team_side": "team",
                "points_value": 0,
                "result_possession": "rebound_live",
                "scorer_role": "field_player",
                "event_subtype": None,
            },
            {
                "event_type": "ball_control_turnover",
                "team_side": "team",
                "points_value": 0,
                "result_possession": "lost_possession_no_shot",
                "scorer_role": None,
                "event_subtype": "bad_pass",
            },
            {
                "event_type": "passive_play_turnover",
                "team_side": "team",
                "points_value": 0,
                "result_possession": "lost_possession_no_shot",
                "scorer_role": None,
                "event_subtype": "forewarning_expired",
            },
        ]
    )
    possessions = pd.DataFrame(
        [
            {"id": 1, "team_side": "team"},
            {"id": 2, "team_side": "team"},
            {"id": 3, "team_side": "team"},
            {"id": 4, "team_side": "team"},
            {"id": 5, "team_side": "team"},
        ]
    )

    kpis = collective_kpis(events, possessions=possessions, taxonomy_status="approved")

    assert kpis["no_shot_attack_total"] == 2
    assert kpis["no_shot_attack_causes"] == {
        "bad_pass": 1,
        "forewarning_expired": 1,
    }
    assert kpis["finalization_attempts_total"] == 3
    assert kpis["finalization_efficiency_by_type"]["simple_shot"] == 1.0
    assert kpis["finalization_efficiency_by_type"]["spin_shot"] == 0.0
    assert kpis["points_by_technical_type"] == {
        "simple_shot": 2,
        "six_metre_throw": 0,
        "spin_shot": 0,
    }
    assert kpis["points_by_scorer_role"] == {"field_player": 0, "specialist": 2}
    assert kpis["specialist_shots_total"] == 1
    assert kpis["six_metre_throw_breakdown"] == {"rebound_live": 1}


def test_v1_report_payloads_and_html_expose_minimum_breakdowns(tmp_path: Path) -> None:
    engine = create_test_engine(tmp_path)
    report_dir = tmp_path / "reports"

    with Session(engine) as session:
        fixture = seed_v1_report_fixture(session)
        collective_payload = build_collective_report_payload(
            session,
            match_id=fixture["match_id"],
            taxonomy_version_id=fixture["taxonomy_id"],
            require_approved_taxonomy=True,
        )
        individual_payload = build_individual_report_payload(
            session,
            match_id=fixture["match_id"],
            player_id=fixture["team_player_id"],
            taxonomy_version_id=fixture["taxonomy_id"],
            require_approved_taxonomy=True,
        )
        opponent_payload = build_opponent_report_payload(
            session,
            match_id=fixture["match_id"],
            taxonomy_version_id=fixture["taxonomy_id"],
            require_approved_taxonomy=True,
        )
        collective_report = generate_collective_report(
            session,
            match_id=fixture["match_id"],
            taxonomy_version_id=fixture["taxonomy_id"],
            output_dir=report_dir,
            require_approved_taxonomy=True,
        )

    assert collective_payload["kpis"]["no_shot_attack_total"] == 2
    assert collective_payload["kpis"]["finalization_attempts_total"] == 3
    assert collective_payload["kpis"]["points_by_scorer_role"]["specialist"] == 2
    assert collective_payload["kpis"]["specialist_shots_total"] == 1
    assert collective_payload["kpis"]["six_metre_throw_breakdown"] == {
        "rebound_live": 1
    }

    assert individual_payload["kpis"]["finalization_attempts_total"] == 3
    assert individual_payload["kpis"]["conversion_by_type"]["specialist"] == 1.0
    assert individual_payload["kpis"]["conversion_by_type"]["two_point"] == 0.333
    assert individual_payload["kpis"]["points_by_technical_type"]["simple_shot"] == 2
    assert individual_payload["kpis"]["specialist_shots_total"] == 1

    assert opponent_payload["kpis"]["no_shot_attack_total"] == 1
    assert opponent_payload["kpis"]["finalization_attempts_total"] == 3
    assert (
        opponent_payload["kpis"]["top_two_point_scorer_player_id"]
        == fixture["opponent_player_id"]
    )
    assert opponent_payload["kpis"]["six_metre_throw_breakdown"] == {
        "execution_invalid_6m": 1
    }

    collective_html = Path(collective_report.file_path).read_text(encoding="utf-8")
    assert "Posses sem finalização: 2" in collective_html
    assert "Total de finalizações v1: 3" in collective_html
    assert "Arremessos da especialista: 1" in collective_html
    assert "bad_pass: 1" in collective_html
    assert "simple_shot: 1.0" in collective_html
    assert "specialist: 2" in collective_html
    assert "rebound_live: 1" in collective_html
