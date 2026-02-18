"""GraphQL client wrapper for library data."""

from AMM_web.graphql import gql
from AMM_web.models.library import (
    AlbumSummary,
    FileSummary,
    LabelSummary,
    PersonSummary,
    PlaylistSummary,
    QueueSummary,
    TaskDisplaySummary,
    TrackSummary,
)


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
            items { id mbid composed releaseDate }
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
            items { id mbid title subtitle releaseDate labelId trackCount discCount }
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

    async def list_persons(self, limit: int = 25, offset: int = 0) -> tuple[list[PersonSummary], int]:
        query = """
        query GetPersons($limit: Int!, $offset: Int!) {
          getPersons(limit: $limit, offset: $offset) {
            total
            items { id mbid fullName firstName middleName lastName sortName }
          }
        }
        """
        data = await gql(query, variables={"limit": limit, "offset": offset})
        if "errors" in data:
            raise RuntimeError(self._graphql_error(data, "Failed to load persons"))
        payload = ((data.get("data") or {}).get("getPersons") or {})
        items = [PersonSummary(**item) for item in payload.get("items", [])]
        total = payload.get("total", 0)
        return items, total

    async def list_labels(self, limit: int = 25, offset: int = 0) -> tuple[list[LabelSummary], int]:
        query = """
        query GetLabels($limit: Int!, $offset: Int!) {
          getLabels(limit: $limit, offset: $offset) {
            total
            items { id name mbid description ownerId parentId founded defunct }
          }
        }
        """
        data = await gql(query, variables={"limit": limit, "offset": offset})
        if "errors" in data:
            raise RuntimeError(self._graphql_error(data, "Failed to load labels"))
        payload = ((data.get("data") or {}).get("getLabels") or {})
        items = [LabelSummary(**item) for item in payload.get("items", [])]
        total = payload.get("total", 0)
        return items, total

    async def list_playlists(self, access_token: str) -> list[PlaylistSummary]:
        if not access_token:
            raise RuntimeError("Authentication required")
        query = """
        query Playlists {
          playlists { id name userId playlistTrackIds trackIds }
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
          queue { id userId trackIds }
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
          getTrack(trackId: $trackId) {
            id
            composed
            releaseDate
            mbid
            fileIds
            albumTrackIds
            keyId
            genreIds
            performerIds
            conductorIds
            composerIds
            lyricistIds
            producerIds
            taskIds
            lyricId
            tracktagIds
          }
        }
        """
        data = await gql(query, variables={"trackId": track_id}, access_token=access_token)
        if "errors" in data:
            return None
        payload = ((data.get("data") or {}).get("getTrack"))
        if not payload:
            return None
        return TrackSummary(**payload)

    async def get_album(self, album_id: int, access_token: str | None = None) -> AlbumSummary | None:
        query = """
        query GetAlbum($albumId: Int!) {
          getAlbum(albumId: $albumId) {
            id
            mbid
            title
            titleSort
            subtitle
            releaseDate
            releaseCountry
            discCount
            trackCount
            taskId
            labelId
            albumTrackIds
            genreIds
            artistIds
            conductorIds
            composerIds
            lyricistIds
            producerIds
            pictureId
          }
        }
        """
        data = await gql(query, variables={"albumId": album_id}, access_token=access_token)
        if "errors" in data:
            return None
        payload = ((data.get("data") or {}).get("getAlbum"))
        if not payload:
            return None
        return AlbumSummary(**payload)

    async def get_person(self, person_id: int, access_token: str | None = None) -> PersonSummary | None:
        query = """
        query GetPerson($personId: Int!) {
          getPerson(personId: $personId) {
            id
            mbid
            firstName
            middleName
            lastName
            sortName
            fullName
            nickName
            alias
            dateOfBirth
            dateOfDeath
            pictureId
            performedTrackIds
            conductedTrackIds
            composedTrackIds
            lyricTrackIds
            producedTrackIds
            performedAlbumIds
            conductedAlbumIds
            composedAlbumIds
            lyricAlbumIds
            producedAlbumIds
            taskIds
            labelIds
          }
        }
        """
        data = await gql(query, variables={"personId": person_id}, access_token=access_token)
        if "errors" in data:
            return None
        payload = ((data.get("data") or {}).get("getPerson"))
        if not payload:
            return None
        return PersonSummary(**payload)

    async def get_label(self, label_id: int, access_token: str | None = None) -> LabelSummary | None:
        query = """
        query GetLabel($labelId: Int!) {
          getLabel(labelId: $labelId) {
            id
            name
            mbid
            founded
            defunct
            description
            ownerId
            parentId
            childIds
            pictureId
            albumIds
          }
        }
        """
        data = await gql(query, variables={"labelId": label_id}, access_token=access_token)
        if "errors" in data:
            return None
        payload = ((data.get("data") or {}).get("getLabel"))
        if not payload:
            return None
        return LabelSummary(**payload)
    
    async def get_file(self, file_id: int, access_token: str | None = None) -> FileSummary | None:
        query = """
        query GetFile($fileId: Int!) {
          getFile(fileId: $fileId) {
            id
            audioIp
            imported
            processed
            bitrate
            sampleRate
            channels
            fileType
            fileSize
            fileName
            fileExtension
            codec
            duration
            trackId
            taskId
            filePath
            stageType
            completedTasks
          }
        }
        """
        data = await gql(query, variables={"fileId": file_id}, access_token=access_token)
        if "errors" in data:
            return None
        payload = ((data.get("data") or {}).get("getFile"))
        if not payload:
            return None
        return FileSummary(**payload)

    async def list_task_display(self, access_token: str | None = None) -> list[TaskDisplaySummary]:
        query = """
        query TaskDisplay {
          getTaskDisplay { taskId taskType progress startTime status }
        }
        """
        data = await gql(query, access_token=access_token)
        if "errors" in data:
            raise RuntimeError(self._graphql_error(data, "Failed to load task display"))
        items = ((data.get("data") or {}).get("getTaskDisplay") or [])
        return [TaskDisplaySummary(**item) for item in items]


library_service = LibraryService()
