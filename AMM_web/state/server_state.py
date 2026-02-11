"""State for server reachability checks."""

from __future__ import annotations

import reflex as rx

from AMM_web.graphql import gql, is_offline_mode


class ServerState(rx.State):
    """Tracks connectivity status to the GraphQL server."""

    server_ok: bool | None = None
    server_message: str = "Checking server..."

    async def check_server(self) -> None:
        if is_offline_mode():
            self.server_ok = True
            self.server_message = "Offline mock mode enabled"
            return
        try:
            data = await gql("query ServerHealth { __typename }")
            if data.get("errors"):
                self.server_ok = False
                self.server_message = "Server reachable but GraphQL returned errors"
                return
            self.server_ok = True
            self.server_message = "Server reachable"
        except Exception as exc:
            self.server_ok = False
            self.server_message = f"Server unreachable: {exc}"

