import reflex as rx

from ..auth_state import AuthState
from ..components import detail_shell
from ..states import LabelState
from ._edit_helpers import edit_field, edit_header, edit_messages, edit_textarea, id_field


def label_edit(label_id: str = ""):
    return rx.container(
        detail_shell(
            "Edit Label",
            rx.vstack(
                edit_header("Label", "/labels/" + label_id),
                rx.cond(
                    LabelState.label,
                    rx.vstack(
                        id_field(LabelState.label.id),
                        edit_field("Name", LabelState.name, LabelState.set_name),
                        edit_field("MBID", LabelState.mbid, LabelState.set_mbid),
                        edit_textarea("Description", LabelState.description, LabelState.set_description),
                        edit_field("Founded", LabelState.founded, LabelState.set_founded, "YYYY-MM-DD"),
                        edit_field("Defunct", LabelState.defunct, LabelState.set_defunct, "YYYY-MM-DD"),
                        edit_field("Owner ID", LabelState.owner_id, LabelState.set_owner_id),
                        edit_field("Parent ID", LabelState.parent_id, LabelState.set_parent_id),
                        edit_field("Picture ID", LabelState.picture_id, LabelState.set_picture_id),
                        edit_field("Child IDs", LabelState.child_ids, LabelState.set_child_ids, "1, 2, 3"),
                        edit_field("Album IDs", LabelState.album_ids, LabelState.set_album_ids, "1, 2, 3"),
                        edit_messages(LabelState.error, LabelState.success_message),
                        rx.hstack(
                            rx.button(
                                "Save",
                                on_click=LabelState.save(AuthState.access_token),
                                is_loading=LabelState.loading,
                            ),
                            rx.button(
                                "Cancel",
                                variant="outline",
                                on_click=rx.redirect("/labels/" + label_id),
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
