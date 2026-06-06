from sqlmodel import Field, SQLModel


class Clip(SQLModel, table=True):
    __tablename__ = "clips"

    id: int | None = Field(default=None, primary_key=True)
    match_id: int = Field(foreign_key="matches.id")
    event_id: int | None = Field(default=None, foreign_key="events.id")
    player_id: int | None = Field(default=None, foreign_key="players.id")
    clip_path: str
    start_second: float
    end_second: float
    label: str
