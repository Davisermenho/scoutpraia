from datetime import date

from sqlmodel import Field, SQLModel


class Match(SQLModel, table=True):
    __tablename__ = "matches"

    id: int | None = Field(default=None, primary_key=True)
    match_date: date | None = None
    competition_name: str | None = None
    phase: str | None = None
    opponent_id: int | None = Field(default=None, foreign_key="opponents.id")
    video_path: str | None = None
    duration_seconds: float | None = None
    video_width: int | None = None
    video_height: int | None = None
    video_fps: float | None = None
    video_codec: str | None = None
    final_score_team: int | None = None
    final_score_opponent: int | None = None
    notes: str | None = None


class MatchRoster(SQLModel, table=True):
    __tablename__ = "match_roster"

    id: int | None = Field(default=None, primary_key=True)
    match_id: int = Field(foreign_key="matches.id")
    player_id: int = Field(foreign_key="players.id")
    available: bool = True
    starter: bool = False


class SetSegment(SQLModel, table=True):
    __tablename__ = "sets"

    id: int | None = Field(default=None, primary_key=True)
    match_id: int = Field(foreign_key="matches.id")
    set_number: int
    start_second: float | None = None
    end_second: float | None = None
    score_team: int | None = None
    score_opponent: int | None = None


class Possession(SQLModel, table=True):
    __tablename__ = "possessions"

    id: int | None = Field(default=None, primary_key=True)
    match_id: int = Field(foreign_key="matches.id")
    set_id: int | None = Field(default=None, foreign_key="sets.id")
    team_side: str
    start_second: float | None = None
    end_second: float | None = None
    result: str | None = None
    points_scored: int = 0
    points_conceded: int = 0
