"""custom reflex webpage components"""

from datetime import datetime

import reflex as rx

from AMM_web import routes
from state.player_state import PlayerState


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
                    navbar_link("About", routes.ABOUT_ROUTE),
                    navbar_link("Contact", routes.CONTACT_ROUTE),
                    navbar_link("Login", routes.LOGIN_ROUTE),
                    navbar_link("Sign Up", routes.SIGNUP_ROUTE),
                    navbar_link("Terms & Conditions", routes.TERMS_ROUTE),
                    navbar_link("Privacy Policy", routes.PRIVACY_ROUTE),
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
                        rx.menu.item("About"),
                        rx.menu.item("Contact"),
                        rx.menu.item("Login"),
                        rx.menu.item("Sign Up"),
                        rx.menu.item("Terms & Conditions"),
                        rx.menu.item("Privacy Policy"),
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


def logout_button():
    return rx.button(
        "Logout",
        on_click=rx.script("""
            localStorage.removeItem("auth_token");
            fetch('http://localhost:8000/auth/logout', {method: 'POST', credentials: 'include'});
            window.location.href = '/login';
        """),  # type: ignore
    )
