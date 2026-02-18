from AMM_web.state.base_state import BaseState
from AMM_web.services.library_client import library_service


class LabelState(BaseState):
    label = None
    loading = False

    async def load(self, label_id: str, token: str):
        self.loading = True
        self.label = await library_service.get_label(int(label_id), token)
        self.loading = False
