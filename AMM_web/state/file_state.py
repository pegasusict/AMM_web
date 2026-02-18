from AMM_web.state.base_state import BaseState
from AMM_web.state.edit_helpers import none_if_blank, parse_int_optional
from AMM_web.services.library_client import library_service


class FileState(BaseState):
    file = None
    loading = False
    success_message: str | None = None

    file_name: str = ""
    file_path: str = ""
    file_extension: str = ""
    file_type: str = ""
    codec: str = ""
    file_size: str = ""
    duration: str = ""
    bitrate: str = ""
    sample_rate: str = ""
    channels: str = ""
    audio_ip: str = ""
    imported: str = ""
    processed: str = ""
    track_id: str = ""
    task_id: str = ""
    stage_type: str = ""
    completed_tasks: str = ""

    def _set_messages(self, error: str | None = None, success: str | None = None) -> None:
        self.set_error(error)
        self.success_message = success

    def _populate_form(self) -> None:
        if not self.file:
            return
        self.file_name = self.file.file_name or ""
        self.file_path = self.file.file_path or ""
        self.file_extension = self.file.file_extension or ""
        self.file_type = self.file.file_type or ""
        self.codec = self.file.codec or ""
        self.file_size = "" if self.file.file_size is None else str(self.file.file_size)
        self.duration = "" if self.file.duration is None else str(self.file.duration)
        self.bitrate = "" if self.file.bitrate is None else str(self.file.bitrate)
        self.sample_rate = "" if self.file.sample_rate is None else str(self.file.sample_rate)
        self.channels = "" if self.file.channels is None else str(self.file.channels)
        self.audio_ip = self.file.audio_ip or ""
        self.imported = self.file.imported or ""
        self.processed = self.file.processed or ""
        self.track_id = "" if self.file.track_id is None else str(self.file.track_id)
        self.task_id = "" if self.file.task_id is None else str(self.file.task_id)
        self.stage_type = "" if self.file.stage_type is None else str(self.file.stage_type)
        self.completed_tasks = ", ".join(v for v in (self.file.completed_tasks or []))

    async def load(self, file_id: str, token: str):
        self.loading = True
        self._set_messages()
        self.file = await library_service.get_file(int(file_id), token)
        self._populate_form()
        self.loading = False

    async def save(self, token: str):
        if not self.file or self.file.id is None:
            self._set_messages(error="Load a file before saving.")
            return
        self.loading = True
        self._set_messages()
        try:
            payload = {
                "fileName": none_if_blank(self.file_name),
                "filePath": none_if_blank(self.file_path),
                "fileExtension": none_if_blank(self.file_extension),
                "fileType": none_if_blank(self.file_type),
                "codec": none_if_blank(self.codec),
                "fileSize": parse_int_optional(self.file_size, "File Size"),
                "duration": parse_int_optional(self.duration, "Duration"),
                "bitrate": parse_int_optional(self.bitrate, "Bitrate"),
                "sampleRate": parse_int_optional(self.sample_rate, "Sample Rate"),
                "channels": parse_int_optional(self.channels, "Channels"),
                "audioIp": none_if_blank(self.audio_ip),
                "imported": none_if_blank(self.imported),
                "processed": none_if_blank(self.processed),
                "trackId": parse_int_optional(self.track_id, "Track ID"),
                "taskId": parse_int_optional(self.task_id, "Task ID"),
                "stageType": parse_int_optional(self.stage_type, "Stage Type"),
                "completedTasks": [v.strip() for v in self.completed_tasks.split(",") if v.strip()],
            }
            self.file = await library_service.update_file(self.file.id, payload, access_token=token or None)
            self._populate_form()
            self._set_messages(success="File updated.")
        except Exception as exc:
            self._set_messages(error=str(exc))
        finally:
            self.loading = False
