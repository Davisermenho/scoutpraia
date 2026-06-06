from sqlmodel import Session, SQLModel, create_engine, select

from scoutpraia.core.database import import_models
from scoutpraia.models.clip import Clip
from scoutpraia.models.event import Event
from scoutpraia.models.match import Match, Possession, SetSegment
from scoutpraia.models.opponent import Opponent
from scoutpraia.models.player import Player
from scoutpraia.models.report import Report
from scoutpraia.models.taxonomy import EventDefinition, TaxonomyVersion
from scoutpraia.models.team import Team
from scoutpraia.models.validation import CodingAgreement, CodingSession


def create_test_engine(tmp_path):
    import_models()
    engine = create_engine(f"sqlite:///{tmp_path / 'models.db'}")
    SQLModel.metadata.create_all(engine)
    return engine


def test_core_models_can_be_created_and_queried(tmp_path) -> None:
    engine = create_test_engine(tmp_path)

    with Session(engine) as session:
        team = Team(name="ScoutPraia", category="adulto")
        opponent = Opponent(name="Argentina", category="adulto")
        player = Player(name="Maria", shirt_number=9, primary_role="especialista")
        taxonomy = TaxonomyVersion(name="ScoutPraia v0.1", status="draft")
        session.add(team)
        session.add(opponent)
        session.add(player)
        session.add(taxonomy)
        session.commit()
        session.refresh(opponent)
        session.refresh(player)
        session.refresh(taxonomy)
        player_id = player.id

        event_definition = EventDefinition(
            taxonomy_version_id=taxonomy.id,
            event_type="shot_attempt",
            definition="tentativa de finalização contra o gol adversário",
        )
        match = Match(opponent_id=opponent.id, competition_name="Amistoso")
        session.add(event_definition)
        session.add(match)
        session.commit()
        session.refresh(match)

        set_segment = SetSegment(match_id=match.id, set_number=1)
        possession = Possession(match_id=match.id, team_side="team")
        coding_session = CodingSession(
            match_id=match.id,
            coder_name="Analista 1",
            taxonomy_version_id=taxonomy.id,
            session_type="primary",
        )
        report = Report(
            match_id=match.id,
            report_type="collective",
            file_path="storage/reports/relatorio.html",
        )
        session.add(set_segment)
        session.add(possession)
        session.add(coding_session)
        session.add(report)
        session.commit()
        session.refresh(set_segment)
        session.refresh(possession)
        session.refresh(coding_session)

        event = Event(
            match_id=match.id,
            set_id=set_segment.id,
            possession_id=possession.id,
            taxonomy_version_id=taxonomy.id,
            event_type="shot_attempt",
            player_id=player_id,
            team_side="team",
            timestamp_second=12.5,
            zone="left-wing",
        )
        session.add(event)
        session.commit()
        session.refresh(event)

        clip = Clip(
            match_id=match.id,
            event_id=event.id,
            player_id=player_id,
            clip_path="storage/clips/clip.mp4",
            start_second=6.5,
            end_second=16.5,
            label="shot_attempt",
        )
        agreement = CodingAgreement(
            match_id=match.id,
            taxonomy_version_id=taxonomy.id,
            comparison_type="intraobserver",
            agreement_percent=100.0,
            total_events_compared=1,
            total_disagreements=0,
            disagreements_json="[]",
            approved=True,
        )
        session.add(clip)
        session.add(agreement)
        session.commit()

        persisted_event = session.exec(select(Event)).one()
        persisted_clip = session.exec(select(Clip)).one()
        persisted_report = session.exec(select(Report)).one()
        persisted_agreement = session.exec(select(CodingAgreement)).one()

    assert persisted_event.event_type == "shot_attempt"
    assert persisted_event.player_id == player_id
    assert persisted_clip.event_id == persisted_event.id
    assert persisted_report.report_type == "collective"
    assert persisted_agreement.agreement_percent == 100.0
