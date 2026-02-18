import reflex as rx

from ..auth_state import AuthState
from ..states import AlbumState
from ..components import detail_shell
from ._detail_helpers import detail_content, field


def album_detail(album_id: str = ""):

    return rx.container(
        detail_shell(
            "Album Detail",
            detail_content(
                "Album",
                AlbumState.album,
                [
                    field("ID", AlbumState.album.id),
                    field("Title", AlbumState.album.title),
                    field("Title Sort", AlbumState.album.title_sort),
                    field("Subtitle", AlbumState.album.subtitle),
                    field("MBID", AlbumState.album.mbid),
                    field("Release Date", AlbumState.album.release_date),
                    field("Release Country", AlbumState.album.release_country),
                    field("Disc Count", AlbumState.album.disc_count),
                    field("Track Count", AlbumState.album.track_count),
                    field("Task ID", AlbumState.album.task_id),
                    field("Label ID", AlbumState.album.label_id),
                    field("Picture ID", AlbumState.album.picture_id),
                    field("Album Track IDs", AlbumState.album.album_track_ids, "[]"),
                    field("Genre IDs", AlbumState.album.genre_ids, "[]"),
                    field("Artist IDs", AlbumState.album.artist_ids, "[]"),
                    field("Conductor IDs", AlbumState.album.conductor_ids, "[]"),
                    field("Composer IDs", AlbumState.album.composer_ids, "[]"),
                    field("Lyricist IDs", AlbumState.album.lyricist_ids, "[]"),
                    field("Producer IDs", AlbumState.album.producer_ids, "[]"),
                ],
                edit_href="/albums/" + album_id + "/edit",
            ),
        ),
    )
