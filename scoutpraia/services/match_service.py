from datetime import date
from pathlib import Path

from sqlmodel import Session, select

from scoutpraia.models.match import Match
from scoutpraia.models.opponent import Opponent
from scoutpraia.models.player import Player
from scoutpraia.services.video_service import probe_video_metadata


def create_opponent(
    session: Session,
    name: str,
    category: str | None = None,
    notes: str | None = None,
) -> Opponent:
    opponent = Opponent(name=name.strip(), category=category or None, notes=notes or None)
    if not opponent.name:
        raise ValueError("Nome da adversária é obrigatório.")
    session.add(opponent)
    session.commit()
    session.refresh(opponent)
    return opponent


def create_player(
    session: Session,
    name: str,
    shirt_number: int | None = None,
    primary_role: str | None = None,
    secondary_role: str | None = None,
) -> Player:
    player = Player(
        name=name.strip(),
        shirt_number=shirt_number,
        primary_role=primary_role or None,
        secondary_role=secondary_role or None,
        active=True,
    )
    if not player.name:
        raise ValueError("Nome da atleta é obrigatório.")
    session.add(player)
    session.commit()
    session.refresh(player)
    return player


def create_match_with_video(
    session: Session,
    video_path: str | Path,
    match_date: date | None = None,
    opponent_id: int | None = None,
    competition_name: str | None = None,
    phase: str | None = None,
    notes: str | None = None,
) -> Match:
    metadata = probe_video_metadata(video_path)
    match = Match(
        match_date=match_date,
        competition_name=competition_name or None,
        phase=phase or None,
        opponent_id=opponent_id,
        video_path=str(video_path),
        duration_seconds=metadata.duration_seconds,
        video_width=metadata.width,
        video_height=metadata.height,
        video_fps=metadata.fps,
        video_codec=metadata.codec,
        notes=notes or None,
    )
    session.add(match)
    session.commit()
    session.refresh(match)
    return match


def list_opponents(session: Session) -> list[Opponent]:
    return list(session.exec(select(Opponent).order_by(Opponent.name)).all())


def list_players(session: Session, active_only: bool = True) -> list[Player]:
    statement = select(Player).order_by(Player.name)
    if active_only:
        statement = statement.where(Player.active == True)
    return list(session.exec(statement).all())


def list_matches(session: Session) -> list[Match]:
    return list(session.exec(select(Match).order_by(Match.id.desc())).all())
