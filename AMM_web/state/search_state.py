"""State for structured library search (no ad-hoc GraphQL queries)."""

from __future__ import annotations

from AMM_web.models.library import (
    AlbumSummary,
    LabelSummary,
    PersonSummary,
    PlaylistSummary,
    QueueSummary,
    TaskDisplaySummary,
    TrackSummary,
)
from AMM_web.services.library_client import library_service
from AMM_web.state.base_state import BaseState


def _to_int(value: str, default: int) -> int:
    try:
        return int((value or "").strip())
    except Exception:
        return default


class SearchState(BaseState):
    # Tracks
    tracks_limit: str = "25"
    tracks_offset: str = "0"
    tracks: list[TrackSummary] = []
    tracks_total: int = 0
    track_id: str = ""
    selected_track: TrackSummary | None = None

    # Albums
    albums_limit: str = "25"
    albums_offset: str = "0"
    albums: list[AlbumSummary] = []
    albums_total: int = 0
    album_id: str = ""
    selected_album: AlbumSummary | None = None

    # Persons
    persons_limit: str = "25"
    persons_offset: str = "0"
    persons: list[PersonSummary] = []
    persons_total: int = 0
    person_id: str = ""
    selected_person: PersonSummary | None = None

    # Labels
    labels_limit: str = "25"
    labels_offset: str = "0"
    labels: list[LabelSummary] = []
    labels_total: int = 0
    label_id: str = ""
    selected_label: LabelSummary | None = None

    # Auth / misc
    playlists: list[PlaylistSummary] = []
    queue: QueueSummary = QueueSummary(track_ids=[])
    task_display: list[TaskDisplaySummary] = []

    def _reset_error(self) -> None:
        self.set_error(None)

    async def load_tracks(self) -> None:
        self.set_loading(True)
        self._reset_error()
        try:
            limit = _to_int(self.tracks_limit, 25)
            offset = _to_int(self.tracks_offset, 0)
            self.tracks, self.tracks_total = await library_service.list_tracks(limit=limit, offset=offset)
        except Exception as exc:
            self.set_error(str(exc))
        finally:
            self.set_loading(False)

    async def load_track(self, access_token: str = "") -> None:
        self.set_loading(True)
        self._reset_error()
        try:
            track_id = _to_int(self.track_id, 0)
            if track_id <= 0:
                self.set_error("Enter a Track ID (positive integer).")
                self.selected_track = None
                return
            self.selected_track = await library_service.get_track(track_id, access_token=access_token or None)
            if self.selected_track is None:
                self.set_error(f"Track #{track_id} not found.")
        except Exception as exc:
            self.set_error(str(exc))
        finally:
            self.set_loading(False)

    def select_track(self, track_id: int) -> None:
        self.track_id = str(track_id)

    async def load_albums(self) -> None:
        self.set_loading(True)
        self._reset_error()
        try:
            limit = _to_int(self.albums_limit, 25)
            offset = _to_int(self.albums_offset, 0)
            self.albums, self.albums_total = await library_service.list_albums(limit=limit, offset=offset)
        except Exception as exc:
            self.set_error(str(exc))
        finally:
            self.set_loading(False)

    async def load_album(self, access_token: str = "") -> None:
        self.set_loading(True)
        self._reset_error()
        try:
            album_id = _to_int(self.album_id, 0)
            if album_id <= 0:
                self.set_error("Enter an Album ID (positive integer).")
                self.selected_album = None
                return
            self.selected_album = await library_service.get_album(album_id, access_token=access_token or None)
            if self.selected_album is None:
                self.set_error(f"Album #{album_id} not found (or server does not support getAlbum).")
        except Exception as exc:
            self.set_error(str(exc))
        finally:
            self.set_loading(False)

    def select_album(self, album_id: int) -> None:
        self.album_id = str(album_id)

    async def load_persons(self) -> None:
        self.set_loading(True)
        self._reset_error()
        try:
            limit = _to_int(self.persons_limit, 25)
            offset = _to_int(self.persons_offset, 0)
            self.persons, self.persons_total = await library_service.list_persons(limit=limit, offset=offset)
        except Exception as exc:
            self.set_error(str(exc))
        finally:
            self.set_loading(False)

    async def load_person(self, access_token: str = "") -> None:
        self.set_loading(True)
        self._reset_error()
        try:
            person_id = _to_int(self.person_id, 0)
            if person_id <= 0:
                self.set_error("Enter a Person ID (positive integer).")
                self.selected_person = None
                return
            self.selected_person = await library_service.get_person(person_id, access_token=access_token or None)
            if self.selected_person is None:
                self.set_error(f"Person #{person_id} not found (or server does not support getPerson).")
        except Exception as exc:
            self.set_error(str(exc))
        finally:
            self.set_loading(False)

    def select_person(self, person_id: int) -> None:
        self.person_id = str(person_id)

    async def load_labels(self) -> None:
        self.set_loading(True)
        self._reset_error()
        try:
            limit = _to_int(self.labels_limit, 25)
            offset = _to_int(self.labels_offset, 0)
            self.labels, self.labels_total = await library_service.list_labels(limit=limit, offset=offset)
        except Exception as exc:
            self.set_error(str(exc))
        finally:
            self.set_loading(False)

    async def load_label(self, access_token: str = "") -> None:
        self.set_loading(True)
        self._reset_error()
        try:
            label_id = _to_int(self.label_id, 0)
            if label_id <= 0:
                self.set_error("Enter a Label ID (positive integer).")
                self.selected_label = None
                return
            self.selected_label = await library_service.get_label(label_id, access_token=access_token or None)
            if self.selected_label is None:
                self.set_error(f"Label #{label_id} not found (or server does not support getLabel).")
        except Exception as exc:
            self.set_error(str(exc))
        finally:
            self.set_loading(False)

    def select_label(self, label_id: int) -> None:
        self.label_id = str(label_id)

    async def load_playlists(self, access_token: str = "") -> None:
        self.set_loading(True)
        self._reset_error()
        try:
            self.playlists = await library_service.list_playlists(access_token)
        except Exception as exc:
            self.set_error(str(exc))
            self.playlists = []
        finally:
            self.set_loading(False)

    async def load_queue(self, access_token: str = "") -> None:
        self.set_loading(True)
        self._reset_error()
        try:
            self.queue = await library_service.get_queue(access_token)
        except Exception as exc:
            self.set_error(str(exc))
            self.queue = QueueSummary(track_ids=[])
        finally:
            self.set_loading(False)

    async def load_task_display(self, access_token: str = "") -> None:
        self.set_loading(True)
        self._reset_error()
        try:
            token = access_token or None
            self.task_display = await library_service.list_task_display(access_token=token)
        except Exception as exc:
            self.set_error(str(exc))
            self.task_display = []
        finally:
            self.set_loading(False)

