"""Common reactive state shared by all components."""

import reflex as rx


class BaseState(rx.State):
    loading: bool = False
    error: str | None = None

    def set_loading(self, value: bool) -> None:
        self.loading = value

    def set_error(self, message: str | None) -> None:
        self.error = message
