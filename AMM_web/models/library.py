"""Library models for AMM (Audiophiles' Music Manager)."""

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class TrackSummary(BaseModel):
    id: int | None = None
    mbid: str | None = None
    title: str | None = None


class AlbumSummary(BaseModel):
    id: int | None = None
    title: str | None = None


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
