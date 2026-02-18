import reflex as rx

from ..auth_state import AuthState
from ..components import detail_shell
from ..states import AlbumState
from ._edit_helpers import edit_field, edit_header, edit_messages, id_field


def album_edit(album_id: str):
    return rx.container(
        rx.on_mount(AlbumState.load(album_id, AuthState.access_token)),
        detail_shell(
            "Edit Album",
            rx.vstack(
                edit_header("Album", rx.concat("/albums/", album_id)),
                rx.cond(
                    AlbumState.album,
                    rx.vstack(
                        id_field(AlbumState.album.id),
                        edit_field("Title", AlbumState.title, AlbumState.set_title),
                        edit_field("Title Sort", AlbumState.title_sort, AlbumState.set_title_sort),
                        edit_field("Subtitle", AlbumState.subtitle, AlbumState.set_subtitle),
                        edit_field("MBID", AlbumState.mbid, AlbumState.set_mbid),
                        edit_field("Release Date", AlbumState.release_date, AlbumState.set_release_date, "YYYY-MM-DD"),
                        edit_field("Release Country", AlbumState.release_country, AlbumState.set_release_country),
                        edit_field("Disc Count", AlbumState.disc_count, AlbumState.set_disc_count),
                        edit_field("Track Count", AlbumState.track_count, AlbumState.set_track_count),
                        edit_field("Task ID", AlbumState.task_id, AlbumState.set_task_id),
                        edit_field("Label ID", AlbumState.label_id, AlbumState.set_label_id),
                        edit_field("Picture ID", AlbumState.picture_id, AlbumState.set_picture_id),
                        edit_field(
                            "Album Track IDs",
                            AlbumState.album_track_ids,
                            AlbumState.set_album_track_ids,
                            "1, 2, 3",
                        ),
                        edit_field("Genre IDs", AlbumState.genre_ids, AlbumState.set_genre_ids, "1, 2, 3"),
                        edit_field("Artist IDs", AlbumState.artist_ids, AlbumState.set_artist_ids, "1, 2, 3"),
                        edit_field(
                            "Conductor IDs",
                            AlbumState.conductor_ids,
                            AlbumState.set_conductor_ids,
                            "1, 2, 3",
                        ),
                        edit_field(
                            "Composer IDs",
                            AlbumState.composer_ids,
                            AlbumState.set_composer_ids,
                            "1, 2, 3",
                        ),
                        edit_field(
                            "Lyricist IDs",
                            AlbumState.lyricist_ids,
                            AlbumState.set_lyricist_ids,
                            "1, 2, 3",
                        ),
                        edit_field(
                            "Producer IDs",
                            AlbumState.producer_ids,
                            AlbumState.set_producer_ids,
                            "1, 2, 3",
                        ),
                        edit_messages(AlbumState.error, AlbumState.success_message),
                        rx.hstack(
                            rx.button(
                                "Save",
                                on_click=AlbumState.save(AuthState.access_token),
                                is_loading=AlbumState.loading,
                            ),
                            rx.button(
                                "Cancel",
                                variant="outline",
                                on_click=rx.redirect(rx.concat("/albums/", album_id)),
                            ),
                        ),
                        spacing="2",
                        width="100%",
                        align_items="start",
                    ),
                    rx.text("Loading...", color="gray"),
                ),
                spacing="4",
                width="100%",
                align_items="start",
            ),
        ),
    )
