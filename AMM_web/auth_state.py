"""Authentication state and helpers for Google SSO."""

from __future__ import annotations

import json
from typing import Any

import reflex as rx

from .graphql import gql


class AuthState(rx.State):
    """Auth state with persisted tokens."""

    access_token: str = rx.LocalStorage("")
    refresh_token: str = rx.LocalStorage("")
    _user_json: str = rx.LocalStorage("")
    login_error: str = ""

    @rx.var
    def user(self) -> dict[str, Any] | None:
        if not self._user_json:
            return None
        try:
            return json.loads(self._user_json)
        except json.JSONDecodeError:
            return None

    @rx.var
    def is_authenticated(self) -> bool:
        return bool(self.access_token)

    @rx.var
    def role_name(self) -> str:
        user = self.user or {}
        role = str(user.get("role") or "")
        return role.upper()

    @rx.var
    def is_admin(self) -> bool:
        role = self.role_name
        return role == "ADMIN" or role.endswith(".ADMIN")

    def clear_auth(self) -> None:
        self.access_token = ""
        self.refresh_token = ""
        self._user_json = ""
        self.login_error = ""

    async def login_with_google(self, id_token: str) -> rx.EventSpec | None:
        mutation = """
        mutation LoginWithGoogle($idToken: String!) {
          loginWithGoogle(idToken: $idToken) {
            accessToken
            refreshToken
            user { id username email role isActive }
          }
        }
        """
        variables = {"idToken": id_token}

        try:
            data = await gql(mutation, variables=variables)
        except Exception as exc:
            self.login_error = f"Login failed: {exc}"
            return None

        if "errors" in data:
            self.login_error = data["errors"][0].get("message", "Login failed")
            return None

        payload = (data.get("data") or {}).get("loginWithGoogle") or {}
        self.access_token = payload.get("accessToken") or payload.get("access_token") or ""
        self.refresh_token = payload.get("refreshToken") or payload.get("refresh_token") or ""
        self._user_json = json.dumps(payload.get("user") or {})
        if not self.access_token:
            self.login_error = "Login failed: missing access token"
            return None
        self.login_error = ""
        return rx.redirect("/dashboard")

    async def gql(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        """Authenticated GraphQL helper using stored access token."""
        return await gql(query, variables=variables, access_token=self.access_token)

    def request_google_refresh(self) -> rx.EventSpec:
        """Prompt Google One Tap to re-issue an ID token."""
        return rx.call_script("window.amm_google_prompt && window.amm_google_prompt();")

    def require_admin(self) -> rx.EventSpec | None:
        """Guard admin-only routes."""
        if not self.is_authenticated:
            return rx.redirect("/login")
        if not self.is_admin:
            return rx.redirect("/dashboard")
        return None
