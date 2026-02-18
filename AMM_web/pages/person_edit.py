import reflex as rx

from ..auth_state import AuthState
from ..components import detail_shell
from ..states import PersonState
from ._edit_helpers import edit_field, edit_header, edit_messages, id_field


def person_edit(person_id: str = ""):
    return rx.container(
        detail_shell(
            "Edit Person",
            rx.vstack(
                edit_header("Person", "/persons/" + person_id),
                rx.cond(
                    PersonState.person,
                    rx.vstack(
                        id_field(PersonState.person.id),
                        edit_field("Full Name", PersonState.full_name, PersonState.set_full_name),
                        edit_field("First Name", PersonState.first_name, PersonState.set_first_name),
                        edit_field("Middle Name", PersonState.middle_name, PersonState.set_middle_name),
                        edit_field("Last Name", PersonState.last_name, PersonState.set_last_name),
                        edit_field("Sort Name", PersonState.sort_name, PersonState.set_sort_name),
                        edit_field("Nick Name", PersonState.nick_name, PersonState.set_nick_name),
                        edit_field("Alias", PersonState.alias, PersonState.set_alias),
                        edit_field("MBID", PersonState.mbid, PersonState.set_mbid),
                        edit_field(
                            "Date of Birth",
                            PersonState.date_of_birth,
                            PersonState.set_date_of_birth,
                            "YYYY-MM-DD",
                        ),
                        edit_field(
                            "Date of Death",
                            PersonState.date_of_death,
                            PersonState.set_date_of_death,
                            "YYYY-MM-DD",
                        ),
                        edit_field("Picture ID", PersonState.picture_id, PersonState.set_picture_id),
                        edit_field(
                            "Performed Track IDs",
                            PersonState.performed_track_ids,
                            PersonState.set_performed_track_ids,
                            "1, 2, 3",
                        ),
                        edit_field(
                            "Conducted Track IDs",
                            PersonState.conducted_track_ids,
                            PersonState.set_conducted_track_ids,
                            "1, 2, 3",
                        ),
                        edit_field(
                            "Composed Track IDs",
                            PersonState.composed_track_ids,
                            PersonState.set_composed_track_ids,
                            "1, 2, 3",
                        ),
                        edit_field(
                            "Lyric Track IDs",
                            PersonState.lyric_track_ids,
                            PersonState.set_lyric_track_ids,
                            "1, 2, 3",
                        ),
                        edit_field(
                            "Produced Track IDs",
                            PersonState.produced_track_ids,
                            PersonState.set_produced_track_ids,
                            "1, 2, 3",
                        ),
                        edit_field(
                            "Performed Album IDs",
                            PersonState.performed_album_ids,
                            PersonState.set_performed_album_ids,
                            "1, 2, 3",
                        ),
                        edit_field(
                            "Conducted Album IDs",
                            PersonState.conducted_album_ids,
                            PersonState.set_conducted_album_ids,
                            "1, 2, 3",
                        ),
                        edit_field(
                            "Composed Album IDs",
                            PersonState.composed_album_ids,
                            PersonState.set_composed_album_ids,
                            "1, 2, 3",
                        ),
                        edit_field(
                            "Lyric Album IDs",
                            PersonState.lyric_album_ids,
                            PersonState.set_lyric_album_ids,
                            "1, 2, 3",
                        ),
                        edit_field(
                            "Produced Album IDs",
                            PersonState.produced_album_ids,
                            PersonState.set_produced_album_ids,
                            "1, 2, 3",
                        ),
                        edit_field("Task IDs", PersonState.task_ids, PersonState.set_task_ids, "1, 2, 3"),
                        edit_field("Label IDs", PersonState.label_ids, PersonState.set_label_ids, "1, 2, 3"),
                        edit_messages(PersonState.error, PersonState.success_message),
                        rx.hstack(
                            rx.button(
                                "Save",
                                on_click=PersonState.save(AuthState.access_token),
                                is_loading=PersonState.loading,
                            ),
                            rx.button(
                                "Cancel",
                                variant="outline",
                                on_click=rx.redirect("/persons/" + person_id),
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
