"""Home page of the application."""

import reflex as rx
from page_base import page_base

@page_base
def index() -> rx.Component:
    """Home page of the application
    Returns:
        rx.Component: home page
    """
    return rx.container(
                rx.vstack(
                    rx.heading("Welcome to the AMM Web Application", size="2"),
                    rx.text(
                        "This is the home page of the AMM web application. "
                        "You can find more information about the application "
                        "and its features here."
                    ),
                ),
            )
