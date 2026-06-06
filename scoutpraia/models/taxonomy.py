from datetime import datetime

from sqlmodel import Field, SQLModel

from scoutpraia.utils.datetime import utc_now


class TaxonomyVersion(SQLModel, table=True):
    __tablename__ = "taxonomy_versions"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    status: str = "draft"
    created_at: datetime = Field(default_factory=utc_now)
    approved_at: datetime | None = None
    notes: str | None = None


class EventDefinition(SQLModel, table=True):
    __tablename__ = "event_definitions"

    id: int | None = Field(default=None, primary_key=True)
    taxonomy_version_id: int = Field(foreign_key="taxonomy_versions.id")
    event_type: str
    definition: str
    include_when: str | None = None
    exclude_when: str | None = None
    decision_rule: str | None = None
    evidence_type: str = "practical_hypothesis"
    active: bool = True
