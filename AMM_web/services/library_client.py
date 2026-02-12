"""GraphQL client wrapper for library data."""

from AMM_web.graphql import gql
from AMM_web.models.library import AlbumSummary, PlaylistSummary, QueueSummary, TrackSummary


class LibraryService:
    """Service for retrieving library metadata from AMM_core."""

    @staticmethod
    def _graphql_error(data: dict, fallback: str) -> str:
        errors = data.get("errors") or []
        if errors:
            return errors[0].get("message", fallback)
        return fallback

    async def list_tracks(self, limit: int = 25, offset: int = 0) -> tuple[list[TrackSummary], int]:
        query = """
        query GetTracks($limit: Int!, $offset: Int!) {
          getTracks(limit: $limit, offset: $offset) {
            total
            items { id mbid }
          }
        }
        """
        data = await gql(query, variables={"limit": limit, "offset": offset})
        if "errors" in data:
            raise RuntimeError(self._graphql_error(data, "Failed to load tracks"))
        payload = ((data.get("data") or {}).get("getTracks") or {})
        items = [TrackSummary(**item) for item in payload.get("items", [])]
        total = payload.get("total", 0)
        return items, total

    async def list_albums(self, limit: int = 25, offset: int = 0) -> tuple[list[AlbumSummary], int]:
        query = """
        query GetAlbums($limit: Int!, $offset: Int!) {
          getAlbums(limit: $limit, offset: $offset) {
            total
            items { id title }
          }
        }
        """
        data = await gql(query, variables={"limit": limit, "offset": offset})
        if "errors" in data:
            raise RuntimeError(self._graphql_error(data, "Failed to load albums"))
        payload = ((data.get("data") or {}).get("getAlbums") or {})
        items = [AlbumSummary(**item) for item in payload.get("items", [])]
        total = payload.get("total", 0)
        return items, total

    async def list_playlists(self, access_token: str) -> list[PlaylistSummary]:
        if not access_token:
            raise RuntimeError("Authentication required")
        query = """
        query Playlists {
          playlists { id name trackIds }
        }
        """
        data = await gql(query, access_token=access_token)
        if "errors" in data:
            raise RuntimeError(self._graphql_error(data, "Failed to load playlists"))
        items = ((data.get("data") or {}).get("playlists") or [])
        return [PlaylistSummary(**item) for item in items]

    async def get_queue(self, access_token: str) -> QueueSummary:
        if not access_token:
            raise RuntimeError("Authentication required")
        query = """
        query Queue {
          queue { trackIds }
        }
        """
        data = await gql(query, access_token=access_token)
        if "errors" in data:
            raise RuntimeError(self._graphql_error(data, "Failed to load queue"))
        payload = ((data.get("data") or {}).get("queue") or {})
        return QueueSummary(**payload)

    async def get_track(self, track_id: int, access_token: str | None = None) -> TrackSummary | None:
        query = """
        query GetTrack($trackId: Int!) {
          getTrack(trackId: $trackId) { id mbid }
        }
        """
        data = await gql(query, variables={"trackId": track_id}, access_token=access_token)
        if "errors" in data:
            return None
        payload = ((data.get("data") or {}).get("getTrack"))
        if not payload:
            return None
        return TrackSummary(**payload)


library_service = LibraryService()
