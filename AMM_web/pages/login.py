"""Login page of the application."""

import reflex as rx

from ..components import navbar, footer, google_sign_in_button
from ..auth_state import AuthState


def login() -> rx.Component:
    """About page of the application
    Returns:
        rx.Component: about page
    """
    return rx.container(
        rx.color_mode.button(position="bottom-left"),
        rx.vstack(
            navbar(),
            rx.center(
                rx.vstack(
                    rx.heading("Sign in"),
                    google_sign_in_button(),
                    rx.cond(
                        AuthState.login_error != "",
                        rx.text(AuthState.login_error, color="red"),
                    ),
                    spacing="4",
                ),
                padding="4em 0",
            ),
            footer(),
        ),
    )
