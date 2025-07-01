"""About page of the application."""

import reflex as rx
from page_base import page_base


@page_base
def about() -> rx.Component:
    """About page of the application
    Returns:
        rx.Component: about page
    """
    return rx.container(
                rx.vstack(
                    rx.heading("About the AMM Web Application", size="2"),
                    rx.text(
                        "This is the about page of the AMM web application. "
                        "You can find more information about the application "
                        "and its features here."
                    ),
                    rx.text(
                        "The AMM web application is designed to provide users "
                        "with a seamless experience in managing their music. "
                        "It offers a variety of features and tools to help users."
                    ),
                )
    )