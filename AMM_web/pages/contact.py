"""Contact page of the application."""

import reflex as rx

from ..components import footer, navbar, player_shell
from ..states import ContactState


def contact() -> rx.Component:
    """Contact page of the application.

    Returns:
        rx.Component: contact page
    """
    return rx.container(
        rx.color_mode.button(position="bottom-left"),
        player_shell(
            rx.vstack(
                navbar(),
                rx.center(
                    rx.card(
                        rx.vstack(
                            rx.heading("Contact us", size="8"),
                            rx.text(
                                "If you have any questions or feedback, please send us a message."
                            ),
                            rx.input(
                                placeholder="Your name",
                                value=ContactState.name,
                                on_change=ContactState.set_name,
                            ),
                            rx.input(
                                placeholder="Your email",
                                type="email",
                                value=ContactState.email,
                                on_change=ContactState.set_email,
                            ),
                            rx.text_area(
                                placeholder="Your message",
                                min_height="160px",
                                value=ContactState.message,
                                on_change=ContactState.set_message,
                            ),
                            rx.button("Send message", on_click=ContactState.submit),
                            rx.cond(
                                ContactState.submitted,
                                rx.text(
                                    "Message sent. Thank you, we will get back to you soon.",
                                    color="green",
                                ),
                            ),
                            rx.cond(
                                ContactState.submit_error != "",
                                rx.text(ContactState.submit_error, color="red"),
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        width="100%",
                        max_width="640px",
                    ),
                    width="100%",
                    padding="2rem 1rem",
                ),
                footer(),
                width="100%",
            )
        ),
    )
