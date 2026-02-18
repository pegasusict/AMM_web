from AMM_web.state.base_state import BaseState
from AMM_web.state.edit_helpers import none_if_blank, parse_int_optional
from AMM_web.models.library import LabelSummary
from AMM_web.services.library_client import library_service


class LabelState(BaseState):
    label: LabelSummary | None = None
    loading = False
    success_message: str | None = None

    name: str = ""
    mbid: str = ""
    description: str = ""
    founded: str = ""
    defunct: str = ""
    owner_id: str = ""
    parent_id: str = ""
    picture_id: str = ""
    child_ids: str = ""
    album_ids: str = ""

    def _set_messages(self, error: str | None = None, success: str | None = None) -> None:
        self.set_error(error)
        self.success_message = success

    def _populate_form(self) -> None:
        if not self.label:
            return
        self.name = self.label.name or ""
        self.mbid = self.label.mbid or ""
        self.description = self.label.description or ""
        self.founded = self.label.founded.isoformat() if self.label.founded else ""
        self.defunct = self.label.defunct.isoformat() if self.label.defunct else ""
        self.owner_id = "" if self.label.owner_id is None else str(self.label.owner_id)
        self.parent_id = "" if self.label.parent_id is None else str(self.label.parent_id)
        self.picture_id = "" if self.label.picture_id is None else str(self.label.picture_id)
        self.child_ids = ", ".join(str(v) for v in (self.label.child_ids or []))
        self.album_ids = ", ".join(str(v) for v in (self.label.album_ids or []))

    async def load(self, label_id: str, token: str):
        self.loading = True
        self._set_messages()
        self.label = await library_service.get_label(int(label_id), token)
        self._populate_form()
        self.loading = False

    async def load_from_route(self, token: str = ""):
        route_id = str(self.router.page.params.get("label_id", "")).strip()
        if not route_id:
            return
        await self.load(route_id, token)

    async def save(self, token: str):
        if not self.label or self.label.id is None:
            self._set_messages(error="Load a label before saving.")
            return
        self.loading = True
        self._set_messages()
        try:
            payload = {
                "name": none_if_blank(self.name),
                "mbid": none_if_blank(self.mbid),
                "description": none_if_blank(self.description),
                "founded": none_if_blank(self.founded),
                "defunct": none_if_blank(self.defunct),
                "ownerId": parse_int_optional(self.owner_id, "Owner ID"),
                "parentId": parse_int_optional(self.parent_id, "Parent ID"),
            }
            self.label = await library_service.update_label(self.label.id, payload, access_token=token or None)
            self._populate_form()
            self._set_messages(success="Label updated.")
        except Exception as exc:
            self._set_messages(error=str(exc))
        finally:
            self.loading = False
