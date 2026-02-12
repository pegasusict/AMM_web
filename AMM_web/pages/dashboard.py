"""Dashboard page of the application."""

import reflex as rx

from ..auth_state import AuthState
from ..components import auth_gate, footer, navbar, player_shell
from ..routes import SEARCH_ROUTE
from ..state.library_state import LibraryState


def dashboard() -> rx.Component:
    """Dashboard page of the application
    Returns:
        rx.Component: dashboard page
    """
    return rx.container(
        rx.color_mode.button(position="bottom-left"),
        player_shell(
            rx.vstack(
                navbar(),
                auth_gate(
                    rx.vstack(
                        rx.center(
                            rx.hstack(
                                rx.button(
                                    "Refresh Session",
                                    on_click=AuthState.request_google_refresh,
                                ),
                                rx.button("Logout", on_click=AuthState.clear_auth),
                                spacing="4",
                            ),
                            padding="2em 0 1em",
                        ),
                        rx.hstack(
                            rx.heading("Library", size="5"),
                            rx.button(
                                "Refresh Library",
                                on_click=LibraryState.load_library(
                                    AuthState.access_token
                                ),
                            ),
                            rx.link(
                                rx.button("Open Search", variant="outline"),
                                href=SEARCH_ROUTE,
                            ),
                            spacing="4",
                            align_items="center",
                        ),
                        rx.cond(
                            LibraryState.loading,
                            rx.text("Loading library..."),
                            rx.cond(
                                LibraryState.error,
                                rx.text(LibraryState.error, color="red"),
                                rx.vstack(
                                    rx.vstack(
                                        rx.heading(
                                            f"Tracks ({LibraryState.total_tracks})",
                                            size="4",
                                        ),
                                        rx.foreach(
                                            LibraryState.tracks,
                                            lambda track: rx.text(
                                                rx.cond(
                                                    track.mbid,
                                                    track.mbid,
                                                    f"Track #{track.id}",
                                                )
                                            ),
                                        ),
                                        spacing="2",
                                    ),
                                    rx.vstack(
                                        rx.heading(
                                            f"Albums ({LibraryState.total_albums})",
                                            size="4",
                                        ),
                                        rx.foreach(
                                            LibraryState.albums,
                                            lambda album: rx.text(
                                                rx.cond(
                                                    album.title,
                                                    album.title,
                                                    "Untitled",
                                                )
                                            ),
                                        ),
                                        spacing="2",
                                    ),
                                    rx.vstack(
                                        rx.heading("Playlists", size="4"),
                                        rx.cond(
                                            LibraryState.auth_error,
                                            rx.text(
                                                "Sign in to view playlists and queue.",
                                                color="gray",
                                            ),
                                            rx.foreach(
                                                LibraryState.playlists,
                                                lambda pl: rx.text(pl.name),
                                            ),
                                        ),
                                        spacing="2",
                                    ),
                                    rx.vstack(
                                        rx.heading("Now Playing / Queue", size="4"),
                                        rx.cond(
                                            LibraryState.auth_error,
                                            rx.text(
                                                "Sign in to view now playing and queue.",
                                                color="gray",
                                            ),
                                            rx.vstack(
                                                rx.text(
                                                    rx.cond(
                                                        LibraryState.now_playing,
                                                        rx.cond(
                                                            LibraryState.now_playing.mbid,
                                                            LibraryState.now_playing.mbid,
                                                            "Nothing playing",
                                                        ),
                                                        "Nothing playing",
                                                    )
                                                ),
                                                rx.foreach(
                                                    LibraryState.queue.track_ids,
                                                    lambda track_id: rx.text(
                                                        f"Track ID: {track_id}"
                                                    ),
                                                ),
                                                spacing="2",
                                            ),
                                        ),
                                        spacing="2",
                                    ),
                                    spacing="4",
                                    padding_top="0.5em",
                                ),
                            ),
                        ),
                        spacing="4",
                        padding="1em 0 2em",
                        width="100%",
                    )
                ),
                footer(),
            )
        ),
    )
