"""Structured library search page (no ad-hoc GraphQL queries)."""

import reflex as rx

from ..auth_state import AuthState
from ..components import footer, navbar, player_shell
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
    title = track.title or ""
    mbid = track.mbid or ""
    label = f"#{track.id}  {title}".strip() if track.id else "(unknown track)"
    meta = mbid if mbid else "(no mbid)"
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(label, weight="medium"),
                rx.spacer(),
                rx.button(
                    "View",
                    size="2",
                    variant="outline",
                    on_click=[
                        SearchState.select_track(track.id or 0),
                        SearchState.load_track(AuthState.access_token),
                    ],
                    is_disabled=(track.id is None),
                ),
                spacing="3",
                align_items="center",
                width="100%",
            ),
            rx.text(meta, size="2", color="gray"),
            spacing="1",
            width="100%",
        ),
        border=_CARD_BORDER,
        border_radius="10px",
        padding="0.75em",
        width="100%",
    )


def _album_row(album) -> rx.Component:
    title = album.title or "(untitled)"
    label = f"#{album.id}  {title}".strip() if album.id else "(unknown album)"
    return rx.box(
        rx.hstack(
            rx.text(label, weight="medium"),
            rx.spacer(),
            rx.button(
                "View",
                size="2",
                variant="outline",
                on_click=[
                    SearchState.select_album(album.id or 0),
                    SearchState.load_album(AuthState.access_token),
                ],
                is_disabled=(album.id is None),
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
    name = person.full_name or "(no name)"
    label = f"#{person.id}  {name}".strip() if person.id else "(unknown person)"
    return rx.box(
        rx.hstack(
            rx.text(label, weight="medium"),
            rx.spacer(),
            rx.button(
                "View",
                size="2",
                variant="outline",
                on_click=[
                    SearchState.select_person(person.id or 0),
                    SearchState.load_person(AuthState.access_token),
                ],
                is_disabled=(person.id is None),
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
    name = label.name or "(no name)"
    title = f"#{label.id}  {name}".strip() if label.id else "(unknown label)"
    return rx.box(
        rx.hstack(
            rx.text(title, weight="medium"),
            rx.spacer(),
            rx.button(
                "View",
                size="2",
                variant="outline",
                on_click=[
                    SearchState.select_label(label.id or 0),
                    SearchState.load_label(AuthState.access_token),
                ],
                is_disabled=(label.id is None),
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
                                            _ro_field("MBID", SearchState.selected_track.mbid or ""),
                                            _ro_field("Title", SearchState.selected_track.title or ""),
                                            rx.text("Edit View (read-only)", size="2", color="gray"),
                                            _ro_field("ID", SearchState.selected_track.id.to(str)),
                                            _ro_field("MBID", SearchState.selected_track.mbid or ""),
                                            _ro_field("Title", SearchState.selected_track.title or ""),
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
                                            _ro_field("Title", SearchState.selected_album.title or ""),
                                            rx.text("Edit View (read-only)", size="2", color="gray"),
                                            _ro_field("ID", SearchState.selected_album.id.to(str)),
                                            _ro_field("Title", SearchState.selected_album.title or ""),
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
                                            _ro_field("Full Name", SearchState.selected_person.full_name or ""),
                                            rx.text("Edit View (read-only)", size="2", color="gray"),
                                            _ro_field("ID", SearchState.selected_person.id.to(str)),
                                            _ro_field("Full Name", SearchState.selected_person.full_name or ""),
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
                                            _ro_field("Name", SearchState.selected_label.name or ""),
                                            rx.text("Edit View (read-only)", size="2", color="gray"),
                                            _ro_field("ID", SearchState.selected_label.id.to(str)),
                                            _ro_field("Name", SearchState.selected_label.name or ""),
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
                                            _ro_field("Track IDs", ", ".join([str(i) for i in (pl.track_ids or [])])),
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
                                    ", ".join([str(i) for i in (SearchState.queue.track_ids or [])]),
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
                                            _ro_field("Task ID", task.task_id or ""),
                                            _ro_field("Type", task.task_type or ""),
                                            _ro_field("Progress", (task.progress or 0).to(str)),
                                            _ro_field("Start Time", task.start_time or ""),
                                            _ro_field("Status", task.status or ""),
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
