import reflex as rx

from ..auth_state import AuthState
from ..states import TrackState
from ..components import detail_shell
from ._detail_helpers import detail_content, field


def track_detail(track_id: str):

    return rx.container(
        rx.on_mount(TrackState.load(track_id, AuthState.access_token)),
        detail_shell(
            "Track Detail",
            detail_content(
                "Track",
                TrackState.track,
                [
                    field("ID", TrackState.track.id),
                    field("MBID", TrackState.track.mbid),
                    field("Composed", TrackState.track.composed),
                    field("Release Date", TrackState.track.release_date),
                    field("Key ID", TrackState.track.key_id),
                    field("Lyric ID", TrackState.track.lyric_id),
                    field("File IDs", TrackState.track.file_ids, "[]"),
                    field("Album Track IDs", TrackState.track.album_track_ids, "[]"),
                    field("Genre IDs", TrackState.track.genre_ids, "[]"),
                    field("Performer IDs", TrackState.track.performer_ids, "[]"),
                    field("Conductor IDs", TrackState.track.conductor_ids, "[]"),
                    field("Composer IDs", TrackState.track.composer_ids, "[]"),
                    field("Lyricist IDs", TrackState.track.lyricist_ids, "[]"),
                    field("Producer IDs", TrackState.track.producer_ids, "[]"),
                    field("Task IDs", TrackState.track.task_ids, "[]"),
                    field("Track Tag IDs", TrackState.track.tracktag_ids, "[]"),
                ],
            ),
        ),
    )
