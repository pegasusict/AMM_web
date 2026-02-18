import reflex as rx

from ..auth_state import AuthState
from ..states import FileState
from ..components import detail_shell
from ._detail_helpers import detail_content, field


def file_detail(file_id: str = ""):

    return rx.container(
        detail_shell(
            "File Detail",
            detail_content(
                "File",
                FileState.file,
                [
                    field("ID", FileState.file.id),
                    field("File Name", FileState.file.file_name),
                    field("File Path", FileState.file.file_path),
                    field("File Extension", FileState.file.file_extension),
                    field("File Type", FileState.file.file_type),
                    field("Codec", FileState.file.codec),
                    field("File Size", FileState.file.file_size),
                    field("Duration", FileState.file.duration),
                    field("Bitrate", FileState.file.bitrate),
                    field("Sample Rate", FileState.file.sample_rate),
                    field("Channels", FileState.file.channels),
                    field("Audio IP", FileState.file.audio_ip),
                    field("Imported", FileState.file.imported),
                    field("Processed", FileState.file.processed),
                    field("Track ID", FileState.file.track_id),
                    field("Task ID", FileState.file.task_id),
                    field("Stage Type", FileState.file.stage_type),
                    field("Completed Tasks", FileState.file.completed_tasks, "[]"),
                ],
                edit_href="/files/" + file_id + "/edit",
            ),
        ),
    )
