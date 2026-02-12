"""Contact page of the application."""

import reflex as rx

# from states import ContactState

from ..components import footer, navbar, player_shell


def contact() -> rx.Component:
    """Contact page of the application
    Returns:
        rx.Component: contact page
    """
    return rx.container(
        rx.color_mode.button(position="bottom-left"),
        player_shell(
            rx.vstack(
                navbar(),
                rx.container(
                    rx.vstack(
                        rx.heading("Contact us", size="8"),
                        rx.text(
                            "If you have any questions or feedback,"
                            " please feel free to reach out to us."
                        ),
                    ),
                ),
                footer(),
            )
        ),
    )
