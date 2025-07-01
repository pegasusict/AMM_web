"""Contact page of the application."""

import reflex as rx
from page_base import page_base


@page_base
def contact() -> rx.Component:
    """Contact page of the application
    Returns:
        rx.Component: contact page
    """
    return rx.container(
        rx.vstack(
            rx.heading("Contact us", size="2"),
            rx.text("If you have any questions or feedback, please feel free to reach out to us."),
        ),
    )
