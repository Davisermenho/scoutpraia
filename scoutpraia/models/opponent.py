from sqlmodel import Field, SQLModel


class Opponent(SQLModel, table=True):
    __tablename__ = "opponents"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    category: str | None = None
    notes: str | None = None
