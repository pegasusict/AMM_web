"""Structured library search page (no ad-hoc GraphQL queries)."""

import reflex as rx

from ..auth_state import AuthState
from ..components import auth_gate, footer, navbar, player_shell
from ..state.search_state import SearchState

_CARD_BORDER = "1px solid #E2E8F0"


def _ro_field(label: str, value: str) -> rx.Component:
    return rx.vstack(
        rx.text(label, size="2", color="gray"),
        rx.input(value=value, is_read_only=True),
        spacing="1",
        width="100%",
        align_items="start",
    )


def _track_row(track) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.cond(
                    track.id,
                    rx.text(
                        "#",
                        track.id.to(str),
                        "  ",
                        rx.cond(track.title, track.title, ""),
                        weight="medium",
                    ),
                    rx.text("(unknown track)", weight="medium"),
                ),
                rx.spacer(),
                rx.button(
                    "View",
                    size="2",
                    variant="outline",
                    on_click=[
                        SearchState.select_track(track.id),
                        SearchState.load_track(AuthState.access_token),
                    ],
                    is_disabled=rx.cond(track.id, False, True),
                ),
                spacing="3",
                align_items="center",
                width="100%",
            ),
            rx.text(
                rx.cond(track.mbid, track.mbid, "(no mbid)"),
                size="2",
                color="gray",
            ),
            spacing="1",
            width="100%",
        ),
        border=_CARD_BORDER,
        border_radius="10px",
        padding="0.75em",
        width="100%",
    )


def _album_row(album) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.cond(
                album.id,
                rx.text(
                    "#",
                    album.id.to(str),
                    "  ",
                    rx.cond(album.title, album.title, "(untitled)"),
                    weight="medium",
                ),
                rx.text("(unknown album)", weight="medium"),
            ),
            rx.spacer(),
            rx.button(
                "View",
                size="2",
                variant="outline",
                on_click=[
                    SearchState.select_album(album.id),
                    SearchState.load_album(AuthState.access_token),
                ],
                is_disabled=rx.cond(album.id, False, True),
            ),
            spacing="3",
            align_items="center",
            width="100%",
        ),
        border=_CARD_BORDER,
        border_radius="10px",
        padding="0.75em",
        width="100%",
    )


def _person_row(person) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.cond(
                person.id,
                rx.text(
                    "#",
                    person.id.to(str),
                    "  ",
                    rx.cond(person.full_name, person.full_name, "(no name)"),
                    weight="medium",
                ),
                rx.text("(unknown person)", weight="medium"),
            ),
            rx.spacer(),
            rx.button(
                "View",
                size="2",
                variant="outline",
                on_click=[
                    SearchState.select_person(person.id),
                    SearchState.load_person(AuthState.access_token),
                ],
                is_disabled=rx.cond(person.id, False, True),
            ),
            spacing="3",
            align_items="center",
            width="100%",
        ),
        border=_CARD_BORDER,
        border_radius="10px",
        padding="0.75em",
        width="100%",
    )


def _label_row(label) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.cond(
                label.id,
                rx.text(
                    "#",
                    label.id.to(str),
                    "  ",
                    rx.cond(label.name, label.name, "(no name)"),
                    weight="medium",
                ),
                rx.text("(unknown label)", weight="medium"),
            ),
            rx.spacer(),
            rx.button(
                "View",
                size="2",
                variant="outline",
                on_click=[
                    SearchState.select_label(label.id),
                    SearchState.load_label(AuthState.access_token),
                ],
                is_disabled=rx.cond(label.id, False, True),
            ),
            spacing="3",
            align_items="center",
            width="100%",
        ),
        border=_CARD_BORDER,
        border_radius="10px",
        padding="0.75em",
        width="100%",
    )


def search() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="bottom-left"),
        player_shell(
            rx.vstack(
                navbar(),
                auth_gate(),
                rx.container(
                    rx.vstack(
                        rx.heading("Library Search", size="8"),
                        rx.text(
                            "Browse library entities with structured search forms. "
                            "Detail and edit views are displayed as read-only forms."
                        ),
                        rx.cond(SearchState.error, rx.text(SearchState.error, color="red")),
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.heading(f"Tracks ({SearchState.tracks_total})", size="4"),
                                    rx.spacer(),
                                    rx.text("Limit", size="2", color="gray"),
                                    rx.input(
                                        width="6em",
                                        value=SearchState.tracks_limit,
                                        on_change=SearchState.set_tracks_limit,
                                    ),
                                    rx.text("Offset", size="2", color="gray"),
                                    rx.input(
                                        width="6em",
                                        value=SearchState.tracks_offset,
                                        on_change=SearchState.set_tracks_offset,
                                    ),
                                    rx.button(
                                        "Search",
                                        on_click=SearchState.load_tracks,
                                        is_loading=SearchState.loading,
                                    ),
                                    spacing="3",
                                    align_items="center",
                                    width="100%",
                                ),
                                rx.hstack(
                                    rx.input(
                                        placeholder="Track ID",
                                        width="12em",
                                        value=SearchState.track_id,
                                        on_change=SearchState.set_track_id,
                                    ),
                                    rx.button(
                                        "Load Track",
                                        variant="outline",
                                        on_click=SearchState.load_track(AuthState.access_token),
                                        is_loading=SearchState.loading,
                                    ),
                                    spacing="3",
                                    align_items="center",
                                    width="100%",
                                ),
                                rx.cond(
                                    SearchState.selected_track,
                                    rx.box(
                                        rx.vstack(
                                            rx.heading("Track Detail", size="3"),
                                            _ro_field(
                                                "ID",
                                                rx.cond(
                                                    SearchState.selected_track.id,
                                                    SearchState.selected_track.id.to(str),
                                                    "",
                                                ),
                                            ),
                                            _ro_field("MBID", rx.cond(SearchState.selected_track.mbid, SearchState.selected_track.mbid, "")),
                                            _ro_field("Title", rx.cond(SearchState.selected_track.title, SearchState.selected_track.title, "")),
                                            rx.text("Edit View (read-only)", size="2", color="gray"),
                                            _ro_field("ID", SearchState.selected_track.id.to(str)),
                                            _ro_field("MBID", rx.cond(SearchState.selected_track.mbid, SearchState.selected_track.mbid, "")),
                                            _ro_field("Title", rx.cond(SearchState.selected_track.title, SearchState.selected_track.title, "")),
                                            spacing="2",
                                            width="100%",
                                            align_items="start",
                                        ),
                                        border=_CARD_BORDER,
                                        border_radius="10px",
                                        padding="1em",
                                        width="100%",
                                    ),
                                ),
                                rx.cond(
                                    SearchState.loading,
                                    rx.text("Loading...", color="gray"),
                                    rx.foreach(SearchState.tracks, _track_row),
                                ),
                                spacing="3",
                                width="100%",
                                align_items="start",
                            ),
                            border=_CARD_BORDER,
                            border_radius="12px",
                            padding="1em",
                            width="100%",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.heading(f"Albums ({SearchState.albums_total})", size="4"),
                                    rx.spacer(),
                                    rx.text("Limit", size="2", color="gray"),
                                    rx.input(
                                        width="6em",
                                        value=SearchState.albums_limit,
                                        on_change=SearchState.set_albums_limit,
                                    ),
                                    rx.text("Offset", size="2", color="gray"),
                                    rx.input(
                                        width="6em",
                                        value=SearchState.albums_offset,
                                        on_change=SearchState.set_albums_offset,
                                    ),
                                    rx.button(
                                        "Search",
                                        on_click=SearchState.load_albums,
                                        is_loading=SearchState.loading,
                                    ),
                                    spacing="3",
                                    align_items="center",
                                    width="100%",
                                ),
                                rx.hstack(
                                    rx.input(
                                        placeholder="Album ID",
                                        width="12em",
                                        value=SearchState.album_id,
                                        on_change=SearchState.set_album_id,
                                    ),
                                    rx.button(
                                        "Load Album",
                                        variant="outline",
                                        on_click=SearchState.load_album(AuthState.access_token),
                                        is_loading=SearchState.loading,
                                    ),
                                    spacing="3",
                                    align_items="center",
                                    width="100%",
                                ),
                                rx.cond(
                                    SearchState.selected_album,
                                    rx.box(
                                        rx.vstack(
                                            rx.heading("Album Detail", size="3"),
                                            _ro_field("ID", SearchState.selected_album.id.to(str)),
                                            _ro_field("Title", rx.cond(SearchState.selected_album.title, SearchState.selected_album.title, "")),
                                            rx.text("Edit View (read-only)", size="2", color="gray"),
                                            _ro_field("ID", SearchState.selected_album.id.to(str)),
                                            _ro_field("Title", rx.cond(SearchState.selected_album.title, SearchState.selected_album.title, "")),
                                            spacing="2",
                                            width="100%",
                                            align_items="start",
                                        ),
                                        border=_CARD_BORDER,
                                        border_radius="10px",
                                        padding="1em",
                                        width="100%",
                                    ),
                                ),
                                rx.cond(
                                    SearchState.loading,
                                    rx.text("Loading...", color="gray"),
                                    rx.foreach(SearchState.albums, _album_row),
                                ),
                                spacing="3",
                                width="100%",
                                align_items="start",
                            ),
                            border=_CARD_BORDER,
                            border_radius="12px",
                            padding="1em",
                            width="100%",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.heading(f"Persons ({SearchState.persons_total})", size="4"),
                                    rx.spacer(),
                                    rx.text("Limit", size="2", color="gray"),
                                    rx.input(
                                        width="6em",
                                        value=SearchState.persons_limit,
                                        on_change=SearchState.set_persons_limit,
                                    ),
                                    rx.text("Offset", size="2", color="gray"),
                                    rx.input(
                                        width="6em",
                                        value=SearchState.persons_offset,
                                        on_change=SearchState.set_persons_offset,
                                    ),
                                    rx.button(
                                        "Search",
                                        on_click=SearchState.load_persons,
                                        is_loading=SearchState.loading,
                                    ),
                                    spacing="3",
                                    align_items="center",
                                    width="100%",
                                ),
                                rx.hstack(
                                    rx.input(
                                        placeholder="Person ID",
                                        width="12em",
                                        value=SearchState.person_id,
                                        on_change=SearchState.set_person_id,
                                    ),
                                    rx.button(
                                        "Load Person",
                                        variant="outline",
                                        on_click=SearchState.load_person(AuthState.access_token),
                                        is_loading=SearchState.loading,
                                    ),
                                    spacing="3",
                                    align_items="center",
                                    width="100%",
                                ),
                                rx.cond(
                                    SearchState.selected_person,
                                    rx.box(
                                        rx.vstack(
                                            rx.heading("Person Detail", size="3"),
                                            _ro_field("ID", SearchState.selected_person.id.to(str)),
                                            _ro_field("Full Name", rx.cond(SearchState.selected_person.full_name, SearchState.selected_person.full_name, "")),
                                            rx.text("Edit View (read-only)", size="2", color="gray"),
                                            _ro_field("ID", SearchState.selected_person.id.to(str)),
                                            _ro_field("Full Name", rx.cond(SearchState.selected_person.full_name, SearchState.selected_person.full_name, "")),
                                            spacing="2",
                                            width="100%",
                                            align_items="start",
                                        ),
                                        border=_CARD_BORDER,
                                        border_radius="10px",
                                        padding="1em",
                                        width="100%",
                                    ),
                                ),
                                rx.cond(
                                    SearchState.loading,
                                    rx.text("Loading...", color="gray"),
                                    rx.foreach(SearchState.persons, _person_row),
                                ),
                                spacing="3",
                                width="100%",
                                align_items="start",
                            ),
                            border=_CARD_BORDER,
                            border_radius="12px",
                            padding="1em",
                            width="100%",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.heading(f"Labels ({SearchState.labels_total})", size="4"),
                                    rx.spacer(),
                                    rx.text("Limit", size="2", color="gray"),
                                    rx.input(
                                        width="6em",
                                        value=SearchState.labels_limit,
                                        on_change=SearchState.set_labels_limit,
                                    ),
                                    rx.text("Offset", size="2", color="gray"),
                                    rx.input(
                                        width="6em",
                                        value=SearchState.labels_offset,
                                        on_change=SearchState.set_labels_offset,
                                    ),
                                    rx.button(
                                        "Search",
                                        on_click=SearchState.load_labels,
                                        is_loading=SearchState.loading,
                                    ),
                                    spacing="3",
                                    align_items="center",
                                    width="100%",
                                ),
                                rx.hstack(
                                    rx.input(
                                        placeholder="Label ID",
                                        width="12em",
                                        value=SearchState.label_id,
                                        on_change=SearchState.set_label_id,
                                    ),
                                    rx.button(
                                        "Load Label",
                                        variant="outline",
                                        on_click=SearchState.load_label(AuthState.access_token),
                                        is_loading=SearchState.loading,
                                    ),
                                    spacing="3",
                                    align_items="center",
                                    width="100%",
                                ),
                                rx.cond(
                                    SearchState.selected_label,
                                    rx.box(
                                        rx.vstack(
                                            rx.heading("Label Detail", size="3"),
                                            _ro_field("ID", SearchState.selected_label.id.to(str)),
                                            _ro_field("Name", rx.cond(SearchState.selected_label.name, SearchState.selected_label.name, "")),
                                            rx.text("Edit View (read-only)", size="2", color="gray"),
                                            _ro_field("ID", SearchState.selected_label.id.to(str)),
                                            _ro_field("Name", rx.cond(SearchState.selected_label.name, SearchState.selected_label.name, "")),
                                            spacing="2",
                                            width="100%",
                                            align_items="start",
                                        ),
                                        border=_CARD_BORDER,
                                        border_radius="10px",
                                        padding="1em",
                                        width="100%",
                                    ),
                                ),
                                rx.cond(
                                    SearchState.loading,
                                    rx.text("Loading...", color="gray"),
                                    rx.foreach(SearchState.labels, _label_row),
                                ),
                                spacing="3",
                                width="100%",
                                align_items="start",
                            ),
                            border=_CARD_BORDER,
                            border_radius="12px",
                            padding="1em",
                            width="100%",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.heading("Playlists (auth)", size="4"),
                                    rx.spacer(),
                                    rx.button(
                                        "Load Playlists",
                                        on_click=SearchState.load_playlists(AuthState.access_token),
                                        is_loading=SearchState.loading,
                                    ),
                                    spacing="3",
                                    align_items="center",
                                    width="100%",
                                ),
                                rx.cond(
                                    AuthState.is_authenticated,
                                    rx.text("Using your session token.", size="2", color="gray"),
                                    rx.text("Not signed in. Auth-only sections will fail.", size="2", color="gray"),
                                ),
                                rx.foreach(
                                    SearchState.playlists,
                                    lambda pl: rx.box(
                                        rx.vstack(
                                            rx.text(f"#{pl.id}  {pl.name}", weight="medium"),
                                            _ro_field("Track IDs", rx.cond(pl.track_ids, pl.track_ids.to(str), "[]")),
                                            spacing="2",
                                            width="100%",
                                            align_items="start",
                                        ),
                                        border=_CARD_BORDER,
                                        border_radius="10px",
                                        padding="0.75em",
                                        width="100%",
                                    ),
                                ),
                                spacing="3",
                                width="100%",
                                align_items="start",
                            ),
                            border=_CARD_BORDER,
                            border_radius="12px",
                            padding="1em",
                            width="100%",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.heading("Queue (auth)", size="4"),
                                    rx.spacer(),
                                    rx.button(
                                        "Load Queue",
                                        on_click=SearchState.load_queue(AuthState.access_token),
                                        is_loading=SearchState.loading,
                                    ),
                                    spacing="3",
                                    align_items="center",
                                    width="100%",
                                ),
                                _ro_field(
                                    "Track IDs",
                                    rx.cond(SearchState.queue.track_ids, SearchState.queue.track_ids.to(str), "[]"),
                                ),
                                spacing="3",
                                width="100%",
                                align_items="start",
                            ),
                            border=_CARD_BORDER,
                            border_radius="12px",
                            padding="1em",
                            width="100%",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.heading("Task Display", size="4"),
                                    rx.spacer(),
                                    rx.button(
                                        "Refresh",
                                        on_click=SearchState.load_task_display(AuthState.access_token),
                                        is_loading=SearchState.loading,
                                    ),
                                    spacing="3",
                                    align_items="center",
                                    width="100%",
                                ),
                                rx.foreach(
                                    SearchState.task_display,
                                    lambda task: rx.box(
                                        rx.vstack(
                                            _ro_field("Task ID", rx.cond(task.task_id, task.task_id, "")),
                                            _ro_field("Type", rx.cond(task.task_type, task.task_type, "")),
                                            _ro_field("Progress", rx.cond(task.progress, task.progress.to(str), "0")),
                                            _ro_field("Start Time", rx.cond(task.start_time, task.start_time, "")),
                                            _ro_field("Status", rx.cond(task.status, task.status, "")),
                                            spacing="2",
                                            width="100%",
                                            align_items="start",
                                        ),
                                        border=_CARD_BORDER,
                                        border_radius="10px",
                                        padding="0.75em",
                                        width="100%",
                                    ),
                                ),
                                spacing="3",
                                width="100%",
                                align_items="start",
                            ),
                            border=_CARD_BORDER,
                            border_radius="12px",
                            padding="1em",
                            width="100%",
                        ),
                        spacing="4",
                    ),
                    padding="1em 0 2em",
                ),
                footer(),
                spacing="4",
            )
        ),
    )
