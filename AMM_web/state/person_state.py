from AMM_web.state.base_state import BaseState
from AMM_web.services.library_client import library_service


class PersonState(BaseState):
    person = None
    loading = False

    async def load(self, person_id: str, token: str):
        self.loading = True
        self.person = await library_service.get_person(int(person_id), token)
        self.loading = False
