import reflex as rx
from ..components import navbar, footer


def page_base(func):
    """Base page of the application.

    Args:
        func (rx.Component): Function to be wrapped as a page.

    Returns:
        rx.Component: Base page with navbar and footer.
    """

    def wrapper():
        return rx.container(
            rx.color_mode.button(position="bottom-left"),
            rx.hstack(
                navbar(),
                func(),
                footer(),
            ),
        )

    return wrapper
