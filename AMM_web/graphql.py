"""GraphQL client helper for AMM Web."""

from __future__ import annotations

import os
from typing import Any

import httpx


def is_offline_mode() -> bool:
    value = os.getenv("AMM_OFFLINE_MODE", "")
    return value.lower() in {"1", "true", "yes", "on"}


def _graphql_url() -> str:
    explicit = os.getenv("AMM_GRAPHQL_URL")
    if explicit:
        return explicit
    api_base = os.getenv("AMM_API_BASE_URL")
    if api_base:
        return f"{api_base.rstrip('/')}/graphql"
    return "http://localhost:8000/graphql"


def _mock_paginated(variables: dict[str, Any] | None, label: str) -> dict[str, Any]:
    values = variables or {}
    limit = int(values.get("limit", 25))
    offset = int(values.get("offset", 0))
    items: list[dict[str, Any]] = []
    for i in range(limit):
        idx = offset + i + 1
        items.append({"id": idx, "title": f"{label} {idx}"})
    return {"total": 500, "items": items}


def _mock_paginated_tracks(variables: dict[str, Any] | None) -> dict[str, Any]:
    values = variables or {}
    limit = int(values.get("limit", 25))
    offset = int(values.get("offset", 0))
    items = [{"id": offset + i + 1, "mbid": f"offline-track-{offset + i + 1}"} for i in range(limit)]
    return {"total": 500, "items": items}


def _mock_graphql(query: str, variables: dict[str, Any] | None) -> dict[str, Any]:
    if "loginWithGoogle" in query:
        return {
            "data": {
                "loginWithGoogle": {
                    "accessToken": "offline-access-token",
                    "refreshToken": "offline-refresh-token",
                    "user": {
                        "id": 1,
                        "username": "offline",
                        "email": "offline@example.com",
                        "role": "ADMIN",
                        "isActive": True,
                    },
                }
            }
        }
    if "getTracks(" in query:
        return {"data": {"getTracks": _mock_paginated_tracks(variables)}}
    if "getAlbums(" in query:
        return {"data": {"getAlbums": _mock_paginated(variables, "Album")}}
    if "getPersons(" in query:
        values = variables or {}
        limit = int(values.get("limit", 25))
        offset = int(values.get("offset", 0))
        items = [{"id": offset + i + 1, "fullName": f"Person {offset + i + 1}"} for i in range(limit)]
        return {"data": {"getPersons": {"total": 100, "items": items}}}
    if "getLabels(" in query:
        values = variables or {}
        limit = int(values.get("limit", 25))
        offset = int(values.get("offset", 0))
        items = [{"id": offset + i + 1, "name": f"Label {offset + i + 1}"} for i in range(limit)]
        return {"data": {"getLabels": {"total": 80, "items": items}}}
    if "getTrack(" in query:
        values = variables or {}
        track_id = int(values.get("trackId", 1))
        return {"data": {"getTrack": {"id": track_id, "mbid": f"offline-track-{track_id}"}}}
    if "playlists" in query:
        return {"data": {"playlists": [{"id": 1, "name": "Offline Playlist", "trackIds": [1, 2, 3]}]}}
    if "queue" in query:
        return {"data": {"queue": {"trackIds": [1, 2, 3]}}}
    if "users(" in query:
        return {
            "data": {
                "users": {
                    "total": 3,
                    "items": [
                        {
                            "id": 1,
                            "username": "admin",
                            "email": "admin@example.com",
                            "role": "ADMIN",
                            "isActive": True,
                            "firstName": "Admin",
                            "lastName": "User",
                        },
                        {
                            "id": 2,
                            "username": "demo",
                            "email": "demo@example.com",
                            "role": "USER",
                            "isActive": True,
                            "firstName": "Demo",
                            "lastName": "User",
                        },
                        {
                            "id": 3,
                            "username": "inactive",
                            "email": "inactive@example.com",
                            "role": "USER",
                            "isActive": False,
                            "firstName": "Inactive",
                            "lastName": "User",
                        },
                    ],
                }
            }
        }
    if "createUser(" in query:
        payload = ((variables or {}).get("data") or {})
        return {
            "data": {
                "createUser": {
                    "id": 999,
                    "username": payload.get("username", "newuser"),
                    "email": payload.get("email", "new@example.com"),
                    "role": payload.get("role", "USER"),
                    "isActive": payload.get("isActive", True),
                }
            }
        }
    if "updateUser(" in query:
        user_id = int((variables or {}).get("userId", 1))
        data = ((variables or {}).get("data") or {})
        return {
            "data": {
                "updateUser": {
                    "id": user_id,
                    "role": data.get("role", "USER"),
                    "isActive": data.get("isActive", True),
                }
            }
        }
    if "deleteUser(" in query:
        user_id = int((variables or {}).get("userId", 1))
        return {"data": {"deleteUser": {"id": user_id}}}
    if "getTaskDisplay" in query:
        return {
            "data": {
                "getTaskDisplay": [
                    {
                        "taskId": "offline-1",
                        "taskType": "import",
                        "progress": 100,
                        "startTime": "2026-01-01T00:00:00Z",
                        "status": "done",
                    }
                ]
            }
        }
    if "__typename" in query:
        return {"data": {"__typename": "Query"}}
    return {"data": {}}


async def gql(
    query: str,
    variables: dict[str, Any] | None = None,
    access_token: str | None = None,
) -> dict[str, Any]:
    """Execute a GraphQL request and return the JSON response."""
    if is_offline_mode():
        return _mock_graphql(query, variables)

    headers: dict[str, str] = {}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    async with httpx.AsyncClient(timeout=20.0) as client:
        resp = await client.post(
            _graphql_url(),
            json={"query": query, "variables": variables or {}},
            headers=headers,
        )
        resp.raise_for_status()
        return resp.json()
