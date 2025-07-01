"""Dashboard page of the application."""

import reflex as rx
from page_base import page_base


@page_base
def dashboard() -> rx.Component:
    """Dashboard page of the application
    Returns:
        rx.Component: dashboard page
    """
    return rx.container(
        rx.vstack(
            rx.heading("Dashboard", size="2"),
            rx.text("Welcome to the dashboard!"),
        )
    )
