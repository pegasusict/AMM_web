"""Admin system page."""

import reflex as rx
from ..components import admin_gate, footer, navbar, player_shell

def admin_system() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="bottom-left"),
        player_shell(
            rx.vstack(
                navbar(),
                admin_gate(
                    rx.vstack(
                        rx.hstack(
                            rx.heading("Admin: User Management", size="5"),
                        ),
                        rx.text("System management features coming soon!"),
                        spacing="2",
                    ),
                ),
                footer(),
                spacing="2",
            ),
        ),
        border="1px solid #E2E8F0",
        border_radius="10px",
        padding="0.75em",
        width="100%",
    )