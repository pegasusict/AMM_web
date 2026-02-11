"""Admin users management page."""

import reflex as rx

from ..auth_state import AuthState
from ..components import admin_gate, footer, navbar, player_shell
from ..state.admin_users_state import AdminUsersState


def _user_row(user) -> rx.Component:
    current_role = (user.role or "USER").upper()
    target_role = "ADMIN" if current_role != "ADMIN" else "USER"
    role_button_label = "Make Admin" if target_role == "ADMIN" else "Make User"
    is_active = bool(user.is_active)

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(f"#{user.id}", weight="medium"),
                rx.text(user.username or "(no username)", weight="bold"),
                rx.badge(current_role),
                rx.badge("Active" if is_active else "Inactive", color_scheme="green" if is_active else "gray"),
                spacing="3",
                align_items="center",
            ),
            rx.text(user.email or "", color="gray"),
            rx.hstack(
                rx.button(
                    role_button_label,
                    size="2",
                    variant="outline",
                    on_click=AdminUsersState.set_user_role(
                        user.id or 0,
                        target_role,
                        AuthState.access_token,
                        AuthState.is_admin,
                    ),
                    is_disabled=(user.id is None),
                ),
                rx.button(
                    "Deactivate" if is_active else "Activate",
                    size="2",
                    variant="outline",
                    on_click=AdminUsersState.set_user_active(
                        user.id or 0,
                        not is_active,
                        AuthState.access_token,
                        AuthState.is_admin,
                    ),
                    is_disabled=(user.id is None),
                ),
                rx.button(
                    "Delete",
                    size="2",
                    color_scheme="red",
                    variant="outline",
                    on_click=AdminUsersState.delete_user(
                        user.id or 0,
                        AuthState.access_token,
                        AuthState.is_admin,
                    ),
                    is_disabled=(user.id is None),
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
