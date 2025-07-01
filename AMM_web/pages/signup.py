"""Sign up page of the application."""

import reflex as rx
from page_base import page_base


@page_base
def signup() -> rx.Component:
    """Sign up page of the application
    Returns:
        rx.Component: sign up page
    """
    return rx.container(
        rx.vstack(
            rx.heading("Sign Up", size="2"),
            rx.text("Please enter your details to create an account."),
        )
    )
