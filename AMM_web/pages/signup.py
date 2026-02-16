"""Login page of the application."""

import reflex as rx

from ..components import footer, navbar, player_shell


def signup() -> rx.Component:
    """About page of the application
    Returns:
        rx.Component: about page
    """
    return rx.container(
        rx.color_mode.button(position="bottom-left"),
        player_shell(
            rx.vstack(
                navbar(),
                rx.container(),
                footer(),
            )
        ),
    )
