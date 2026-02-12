"""Login page of the application."""

import reflex as rx

from ..auth_state import AuthState
from ..components import footer, google_sign_in_button, navbar, player_shell


def login() -> rx.Component:
    """About page of the application
    Returns:
        rx.Component: about page
    """
    return rx.container(
        rx.color_mode.button(position="bottom-left"),
        player_shell(
            rx.vstack(
                navbar(),
                rx.center(
                    rx.vstack(
                        rx.heading("Sign in"),
                        rx.button(
                            "Complete Google Sign In",
                            id="google_signin_submit",
                            on_click=AuthState.submit_google_login,
                            display="none",
                        ),
                        google_sign_in_button(submit_button_id="google_signin_submit"),
                        rx.cond(
                            AuthState.login_error != "",
                            rx.text(AuthState.login_error, color="red"),
                        ),
                        spacing="4",
                    ),
                    padding="4em 0",
                ),
                footer(),
            )
        ),
    )
