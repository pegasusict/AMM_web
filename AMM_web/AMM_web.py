"""Contains the pages and routes for the AMM web application."""

import reflex as rx

from AMM_web.auth_state import AuthState
from AMM_web.pages import (
    about,
    contact,
    dashboard,
    index,
    login,
    privacy,
    search,
    signup,
    terms,
    track_detail,
    album_detail,
    person_detail,
    file_detail,
    label_detail,
    admin_system,
    admin_users
)
from AMM_web.state.library_state import LibraryState
from AMM_web.state.server_state import ServerState
from AMM_web.routes import (
    HOME_ROUTE,
    ABOUT_ROUTE,
    CONTACT_ROUTE,
    LOGIN_ROUTE,
    SIGNUP_ROUTE,
    TERMS_ROUTE,
    DASHBOARD_ROUTE,
    PRIVACY_ROUTE,
    SEARCH_ROUTE,
    ADMIN_USERS_ROUTE,
    ADMIN_SYSTEM_ROUTE,
    TRACK_DETAIL_ROUTE,
    ALBUM_DETAIL_ROUTE,
    PERSON_DETAIL_ROUTE,
    FILE_DETAIL_ROUTE,
    LABEL_DETAIL_ROUTE,
)

app = rx.App()

# public pages
app.add_page(index, HOME_ROUTE, on_load=ServerState.check_server)
app.add_page(about, ABOUT_ROUTE, on_load=ServerState.check_server)
app.add_page(signup, SIGNUP_ROUTE, on_load=ServerState.check_server)
app.add_page(privacy, PRIVACY_ROUTE, on_load=ServerState.check_server)
app.add_page(terms, TERMS_ROUTE, on_load=ServerState.check_server)
app.add_page(login, LOGIN_ROUTE, on_load=ServerState.check_server)

# behind authentication
app.add_page(contact, CONTACT_ROUTE, on_load=ServerState.check_server)
app.add_page(
    dashboard,
    DASHBOARD_ROUTE,
    on_load=[
        ServerState.check_server,
        LibraryState.load_library(access_token=AuthState.access_token), # Load the user's library when the dashboard page is accessed
    ],
)
app.add_page(search, SEARCH_ROUTE, on_load=ServerState.check_server)

# admin pages
app.add_page(admin_users, ADMIN_USERS_ROUTE, on_load=ServerState.check_server)
app.add_page(admin_system, ADMIN_SYSTEM_ROUTE, on_load=ServerState.check_server)

# dynamic pages
app.add_page(track_detail, TRACK_DETAIL_ROUTE, on_load=ServerState.check_server)
app.add_page(album_detail, ALBUM_DETAIL_ROUTE, on_load=ServerState.check_server)
app.add_page(person_detail, PERSON_DETAIL_ROUTE, on_load=ServerState.check_server)
app.add_page(file_detail, FILE_DETAIL_ROUTE, on_load=ServerState.check_server)
app.add_page(label_detail, LABEL_DETAIL_ROUTE, on_load=ServerState.check_server)
