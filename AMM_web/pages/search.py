"""GraphQL search page for executing queries against AMM_core."""

import reflex as rx

from ..auth_state import AuthState
from ..components import footer, navbar, player_shell
from ..state.search_state import SearchState

PRESET_OPTIONS = [
    "Tracks (list)",
    "Albums (list)",
    "Persons (list)",
    "Labels (list)",
    "Playlists (auth)",
    "Queue (auth)",
    "Task Display",
]


def search() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="bottom-left"),
        player_shell(
            rx.vstack(
                navbar(),
                rx.container(
                    rx.vstack(
                        rx.heading("GraphQL Search", size="8"),
                        rx.text(
                            "Run any GraphQL query against AMM_core. "
                            "Authenticated queries will use your session token."
                        ),
                        rx.hstack(
                            rx.select(
                                PRESET_OPTIONS,
                                placeholder="Choose a preset query",
                                value=SearchState.preset,
                                on_change=SearchState.load_preset,
                                width="18em",
                            ),
                            rx.button(
                                "Load Preset",
                                on_click=SearchState.load_preset(SearchState.preset),
                                variant="outline",
                            ),
                            spacing="3",
                            align_items="center",
                        ),
                        rx.text_area(
                            placeholder="Enter GraphQL query...",
                            value=SearchState.query,
                            on_change=SearchState.set_query,
                            height="12em",
                        ),
                        rx.text_area(
                            placeholder='Variables as JSON (e.g. {"limit": 25})',
                            value=SearchState.variables,
                            on_change=SearchState.set_variables,
                            height="6em",
                        ),
                        rx.hstack(
                            rx.button(
                                "Run Query",
                                on_click=SearchState.run_query(AuthState.access_token),
                                is_loading=SearchState.loading,
                            ),
                            rx.cond(
                                AuthState.is_authenticated,
                                rx.text("Using your session token."),
                                rx.text("Not signed in. Auth-only queries will fail."),
                            ),
                            spacing="4",
                            align_items="center",
                        ),
                        rx.cond(
                            SearchState.error,
                            rx.text(SearchState.error, color="red"),
                            rx.code_block(
                                rx.cond(
                                    SearchState.response,
                                    SearchState.response,
                                    "Response will appear here.",
                                ),
                                language="json",
                            ),
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
