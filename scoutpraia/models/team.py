from sqlmodel import Field, SQLModel


class Team(SQLModel, table=True):
    __tablename__ = "teams"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    category: str | None = None
    notes: str | None = None
