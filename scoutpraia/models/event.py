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
    result_possession: str | None = None
    scorer_role: str | None = None
    court_lane: str | None = None
    shot_origin_depth: str | None = None
    goal_zone: str | None = None
    trajectory_visible: bool | None = None
    derived_points: int | None = Field(default=None, ge=0, le=2)
    review_marker: bool | None = None
    notes: str | None = None
