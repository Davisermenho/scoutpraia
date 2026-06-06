from datetime import datetime

from sqlmodel import Field, SQLModel


class Report(SQLModel, table=True):
    __tablename__ = "reports"

    id: int | None = Field(default=None, primary_key=True)
    match_id: int = Field(foreign_key="matches.id")
    report_type: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    file_path: str
    payload_json: str | None = None
