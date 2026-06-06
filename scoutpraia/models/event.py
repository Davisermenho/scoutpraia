from sqlmodel import Field, SQLModel


class Event(SQLModel, table=True):
    __tablename__ = "events"

    id: int | None = Field(default=None, primary_key=True)
    match_id: int = Field(foreign_key="matches.id")
    set_id: int | None = Field(default=None, foreign_key="sets.id")
    possession_id: int | None = Field(default=None, foreign_key="possessions.id")
    taxonomy_version_id: int = Field(foreign_key="taxonomy_versions.id")
    event_type: str
    event_subtype: str | None = None
    player_id: int | None = Field(default=None, foreign_key="players.id")
    secondary_player_id: int | None = Field(default=None, foreign_key="players.id")
    team_side: str
    timestamp_second: float = Field(ge=0)
    outcome: str | None = None
    zone: str | None = None
    points_value: int = Field(default=0, ge=0, le=2)
    notes: str | None = None
