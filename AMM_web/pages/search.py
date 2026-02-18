"""Structured library search page (no ad-hoc GraphQL queries)."""

import reflex as rx

from ..auth_state import AuthState
from ..components import CARD_BORDER, auth_gate, entity_row, footer, navbar, player_shell, ro_field
from ..state.search_state import SearchState


def _panel(*children: rx.Component) -> rx.Component:
    return rx.box(
        rx.vstack(
            *children,
            spacing="3",
            width="100%",
            align_items="start",
        ),
        border=CARD_BORDER,
        border_radius="12px",
        padding="1em",
        width="100%",
    )


def _pager_row(
    heading: rx.Var | str,
    limit_value: rx.Var,
    limit_setter,
    offset_value: rx.Var,
    offset_setter,
    on_search,
) -> rx.Component:
    return rx.hstack(
        rx.heading(heading, size="4"),
        rx.spacer(),
        rx.text("Limit", size="2", color="gray"),
        rx.input(width="6em", value=limit_value, on_change=limit_setter),
        rx.text("Offset", size="2", color="gray"),
        rx.input(width="6em", value=offset_value, on_change=offset_setter),
        rx.button("Search", on_click=on_search, is_loading=SearchState.loading),
        spacing="3",
        align_items="center",
        width="100%",
    )


def _load_row(placeholder: str, value: rx.Var, setter, on_load) -> rx.Component:
    return rx.hstack(
        rx.input(placeholder=placeholder, width="12em", value=value, on_change=setter),
        rx.button("Load", variant="outline", on_click=on_load, is_loading=SearchState.loading),
        spacing="3",
        align_items="center",
        width="100%",
    )


def _selected_card(title: str, fields: list[tuple[str, rx.Var]]) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading(title, size="3"),
            *[ro_field(label, value) for label, value in fields],
            spacing="2",
            width="100%",
            align_items="start",
        ),
        border=CARD_BORDER,
        border_radius="10px",
        padding="0.75em",
        width="100%",
    )


def _track_panel() -> rx.Component:
    return _panel(
        _pager_row(
            heading=f"Tracks ({SearchState.tracks_total})",
            limit_value=SearchState.tracks_limit,
            limit_setter=SearchState.set_tracks_limit,
            offset_value=SearchState.tracks_offset,
            offset_setter=SearchState.set_tracks_offset,
            on_search=SearchState.load_tracks,
        ),
        _load_row(
            placeholder="Track ID",
            value=SearchState.track_id,
            setter=SearchState.set_track_id,
            on_load=SearchState.load_track(AuthState.access_token),
        ),
        rx.cond(
            SearchState.loading,
            rx.text("Loading...", color="gray"),
            rx.foreach(
                SearchState.tracks,
                lambda t: entity_row(
                    entity_id=t.id,
                    title=rx.cond(t.title, t.title, "(untitled)"),
                    route_prefix="tracks",
                ),
            ),
        ),
        rx.cond(
            SearchState.selected_track,
            _selected_card(
                "Selected Track",
                [
                    ("ID", rx.cond(SearchState.selected_track.id, SearchState.selected_track.id.to(str), "")),
                    ("MBID", rx.cond(SearchState.selected_track.mbid, SearchState.selected_track.mbid, "")),
                    (
                        "Composed",
                        rx.cond(SearchState.selected_track.composed, SearchState.selected_track.composed.to(str), ""),
                    ),
                    (
                        "Release Date",
                        rx.cond(
                            SearchState.selected_track.release_date,
                            SearchState.selected_track.release_date.to(str),
                            "",
                        ),
                    ),
                    ("Key ID", rx.cond(SearchState.selected_track.key_id, SearchState.selected_track.key_id.to(str), "")),
                    (
                        "Lyric ID",
                        rx.cond(SearchState.selected_track.lyric_id, SearchState.selected_track.lyric_id.to(str), ""),
                    ),
                    (
                        "File IDs",
                        rx.cond(SearchState.selected_track.file_ids, SearchState.selected_track.file_ids.to(str), "[]"),
                    ),
                    (
                        "Album Track IDs",
                        rx.cond(
                            SearchState.selected_track.album_track_ids,
                            SearchState.selected_track.album_track_ids.to(str),
                            "[]",
                        ),
                    ),
                    (
                        "Genre IDs",
                        rx.cond(SearchState.selected_track.genre_ids, SearchState.selected_track.genre_ids.to(str), "[]"),
                    ),
                    ("Task IDs", rx.cond(SearchState.selected_track.task_ids, SearchState.selected_track.task_ids.to(str), "[]")),
                ],
            ),
            rx.fragment(),
        ),
    )


def _album_panel() -> rx.Component:
    return _panel(
        _pager_row(
            heading=f"Albums ({SearchState.albums_total})",
            limit_value=SearchState.albums_limit,
            limit_setter=SearchState.set_albums_limit,
            offset_value=SearchState.albums_offset,
            offset_setter=SearchState.set_albums_offset,
            on_search=SearchState.load_albums,
        ),
        _load_row(
            placeholder="Album ID",
            value=SearchState.album_id,
            setter=SearchState.set_album_id,
            on_load=SearchState.load_album(AuthState.access_token),
        ),
        rx.cond(
            SearchState.loading,
            rx.text("Loading...", color="gray"),
            rx.foreach(
                SearchState.albums,
                lambda a: entity_row(
                    entity_id=a.id,
                    title=rx.cond(a.title, a.title, "(untitled)"),
                    route_prefix="albums",
                ),
            ),
        ),
        rx.cond(
            SearchState.selected_album,
            _selected_card(
                "Selected Album",
                [
                    ("ID", rx.cond(SearchState.selected_album.id, SearchState.selected_album.id.to(str), "")),
                    ("Title", rx.cond(SearchState.selected_album.title, SearchState.selected_album.title, "")),
                    ("MBID", rx.cond(SearchState.selected_album.mbid, SearchState.selected_album.mbid, "")),
                    ("Subtitle", rx.cond(SearchState.selected_album.subtitle, SearchState.selected_album.subtitle, "")),
                    (
                        "Release Date",
                        rx.cond(
                            SearchState.selected_album.release_date,
                            SearchState.selected_album.release_date.to(str),
                            "",
                        ),
                    ),
                    (
                        "Release Country",
                        rx.cond(SearchState.selected_album.release_country, SearchState.selected_album.release_country, ""),
                    ),
                    (
                        "Disc Count",
                        rx.cond(SearchState.selected_album.disc_count, SearchState.selected_album.disc_count.to(str), ""),
                    ),
                    (
                        "Track Count",
                        rx.cond(SearchState.selected_album.track_count, SearchState.selected_album.track_count.to(str), ""),
                    ),
                    (
                        "Label ID",
                        rx.cond(SearchState.selected_album.label_id, SearchState.selected_album.label_id.to(str), ""),
                    ),
                    (
                        "Album Track IDs",
                        rx.cond(
                            SearchState.selected_album.album_track_ids,
                            SearchState.selected_album.album_track_ids.to(str),
                            "[]",
                        ),
                    ),
                    (
                        "Genre IDs",
                        rx.cond(SearchState.selected_album.genre_ids, SearchState.selected_album.genre_ids.to(str), "[]"),
                    ),
                ],
            ),
            rx.fragment(),
        ),
    )


def _person_panel() -> rx.Component:
    return _panel(
        _pager_row(
            heading=f"Persons ({SearchState.persons_total})",
            limit_value=SearchState.persons_limit,
            limit_setter=SearchState.set_persons_limit,
            offset_value=SearchState.persons_offset,
            offset_setter=SearchState.set_persons_offset,
            on_search=SearchState.load_persons,
        ),
        _load_row(
            placeholder="Person ID",
            value=SearchState.person_id,
            setter=SearchState.set_person_id,
            on_load=SearchState.load_person(AuthState.access_token),
        ),
        rx.cond(
            SearchState.loading,
            rx.text("Loading...", color="gray"),
            rx.foreach(
                SearchState.persons,
                lambda p: entity_row(
                    entity_id=p.id,
                    title=rx.cond(p.title, p.title, "(untitled)"),
                    route_prefix="persons",
                ),
            ),
        ),
        rx.cond(
            SearchState.selected_person,
            _selected_card(
                "Selected Person",
                [
                    ("ID", rx.cond(SearchState.selected_person.id, SearchState.selected_person.id.to(str), "")),
                    (
                        "Full Name",
                        rx.cond(SearchState.selected_person.full_name, SearchState.selected_person.full_name, ""),
                    ),
                    (
                        "First Name",
                        rx.cond(SearchState.selected_person.first_name, SearchState.selected_person.first_name, ""),
                    ),
                    (
                        "Last Name",
                        rx.cond(SearchState.selected_person.last_name, SearchState.selected_person.last_name, ""),
                    ),
                    ("MBID", rx.cond(SearchState.selected_person.mbid, SearchState.selected_person.mbid, "")),
                    (
                        "Date of Birth",
                        rx.cond(
                            SearchState.selected_person.date_of_birth,
                            SearchState.selected_person.date_of_birth.to(str),
                            "",
                        ),
                    ),
                    (
                        "Date of Death",
                        rx.cond(
                            SearchState.selected_person.date_of_death,
                            SearchState.selected_person.date_of_death.to(str),
                            "",
                        ),
                    ),
                    (
                        "Task IDs",
                        rx.cond(SearchState.selected_person.task_ids, SearchState.selected_person.task_ids.to(str), "[]"),
                    ),
                    (
                        "Label IDs",
                        rx.cond(SearchState.selected_person.label_ids, SearchState.selected_person.label_ids.to(str), "[]"),
                    ),
                ],
            ),
            rx.fragment(),
        ),
    )


def _label_panel() -> rx.Component:
    return _panel(
        _pager_row(
            heading=f"Labels ({SearchState.labels_total})",
            limit_value=SearchState.labels_limit,
            limit_setter=SearchState.set_labels_limit,
            offset_value=SearchState.labels_offset,
            offset_setter=SearchState.set_labels_offset,
            on_search=SearchState.load_labels,
        ),
        _load_row(
            placeholder="Label ID",
            value=SearchState.label_id,
            setter=SearchState.set_label_id,
            on_load=SearchState.load_label(AuthState.access_token),
        ),
        rx.cond(
            SearchState.loading,
            rx.text("Loading...", color="gray"),
            rx.foreach(
                SearchState.labels,
                lambda l: entity_row(
                    entity_id=l.id,
                    title=rx.cond(l.title, l.title, "(untitled)"),
                    route_prefix="labels",
                ),
            ),
        ),
        rx.cond(
            SearchState.selected_label,
            _selected_card(
                "Selected Label",
                [
                    ("ID", rx.cond(SearchState.selected_label.id, SearchState.selected_label.id.to(str), "")),
                    ("Name", rx.cond(SearchState.selected_label.name, SearchState.selected_label.name, "")),
                    ("MBID", rx.cond(SearchState.selected_label.mbid, SearchState.selected_label.mbid, "")),
                    (
                        "Description",
                        rx.cond(SearchState.selected_label.description, SearchState.selected_label.description, ""),
                    ),
                    (
                        "Founded",
                        rx.cond(SearchState.selected_label.founded, SearchState.selected_label.founded.to(str), ""),
                    ),
                    (
                        "Defunct",
                        rx.cond(SearchState.selected_label.defunct, SearchState.selected_label.defunct.to(str), ""),
                    ),
                    (
                        "Owner ID",
                        rx.cond(SearchState.selected_label.owner_id, SearchState.selected_label.owner_id.to(str), ""),
                    ),
                    (
                        "Parent ID",
                        rx.cond(SearchState.selected_label.parent_id, SearchState.selected_label.parent_id.to(str), ""),
                    ),
                    (
                        "Child IDs",
                        rx.cond(SearchState.selected_label.child_ids, SearchState.selected_label.child_ids.to(str), "[]"),
                    ),
                    (
                        "Album IDs",
                        rx.cond(SearchState.selected_label.album_ids, SearchState.selected_label.album_ids.to(str), "[]"),
                    ),
                ],
            ),
            rx.fragment(),
        ),
    )


def _playlists_panel() -> rx.Component:
    return _panel(
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
                    ro_field("User ID", rx.cond(pl.user_id, pl.user_id.to(str), "")),
                    ro_field("Playlist Track IDs", rx.cond(pl.playlist_track_ids, pl.playlist_track_ids.to(str), "[]")),
                    ro_field("Track IDs", rx.cond(pl.track_ids, pl.track_ids.to(str), "[]")),
                    spacing="2",
                    width="100%",
                    align_items="start",
                ),
                border=CARD_BORDER,
                border_radius="10px",
                padding="0.75em",
                width="100%",
            ),
        ),
    )


def _queue_panel() -> rx.Component:
    return _panel(
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
        ro_field("Queue ID", rx.cond(SearchState.queue.id, SearchState.queue.id.to(str), "")),
        ro_field("User ID", rx.cond(SearchState.queue.user_id, SearchState.queue.user_id.to(str), "")),
        ro_field("Track IDs", rx.cond(SearchState.queue.track_ids, SearchState.queue.track_ids.to(str), "[]")),
    )


def _task_display_panel() -> rx.Component:
    return _panel(
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
                    ro_field("Task ID", rx.cond(task.task_id, task.task_id, "")),
                    ro_field("Type", rx.cond(task.task_type, task.task_type, "")),
                    ro_field("Progress", rx.cond(task.progress, task.progress.to(str), "0")),
                    ro_field("Start Time", rx.cond(task.start_time, task.start_time, "")),
                    ro_field("Status", rx.cond(task.status, task.status, "")),
                    spacing="2",
                    width="100%",
                    align_items="start",
                ),
                border=CARD_BORDER,
                border_radius="10px",
                padding="0.75em",
                width="100%",
            ),
        ),
    )


def search() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="bottom-left"),
        player_shell(
            rx.vstack(
                navbar(),
                auth_gate(
                    rx.container(
                        rx.vstack(
                            rx.heading("Library Search", size="8"),
                            rx.text(
                                "Browse library entities with structured search forms. "
                                "Detail and edit views are displayed as read-only forms."
                            ),
                            rx.cond(SearchState.error, rx.text(SearchState.error, color="red")),
                            _track_panel(),
                            _album_panel(),
                            _person_panel(),
                            _label_panel(),
                            _playlists_panel(),
                            _queue_panel(),
                            _task_display_panel(),
                            spacing="4",
                        ),
                        padding="1em 0 2em",
                    ),
                ),
                footer(),
                spacing="4",
            )
        ),
    )
