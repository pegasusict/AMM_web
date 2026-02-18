from AMM_web.state.base_state import BaseState
from AMM_web.services.library_client import library_service


class FileState(BaseState):
    file = None
    loading = False

    async def load(self, file_id: str, token: str):
        self.loading = True
        self.file = await library_service.get_file(int(file_id), token)
        self.loading = False
