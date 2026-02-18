from AMM_web.state.base_state import BaseState
from AMM_web.services.library_client import library_service

class AlbumState(BaseState):
    album = None
    loading = False

    async def load(self, album_id: str, token: str):
        self.loading = True
        self.album = await library_service.get_album(int(album_id), token)
        self.loading = False
    