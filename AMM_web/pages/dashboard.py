"""Dashboard page of the application."""

import reflex as rx

from ..components import navbar, footer, auth_gate
from ..auth_state import AuthState
from .. import routes


def dashboard() -> rx.Component:
    """Dashboard page of the application
    Returns:
        rx.Component: dashboard page
    """
    return rx.container(
        rx.color_mode.button(position="bottom-left"),
        rx.vstack(
            navbar(),
            auth_gate(
                rx.center(
                    rx.hstack(
                        rx.button("Refresh Session", on_click=AuthState.request_google_refresh),
                        rx.button("Logout", on_click=AuthState.clear_auth),
                        spacing="4",
                    ),
                    padding="4em 0",
                )
            ),
            footer(),
        ),
    )
