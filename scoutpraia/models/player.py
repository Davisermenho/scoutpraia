from sqlmodel import Field, SQLModel


class Player(SQLModel, table=True):
    __tablename__ = "players"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    shirt_number: int | None = None
    primary_role: str | None = None
    secondary_role: str | None = None
    active: bool = True
