from AMM_web.state.base_state import BaseState
from AMM_web.state.edit_helpers import none_if_blank
from AMM_web.services.library_client import library_service


class PersonState(BaseState):
    person = None
    loading = False
    success_message: str | None = None

    mbid: str = ""
    first_name: str = ""
    middle_name: str = ""
    last_name: str = ""
    sort_name: str = ""
    full_name: str = ""
    nick_name: str = ""
    alias: str = ""
    date_of_birth: str = ""
    date_of_death: str = ""
    picture_id: str = ""
    performed_track_ids: str = ""
    conducted_track_ids: str = ""
    composed_track_ids: str = ""
    lyric_track_ids: str = ""
    produced_track_ids: str = ""
    performed_album_ids: str = ""
    conducted_album_ids: str = ""
    composed_album_ids: str = ""
    lyric_album_ids: str = ""
    produced_album_ids: str = ""
    task_ids: str = ""
    label_ids: str = ""

    def _set_messages(self, error: str | None = None, success: str | None = None) -> None:
        self.set_error(error)
        self.success_message = success

    def _populate_form(self) -> None:
        if not self.person:
            return
        self.mbid = self.person.mbid or ""
        self.first_name = self.person.first_name or ""
        self.middle_name = self.person.middle_name or ""
        self.last_name = self.person.last_name or ""
        self.sort_name = self.person.sort_name or ""
        self.full_name = self.person.full_name or ""
        self.nick_name = self.person.nick_name or ""
        self.alias = self.person.alias or ""
        self.date_of_birth = self.person.date_of_birth.isoformat() if self.person.date_of_birth else ""
        self.date_of_death = self.person.date_of_death.isoformat() if self.person.date_of_death else ""
        self.picture_id = "" if self.person.picture_id is None else str(self.person.picture_id)
        self.performed_track_ids = ", ".join(str(v) for v in (self.person.performed_track_ids or []))
        self.conducted_track_ids = ", ".join(str(v) for v in (self.person.conducted_track_ids or []))
        self.composed_track_ids = ", ".join(str(v) for v in (self.person.composed_track_ids or []))
        self.lyric_track_ids = ", ".join(str(v) for v in (self.person.lyric_track_ids or []))
        self.produced_track_ids = ", ".join(str(v) for v in (self.person.produced_track_ids or []))
        self.performed_album_ids = ", ".join(str(v) for v in (self.person.performed_album_ids or []))
        self.conducted_album_ids = ", ".join(str(v) for v in (self.person.conducted_album_ids or []))
        self.composed_album_ids = ", ".join(str(v) for v in (self.person.composed_album_ids or []))
        self.lyric_album_ids = ", ".join(str(v) for v in (self.person.lyric_album_ids or []))
        self.produced_album_ids = ", ".join(str(v) for v in (self.person.produced_album_ids or []))
        self.task_ids = ", ".join(str(v) for v in (self.person.task_ids or []))
        self.label_ids = ", ".join(str(v) for v in (self.person.label_ids or []))

    async def load(self, person_id: str, token: str):
        self.loading = True
        self._set_messages()
        self.person = await library_service.get_person(int(person_id), token)
        self._populate_form()
        self.loading = False

    async def save(self, token: str):
        if not self.person or self.person.id is None:
            self._set_messages(error="Load a person before saving.")
            return
        self.loading = True
        self._set_messages()
        try:
            payload = {
                "mbid": none_if_blank(self.mbid),
                "firstName": none_if_blank(self.first_name),
                "middleName": none_if_blank(self.middle_name),
                "lastName": none_if_blank(self.last_name),
                "sortName": none_if_blank(self.sort_name),
                "fullName": none_if_blank(self.full_name),
                "nickName": none_if_blank(self.nick_name),
                "alias": none_if_blank(self.alias),
                "dateOfBirth": none_if_blank(self.date_of_birth),
                "dateOfDeath": none_if_blank(self.date_of_death),
            }
            self.person = await library_service.update_person(self.person.id, payload, access_token=token or None)
            self._populate_form()
            self._set_messages(success="Person updated.")
        except Exception as exc:
            self._set_messages(error=str(exc))
        finally:
            self.loading = False
