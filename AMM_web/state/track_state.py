from AMM_web.state.base_state import BaseState
from AMM_web.state.edit_helpers import none_if_blank
from AMM_web.services.library_client import library_service


class TrackState(BaseState):
    track = None
    loading = False
    success_message: str | None = None

    mbid: str = ""
    composed: str = ""
    release_date: str = ""
    key_id: str = ""
    lyric_id: str = ""
    file_ids: str = ""
    album_track_ids: str = ""
    genre_ids: str = ""
    performer_ids: str = ""
    conductor_ids: str = ""
    composer_ids: str = ""
    lyricist_ids: str = ""
    producer_ids: str = ""
    task_ids: str = ""
    tracktag_ids: str = ""

    def _set_messages(self, error: str | None = None, success: str | None = None) -> None:
        self.set_error(error)
        self.success_message = success

    def _populate_form(self) -> None:
        if not self.track:
            return
        self.mbid = self.track.mbid or ""
        self.composed = self.track.composed.isoformat() if self.track.composed else ""
        self.release_date = self.track.release_date.isoformat() if self.track.release_date else ""
        self.key_id = "" if self.track.key_id is None else str(self.track.key_id)
        self.lyric_id = "" if self.track.lyric_id is None else str(self.track.lyric_id)
        self.file_ids = ", ".join(str(v) for v in (self.track.file_ids or []))
        self.album_track_ids = ", ".join(str(v) for v in (self.track.album_track_ids or []))
        self.genre_ids = ", ".join(str(v) for v in (self.track.genre_ids or []))
        self.performer_ids = ", ".join(str(v) for v in (self.track.performer_ids or []))
        self.conductor_ids = ", ".join(str(v) for v in (self.track.conductor_ids or []))
        self.composer_ids = ", ".join(str(v) for v in (self.track.composer_ids or []))
        self.lyricist_ids = ", ".join(str(v) for v in (self.track.lyricist_ids or []))
        self.producer_ids = ", ".join(str(v) for v in (self.track.producer_ids or []))
        self.task_ids = ", ".join(str(v) for v in (self.track.task_ids or []))
        self.tracktag_ids = ", ".join(str(v) for v in (self.track.tracktag_ids or []))

    async def load(self, track_id: str, token: str):
        self.loading = True
        self._set_messages()
        self.track = await library_service.get_track(int(track_id), token)
        self._populate_form()
        self.loading = False

    async def save(self, token: str):
        if not self.track or self.track.id is None:
            self._set_messages(error="Load a track before saving.")
            return
        self.loading = True
        self._set_messages()
        try:
            payload = {
                "mbid": none_if_blank(self.mbid),
                "composed": none_if_blank(self.composed),
                "releaseDate": none_if_blank(self.release_date),
            }
            self.track = await library_service.update_track(self.track.id, payload, access_token=token or None)
            self._populate_form()
            self._set_messages(success="Track updated.")
        except Exception as exc:
            self._set_messages(error=str(exc))
        finally:
            self.loading = False
