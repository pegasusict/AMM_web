import reflex as rx

from ..auth_state import AuthState
from ..components import detail_shell
from ..states import TrackState
from ._edit_helpers import edit_field, edit_header, edit_messages, id_field


def track_edit(track_id: str):
    return rx.container(
        rx.on_mount(TrackState.load(track_id, AuthState.access_token)),
        detail_shell(
            "Edit Track",
            rx.vstack(
                edit_header("Track", rx.concat("/tracks/", track_id)),
                rx.cond(
                    TrackState.track,
                    rx.vstack(
                        id_field(TrackState.track.id),
                        edit_field("MBID", TrackState.mbid, TrackState.set_mbid),
                        edit_field("Composed", TrackState.composed, TrackState.set_composed, "YYYY-MM-DD"),
                        edit_field(
                            "Release Date",
                            TrackState.release_date,
                            TrackState.set_release_date,
                            "YYYY-MM-DD",
                        ),
                        edit_field("Key ID", TrackState.key_id, TrackState.set_key_id),
                        edit_field("Lyric ID", TrackState.lyric_id, TrackState.set_lyric_id),
                        edit_field("File IDs", TrackState.file_ids, TrackState.set_file_ids, "1, 2, 3"),
                        edit_field(
                            "Album Track IDs",
                            TrackState.album_track_ids,
                            TrackState.set_album_track_ids,
                            "1, 2, 3",
                        ),
                        edit_field("Genre IDs", TrackState.genre_ids, TrackState.set_genre_ids, "1, 2, 3"),
                        edit_field(
                            "Performer IDs",
                            TrackState.performer_ids,
                            TrackState.set_performer_ids,
                            "1, 2, 3",
                        ),
                        edit_field(
                            "Conductor IDs",
                            TrackState.conductor_ids,
                            TrackState.set_conductor_ids,
                            "1, 2, 3",
                        ),
                        edit_field(
                            "Composer IDs",
                            TrackState.composer_ids,
                            TrackState.set_composer_ids,
                            "1, 2, 3",
                        ),
                        edit_field(
                            "Lyricist IDs",
                            TrackState.lyricist_ids,
                            TrackState.set_lyricist_ids,
                            "1, 2, 3",
                        ),
                        edit_field(
                            "Producer IDs",
                            TrackState.producer_ids,
                            TrackState.set_producer_ids,
                            "1, 2, 3",
                        ),
                        edit_field("Task IDs", TrackState.task_ids, TrackState.set_task_ids, "1, 2, 3"),
                        edit_field(
                            "Track Tag IDs",
                            TrackState.tracktag_ids,
                            TrackState.set_tracktag_ids,
                            "1, 2, 3",
                        ),
                        edit_messages(TrackState.error, TrackState.success_message),
                        rx.hstack(
                            rx.button(
                                "Save",
                                on_click=TrackState.save(AuthState.access_token),
                                is_loading=TrackState.loading,
                            ),
                            rx.button(
                                "Cancel",
                                variant="outline",
                                on_click=rx.redirect(rx.concat("/tracks/", track_id)),
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
