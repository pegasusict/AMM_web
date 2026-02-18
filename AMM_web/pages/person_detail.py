import reflex as rx

from ..auth_state import AuthState
from ..states import PersonState
from ..components import detail_shell
from ._detail_helpers import detail_content, field


def person_detail(person_id: str):

    return rx.container(
        rx.on_mount(PersonState.load(person_id, AuthState.access_token)),
        detail_shell(
            "Person Detail",
            detail_content(
                "Person",
                PersonState.person,
                [
                    field("ID", PersonState.person.id),
                    field("Full Name", PersonState.person.full_name),
                    field("First Name", PersonState.person.first_name),
                    field("Middle Name", PersonState.person.middle_name),
                    field("Last Name", PersonState.person.last_name),
                    field("Sort Name", PersonState.person.sort_name),
                    field("Nick Name", PersonState.person.nick_name),
                    field("Alias", PersonState.person.alias),
                    field("MBID", PersonState.person.mbid),
                    field("Date of Birth", PersonState.person.date_of_birth),
                    field("Date of Death", PersonState.person.date_of_death),
                    field("Picture ID", PersonState.person.picture_id),
                    field("Performed Track IDs", PersonState.person.performed_track_ids, "[]"),
                    field("Conducted Track IDs", PersonState.person.conducted_track_ids, "[]"),
                    field("Composed Track IDs", PersonState.person.composed_track_ids, "[]"),
                    field("Lyric Track IDs", PersonState.person.lyric_track_ids, "[]"),
                    field("Produced Track IDs", PersonState.person.produced_track_ids, "[]"),
                    field("Performed Album IDs", PersonState.person.performed_album_ids, "[]"),
                    field("Conducted Album IDs", PersonState.person.conducted_album_ids, "[]"),
                    field("Composed Album IDs", PersonState.person.composed_album_ids, "[]"),
                    field("Lyric Album IDs", PersonState.person.lyric_album_ids, "[]"),
                    field("Produced Album IDs", PersonState.person.produced_album_ids, "[]"),
                    field("Task IDs", PersonState.person.task_ids, "[]"),
                    field("Label IDs", PersonState.person.label_ids, "[]"),
                ],
            ),
        ),
    )
