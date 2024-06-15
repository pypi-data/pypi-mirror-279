from sqlmodel import Field

from systema.base import (
    BaseModel,
    CreatedAtMixin,
    IdMixin,
    UpdatedAtMixin,
)


class ConnectorBase(BaseModel):
    a: str = Field(..., foreign_key="node.id")
    b: str = Field(..., foreign_key="node.id")


class ConnectorCreate(ConnectorBase):
    pass


class ConnectorUpdate(BaseModel):
    a: str | None = None
    b: str | None = None


class Connector(
    ConnectorBase,
    IdMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
    table=True,
):
    mind_map_id: str = Field(..., foreign_key="mindmap.id")


class ConnectorRead(
    ConnectorBase,
    CreatedAtMixin,
    UpdatedAtMixin,
):
    id: str
    mind_map_id: str

    @classmethod
    def from_conn(cls, conn: Connector):
        return ConnectorRead.model_validate(conn)
