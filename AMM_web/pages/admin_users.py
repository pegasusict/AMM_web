"""Admin users management page."""

import reflex as rx

from ..auth_state import AuthState
from ..components import admin_gate, footer, navbar, player_shell
from ..state.admin_users_state import AdminUsersState


def _user_row(user) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text("#", user.id.to_string(), weight="medium"),
                rx.text(rx.cond(user.username, user.username, "(no username)"), weight="bold"),
                rx.badge(rx.cond(user.role, user.role, "USER")),
                rx.badge(
                    rx.cond(user.is_active, "Active", "Inactive"),
                    color_scheme=rx.cond(user.is_active, "green", "gray"),
                ),
                spacing="3",
                align_items="center",
            ),
            rx.text(rx.cond(user.email, user.email, ""), color="gray"),
            rx.hstack(
                rx.button(
                    "Make Admin",
                    size="2",
                    variant="outline",
                    on_click=AdminUsersState.set_user_role(
                        user.id,
                        "ADMIN",
                        AuthState.access_token,
                        AuthState.is_admin,
                    ),
                ),
                rx.button(
                    "Make User",
                    size="2",
                    variant="outline",
                    on_click=AdminUsersState.set_user_role(
                        user.id,
                        "USER",
                        AuthState.access_token,
                        AuthState.is_admin,
                    ),
                ),
                rx.button(
                    "Activate",
                    size="2",
                    variant="outline",
                    on_click=AdminUsersState.set_user_active(
                        user.id,
                        True,
                        AuthState.access_token,
                        AuthState.is_admin,
                    ),
                ),
                rx.button(
                    "Deactivate",
                    size="2",
                    variant="outline",
                    on_click=AdminUsersState.set_user_active(
                        user.id,
                        False,
                        AuthState.access_token,
                        AuthState.is_admin,
                    ),
                ),
                rx.button(
                    "Delete",
                    size="2",
                    color_scheme="red",
                    variant="outline",
                    on_click=AdminUsersState.delete_user(
                        user.id,
                        AuthState.access_token,
                        AuthState.is_admin,
                    ),
                ),
                spacing="2",
            ),
            spacing="2",
            width="100%",
        ),
        border="1px solid #E2E8F0",
        border_radius="10px",
        padding="0.75em",
        width="100%",
    )


def admin_users() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="bottom-left"),
        player_shell(
            rx.vstack(
                navbar(),
                admin_gate(
                    rx.vstack(
                        rx.hstack(
                            rx.heading("Admin: User Management", size="5"),
                            rx.button(
                                "Refresh",
                                on_click=AdminUsersState.load_users(
                                    AuthState.access_token,
                                    AuthState.is_admin,
                                ),
                            ),
                            spacing="4",
                            align_items="center",
                        ),
                        rx.cond(AdminUsersState.error, rx.text(AdminUsersState.error, color="red")),
                        rx.cond(AdminUsersState.auth_error, rx.text(AdminUsersState.auth_error, color="red")),
                        rx.cond(
                            AdminUsersState.success_message,
                            rx.text(AdminUsersState.success_message, color="green"),
                        ),
                        rx.box(
                            rx.vstack(
                                rx.heading("Create User", size="4"),
                                rx.input(
                                    placeholder="Username",
                                    value=AdminUsersState.new_username,
                                    on_change=AdminUsersState.set_new_username,
                                ),
                                rx.input(
                                    placeholder="Email",
                                    value=AdminUsersState.new_email,
                                    on_change=AdminUsersState.set_new_email,
                                ),
                                rx.input(
                                    placeholder="Password Hash",
                                    value=AdminUsersState.new_password_hash,
                                    on_change=AdminUsersState.set_new_password_hash,
                                ),
                                rx.select(
                                    ["USER", "ADMIN"],
                                    value=AdminUsersState.new_role,
                                    on_change=AdminUsersState.set_new_role,
                                    width="12em",
                                ),
                                rx.hstack(
                                    rx.text("Active"),
                                    rx.switch(
                                        checked=AdminUsersState.new_is_active,
                                        on_change=AdminUsersState.set_new_is_active,
                                    ),
                                    spacing="2",
                                ),
                                rx.button(
                                    "Create User",
                                    on_click=AdminUsersState.create_user(
                                        AuthState.access_token,
                                        AuthState.is_admin,
                                    ),
                                    is_loading=AdminUsersState.loading,
                                ),
                                spacing="3",
                                width="100%",
                                align_items="start",
                            ),
                            border="1px solid #E2E8F0",
                            border_radius="10px",
                            padding="1em",
                            width="100%",
                        ),
                        rx.vstack(
                            rx.hstack(
                                rx.heading(f"Users ({AdminUsersState.total_users})", size="4"),
                                spacing="3",
                            ),
                            rx.cond(
                                AdminUsersState.loading,
                                rx.text("Loading users..."),
                                rx.foreach(AdminUsersState.users, _user_row),
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        spacing="4",
                        padding="1em 0 2em",
                        width="100%",
                    )
                ),
                footer(),
                width="100%",
            )
        ),
    )
