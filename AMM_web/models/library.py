"""Library models for AMM (Audiophiles' Music Manager)."""

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class TrackSummary(BaseModel):
    id: int | None = None
    mbid: str | None = None
    title: str | None = None


class AlbumSummary(BaseModel):
    id: int | None = None
    title: str | None = None


class PersonSummary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int | None = None
    full_name: str | None = Field(
        default=None,
        validation_alias=AliasChoices("full_name", "fullName"),
    )


class LabelSummary(BaseModel):
    id: int | None = None
    name: str | None = None


class PlaylistSummary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    name: str
    track_ids: list[int] = Field(
        default_factory=list,
        validation_alias=AliasChoices("track_ids", "trackIds"),
    )


class QueueSummary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    track_ids: list[int] = Field(
        default_factory=list,
        validation_alias=AliasChoices("track_ids", "trackIds"),
    )


class TaskDisplaySummary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    task_id: str | None = Field(
        default=None,
        validation_alias=AliasChoices("task_id", "taskId"),
    )
    task_type: str | None = Field(
        default=None,
        validation_alias=AliasChoices("task_type", "taskType"),
    )
    progress: int | None = None
    start_time: str | None = Field(
        default=None,
        validation_alias=AliasChoices("start_time", "startTime"),
    )
    status: str | None = None
