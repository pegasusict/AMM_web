"""Compatibility exports for page state imports.

This keeps legacy imports like `from ..states import TrackState` working
while state classes live under `AMM_web.state.*` modules.
"""

from AMM_web.state.contact_state import ContactState
from AMM_web.state.signup_state import SignupState
from AMM_web.state.track_state import TrackState
from AMM_web.state.album_state import AlbumState
from AMM_web.state.person_state import PersonState
from AMM_web.state.file_state import FileState
from AMM_web.state.label_state import LabelState

__all__ = [
    "ContactState",
    "SignupState",
    "TrackState",
    "AlbumState",
    "PersonState",
    "FileState",
    "LabelState",
]
