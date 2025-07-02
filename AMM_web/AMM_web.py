"""Contains the pages and routes for the AMM web application."""

import reflex as rx

from AMM_web.pages import (
    index,
    about,
    contact,
    login,
    signup,
    privacy,
    terms,
    dashboard,
)
from AMM_web.routes import (
    HOME_ROUTE,
    ABOUT_ROUTE,
    CONTACT_ROUTE,
    LOGIN_ROUTE,
    SIGNUP_ROUTE,
)
from AMM_web.routes import TERMS_ROUTE, DASHBOARD_ROUTE, PRIVACY_ROUTE

app = rx.App()

app.add_page(index, HOME_ROUTE)
app.add_page(about, ABOUT_ROUTE)
app.add_page(contact, CONTACT_ROUTE)
app.add_page(login, LOGIN_ROUTE)
app.add_page(signup, SIGNUP_ROUTE)
app.add_page(privacy, PRIVACY_ROUTE)
app.add_page(terms, TERMS_ROUTE)
app.add_page(dashboard, DASHBOARD_ROUTE)


def callback():
    return rx.script("""
    const params = new URLSearchParams(window.location.search);
    const token = params.get("token");
    if (token) {
        localStorage.setItem("auth_token", token);
        window.location.href = "/";
    } else {
        alert("Login failed");
    }
    """)
