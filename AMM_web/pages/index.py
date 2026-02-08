"""Home page of the application."""

import reflex as rx

from ..components import navbar, footer


def index() -> rx.Component:
    """Home page of the application
    Returns:
        rx.Component: home page
    """
    return rx.container(
        rx.color_mode.button(position="bottom-left"),
        rx.hstack(
            navbar(),
            rx.container(
                rx.vstack(
                    rx.heading("Welcome to the AMM Web Application", size="2xl"),
                    rx.text(
                        "This is the home page of the AMM web application. "
                        "You can find more information about the application "
                        "and its features here."
                    ),
                ),
            ),
            footer(),
        ),
    )
