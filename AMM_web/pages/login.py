"""Login page of the application."""

import reflex as rx
from page_base import page_base


@page_base
def login() -> rx.Component:
    """Login page of the application
    Returns:
        rx.Component: login page
    """
    return rx.container(
        rx.vstack(
            rx.heading("Login", size="2"),
            rx.text("Please enter your credentials to log in."),
        )
    )
