from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


TaskStatus = Literal["Todo", "In Progress", "Done"]


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    status: TaskStatus = "Todo"

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return value.strip()


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: TaskStatus | None = None

    @field_validator("title", mode="before", json_schema_input_type=str)
    @classmethod
    def title_must_not_be_blank(cls, value: object) -> object:
        if value is None:
            raise ValueError("Title cannot be null")
        if isinstance(value, str) and not value.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return value.strip() if isinstance(value, str) else value

    @field_validator("status", mode="before", json_schema_input_type=TaskStatus)
    @classmethod
    def status_cannot_be_null(cls, value: object) -> object:
        if value is None:
            raise ValueError("Status cannot be null")
        return value

    @model_validator(mode="after")
    def require_a_field_to_update(self) -> "TaskUpdate":
        if not self.model_fields_set:
            raise ValueError("At least one field must be provided")
        return self


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus

    model_config = ConfigDict(from_attributes=True)
