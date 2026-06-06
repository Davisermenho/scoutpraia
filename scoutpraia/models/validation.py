from datetime import datetime

from sqlmodel import Field, SQLModel


class CodingSession(SQLModel, table=True):
    __tablename__ = "coding_sessions"

    id: int | None = Field(default=None, primary_key=True)
    match_id: int = Field(foreign_key="matches.id")
    taxonomy_version_id: int = Field(foreign_key="taxonomy_versions.id")
    coder_name: str
    session_type: str
    started_at: datetime = Field(default_factory=datetime.utcnow)
    finished_at: datetime | None = None
    notes: str | None = None


class CodingAgreement(SQLModel, table=True):
    __tablename__ = "coding_agreements"

    id: int | None = Field(default=None, primary_key=True)
    match_id: int = Field(foreign_key="matches.id")
    taxonomy_version_id: int = Field(foreign_key="taxonomy_versions.id")
    comparison_type: str
    agreement_percent: float
    total_events_compared: int
    total_disagreements: int
    disagreements_json: str | None = None
    approved: bool = False
    notes: str | None = None
