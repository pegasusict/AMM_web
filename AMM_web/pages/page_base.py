import reflex as rx

from ..components import navbar, footer, player_widget


def page_base(func):
    """Base page of the application.

    Args:
        func (rx.Component): Function to be wrapped as a page.

    Returns:
        rx.Component: Base page with navbar and footer.
    """

    def wrapper():
        return rx.container(
            rx.script(src="/graphql/js_client.js", is_module=True),
            rx.script(src="/graphql/subscriptions.js", is_module=True),
            rx.color_mode.button(position="bottom-left"),
            rx.hstack(
                navbar(),
                player_widget(),
                func(),
                footer(),
            ),
        )

    return wrapper
