from datetime import date
from pathlib import Path

from sqlmodel import Session, select

from scoutpraia.models.clip import Clip
from scoutpraia.models.event import Event
from scoutpraia.models.match import Match, MatchRoster
from scoutpraia.models.opponent import Opponent
from scoutpraia.models.player import Player
from scoutpraia.models.report import Report
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


def update_opponent(
    session: Session,
    opponent_id: int,
    *,
    name: str,
    category: str | None = None,
    notes: str | None = None,
) -> Opponent:
    opponent = session.get(Opponent, opponent_id)
    if opponent is None:
        raise ValueError(f"Adversária não encontrada: {opponent_id}")
    opponent.name = name.strip()
    opponent.category = category or None
    opponent.notes = notes or None
    if not opponent.name:
        raise ValueError("Nome da adversária é obrigatório.")
    session.add(opponent)
    session.commit()
    session.refresh(opponent)
    return opponent


def delete_opponent(session: Session, opponent_id: int) -> bool:
    opponent = session.get(Opponent, opponent_id)
    if opponent is None:
        return False
    linked_match = session.exec(
        select(Match).where(Match.opponent_id == opponent_id)
    ).first()
    if linked_match is not None:
        raise ValueError(
            f"Adversária {opponent_id} possui jogos vinculados e não pode ser excluída."
        )
    session.delete(opponent)
    session.commit()
    return True


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


def update_player(
    session: Session,
    player_id: int,
    *,
    name: str,
    shirt_number: int | None = None,
    primary_role: str | None = None,
    secondary_role: str | None = None,
    active: bool = True,
) -> Player:
    player = session.get(Player, player_id)
    if player is None:
        raise ValueError(f"Atleta não encontrada: {player_id}")
    player.name = name.strip()
    player.shirt_number = shirt_number
    player.primary_role = primary_role or None
    player.secondary_role = secondary_role or None
    player.active = active
    if not player.name:
        raise ValueError("Nome da atleta é obrigatório.")
    session.add(player)
    session.commit()
    session.refresh(player)
    return player


def delete_player(session: Session, player_id: int) -> bool:
    player = session.get(Player, player_id)
    if player is None:
        return False
    dependencies = [
        session.exec(select(MatchRoster).where(MatchRoster.player_id == player_id)).first(),
        session.exec(select(Event).where(Event.player_id == player_id)).first(),
        session.exec(select(Event).where(Event.secondary_player_id == player_id)).first(),
        session.exec(select(Clip).where(Clip.player_id == player_id)).first(),
    ]
    if any(item is not None for item in dependencies):
        raise ValueError(
            f"Atleta {player_id} possui vínculos operacionais e não pode ser excluída."
        )
    session.delete(player)
    session.commit()
    return True


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


def update_match_with_video(
    session: Session,
    match_id: int,
    *,
    video_path: str | Path,
    match_date: date | None = None,
    opponent_id: int | None = None,
    competition_name: str | None = None,
    phase: str | None = None,
    notes: str | None = None,
    final_score_team: int | None = None,
    final_score_opponent: int | None = None,
) -> Match:
    match = session.get(Match, match_id)
    if match is None:
        raise ValueError(f"Jogo não encontrado: {match_id}")
    metadata = probe_video_metadata(video_path)
    match.match_date = match_date
    match.opponent_id = opponent_id
    match.competition_name = competition_name or None
    match.phase = phase or None
    match.video_path = str(video_path)
    match.duration_seconds = metadata.duration_seconds
    match.video_width = metadata.width
    match.video_height = metadata.height
    match.video_fps = metadata.fps
    match.video_codec = metadata.codec
    match.notes = notes or None
    match.final_score_team = final_score_team
    match.final_score_opponent = final_score_opponent
    session.add(match)
    session.commit()
    session.refresh(match)
    return match


def delete_match(session: Session, match_id: int) -> bool:
    match = session.get(Match, match_id)
    if match is None:
        return False
    dependencies = [
        session.exec(select(MatchRoster).where(MatchRoster.match_id == match_id)).first(),
        session.exec(select(Event).where(Event.match_id == match_id)).first(),
        session.exec(select(Clip).where(Clip.match_id == match_id)).first(),
        session.exec(select(Report).where(Report.match_id == match_id)).first(),
    ]
    if any(item is not None for item in dependencies):
        raise ValueError(
            f"Jogo {match_id} possui vínculos operacionais e não pode ser excluído."
        )
    session.delete(match)
    session.commit()
    return True


def list_opponents(session: Session) -> list[Opponent]:
    return list(session.exec(select(Opponent).order_by(Opponent.name)).all())


def list_players(session: Session, active_only: bool = True) -> list[Player]:
    statement = select(Player).order_by(Player.name)
    if active_only:
        statement = statement.where(Player.active == True)
    return list(session.exec(statement).all())


def list_matches(session: Session) -> list[Match]:
    return list(session.exec(select(Match).order_by(Match.id.desc())).all())


def add_player_to_match(
    session: Session,
    match_id: int,
    player_id: int,
    available: bool = True,
    starter: bool = False,
) -> MatchRoster:
    match = session.get(Match, match_id)
    if match is None:
        raise ValueError(f"Jogo não encontrado: {match_id}")

    player = session.get(Player, player_id)
    if player is None:
        raise ValueError(f"Atleta não encontrada: {player_id}")

    roster_entry = session.exec(
        select(MatchRoster).where(
            MatchRoster.match_id == match_id,
            MatchRoster.player_id == player_id,
        )
    ).first()
    if roster_entry is None:
        roster_entry = MatchRoster(
            match_id=match_id,
            player_id=player_id,
            available=available,
            starter=starter,
        )
    else:
        roster_entry.available = available
        roster_entry.starter = starter

    session.add(roster_entry)
    session.commit()
    session.refresh(roster_entry)
    return roster_entry


def list_match_roster(session: Session, match_id: int) -> list[MatchRoster]:
    return list(
        session.exec(
            select(MatchRoster)
            .where(MatchRoster.match_id == match_id)
            .order_by(MatchRoster.id)
        ).all()
    )


def remove_player_from_match(session: Session, match_id: int, player_id: int) -> bool:
    roster_entry = session.exec(
        select(MatchRoster).where(
            MatchRoster.match_id == match_id,
            MatchRoster.player_id == player_id,
        )
    ).first()
    if roster_entry is None:
        return False

    session.delete(roster_entry)
    session.commit()
    return True
