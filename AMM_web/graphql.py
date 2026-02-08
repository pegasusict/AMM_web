"""GraphQL client helper for AMM Web."""

from __future__ import annotations

import os
from typing import Any

import httpx

GRAPHQL_URL = os.getenv("AMM_GRAPHQL_URL", "http://localhost:8000/graphql")


async def gql(
    query: str,
    variables: dict[str, Any] | None = None,
    access_token: str | None = None,
) -> dict[str, Any]:
    """Execute a GraphQL request and return the JSON response."""
    headers: dict[str, str] = {}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            GRAPHQL_URL,
            json={"query": query, "variables": variables or {}},
            headers=headers,
        )
        return resp.json()
