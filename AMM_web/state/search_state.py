"""State for executing ad-hoc GraphQL queries."""

from __future__ import annotations

import json

from AMM_web.graphql import gql
from AMM_web.state.base_state import BaseState


class SearchState(BaseState):
    query: str = ""
    variables: str = "{}"
    response: str = ""
    preset: str = ""

    def load_preset(self, name: str) -> None:
        presets = {
            "Tracks (list)": (
                "query GetTracks($limit: Int!, $offset: Int!) {\\n"
                "  getTracks(limit: $limit, offset: $offset) {\\n"
                "    total\\n"
                "    items { id mbid }\\n"
                "  }\\n"
                "}\\n",
                "{\"limit\": 25, \"offset\": 0}",
            ),
            "Albums (list)": (
                "query GetAlbums($limit: Int!, $offset: Int!) {\\n"
                "  getAlbums(limit: $limit, offset: $offset) {\\n"
                "    total\\n"
                "    items { id title }\\n"
                "  }\\n"
                "}\\n",
                "{\"limit\": 25, \"offset\": 0}",
            ),
            "Persons (list)": (
                "query GetPersons($limit: Int!, $offset: Int!) {\\n"
                "  getPersons(limit: $limit, offset: $offset) {\\n"
                "    total\\n"
                "    items { id fullName }\\n"
                "  }\\n"
                "}\\n",
                "{\"limit\": 25, \"offset\": 0}",
            ),
            "Labels (list)": (
                "query GetLabels($limit: Int!, $offset: Int!) {\\n"
                "  getLabels(limit: $limit, offset: $offset) {\\n"
                "    total\\n"
                "    items { id name }\\n"
                "  }\\n"
                "}\\n",
                "{\"limit\": 25, \"offset\": 0}",
            ),
            "Playlists (auth)": (
                "query Playlists {\\n"
                "  playlists { id name trackIds }\\n"
                "}\\n",
                "{}",
            ),
            "Queue (auth)": (
                "query Queue {\\n"
                "  queue { trackIds }\\n"
                "}\\n",
                "{}",
            ),
            "Task Display": (
                "query TaskDisplay {\\n"
                "  getTaskDisplay { taskId taskType progress startTime status }\\n"
                "}\\n",
                "{}",
            ),
        }
        preset = presets.get(name)
        if not preset:
            return
        self.preset = name
        self.query, self.variables = preset

    async def run_query(self, access_token: str = "") -> None:
        self.set_loading(True)
        self.set_error(None)
        try:
            variables = {}
            if self.variables.strip():
                variables = json.loads(self.variables)
            data = await gql(self.query, variables=variables, access_token=access_token or None)
            self.response = json.dumps(data, indent=2, sort_keys=True)
        except Exception as exc:
            self.set_error(str(exc))
        finally:
            self.set_loading(False)
