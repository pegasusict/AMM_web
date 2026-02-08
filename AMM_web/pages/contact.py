"""Contact page of the application."""

import reflex as rx

# from states import ContactState

from ..components import navbar, footer


def contact() -> rx.Component:
    """Contact page of the application
    Returns:
        rx.Component: contact page
    """
    return rx.container(
        rx.color_mode.button(position="bottom-left"),
        rx.vstack(
            navbar(),
            rx.container(
                rx.vstack(
                    rx.heading("Contact us", size="2xl"),
                    rx.text(
                        "If you have any questions or feedback,"
                        " please feel free to reach out to us."
                    ),
                ),
            ),
            footer(),
        ),
    )
