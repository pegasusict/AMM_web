import reflex as rx

from ..auth_state import AuthState
from ..components import detail_shell
from ..states import FileState
from ._edit_helpers import edit_field, edit_header, edit_messages, id_field


def file_edit(file_id: str):
    return rx.container(
        rx.on_mount(FileState.load(file_id, AuthState.access_token)),
        detail_shell(
            "Edit File",
            rx.vstack(
                edit_header("File", rx.concat("/files/", file_id)),
                rx.cond(
                    FileState.file,
                    rx.vstack(
                        id_field(FileState.file.id),
                        edit_field("File Name", FileState.file_name, FileState.set_file_name),
                        edit_field("File Path", FileState.file_path, FileState.set_file_path),
                        edit_field("File Extension", FileState.file_extension, FileState.set_file_extension),
                        edit_field("File Type", FileState.file_type, FileState.set_file_type),
                        edit_field("Codec", FileState.codec, FileState.set_codec),
                        edit_field("File Size", FileState.file_size, FileState.set_file_size),
                        edit_field("Duration", FileState.duration, FileState.set_duration),
                        edit_field("Bitrate", FileState.bitrate, FileState.set_bitrate),
                        edit_field("Sample Rate", FileState.sample_rate, FileState.set_sample_rate),
                        edit_field("Channels", FileState.channels, FileState.set_channels),
                        edit_field("Audio IP", FileState.audio_ip, FileState.set_audio_ip),
                        edit_field("Imported", FileState.imported, FileState.set_imported),
                        edit_field("Processed", FileState.processed, FileState.set_processed),
                        edit_field("Track ID", FileState.track_id, FileState.set_track_id),
                        edit_field("Task ID", FileState.task_id, FileState.set_task_id),
                        edit_field("Stage Type", FileState.stage_type, FileState.set_stage_type),
                        edit_field(
                            "Completed Tasks",
                            FileState.completed_tasks,
                            FileState.set_completed_tasks,
                            "imported, parsed",
                        ),
                        edit_messages(FileState.error, FileState.success_message),
                        rx.hstack(
                            rx.button(
                                "Save",
                                on_click=FileState.save(AuthState.access_token),
                                is_loading=FileState.loading,
                            ),
                            rx.button(
                                "Cancel",
                                variant="outline",
                                on_click=rx.redirect(rx.concat("/files/", file_id)),
                            ),
                        ),
                        spacing="2",
                        width="100%",
                        align_items="start",
                    ),
                    rx.text("Loading...", color="gray"),
                ),
                spacing="4",
                width="100%",
                align_items="start",
            ),
        ),
    )
