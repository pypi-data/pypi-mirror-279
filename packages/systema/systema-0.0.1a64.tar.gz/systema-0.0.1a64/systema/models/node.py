from __future__ import annotations

from pydantic import model_validator
from sqlmodel import Field

from systema.base import (
    BaseModel,
    CreatedAtMixin,
    UpdatedAtMixin,
)
from systema.models.task import (
    SubTaskMixin,
    TaskCreate,
    TaskRead,
    TaskUpdate,
)


class NodeBase(BaseModel):
    x: int | None = Field(default=None, nullable=True)
    y: int | None = Field(default=None, nullable=True)


class NodeCreate(TaskCreate, NodeBase):
    pass


class NodeRead(
    TaskRead,
    NodeBase,
    CreatedAtMixin,
    UpdatedAtMixin,
):
    @property
    def has_position(self):
        return self.x is not None and self.y is not None


class NodeUpdate(TaskUpdate):
    x: int | None = Field(default=None, nullable=True)
    y: int | None = Field(default=None, nullable=True)

    @model_validator(mode="after")
    def validate_position(self):
        if (self.x is None and self.y is not None) or (
            self.x is not None and self.y is None
        ):
            raise ValueError("Either both x and y must have values or neither.")
        return self


class Node(
    SubTaskMixin,
    NodeBase,
    CreatedAtMixin,
    UpdatedAtMixin,
    table=True,
):
    pass
