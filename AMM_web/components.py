"""custom reflex webpage components"""

from datetime import datetime
import os
from pathlib import Path

import reflex as rx

from AMM_web import routes
from AMM_web.auth_state import AuthState
from AMM_web.state.server_state import ServerState


def _read_env_value(key: str) -> str:
    """Read a config value from process env, with .env fallback."""
    value = os.getenv(key, "")
    if value:
        return value
    env_path = Path(".env")
    if not env_path.exists():
        return ""
    for line in env_path.read_text(encoding="utf-8").splitlines():
        entry = line.strip()
        if not entry or entry.startswith("#") or "=" not in entry:
            continue
        name, raw = entry.split("=", 1)
        if name.strip() == key:
            return raw.strip().strip("'\"")
    return ""


def navbar_logo() -> rx.Component:
    """Navbar logo element"""
    return rx.image(
        src="/logo.png",
        width="2.25em",
        height="auto",
        border_radius="25%",
    )


def navbar_title() -> rx.Component:
    """Navbar title element"""
    return rx.heading("AMM", size="7", weight="bold")


def navbar_link(text: str, url: str) -> rx.Component:
    """Navbar link element"""
    return rx.link(rx.text(text, size="4", weight="medium"), href=url)


def navbar() -> rx.Component:
    """Navigation bar for anonymous visitors

    Returns:
        rx.Component: Navbar component
    """
    return rx.box(
        rx.vstack(
            rx.desktop_only(
                rx.hstack(
                    rx.hstack(
                        navbar_logo(),
                        navbar_title(),
                        align_items="center",
                    ),
                    rx.hstack(
                        navbar_link("Home", routes.HOME_ROUTE),
                        # rx.menu.root(
                        #     rx.menu.trigger(
                        #         rx.button(
                        #             rx.text(
                        #                 "Services",
                        #                 size="4",
                        #                 weight="medium",
                        #             ),
                        #             rx.icon("chevron-down"),
                        #             weight="medium",
                        #             variant="ghost",
                        #             size="3",
                        #         ),
                        #     ),
                        #     rx.menu.content(
                        #         rx.menu.item("Service 1"),
                        #         rx.menu.item("Service 2"),
                        #         rx.menu.item("Service 3"),
                        #     ),
                        # ),
                        navbar_link("About", routes.ABOUT_ROUTE),
                        navbar_link("Contact", routes.CONTACT_ROUTE),
                        rx.cond(
                            AuthState.is_admin,
                            navbar_link("Admin", routes.ADMIN_USERS_ROUTE),
                            rx.fragment(),
                        ),
                        navbar_link("Login", routes.LOGIN_ROUTE),
                        navbar_link("Sign Up", routes.SIGNUP_ROUTE),
                        justify="end",
                        spacing="5",
                    ),
                    justify="between",
                    align_items="center",
                ),
            ),
            rx.mobile_and_tablet(
                rx.hstack(
                    rx.hstack(
                        navbar_logo(),
                        navbar_title(),
                        align_items="center",
                    ),
                    rx.menu.root(
                        rx.menu.trigger(rx.icon("menu", size=30)),
                        rx.menu.content(
                            rx.menu.item("Home"),
                            # rx.menu.sub(
                            #     rx.menu.sub_trigger("Services"),
                            #     rx.menu.sub_content(
                            #         rx.menu.item("Service 1"),
                            #         rx.menu.item("Service 2"),
                            #         rx.menu.item("Service 3"),
                            #     ),
                            # ),
                            rx.menu.item("About"),
                            rx.menu.item("Contact"),
                            rx.cond(
                                AuthState.is_admin,
                                rx.link("Admin", href=routes.ADMIN_USERS_ROUTE),
                                rx.fragment(),
                            ),
                        ),
                        justify="end",
                    ),
                    justify="between",
                    align_items="center",
                ),
            ),
            server_status_banner(),
            spacing="2",
            width="100%",
        ),
        padding="1em",
        width="100%",
    )


def server_status_banner() -> rx.Component:
    return rx.cond(
        ServerState.server_ok == True,
        rx.box(
            rx.text(ServerState.server_message, color="#14532D", size="2"),
            background="#DCFCE7",
            border="1px solid #86EFAC",
            border_radius="8px",
            padding="0.5em 0.75em",
            width="100%",
        ),
        rx.cond(
            ServerState.server_ok == False,
            rx.box(
                rx.text(ServerState.server_message, color="#7F1D1D", size="2"),
                background="#FEE2E2",
                border="1px solid #FCA5A5",
                border_radius="8px",
                padding="0.5em 0.75em",
                width="100%",
            ),
            rx.box(
                rx.text(ServerState.server_message, color="#78350F", size="2"),
                background="#FEF3C7",
                border="1px solid #FCD34D",
                border_radius="8px",
                padding="0.5em 0.75em",
                width="100%",
            ),
        ),
    )


def footer() -> rx.Component:
    """Footer for the webpage

    Returns:
        rx.Component: Footer component
    """
    return rx.box(
        rx.hstack(
            rx.text(f"© 2002-{datetime.now().year} Pegasus ICT"),
            rx.link("Privacy Policy", href=routes.PRIVACY_ROUTE),
            rx.link("Terms of Service", href=routes.TERMS_ROUTE),
            justify="end",
            spacing="5",
        ),
        padding="1em",
        width="100%",
    )


def google_sign_in_button(
    client_id: str | None = None,
    button_id: str = "google_signin_button",
    submit_button_id: str = "google_signin_submit",
) -> rx.Component:
    """Reusable Google Sign-In button using GIS."""
    client_id = client_id or _read_env_value("AMM_GOOGLE_CLIENT_ID")
    return rx.box(
        rx.box(id=button_id),
        rx.script(
            """
            window.addEventListener("google_id_token", (e) => {
              const token = e.detail;
              window.__amm_google_id_token = token;
              const submitButton = document.getElementById("%s");
              if (submitButton) {
                submitButton.click();
              }
            });
            """
            % submit_button_id
        ),
        rx.script(
            f"""
            (function initGoogle() {{
              if (!window.google || !google.accounts || !google.accounts.id) {{
                setTimeout(initGoogle, 50);
                return;
              }}
              google.accounts.id.initialize({{
                client_id: "{client_id}",
                callback: (response) => {{
                  window.dispatchEvent(new CustomEvent("google_id_token", {{
                    detail: response.credential
                  }}));
                }},
              }});
              const container = document.getElementById("{button_id}");
              if (container) {{
                google.accounts.id.renderButton(container, {{
                  theme: "outline",
                  size: "large",
                  shape: "pill",
                }});
              }}
              window.amm_google_prompt = function () {{
                google.accounts.id.prompt();
              }};
            }})();
            """
        ),
        rx.script(
            src="https://accounts.google.com/gsi/client",
            async_=True,
            defer=True,
        ),
    )


def auth_gate(content: rx.Component) -> rx.Component:
    """Gate content behind authentication."""
    return rx.cond(
        AuthState.is_authenticated,
        content,
        rx.center(
            rx.vstack(
                rx.text("Please sign in to continue."),
                rx.link("Login", href=routes.LOGIN_ROUTE),
                spacing="3",
            ),
            padding="4em 0",
        ),
    )


def admin_gate(content: rx.Component) -> rx.Component:
    """Gate content behind admin access."""
    return rx.cond(
        AuthState.is_authenticated,
        rx.cond(
            AuthState.is_admin,
            content,
            rx.center(
                rx.vstack(
                    rx.text("You do not have permission to view this page."),
                    rx.link("Go to Dashboard", href=routes.DASHBOARD_ROUTE),
                    spacing="3",
                ),
                padding="4em 0",
            ),
        ),
        rx.center(
            rx.vstack(
                rx.text("Please sign in to continue."),
                rx.link("Login", href=routes.LOGIN_ROUTE),
                spacing="3",
            ),
            padding="4em 0",
        ),
    )


def player_bar() -> rx.Component:
    """Lightweight player UI shown to authenticated users."""
    return rx.box(
        rx.hstack(
            rx.icon("music", size=20),
            rx.text("Now Playing", weight="medium"),
            rx.spacer(),
            rx.button(rx.icon("skip-back"), size="2", variant="ghost"),
            rx.button(rx.icon("play"), size="2", variant="solid"),
            rx.button(rx.icon("skip-forward"), size="2", variant="ghost"),
            spacing="3",
            align_items="center",
            width="100%",
        ),
        padding="0.75em 1em",
        border_top="1px solid #E2E8F0",
        width="100%",
    )


def player_shell(content: rx.Component) -> rx.Component:
    """Wrap content with the player bar when authenticated."""
    return rx.vstack(
        content,
        rx.cond(AuthState.is_authenticated, player_bar(), rx.fragment()),
        spacing="0",
        width="100%",
    )
