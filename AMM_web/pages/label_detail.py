import reflex as rx

from ..auth_state import AuthState
from ..states import LabelState
from ..components import detail_shell
from ._detail_helpers import detail_content, field


def label_detail(label_id: str):

    return rx.container(
        rx.on_mount(LabelState.load(label_id, AuthState.access_token)),
        detail_shell(
            "Label Detail",
            detail_content(
                "Label",
                LabelState.label,
                [
                    field("ID", LabelState.label.id),
                    field("Name", LabelState.label.name),
                    field("MBID", LabelState.label.mbid),
                    field("Description", LabelState.label.description),
                    field("Founded", LabelState.label.founded),
                    field("Defunct", LabelState.label.defunct),
                    field("Owner ID", LabelState.label.owner_id),
                    field("Parent ID", LabelState.label.parent_id),
                    field("Picture ID", LabelState.label.picture_id),
                    field("Child IDs", LabelState.label.child_ids, "[]"),
                    field("Album IDs", LabelState.label.album_ids, "[]"),
                ],
                edit_href=rx.concat("/labels/", label_id, "/edit"),
            ),
        ),
    )
