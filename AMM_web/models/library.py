"""Library models for AMM (Audiophiles' Music Manager)."""

from datetime import date

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, model_validator


def _to_camel(value: str) -> str:
    parts = value.split("_")
    return parts[0] + "".join(part.capitalize() for part in parts[1:])


class LibraryModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=_to_camel,
    )


class TrackSummary(LibraryModel):
    id: int | None = None
    composed: date | None = None
    release_date: date | None = None
    mbid: str | None = None
    file_ids: list[int] = Field(default_factory=list)
    album_track_ids: list[int] = Field(default_factory=list)
    key_id: int | None = None
    genre_ids: list[int] = Field(default_factory=list)
    performer_ids: list[int] = Field(default_factory=list)
    conductor_ids: list[int] = Field(default_factory=list)
    composer_ids: list[int] = Field(default_factory=list)
    lyricist_ids: list[int] = Field(default_factory=list)
    producer_ids: list[int] = Field(default_factory=list)
    task_ids: list[int] = Field(default_factory=list)
    lyric_id: int | None = None
    tracktag_ids: list[int] = Field(default_factory=list)

    # Legacy UI field; server track type does not currently expose title.
    title: str | None = None

    @model_validator(mode="after")
    def set_legacy_title(self) -> "TrackSummary":
        if self.title is None and self.mbid:
            self.title = self.mbid
        return self


class AlbumSummary(LibraryModel):
    id: int | None = None
    mbid: str | None = None
    title: str | None = None
    title_sort: str | None = None
    subtitle: str | None = None
    release_date: date | None = None
    release_country: str | None = None
    disc_count: int | None = None
    track_count: int | None = None
    task_id: int | None = None
    label_id: int | None = None
    album_track_ids: list[int] = Field(default_factory=list)
    genre_ids: list[int] = Field(default_factory=list)
    artist_ids: list[int] = Field(default_factory=list)
    conductor_ids: list[int] = Field(default_factory=list)
    composer_ids: list[int] = Field(default_factory=list)
    lyricist_ids: list[int] = Field(default_factory=list)
    producer_ids: list[int] = Field(default_factory=list)
    picture_id: int | None = None


class PersonSummary(LibraryModel):
    id: int | None = None
    mbid: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    sort_name: str | None = None
    full_name: str | None = None
    nick_name: str | None = None
    alias: str | None = None
    date_of_birth: date | None = None
    date_of_death: date | None = None
    picture_id: int | None = None
    performed_track_ids: list[int] = Field(default_factory=list)
    conducted_track_ids: list[int] = Field(default_factory=list)
    composed_track_ids: list[int] = Field(default_factory=list)
    lyric_track_ids: list[int] = Field(default_factory=list)
    produced_track_ids: list[int] = Field(default_factory=list)
    performed_album_ids: list[int] = Field(default_factory=list)
    conducted_album_ids: list[int] = Field(default_factory=list)
    composed_album_ids: list[int] = Field(default_factory=list)
    lyric_album_ids: list[int] = Field(default_factory=list)
    produced_album_ids: list[int] = Field(default_factory=list)
    task_ids: list[int] = Field(default_factory=list)
    label_ids: list[int] = Field(default_factory=list)

    # Legacy UI field used on search cards.
    title: str | None = None

    @model_validator(mode="after")
    def set_legacy_title(self) -> "PersonSummary":
        if self.title is None and self.full_name:
            self.title = self.full_name
        return self


class LabelSummary(LibraryModel):
    id: int | None = None
    name: str | None = None
    mbid: str | None = None
    founded: date | None = None
    defunct: date | None = None
    description: str | None = None
    owner_id: int | None = None
    parent_id: int | None = None
    child_ids: list[int] = Field(default_factory=list)
    picture_id: int | None = None
    album_ids: list[int] = Field(default_factory=list)

    # Legacy UI field used on search cards.
    title: str | None = None

    @model_validator(mode="after")
    def set_legacy_title(self) -> "LabelSummary":
        if self.title is None and self.name:
            self.title = self.name
        return self


class FileSummary(LibraryModel):
    id: int | None = None
    audio_ip: str | None = None
    imported: str | None = None
    processed: str | None = None
    bitrate: int | None = None
    sample_rate: int | None = None
    channels: int | None = None
    file_type: str | None = None
    file_size: int | None = None
    file_name: str | None = None
    file_extension: str | None = None
    codec: str | None = None
    duration: int | None = None
    track_id: int | None = None
    task_id: int | None = None
    file_path: str | None = None
    stage_type: int | None = None
    completed_tasks: list[str] = Field(default_factory=list)

    # Backward compatibility aliases.
    filename: str | None = Field(
        default=None,
        validation_alias=AliasChoices("filename", "file_name", "fileName"),
    )
    filepath: str | None = Field(
        default=None,
        validation_alias=AliasChoices("filepath", "file_path", "filePath"),
    )
    filesize: int | None = Field(
        default=None,
        validation_alias=AliasChoices("filesize", "file_size", "fileSize"),
    )
    filetype: str | None = Field(
        default=None,
        validation_alias=AliasChoices("filetype", "file_type", "fileType"),
    )

    @model_validator(mode="after")
    def sync_legacy_file_fields(self) -> "FileSummary":
        if self.filename is None:
            self.filename = self.file_name
        if self.file_name is None:
            self.file_name = self.filename

        if self.filepath is None:
            self.filepath = self.file_path
        if self.file_path is None:
            self.file_path = self.filepath

        if self.filesize is None:
            self.filesize = self.file_size
        if self.file_size is None:
            self.file_size = self.filesize

        if self.filetype is None:
            self.filetype = self.file_type
        if self.file_type is None:
            self.file_type = self.filetype

        return self


class PlaylistSummary(LibraryModel):
    id: int | None = None
    name: str | None = None
    user_id: int | None = None
    playlist_track_ids: list[int] = Field(default_factory=list)
    track_ids: list[int] = Field(default_factory=list)


class QueueSummary(LibraryModel):
    id: int | None = None
    user_id: int | None = None
    track_ids: list[int] = Field(default_factory=list)


class TaskDisplaySummary(LibraryModel):
    task_id: str | None = None
    task_type: str | None = None
    progress: int | None = None
    start_time: str | None = None
    status: str | None = None
