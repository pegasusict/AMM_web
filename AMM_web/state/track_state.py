from AMM_web.state.base_state import BaseState
from AMM_web.services.library_client import library_service


class TrackState(BaseState):
    track = None
    loading = False

    async def load(self, track_id: str, token: str):
        self.loading = True
        self.track = await library_service.get_track(int(track_id), token)
        self.loading = False
