"""Login page of the application."""

import reflex as rx

from ..components import navbar, footer


def signup() -> rx.Component:
    """About page of the application
    Returns:
        rx.Component: about page
    """
    return rx.container(
        rx.color_mode.button(position="bottom-left"),
        rx.hstack(
            navbar(),
            rx.container(),
            footer(),
        ),
    )
