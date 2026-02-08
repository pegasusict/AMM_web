"""Authentication state and helpers for Google SSO."""

from __future__ import annotations

import json
import os
from typing import Any

import httpx
import reflex as rx

from .graphql import gql

GRAPHQL_URL = os.getenv("AMM_GRAPHQL_URL", "http://localhost:8000/graphql")


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

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                GRAPHQL_URL,
                json={"query": mutation, "variables": variables},
            )
            data = resp.json()

        if "errors" in data:
            self.login_error = data["errors"][0].get("message", "Login failed")
            return None

        payload = data["data"]["loginWithGoogle"]
        self.access_token = payload["accessToken"]
        self.refresh_token = payload["refreshToken"]
        self._user_json = json.dumps(payload["user"])
        self.login_error = ""
        return rx.redirect("/")

    async def gql(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        """Authenticated GraphQL helper using stored access token."""
        return await gql(query, variables=variables, access_token=self.access_token)

    def request_google_refresh(self) -> rx.EventSpec:
        """Prompt Google One Tap to re-issue an ID token."""
        return rx.call_script("window.amm_google_prompt && window.amm_google_prompt();")
