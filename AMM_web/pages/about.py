"""About page of the application."""

import reflex as rx

# from states import State

from ..components import navbar, footer


def about() -> rx.Component:
    """About page of the application
    Returns:
        rx.Component: about page
    """
    return rx.container(
        rx.color_mode.button(position="bottom-left"),
        rx.hstack(
            navbar(),
            rx.container(
                rx.vstack(
                    rx.heading("About the AMM Web Application", size="2xl"),
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
                ),
                footer(),
            ),
        ),
    )
