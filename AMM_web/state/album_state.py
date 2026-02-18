from AMM_web.state.base_state import BaseState
from AMM_web.state.edit_helpers import none_if_blank, parse_int_optional
from AMM_web.models.library import AlbumSummary
from AMM_web.services.library_client import library_service


class AlbumState(BaseState):
    album: AlbumSummary | None = None
    loading = False
    success_message: str | None = None

    mbid: str = ""
    title: str = ""
    title_sort: str = ""
    subtitle: str = ""
    release_date: str = ""
    release_country: str = ""
    disc_count: str = ""
    track_count: str = ""
    task_id: str = ""
    album_label_id: str = ""
    picture_id: str = ""
    album_track_ids: str = ""
    genre_ids: str = ""
    artist_ids: str = ""
    conductor_ids: str = ""
    composer_ids: str = ""
    lyricist_ids: str = ""
    producer_ids: str = ""

    def _set_messages(self, error: str | None = None, success: str | None = None) -> None:
        self.set_error(error)
        self.success_message = success

    def _populate_form(self) -> None:
        if not self.album:
            return
        self.mbid = self.album.mbid or ""
        self.title = self.album.title or ""
        self.title_sort = self.album.title_sort or ""
        self.subtitle = self.album.subtitle or ""
        self.release_date = self.album.release_date.isoformat() if self.album.release_date else ""
        self.release_country = self.album.release_country or ""
        self.disc_count = "" if self.album.disc_count is None else str(self.album.disc_count)
        self.track_count = "" if self.album.track_count is None else str(self.album.track_count)
        self.task_id = "" if self.album.task_id is None else str(self.album.task_id)
        self.album_label_id = "" if self.album.label_id is None else str(self.album.label_id)
        self.picture_id = "" if self.album.picture_id is None else str(self.album.picture_id)
        self.album_track_ids = ", ".join(str(v) for v in (self.album.album_track_ids or []))
        self.genre_ids = ", ".join(str(v) for v in (self.album.genre_ids or []))
        self.artist_ids = ", ".join(str(v) for v in (self.album.artist_ids or []))
        self.conductor_ids = ", ".join(str(v) for v in (self.album.conductor_ids or []))
        self.composer_ids = ", ".join(str(v) for v in (self.album.composer_ids or []))
        self.lyricist_ids = ", ".join(str(v) for v in (self.album.lyricist_ids or []))
        self.producer_ids = ", ".join(str(v) for v in (self.album.producer_ids or []))

    async def load(self, album_id: str, token: str):
        self.loading = True
        self._set_messages()
        self.album = await library_service.get_album(int(album_id), token)
        self._populate_form()
        self.loading = False

    async def load_from_route(self, token: str = ""):
        route_id = str(self.router.page.params.get("album_id", "")).strip()
        if not route_id:
            return
        await self.load(route_id, token)

    async def save(self, token: str):
        if not self.album or self.album.id is None:
            self._set_messages(error="Load an album before saving.")
            return
        self.loading = True
        self._set_messages()
        try:
            payload = {
                "mbid": none_if_blank(self.mbid),
                "title": none_if_blank(self.title),
                "titleSort": none_if_blank(self.title_sort),
                "subtitle": none_if_blank(self.subtitle),
                "releaseDate": none_if_blank(self.release_date),
                "releaseCountry": none_if_blank(self.release_country),
                "discCount": parse_int_optional(self.disc_count, "Disc Count"),
                "trackCount": parse_int_optional(self.track_count, "Track Count"),
                "taskId": parse_int_optional(self.task_id, "Task ID"),
            }
            self.album = await library_service.update_album(self.album.id, payload, access_token=token or None)
            self._populate_form()
            self._set_messages(success="Album updated.")
        except Exception as exc:
            self._set_messages(error=str(exc))
        finally:
            self.loading = False
