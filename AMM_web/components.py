"""custom reflex webpage components"""

from datetime import datetime
import os

import reflex as rx

from AMM_web import routes
from AMM_web.auth_state import AuthState


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
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        padding="1em",
        # position="fixed",
        # top="0px",
        # z_index="5",
        width="100%",
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
) -> rx.Component:
    """Reusable Google Sign-In button using GIS."""
    client_id = client_id or os.getenv("AMM_GOOGLE_CLIENT_ID", "")
    return rx.box(
        rx.box(id=button_id),
        rx.script(
            """
            window.addEventListener("google_id_token", (e) => {
              const token = e.detail;
              if (window.reflex_api && window.reflex_api.set_state) {
                window.reflex_api.set_state("AuthState", "login_with_google", [token]);
              }
            });
            """
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
