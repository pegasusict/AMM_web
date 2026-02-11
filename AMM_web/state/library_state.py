"""Manages library data and user interactions."""

from AMM_web.models.library import AlbumSummary, PlaylistSummary, QueueSummary, TrackSummary
from AMM_web.services.library_client import library_service
from AMM_web.state.base_state import BaseState


class LibraryState(BaseState):
    tracks: list[TrackSummary] = []
    total_tracks: int = 0
    albums: list[AlbumSummary] = []
    total_albums: int = 0
    playlists: list[PlaylistSummary] = []
    queue: QueueSummary = QueueSummary(track_ids=[])
    now_playing: TrackSummary | None = None
    auth_error: str | None = None

    async def load_library(self, access_token: str = "") -> None:
        self.set_loading(True)
        self.set_error(None)
        self.auth_error = None
        try:
            self.tracks, self.total_tracks = await library_service.list_tracks()
            self.albums, self.total_albums = await library_service.list_albums()
        except Exception as exc:
            self.set_error(str(exc))

        try:
            self.playlists = await library_service.list_playlists(access_token)
            self.queue = await library_service.get_queue(access_token)
            if self.queue.track_ids:
                self.now_playing = await library_service.get_track(self.queue.track_ids[0], access_token)
            else:
                self.now_playing = None
        except Exception as exc:
            self.auth_error = str(exc)
        finally:
            self.set_loading(False)
